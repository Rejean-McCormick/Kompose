"""Reference pure state machine for a KOMPOSE session.

No persistence, authentication, clocks or network activity: the host supplies
actor authorization, persistence and transactional optimistic locking.
"""
from __future__ import annotations
from copy import deepcopy

class SessionTransitionError(ValueError):
    """An action is disallowed by the session's current state or guard."""

# Current nomenclature preserves the French v0.1 data contracts.
_STEPS = {
    ("brouillon", "prepare"): ("pret", "session.prete"),
    ("pret", "open"): ("inscriptions", "session.ouverte"),
    ("inscriptions", "close_enrollment"): ("diagnostic", "session.inscriptions_closes"),
    ("diagnostic", "close_diagnostic"): ("attribution", "session.diagnostic_clos"),
    ("attribution", "preview_assignment"): ("validation", "session.attribution_proposee"),
    ("validation", "revise_assignment"): ("attribution", "session.attribution_revision"),
    ("validation", "publish_assignment"): ("aventure", "session.roles_publies"),
    ("aventure", "finish"): ("terminee", "session.terminee"),
}
_TERMINAL = {"terminee", "annulee"}
_PAUSABLE = {"inscriptions", "diagnostic", "attribution", "validation", "aventure"}


def apply_session_command(session: dict, action: str, *, actor_role: str,
                          expected_version: int, guards: dict | None = None):
    """Return (new_session, event). Never mutates input.

    Host MUST authenticate/authorize teacher, use a transactional version check,
    and atomically persist state + event. This function is NOT an access layer.
    """
    if actor_role != "teacher":
        raise PermissionError("Commande de cycle de vie réservée à un enseignant autorisé")
    if not isinstance(expected_version, int) or isinstance(expected_version, bool):
        raise SessionTransitionError("Version attendue invalide")
    actual = session.get("version", 0)
    if actual != expected_version:
        raise SessionTransitionError("Version de séance périmée")
    old = session.get("state")
    if not session.get("id") or not session.get("capsule_id"):
        raise SessionTransitionError("Séance non identifiable")
    flags = guards or {}
    s = deepcopy(session)
    if action == "pause" and old in _PAUSABLE:
        s["paused_from"] = old
        nxt, event_name = "suspendue", "session.suspendue"
    elif action == "resume" and old == "suspendue":
        nxt = s.pop("paused_from", None)
        if nxt not in _PAUSABLE:
            raise SessionTransitionError("État de reprise inconnu")
        event_name = "session.reprise"
    elif action == "cancel" and old not in _TERMINAL:
        nxt, event_name = "annulee", "session.annulee"
        s.pop("paused_from", None)
    elif (old, action) in _STEPS:
        nxt, event_name = _STEPS[(old, action)]
    else:
        raise SessionTransitionError(f"Transition interdite : {old!r} / {action!r}")

    # Explicit approval gates; never infer validity from the action itself.
    if action == "prepare" and flags.get("content_ready") is not True:
        raise SessionTransitionError("Contenus non validés")
    if action == "close_diagnostic" and flags.get("diagnostics_reviewed") is not True:
        raise SessionTransitionError("Diagnostics non vérifiés; prévoir le mode guidé")
    if action == "preview_assignment" and flags.get("plan_checked") is not True:
        raise SessionTransitionError("Attribution non vérifiée")
    if action == "publish_assignment":
        if s.get("teacher_approval") is not True:
            raise SessionTransitionError("Approbation explicite de l'enseignant requise")
        if not all(flags.get(k) is True for k in ("hard_constraints_satisfied", "roles_complete", "accessibility_checked")):
            raise SessionTransitionError("Contraintes, couverture des rôles ou accessibilité non confirmées")
    s["state"] = nxt
    s["version"] = expected_version + 1
    event = {
        "name": event_name,
        "aggregate_id": s["id"],
        "session_id": s["id"],
        "payload": {"from_state": old, "to_state": nxt, "session_version": s["version"]},
    }
    return s, event
