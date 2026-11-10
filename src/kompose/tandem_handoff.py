"""Independent, read-only conformance gate for the Ekole P1 teacher preview.

NOT an Orgo authorization check or a session/workflow engine.
"""
from __future__ import annotations

import re
import json
from pathlib import Path
from uuid import UUID

TOP={'format','mode','authority','tenant_id','world_id','world_release_id','scenario_ref','workflow_ref','tasks'}
TASK={'task_ref','role_code','state','fragment_refs'}
REF=re.compile(r'[a-zA-Z0-9][a-zA-Z0-9_-]{1,63}\Z')
STATES={'ready','waiting','in_progress','done','blocked'}
MAX_BYTES = 131072

class TandemHandoffError(ValueError):
    """Nonconforming or unsafely scoped synthetic projection."""


def _ref(value: object) -> bool:
    return isinstance(value,str) and REF.fullmatch(value) is not None


def _uuid(value: object) -> bool:
    if not isinstance(value,str):return False
    try:identifier=UUID(value)
    except (ValueError,AttributeError):return False
    return identifier.int!=0 and str(identifier)==value.lower()


def verify_teacher_preview(value: object) -> dict:
    """Check the *shape* only. Does not authenticate teacher or validate release."""
    if not isinstance(value,dict) or set(value)!=TOP:
        raise TandemHandoffError('Champs non autorisés dans la projection enseignant')
    if (value['format']!='ekole.tandem-teacher-preview/1.0' or
        value['mode']!='synthetic' or value['authority']!='orgo'):
        raise TandemHandoffError('Seul l’aperçu synthétique sous autorité Orgo est accepté')
    if not all(_uuid(value[key]) for key in ('tenant_id','world_id','world_release_id')):
        raise TandemHandoffError('Contexte tenant/World/release UUID invalide')
    if not all(_ref(value[key]) for key in ('scenario_ref','workflow_ref')):
        raise TandemHandoffError('Référence invalide')
    tasks=value['tasks']
    if not isinstance(tasks,list) or not 1<=len(tasks)<=50:
        raise TandemHandoffError('Nombre de tâches hors contrat')
    ids=set()
    for row in tasks:
        if not isinstance(row,dict) or set(row)!=TASK:
            raise TandemHandoffError('Tâche invalide / champ potentiellement sensible')
        if not _ref(row['task_ref']) or not _ref(row['role_code']) or row['task_ref'] in ids:
            raise TandemHandoffError('Références de tâche ou rôle invalides')
        ids.add(row['task_ref'])
        if not isinstance(row['state'],str) or row['state'] not in STATES:
            raise TandemHandoffError('État de tâche inconnu')
        refs=row['fragment_refs']
        if not isinstance(refs,list) or len(refs)>8 or not all(_ref(ref) for ref in refs) or len(set(refs))!=len(refs):
            raise TandemHandoffError('Références de fragments invalides')
    return {'format':value['format'],'valid':True,'task_count':len(tasks),
            'authority':'orgo','mode':'synthetic','runtime_admitted':False,
            'permissions_verified':False,'world_release_verified':False}



def verify_initial_design_preview(preview: object, mission: object) -> dict:
    """Match Kontexte's initial synthetic design to the teacher preview.

    The closed Ekole P1 schema allows later *display* states such as ``done``.
    An Akor review-only handoff must not infer those from unexecuted Kontexte
    source steps. This is source fidelity, NOT actual teacher/World/Orgo approval.
    """
    verified = verify_teacher_preview(preview)
    if not isinstance(mission, dict) or mission.get('format') != 'kontexte.mission/1' or mission.get('synthetic') is not True:
        raise TandemHandoffError('Mission source Kontexte non synthétique')
    safety = mission.get('safety')
    if (not isinstance(safety, dict) or safety.get('real_spending') is not False or
            safety.get('real_taxes') is not False or safety.get('publication_default') != 'private'):
        raise TandemHandoffError('Absence de garanties privées / sans dépenses réelles')
    steps = mission.get('steps')
    declared = mission.get('roles')
    if (not isinstance(steps, list) or not isinstance(declared, list) or
            not declared or any(not _ref(role) for role in declared) or
            len(declared) != len(set(declared)) or len(steps) != verified['task_count']):
        raise TandemHandoffError('Mission / nombre de rôles ou étapes invalide')
    seen = set()
    for step, task in zip(steps, preview['tasks']):
        if not isinstance(step, dict) or not _ref(step.get('id')) or not _ref(step.get('role')):
            raise TandemHandoffError('Étape de conception invalide')
        deps = step.get('depends_on')
        if (not isinstance(deps, list) or any(not isinstance(ref, str) for ref in deps) or
                len(deps) != len(set(deps)) or any(ref not in seen for ref in deps)):
            raise TandemHandoffError('Dépendance de conception future, dupliquée ou invalide')
        expected_state = 'waiting' if deps else 'ready'
        if (step['id'] in seen or step['role'] not in declared or
                task['task_ref'] != step['id'] or task['role_code'] != step['role'] or
                task['state'] != expected_state or task['fragment_refs'] != []):
            raise TandemHandoffError('Prévisualisation divergente : ordre, état initial, rôle ou fragments')
        seen.add(step['id'])
    return {'format':'kompose.initial-design-check/1.0',
            'initial_state_checked':True, 'task_count':len(seen),
            'runtime_admitted':False, 'teacher_authorized':False,
            'dispatch_allowed':False}

def load_teacher_preview(path: str | Path) -> dict:
    """Strict file-only fixture reader aligned with Ekole P1; never talks to Orgo."""
    p = Path(path).expanduser()
    if p.is_symlink() or not p.is_file():
        raise TandemHandoffError('Fichier local régulier requis (liens symboliques interdits)')
    if p.stat().st_size > MAX_BYTES:
        raise TandemHandoffError('Projection JSON trop volumineuse')

    def reject_duplicates(pairs):
        out = {}
        for key, item in pairs:
            if key in out:
                raise TandemHandoffError('Clé JSON dupliquée')
            out[key] = item
        return out

    try:
        parsed = json.loads(p.read_text(encoding='utf-8'), object_pairs_hook=reject_duplicates)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise TandemHandoffError('JSON UTF-8 invalide') from exc
    verify_teacher_preview(parsed)
    return parsed
