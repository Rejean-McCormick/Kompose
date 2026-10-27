"""Pure, local dry-run over fictional *receipts* purportedly provided by a mock Orgo.

Not an operational workflow engine. Never talks to Orgo, manages users, stores
records, delivers a clue, grades children, or changes a real mission.
"""
from __future__ import annotations
import json
import re
from .kontexte_preview import ScenarioPreviewError, ready_preview_steps


_ALLOWED = {
    'event_id','sequence','source','synthetic','kind','step_id','role_id',
    'fragment_id','human_reviewed','teacher_authorized',
}


def replay_receipts(plan: dict, receipts: list[dict]) -> dict:
    """Validate a sequence of externally-simulated receipts, preserving idempotence.

    The sequence is NOT a substitute for Orgo's transaction/version/outbox. Mock
    receipts prove nothing about real permissions; teacher_authorized is a
    fixture assertion, never an authorization check in a deployed system.
    """
    if plan.get('format') != 'kompose.kontexte-preview/1' or plan.get('preview_only') is not True:
        raise ScenarioPreviewError('Aperçu compilé attendu')
    if not isinstance(receipts,list):
        raise ScenarioPreviewError('Journal synthétique invalide')
    steps={step['id']:step for step in plan['steps']}
    frags={f['id']:f for f in plan['fragments']}
    completed=set()
    released=set()
    seen={}
    history=[]
    paused=False
    sequence=0
    for row in receipts:
        if not isinstance(row,dict) or set(row)-_ALLOWED:
            raise ScenarioPreviewError('Reçu invalide ou transportant des données non autorisées')
        eid=row.get('event_id')
        if not isinstance(eid,str) or not re.fullmatch(r'[A-Za-z0-9_.-]{1,90}',eid):
            raise ScenarioPreviewError('event_id obligatoire')
        if row.get('source') != 'orgo_mock_fixture' or row.get('synthetic') is not True:
            raise ScenarioPreviewError('Reçu non synthétique interdit dans le démonstrateur')
        canonical=json.dumps(row,sort_keys=True,ensure_ascii=False)
        if eid in seen:
            if seen[eid] != canonical:
                raise ScenarioPreviewError('Reçu dupliqué avec contenu contradictoire')
            continue   # transport re-delivery: strictly idempotent in this pure preview
        rev=row.get('sequence')
        if not isinstance(rev,int) or isinstance(rev,bool) or rev != sequence+1:
            raise ScenarioPreviewError('Séquence non linéaire : rejeter les événements périmés ou sautés')
        kind=row.get('kind')
        if kind=='pause':
            if paused or row.get('teacher_authorized') is not True:
                raise ScenarioPreviewError('Pause déjà active ou autorisation enseignante absente')
            paused=True
        elif kind=='resume':
            if not paused or row.get('teacher_authorized') is not True:
                raise ScenarioPreviewError('Reprise invalide')
            paused=False
        elif kind=='step_completed':
            if paused:raise ScenarioPreviewError('Mission en pause')
            sid=row.get('step_id')
            if sid not in steps or sid not in ready_preview_steps(plan,completed,released):
                raise ScenarioPreviewError('Étape inconnue, déjà terminée ou prérequis manquants')
            if row.get('role_id') != steps[sid]['role'] or row.get('human_reviewed') is not True:
                raise ScenarioPreviewError('Rôle erroné ou revue humaine manquante')
            completed.add(sid)
        elif kind=='fragment_authorized':
            if paused:raise ScenarioPreviewError('Mission en pause')
            fid=row.get('fragment_id')
            if fid not in frags or fid in released:
                raise ScenarioPreviewError('Fragment inconnu ou déjà autorisé')
            if row.get('role_id') != frags[fid]['holder_role'] or row.get('teacher_authorized') is not True:
                raise ScenarioPreviewError('Détenteur erroné ou autorisation fictive manquante')
            released.add(fid)
        else:
            raise ScenarioPreviewError('Action du journal non reconnue')
        seen[eid]=canonical
        sequence=rev
        history.append({'event_id':eid,'sequence':sequence,'kind':kind})
    return {
        'format':'kompose.orgo-mock-replay/1',
        'status':'demonstration_only', 'canonical_runtime':'orgo', 'orgo_operations_performed':0,
        'session_state':'paused' if paused else 'preview_open',
        'completed_steps':[step['id'] for step in plan['steps'] if step['id'] in completed],
        'ready_steps':[] if paused else ready_preview_steps(plan,completed,released),
        'authorized_fragment_ids':sorted(released), # IDs only, no fragment content
        'evidence':{'operational_tasks_completed':len(completed),
                    'school_competencies_mastered':None,'validated_by_teacher_in_real_system':False},
        'accepted_event_count':len(history), 'duplicate_count':len(receipts)-len(history),
        'events':history,
    }
