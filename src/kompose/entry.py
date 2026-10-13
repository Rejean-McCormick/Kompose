"""Minimal checks for the Entry Door. No real IAM or code issuing."""
from datetime import datetime, timezone
from hmac import compare_digest

class EntryError(ValueError):
    pass


def may_join(*, submitted_code: str, code_on_server: str, expires_at: datetime,
             now: datetime, authenticated: bool, enrolled: bool,
             seats_available: bool, session_state: str):
    """Check a temporary code AND host-provided school authorization.

    In production, code generation, rate-limits and enrollment checks belong to
    server components; do not send code_on_server to the client.
    """
    if not isinstance(expires_at, datetime) or not isinstance(now, datetime) or not expires_at.tzinfo or not now.tzinfo:
        raise EntryError("Horodatages avec fuseau requis")
    if session_state != "inscriptions":
        raise EntryError("Inscriptions fermées")
    if now >= expires_at.astimezone(timezone.utc):
        raise EntryError("Code expiré")
    if not isinstance(submitted_code, str) or not isinstance(code_on_server, str):
        raise EntryError("Code invalide")
    if not 4 <= len(submitted_code) <= 32 or not compare_digest(submitted_code.encode(), code_on_server.encode()):
        raise EntryError("Code invalide")
    if not authenticated or not enrolled:
        raise PermissionError("Identité ou inscription non autorisée")
    if not seats_available:
        raise EntryError("Capacité atteinte")
    return True
