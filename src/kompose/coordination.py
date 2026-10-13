"""Deterministic mission dependencies & phase coordination (no scheduler)."""
from __future__ import annotations

class CoordinationError(ValueError):
    pass


def validate_dependencies(missions):
    """Validate dependency IDs and reject cycles, including self-cycles."""
    ids = [m['id'] for m in missions]
    if len(ids) != len(set(ids)):
        raise CoordinationError("Missions dupliquées")
    graph = {m['id']: set(m.get('depends_on', [])) for m in missions}
    for node, deps in graph.items():
        missing = deps - graph.keys()
        if missing:
            raise CoordinationError(f"{node}: dépendances inconnues {sorted(missing)}")
    visited = set()
    visiting = set()
    def visit(node):
        if node in visiting:
            raise CoordinationError(f"Cycle détecté : {node}")
        if node in visited:
            return
        visiting.add(node)
        for dep in sorted(graph[node]):
            visit(dep)
        visiting.remove(node)
        visited.add(node)
    for node in graph:
        visit(node)
    return graph


def ready_missions(missions, completed_ids):
    """Return missions available from fulfilled prerequisites, without PII."""
    graph = validate_dependencies(missions)
    completed = set(completed_ids)
    if not completed <= graph.keys():
        raise CoordinationError("Mission terminée inconnue")
    return [m['id'] for m in missions
            if m['id'] not in completed and graph[m['id']] <= completed]


def advance_phase(*, current_phase: str, next_phase: str, ordered_phases: list[str],
                  pending_blockers: list[str], teacher_override: bool = False):
    """Pure phase transition; produces event payload to persist by the host.

    A teacher override may bypass pedagogical blockers, not security/rights.
    """
    if len(ordered_phases) != len(set(ordered_phases)) or not ordered_phases:
        raise CoordinationError("Phases invalides")
    try:
        pos = ordered_phases.index(current_phase)
    except ValueError as exc:
        raise CoordinationError("Phase courante inconnue") from exc
    if pos + 1 >= len(ordered_phases) or ordered_phases[pos + 1] != next_phase:
        raise CoordinationError("Transition de phase non séquentielle")
    if pending_blockers and not teacher_override:
        raise CoordinationError("Dépendances non satisfaites")
    if any(not isinstance(b, str) or not b for b in pending_blockers):
        raise CoordinationError("Identifiant de blocage invalide")
    return {"name": "session.phase_changee", "payload": {
        "from_phase": current_phase, "to_phase": next_phase,
        "pedagogical_override": bool(pending_blockers and teacher_override),
        "pending_count": len(pending_blockers),
    }}


def guardian_fallback(kristal_id, active_guardian, fallback_guardian, available):
    """Propose a custody transfer; host verifies eligibility, approval and audit.

    Never changes the documentary Kristal or grants new reading rights.
    """
    if not all(isinstance(v, str) and v for v in (kristal_id, active_guardian, fallback_guardian)):
        raise CoordinationError("Identifiants invalides")
    if active_guardian == fallback_guardian or fallback_guardian not in set(available):
        raise CoordinationError("Gardien de secours indisponible")
    return {"name": "kristal.transfert_propose", "payload": {
        "kristal_id": kristal_id,
        "from_guardian_id": active_guardian,
        "to_guardian_id": fallback_guardian,
        "requires_teacher_approval": True,
    }}
