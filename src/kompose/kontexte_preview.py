"""Adapter: Kontexte definitions -> a non-executable KOMPOSE pedagogical preview.

Orgo is canonical for real Case/Task/Signal transitions (Kontexte ADR-001).
This module NEVER creates Cases, assigns learners, delivers fragments or makes calls.
"""
from __future__ import annotations

import hashlib
import json

from .coordination import CoordinationError, ready_missions, validate_dependencies


class ScenarioPreviewError(ValueError):
    """A Kontexte scenario is unsuitable even for the dry-run preview."""


def _text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 240:
        raise ScenarioPreviewError(f"{field} invalide")
    return value


def _localized(value: object, field: str) -> str:
    if not isinstance(value, dict) or not isinstance(value.get('fr-CA'), str) or not value['fr-CA'].strip():
        raise ScenarioPreviewError(f"{field}: texte fr-CA requis")
    return value['fr-CA']


def compile_preview(mission: dict, roles: list[dict], *, target_course_id: str | None = None) -> dict:
    """Produce a safe scenario *plan*, without changing Orgo or learner state.

    Role/fragment IDs are definitions, not assignments of real people. 'curriculum_ids'
    are source claims and deliberately NOT silently remapped to target_course_id.
    """
    if not isinstance(mission, dict) or mission.get('format') != 'kontexte.mission/1':
        raise ScenarioPreviewError('Mission Kontexte au format attendu requise')
    if mission.get('synthetic') is not True:
        raise ScenarioPreviewError('Seuls les scénarios explicitement synthétiques sont admissibles en aperçu')
    mid = _text(mission.get('id'), 'id mission')
    _text(mission.get('version'), 'version mission')
    title = _localized(mission.get('title'), 'title')
    fiction = _localized(mission.get('fiction'), 'fiction')
    if not isinstance(roles, list) or not isinstance(mission.get('roles'), list):
        raise ScenarioPreviewError('Liste des rôles manquante')
    declared = mission['roles']
    if not declared or any(not isinstance(x, str) for x in declared) or len(declared) != len(set(declared)):
        raise ScenarioPreviewError('Rôles déclarés dupliqués ou invalides')
    all_roles = {}
    for role in roles:
        if not isinstance(role,dict) or role.get('format') != 'kontexte.role/1':
            raise ScenarioPreviewError('Définition de rôle Kontexte invalide')
        rid = _text(role.get('id'), 'id rôle')
        if rid in all_roles:
            raise ScenarioPreviewError('Définitions de rôles dupliquées')
        all_roles[rid] = role
    missing = sorted(set(declared) - all_roles.keys())
    if missing:
        raise ScenarioPreviewError(f'Rôles non définis : {missing}')
    if not isinstance(mission.get('steps'), list) or not mission['steps']:
        raise ScenarioPreviewError('Aucune étape disponible')
    steps = []
    for raw in mission['steps']:
        if not isinstance(raw,dict) or not isinstance(raw.get('depends_on'),list):
            raise ScenarioPreviewError('Étape ou dépendances invalides')
        sid = _text(raw.get('id'), 'id étape')
        rid = _text(raw.get('role'), 'rôle étape')
        if rid not in declared:
            raise ScenarioPreviewError(f'{sid}: rôle non prévu')
        if any(not isinstance(dep,str) or not dep for dep in raw['depends_on']) or len(raw['depends_on']) != len(set(raw['depends_on'])):
            raise ScenarioPreviewError(f'{sid}: dépendance invalide')
        validation = raw.get('validation')
        if validation not in {'human_review', 'deterministic_practice', 'logistical_only'}:
            raise ScenarioPreviewError(f'{sid}: mode de validation Kontexte non reconnu')
        if not isinstance(raw.get('curriculum_ids'),list) or any(not isinstance(v,str) or not v for v in raw['curriculum_ids']):
            raise ScenarioPreviewError(f'{sid}: références pédagogiques invalides')
        steps.append({'id':sid,'role':rid,'instruction':_localized(raw.get('instruction'),'instruction'),
                      'kind':_text(raw.get('kind'),'kind'),'depends_on':list(raw['depends_on']),
                      'curriculum_ids':list(raw['curriculum_ids']), 'validation':validation})
    try:
        validate_dependencies(steps)
    except (CoordinationError, KeyError, TypeError) as exc:
        raise ScenarioPreviewError(f'Graphe des étapes invalide : {exc}') from exc
    # A join is a source intent; only Orgo can implement access-controlled delivery.
    fragments = []
    for item in mission.get('fragments',[]):
        if not isinstance(item,dict):raise ScenarioPreviewError('Fragment invalide')
        fid = _text(item.get('id'),'id fragment')
        holder = _text(item.get('holder_role'),'détenteur de fragment')
        if holder not in declared or item.get('release') != 'orgo_authorized' or item.get('visibility') != 'participant':
            raise ScenarioPreviewError(f'{fid}: protection des fragments insuffisante')
        _localized(item.get('content'), 'contenu fragment') # Verifier, mais NE PAS l'inclure dans le plan partage.
        fragments.append({'id':fid,'holder_role':holder,'release':'orgo_authorized','visibility':'participant'})
    if len({f['id'] for f in fragments}) != len(fragments):
        raise ScenarioPreviewError('Identifiants de fragments dupliqués')
    fragment_ids = {f['id'] for f in fragments}
    joins=[]
    for item in mission.get('joins',[]):
        if not isinstance(item,dict) or not isinstance(item.get('fragment_ids'),list):
            raise ScenarioPreviewError('Jointure invalide')
        jid = _text(item.get('id'),'id jointure')
        refs = item['fragment_ids']
        if not refs or any(not isinstance(v,str) or not v for v in refs) or len(set(refs)) != len(refs) or not set(refs) <= fragment_ids:
            raise ScenarioPreviewError(f'{jid}: fragments manquants ou dupliqués')
        unlock = _text(item.get('unlock_step'),'étape de déblocage')
        if unlock not in {s['id'] for s in steps}:
            raise ScenarioPreviewError(f'{jid}: étape cible inconnue')
        joins.append({'id':jid,'fragment_ids':list(refs),'unlock_step':unlock,
                      'enforcement':'orgo_not_implemented'})
    if len({j['id'] for j in joins}) != len(joins):
        raise ScenarioPreviewError('Jointures dupliquées')
    source = json.dumps(mission,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf-8')
    digest = hashlib.sha256(source).hexdigest()
    referenced = sorted({c for step in steps for c in step['curriculum_ids']})
    warnings = ['Scénario de squelette Kontexte, non validé pédagogiquement.',
                'Dépendances, fragments et jointures ne sont PAS installés dans Orgo.',
                'Aucun Task COMPLETED ne valide une compétence scolaire.']
    if mission.get('status') != 'scenario_skeleton_requires_pedagogical_review':
        warnings.append('Statut source non reconnu : exiger une revue de contenu.')
    if target_course_id and target_course_id not in referenced:
        warnings.append(f'Écart de référentiel : cible {target_course_id}, sources {", ".join(referenced)}. Aucun remappage automatique.')
    return {
        'format':'kompose.kontexte-preview/1','preview_only':True,
        'canonical_runtime':'orgo','dispatch_allowed':False,
        'scenario':{'id':mid,'title':title,'fiction':fiction,'version':mission['version'],
                    'synthetic':True,'source_status':mission.get('status'),'sha256':digest},
        'roles':[{'id':rid,'name':_localized(all_roles[rid].get('name'),'nom rôle')}
                 for rid in declared],
        'steps':steps,'fragments':fragments,'joins':joins,
        'curriculum':{'source_ids':referenced,'target_course_id':target_course_id,
                      'target_mapped': target_course_id in referenced if target_course_id else None,
                      'mastery_evaluated':False},
        'handoff':{'owner':'orgo','mode':'review_only',
                   'needs':['reviewed_workflow_version','identity_and_authorization',
                            'fragment_release_guards','join_proofs','absence_fallback',
                            'atomic_events_outbox'],
                   'note':'Pour une fixture Orgo de préparation réelle, utiliser le compilateur canonique Kontexte orgo.scenario_fixture; ne pas dupliquer la création de Case/Task ici.'},
        'warnings':warnings,
    }


def role_projection(plan: dict, role_id: str) -> dict:
    """Student-facing preview, with NO private fragment text or other role prompts."""
    available = {r['id'] for r in plan['roles']}
    if role_id not in available:
        raise ScenarioPreviewError('Rôle inconnu')
    own_steps = [{'id':step['id'],'instruction':step['instruction'],
                  'depends_on':list(step['depends_on'])} for step in plan['steps'] if step['role']==role_id]
    return {'format':'kompose.role-preview/1','role_id':role_id,
            'role_name':next(r['name'] for r in plan['roles'] if r['id']==role_id),
            'steps':own_steps,'not_authorization':True,
            'message':'Aperçu fictif : seul Orgo pourra autoriser une véritable mission et ses indices.'}


def ready_preview_steps(plan: dict, completed: set[str], released_fragments: set[str]) -> list[str]:
    """Dry-run projection of readiness only. Never advances actual state."""
    missions = [{'id':s['id'],'depends_on':s['depends_on']} for s in plan['steps']]
    if not released_fragments <= {f['id'] for f in plan['fragments']}:
        raise ScenarioPreviewError('Fragment autorisé inconnu')
    try:
        ready = set(ready_missions(missions,completed))
    except CoordinationError as exc:
        raise ScenarioPreviewError(str(exc)) from exc
    for join in plan['joins']:
        if not set(join['fragment_ids']) <= released_fragments:
            ready.discard(join['unlock_step'])
    return [s['id'] for s in plan['steps'] if s['id'] in ready]


def propose_absence_fallback(plan: dict, absent_role_id: str) -> dict:
    """Propose a private teacher-mediated alternative; NEVER changes access rights.

    A real substitute and re-assignment are Orgo Work/Orchestration concerns,
    and must not be inferred from the content-side role label alone.
    """
    if plan.get('format') != 'kompose.kontexte-preview/1':
        raise ScenarioPreviewError('Aperçu de scénario requis')
    if absent_role_id not in {r['id'] for r in plan['roles']}:
        raise ScenarioPreviewError('Rôle absent inconnu')
    affected = [s['id'] for s in plan['steps'] if s['role'] == absent_role_id]
    held = [f['id'] for f in plan['fragments'] if f['holder_role'] == absent_role_id]
    return {
        'format':'kompose.absence-fallback-proposal/1','preview_only':True,
        'absent_role':absent_role_id,'affected_steps':affected,
        'affected_fragment_ids':held,'status':'teacher_and_orgo_approval_required',
        'suggestions':['prévoir un partenaire de substitution supervisé',
                       'permettre une consigne différée ou médiée par l’enseignant'],
        'automatically_assigned_roles':[], 'granted_fragments':[],
        'orgo_mutations':0,
    }
