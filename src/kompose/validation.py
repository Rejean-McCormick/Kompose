"""Contrôles sémantiques inter-fichiers; pas un moteur JSON Schema exhaustif."""
from __future__ import annotations
import json
from pathlib import Path

class ReferenceError(ValueError):
    """Violation du contrat de référence."""

def load_json(path: Path):
    with Path(path).open(encoding="utf-8") as f:
        return json.load(f)

def _unique(items, label, errors):
    ids = [x.get("id") for x in items]
    if any(not isinstance(i, str) or not i.strip() for i in ids):
        errors.append(f"{label}: identifiant manquant")
    if len(ids) != len(set(ids)):
        errors.append(f"{label}: identifiants dupliqués")
    return set(ids)

def publication_ready(kristal):
    """Barrage de publication: aucun savoir sans sources, droit et revue.

    Des contrôles juridiques/éditoriaux supplémentaires sont requis en production.
    """
    if kristal.get("status") != "published":
        return False
    sources = kristal.get("sources", [])
    review = kristal.get("editorial_review", {})
    if not sources or not all(s.get("verified") is True and s.get("rights_cleared") is True
                              and s.get("citation") and "NE PAS PUBLIER" not in s.get("citation", "")
                              for s in sources):
        return False
    if review.get("status") != "approved" or not review.get("reviewed_at") or not review.get("reviewer_ref"):
        return False
    perspective = kristal.get("perspective", {})
    if perspective.get("type") == "nation_autochtone_identifiee":
        if perspective.get("attribution") in (None, "", "À définir"):
            return False
        if review.get("community_review_status") != "approved":
            return False
    return True

