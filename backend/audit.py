"""Request actor propagation for transactional Oracle audit triggers."""

from contextvars import ContextVar

audit_actor = ContextVar("audit_actor", default="")
