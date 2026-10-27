"""Independent, read-only conformance gate for the Ekole P1 teacher preview.

NOT an Orgo authorization check or a session/workflow engine.
"""
from __future__ import annotations

import re
from uuid import UUID

TOP={'format','mode','authority','tenant_id','world_id','world_release_id','scenario_ref','workflow_ref','tasks'}
TASK={'task_ref','role_code','state','fragment_refs'}
REF=re.compile(r'[a-zA-Z0-9][a-zA-Z0-9_-]{1,63}\Z')
STATES={'ready','waiting','in_progress','done','blocked'}

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
