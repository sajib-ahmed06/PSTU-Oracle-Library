"""Sign-in, staff account management, and authenticated credential changes."""

import re

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from starlette.concurrency import run_in_threadpool
from backend.validation import text_field
from backend.audit import audit_actor
from .member_access import register_member_access_routes
from .passwords import hash_password, verify_password
from .validation import member_number, validate_password, validate_credentials

from .session import (
    SESSION_COOKIE,
    SESSION_SECONDS,
    create_session,
    current_session,
    invalidate_user_sessions,
    remove_session,
    require_admin,
)


def register_auth_routes(app, frontend, rows, execute_dml, quote, form_data, required):
    router = APIRouter()
    register_member_access_routes(router, frontend, rows, form_data, required, quote)

    @router.get("/login")
    def login_page(request: Request):
        if current_session(request):
            return RedirectResponse("/", status_code=303)
        return FileResponse(frontend / "login.html")

    @router.post("/api/auth/login")
    async def login(request: Request):
        data = await form_data(request)
        required(data, "username", "password")
        username = text_field(data["username"], "username", 100)
        if len(data["password"]) > 128:
            raise HTTPException(400, "Password must contain at most 128 characters")

        def authenticate():
            member_login = re.fullmatch(r"(?:PSTU-)?[0-9]{1,20}", username, re.I)
            condition = (
                f"student_id={member_number(username)} AND user_type='STUDENT'"
                if member_login
                else f"LOWER(username)=LOWER({quote(username)})"
            )
            users = rows(
                "SELECT user_id||'|'||username||'|'||user_type||'|'||account_status||'|'||password||'|'||NVL(TO_CHAR(student_id),'~') "
                "FROM login_user "
                f"WHERE {condition}",
                ["user_id", "username", "user_type", "account_status", "password", "student_id"],
                {"user_id", "student_id"},
            )
            if not users or not verify_password(data["password"], users[0]["password"]):
                raise HTTPException(401, "Incorrect username or password")

            user = users[0]
            if user["user_type"] not in {"ADMIN", "LIBRARIAN", "STUDENT"}:
                raise HTTPException(403, "This account cannot access the management dashboard")
            if user["account_status"] != "ACTIVE":
                raise HTTPException(403, "This account has been disabled")
            if user["user_type"] == "STUDENT":
                if not user.get("student_id"):
                    raise HTTPException(
                        403,
                        "Activate your account using your Member ID and registered phone number",
                    )
                members = rows(
                    f"SELECT membership_status FROM student WHERE student_id={user['student_id']}",
                    ["membership_status"],
                )
                if not members or members[0]["membership_status"] != "ACTIVE":
                    raise HTTPException(403, "This membership is disabled")

            if not user["password"].startswith("pbkdf2$"):
                actor_token = audit_actor.set(user["username"])
                try:
                    execute_dml(
                        f"UPDATE login_user SET password={quote(hash_password(data['password']))} WHERE user_id={user['user_id']}"
                    )
                finally:
                    audit_actor.reset(actor_token)
            return user

        # SQL*Plus and password hashing must not block other HTTP requests.
        user = await run_in_threadpool(authenticate)
        remove_session(request.cookies.get(SESSION_COOKIE))
        token = create_session(user)
        response = JSONResponse({"username": user["username"], "user_type": user["user_type"]})
        response.set_cookie(
            SESSION_COOKIE,
            token,
            max_age=SESSION_SECONDS,
            httponly=True,
            samesite="strict",
            secure=request.url.scheme == "https",
        )
        return response

    @router.get("/api/auth/session")
    def auth_session(request: Request):
        session = current_session(request)
        if not session:
            raise HTTPException(401, "Authentication required")
        return {
            "username": session["username"],
            "user_type": session["user_type"],
        }

    @router.post("/api/auth/logout")
    def logout(request: Request):
        remove_session(request.cookies.get(SESSION_COOKIE))
        response = JSONResponse({"message": "Logged out"})
        response.delete_cookie(SESSION_COOKIE)
        return response

    @router.get("/api/accounts")
    def get_accounts(request: Request):
        require_admin(request)
        return rows(
            "SELECT user_id||'|'||username||'|'||user_type||'|'||account_status "
            "FROM login_user WHERE user_type IN ('ADMIN','LIBRARIAN') "
            "ORDER BY DECODE(user_type,'ADMIN',1,2), username",
            ["user_id", "username", "user_type", "account_status"],
            {"user_id"},
        )

    @router.post("/api/accounts/librarians", status_code=201)
    async def create_librarian(request: Request):
        require_admin(request)
        data = await form_data(request)
        required(data, "username", "password")
        username = data["username"].strip()
        password = data["password"]
        validate_credentials(username, password)
        if username_exists(rows, quote, username):
            raise HTTPException(409, "Username already exists")
        execute_dml(
            "INSERT INTO login_user(username,password,user_type,account_status) "
            f"VALUES({quote(username)},{quote(hash_password(password))},'LIBRARIAN','ACTIVE')"
        )
        return {"message": "Librarian account created"}

    @router.post("/api/accounts/{user_id}/toggle")
    def toggle_librarian(user_id: int, request: Request):
        require_admin(request)
        account = librarian(rows, user_id)
        next_status = "DISABLED" if account["account_status"] == "ACTIVE" else "ACTIVE"
        execute_dml(
            "UPDATE login_user " f"SET account_status={quote(next_status)} WHERE user_id={user_id}"
        )
        if next_status == "DISABLED":
            invalidate_user_sessions(user_id)
        return {"message": f"Librarian account {next_status.lower()}"}

    @router.delete("/api/accounts/{user_id}")
    def delete_librarian(user_id: int, request: Request):
        require_admin(request)
        librarian(rows, user_id)
        execute_dml(f"DELETE FROM login_user WHERE user_id={user_id}")
        invalidate_user_sessions(user_id)
        return {"message": "Librarian account deleted"}

    @router.post("/api/auth/change-credentials")
    async def change_admin_credentials(request: Request):
        session = require_admin(request)
        data = await form_data(request)
        required(data, "currentPassword", "newUsername", "newPassword")
        username = data["newUsername"].strip()
        validate_credentials(username, data["newPassword"])

        accounts = rows(
            f"SELECT password FROM login_user WHERE user_id={session['user_id']}",
            ["password"],
        )
        if not accounts or not verify_password(data["currentPassword"], accounts[0]["password"]):
            raise HTTPException(401, "Current password is incorrect")
        if username_exists(rows, quote, username, session["user_id"]):
            raise HTTPException(409, "Username already exists")

        execute_dml(
            f"UPDATE login_user SET username={quote(username)}, "
            f"password={quote(hash_password(data['newPassword']))} "
            f"WHERE user_id={session['user_id']}"
        )
        token = request.cookies.get(SESSION_COOKIE)
        invalidate_user_sessions(session["user_id"])
        session["username"] = username
        from .session import SESSIONS

        SESSIONS[token] = session
        return {
            "message": "Administrator credentials updated",
            "username": username,
        }

    app.include_router(router)


def username_exists(rows, quote, username, excluded_user_id=None):
    exclusion = f" AND user_id<>{excluded_user_id}" if excluded_user_id else ""
    return rows(
        "SELECT COUNT(*) FROM login_user "
        f"WHERE LOWER(username)=LOWER({quote(username)}){exclusion}",
        ["count"],
        {"count"},
    )[0]["count"]


def librarian(rows, user_id):
    accounts = rows(
        "SELECT user_id||'|'||account_status FROM login_user "
        f"WHERE user_id={user_id} AND user_type='LIBRARIAN'",
        ["user_id", "account_status"],
        {"user_id"},
    )
    if not accounts:
        raise HTTPException(404, "Librarian account not found")
    return accounts[0]