def validate_directory(directory: Path):
    directory = Path(directory)
    errors = []
    files = {name:load_json(directory / name) for name in (
        'capsule.json','roles.json','kristals.json','missions.json','prompts.json',
        'diagnostic.json','session.example.json','teacher-constraints.PRIVE-DEMO.json')}
    capsule=files['capsule.json']
    roles=files['roles.json']['roles']
    kristals=files['kristals.json']['kristals']
    missions=files['missions.json']['missions']
    prompts=files['prompts.json']['prompts']
    role_ids=_unique(roles, 'Rôles', errors)
    kristal_ids=_unique(kristals, 'Kristals', errors)
    mission_ids=_unique(missions, 'Missions', errors)
    _unique(prompts, 'Prompts', errors)
    for name, refs, available in [
        ('Rôles de capsule',capsule.get('roles',[]),role_ids),
        ('Kristals de capsule',capsule.get('kristals',[]),kristal_ids),
        ('Missions de capsule',capsule.get('missions',[]),mission_ids)]:
        if len(refs)!=len(set(refs)):
            errors.append(f'{name}: référence dupliquée')
        if not refs or not set(refs).issubset(available):
            errors.append(f'{name}: référence manquante')
    for role in roles:
        if role.get('capacity',0)<1:
            errors.append(f"{role.get('id')}: capacité invalide")
        if not set(role.get('collaborates_with',[])).issubset(role_ids):
            errors.append(f"{role.get('id')}: collaboration vers rôle inconnu")
        if not set(role.get('mission_refs',[])).issubset(mission_ids):
            errors.append(f"{role.get('id')}: référence mission inconnue")
    from .coordination import validate_dependencies, CoordinationError
    try:
        validate_dependencies(missions)
    except CoordinationError as exc:
        errors.append(str(exc))
    for mission in missions:
        if not set(mission.get('related_roles',[])).issubset(role_ids):
            errors.append(f"{mission.get('id')}: rôle inconnu")
        if not set(mission.get('related_kristals',[])).issubset(kristal_ids):
            errors.append(f"{mission.get('id')}: Kristal inconnu")
        if not mission.get('accessibility_alternative'):
            errors.append(f"{mission.get('id')}: alternative accessible manquante")
    for kristal in kristals:
        kid=kristal.get('id')
        if kristal.get('status') == 'published' and not publication_ready(kristal):
            errors.append(f'{kid}: publication sans validation complète')
        if kristal.get('status')=='demo' and any(s.get('verified') for s in kristal.get('sources',[])):
            errors.append(f'{kid}: demo ne doit pas prétendre à des sources vérifiées')
        src_ids = _unique(kristal.get('sources',[]),f'{kid}/sources',errors)
        topic_ids = _unique(kristal.get('topics',[]),f'{kid}/topics',errors)
        all_questions=[]
        for topic in kristal.get('topics',[]):
            for question in topic.get('questions',[]):
                all_questions.append(question)
                if not set(question.get('source_refs',[])).issubset(src_ids):
                    errors.append(f"{kid}/{question.get('id')}: source inconnue")
                if not question.get('answer') or not question.get('limitations'):
                    errors.append(f"{kid}/{question.get('id')}: réponse ou limites manquantes")
        _unique(all_questions,f'{kid}/questions',errors)
        if not topic_ids or not all_questions:
            errors.append(f'{kid}: aucun thème ou question')
    events={'session.roles_publies','role.attribue','kristal.garde_attribuee','kristal.acces_demande','kristal.acces_accorde','kristal.question_consultee','mission.validee'}
    for prompt in prompts:
        if prompt.get('on_event') not in events:
            errors.append(f"{prompt.get('id')}: événement inconnu")
        if prompt.get('dedup_scope')!='event_recipient':
            errors.append(f"{prompt.get('id')}: déduplication incorrecte")
        if 'P-00' in prompt.get('body',''):
            errors.append(f"{prompt.get('id')}: identifiant d'élève dans texte public")
    assign=capsule.get('assignment',{})
    if assign.get('mode')=='tiers_choix' and not (0 < assign.get('top_fraction',0) <= 1):
        errors.append('Quotité de premier choix invalide')
    if assign.get('teacher_approval_required') is not True:
        errors.append('Approbation enseignante manquante')
    if assign.get('fallback_mode')!='attribution_guidee':
        errors.append('Alternative sûre au classement manquante')
    diag=files['diagnostic.json']
    if diag.get('comparability_check_required') is not True or diag.get('default_on_invalid')!='attribution_guidee':
        errors.append('Diagnostic: comparabilité/repli manquant')
    session=files['session.example.json']
    if session.get('capsule_id')!=capsule.get('id') or session.get('capsule_version')!=capsule.get('version'):
        errors.append('Session: capsule/version invalide')
    if len(session.get('participants',[])) != len(set(session.get('participants',[]))):
        errors.append('Session: participant en doublon')
    if session.get('state') != 'brouillon' and any(k.get('status')!='published' for k in kristals):
        errors.append('Séance active avec contenus non publiés')
    for k in kristals:
        if session.get('content_versions',{}).get(k['id'])!=k.get('version'):
            errors.append(f"Session: version de {k['id']} non épinglée")
    priv=files['teacher-constraints.PRIVE-DEMO.json']
    for c in priv.get('constraints',[]):
        if not set(c.get('participant_ids',[])).issubset(set(session.get('participants',[]))):
            errors.append(f"{c.get('id')}: participants hors séance")
        if c.get('type') == 'separation_securite' and c.get('strength')!='hard':
            errors.append(f"{c.get('id')}: contrainte de sécurité doit être dure")
        if not c.get('reason_private') or not c.get('expires_at'):
            errors.append(f"{c.get('id')}: justification/expiration absente")
    phases_path=directory/'phases.json'
    if phases_path.exists():
        phases=load_json(phases_path).get('phases',[])
        phase_ids=_unique(phases,'Phases',errors)
        if not phases or sorted(p.get('order', -1) for p in phases) != list(range(len(phases))):
            errors.append('Phases: séquence contiguë requise dès zéro')
        if any(not set(p.get('blocking_missions',[])).issubset(mission_ids) for p in phases):
            errors.append('Phases: référence vers mission inconnue')
        if session.get('phase_id') not in phase_ids:
            errors.append('Session: phase inconnue')
    preview_path=directory/'allocation.preview.example.json'
    if preview_path.exists():
        preview=load_json(preview_path)
        assignments=preview.get('assignments',[])
        if preview.get('publishable') is not False:
            errors.append('Prévisualisation: doit rester non publiable')
        if len(assignments)!=len(session.get('participants',[])):
            errors.append('Prévisualisation: nombre d’attributions incorrect')
        if set(a.get('participant_id') for a in assignments)!=set(session.get('participants',[])):
            errors.append('Prévisualisation: participants manquants ou supplémentaires')
        if any(a.get('role_id') not in role_ids for a in assignments):
            errors.append('Prévisualisation: rôle inconnu')
        if len(set(a.get('role_id') for a in assignments)) != len(assignments):
            # La fixture a seulement des rôles unitaires.
            errors.append('Prévisualisation: rôle unitaire attribué plusieurs fois')
        chosen=sum(a.get('channel')=='choix_premier_tiers' for a in assignments)
        import math
        expected=math.ceil(len(session.get('participants',[]))*assign.get('top_fraction',0)-1e-12)
        if chosen!=expected or preview.get('quota_first_choice')!=expected:
            errors.append('Prévisualisation: quota premier tiers incohérent')
    return errors
