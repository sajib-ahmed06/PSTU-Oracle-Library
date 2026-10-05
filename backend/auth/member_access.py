"""Public, member-only account activation and password recovery."""

import re
from fastapi import HTTPException, Request
from fastapi.responses import FileResponse
from starlette.concurrency import run_in_threadpool
from backend.audit import audit_actor
from backend.database import run_sql
from backend.validation import text_field, academic_identifier
from .passwords import hash_password
from .session import invalidate_user_sessions
from .validation import member_number, validate_password


def register_member_access_routes(router, frontend, rows, form_data, required, quote):
    @router.get("/forgot-password")
    def recovery_page():
        return FileResponse(frontend / "forgot-password.html")

    @router.post("/api/auth/reset-password")
    async def reset_password(request: Request):
        data = await form_data(request)
        required(
            data,
            "memberId",
            "rollNo",
            "registrationNo",
            "phone",
            "email",
            "password",
            "confirmPassword",
        )
        sid = member_number(data["memberId"])
        roll = academic_identifier(data["rollNo"], "ID/Roll number")
        registration = academic_identifier(data["registrationNo"], "Registration No.")
        phone = data["phone"].strip()
        if not re.fullmatch(r"[0-9]{11}", phone):
            raise HTTPException(400, "Enter the registered 11-digit phone number")
        email = text_field(data["email"], "email", 100).strip().lower()
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
            raise HTTPException(400, "Enter your registered email address")
        validate_password(data["password"])
        if data["password"] != data["confirmPassword"]:
            raise HTTPException(400, "Passwords do not match")

        def save():
            token = audit_actor.set(f"PSTU-{sid:04d}")
            try:
                run_sql(
                    (
                        f"BEGIN "
                        f"reset_student_password_proc({sid},{quote(roll)},{quote(registration)},{quote(phone)},{quote(email)},{quote(hash_password(data['password']))});"
                        f" COMMIT; END;\n/"
                    )
                )
            finally:
                audit_actor.reset(token)
            accounts = rows(
                f"SELECT user_id FROM login_user WHERE student_id={sid} AND user_type='STUDENT'",
                ["user_id"],
                {"user_id"},
            )
            for account in accounts:
                invalidate_user_sessions(account["user_id"])

        await run_in_threadpool(save)
        return {
            "message": "Password changed. Sign in with your Member ID and new password",
            "member_id": f"PSTU-{sid:04d}",
        }

    @router.get("/activate-account")
    def activation_page():
        return FileResponse(frontend / "activate-account.html")

    @router.post("/api/auth/activate")
    async def activate(request: Request):
        data = await form_data(request)
        required(data, "memberId", "phone", "password", "confirmPassword")
        sid = member_number(data["memberId"])
        phone = data["phone"].strip()
        if not re.fullmatch(r"[0-9]{11}", phone):
            raise HTTPException(400, "Enter the registered 11-digit phone number")
        validate_password(data["password"])
        if data["password"] != data["confirmPassword"]:
            raise HTTPException(400, "Passwords do not match")

        def save():
            token = audit_actor.set(f"PSTU-{sid:04d}")
            try:
                run_sql(
                    f"BEGIN activate_student_proc({sid},{quote(phone)},{quote(hash_password(data['password']))}); COMMIT; END;\n/"
                )
            finally:
                audit_actor.reset(token)
            accounts = rows(
                f"SELECT user_id FROM login_user WHERE student_id={sid}", ["user_id"], {"user_id"}
            )
            for account in accounts:
                invalidate_user_sessions(account["user_id"])

        await run_in_threadpool(save)
        return {
            "message": "Account activated. Sign in with your Member ID and password",
            "member_id": f"PSTU-{sid:04d}",
        }
