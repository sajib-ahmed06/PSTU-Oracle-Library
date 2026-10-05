import secrets
import time
from urllib.parse import urlsplit

from fastapi import HTTPException
from backend.audit import audit_actor
from fastapi.responses import JSONResponse, RedirectResponse

SESSION_COOKIE = "library_session"
SESSION_SECONDS = 8 * 60 * 60
SESSIONS = {}


def current_session(request):
    token = request.cookies.get(SESSION_COOKIE)
    session = SESSIONS.get(token)
    if not session:
        return None
    if session["expires"] <= time.time():
        SESSIONS.pop(token, None)
        return None
    return session


def require_admin(request):
    session = current_session(request)
    if not session or session["user_type"] != "ADMIN":
        raise HTTPException(403, "Administrator access required")
    return session


def create_session(user):
    now = time.time()
    for expired_token, session in list(SESSIONS.items()):
        if session["expires"] <= now:
            SESSIONS.pop(expired_token, None)
    token = secrets.token_urlsafe(32)
    SESSIONS[token] = {
        "user_id": user["user_id"],
        "username": user["username"],
        "user_type": user["user_type"],
        "student_id": user.get("student_id"),
        "expires": time.time() + SESSION_SECONDS,
    }
    return token


def remove_session(token):
    if token:
        SESSIONS.pop(token, None)


def invalidate_user_sessions(user_id):
    expired_tokens = [token for token, session in SESSIONS.items() if session["user_id"] == user_id]
    for token in expired_tokens:
        SESSIONS.pop(token, None)


def install_authentication(app):
    @app.middleware("http")
    async def require_authentication(request, call_next):
        path = request.url.path
        public = (
            path == "/login"
            or path == "/activate-account"
            or path == "/forgot-password"
            or path == "/api/health"
            or path
            in {
                "/api/auth/login",
                "/api/auth/activate",
                "/api/auth/reset-password",
                "/api/auth/session",
                "/api/auth/logout",
            }
            or path.startswith("/static/")
        )
        if request.method not in {"GET", "HEAD", "OPTIONS"}:
            origin = request.headers.get("origin")
            if origin and (urlsplit(origin).scheme, urlsplit(origin).netloc) != (
                request.url.scheme,
                request.url.netloc,
            ):
                return JSONResponse(
                    {"detail": "Cross-origin changes are not allowed"}, status_code=403
                )
        if public or current_session(request):
            session = current_session(request)
            if session and session["user_type"] == "STUDENT" and not public:
                allowed = path in {
                    "/student",
                    "/api/student/dashboard",
                    "/api/student/password",
                    "/api/reservations",
                }
                allowed = allowed or (
                    path.startswith("/api/reservations/") and path.endswith("/cancel")
                )
                if not allowed:
                    if path.startswith("/api/"):
                        return JSONResponse(
                            {"detail": "Management access required"}, status_code=403
                        )
                    return RedirectResponse("/student", status_code=303)
            token = audit_actor.set(session["username"] if session else "")
            try:
                response = await call_next(request)
            finally:
                audit_actor.reset(token)
            if not path.startswith("/static/"):
                response.headers["Cache-Control"] = "no-store"
            return response
        if path.startswith("/api/"):
            return JSONResponse({"detail": "Authentication required"}, status_code=401)
        return RedirectResponse("/login", status_code=303)
