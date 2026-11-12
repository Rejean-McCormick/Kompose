"""Suggestions d'incarnation de personnages, uniquement pour l'enseignant.

Kompose propose; l'enseignant choisit; Orgo attribue à des identités
vérifiées. Un manque de preuve n'est pas un score d'intelligence. Le calcul
n'utilise aucun trait sensible ni ne délivre d'autorisation.
"""
from __future__ import annotations
import hashlib
import re

REF=re.compile(r'[a-zA-Z0-9][a-zA-Z0-9._:-]{1,99}\Z')


def _safe_ref(value):
    if not isinstance(value,str) or not REF.fullmatch(value):
        raise ValueError('Référence non pseudonyme ou invalide')
    return value


def propose_roles(mission, learners, *, seed='revue-enseignant'):
    """Return unique role proposals without assignments or permission changes.

    Each learner supplies explicit curricular IDs: ``pratique_souhaitee`` and
    ``deja_pratique``.  No psychometric comparisons across children.  Matching
    is seeded for reproducibility and can leave roles unfilled.
    """
    if mission.get('format')!='kontexte.mission/1' or mission.get('synthetic') is not True:
        raise ValueError('Mission source synthétique requise')
    safety=mission.get('safety')
    if not isinstance(safety,dict) or safety.get('publication_default')!='private':
        raise ValueError('Garanties de confidentialité absentes')
    roles=mission.get('roles',[])
    if not isinstance(roles,list) or len(roles)!=len(set(roles)) or not roles:
        raise ValueError('Rôles incohérents')
    for role in roles:_safe_ref(role)
    if not isinstance(learners,list) or not 1 <= len(learners) <= 100:
        raise ValueError('Participants de revue requis')
    children={}
    for row in learners:
        if not isinstance(row,dict) or set(row)!={'eleve_ref','pratique_souhaitee','deja_pratique'}:
            raise ValueError('Données de participant hors contrat')
        pid=_safe_ref(row['eleve_ref'])
        if pid in children:raise ValueError('Participant dupliqué')
        for key in ('pratique_souhaitee','deja_pratique'):
            if not isinstance(row[key],list) or any(not isinstance(x,str) or not REF.fullmatch(x) for x in row[key]):
                raise ValueError('Références d’objectif invalides')
        children[pid]={'needs':set(row['pratique_souhaitee']),'done':set(row['deja_pratique'])}
    if not isinstance(seed,str) or len(seed)<4:
        raise ValueError('Graine de revue nécessaire')
    skills={role:set() for role in roles}
    for step in mission.get('steps',[]):
        if step.get('role') not in skills:raise ValueError('Étape avec personnage inconnu')
        skills[step['role']].update(step.get('curriculum_ids',[]))
    remaining=set(children)
    proposals=[]
    for role in roles:
        if not remaining:
            proposals.append({'role_code':role,'eleve_ref':None,'raison':'À attribuer par l’enseignant'})
            continue
        def key(pid):
            relevant=skills[role]
            # Learning opportunities first; existing practice is a
            # complementary asset, not a universal person rank.
            need=len(relevant & children[pid]['needs'])
            practiced=len(relevant & children[pid]['done'])
            tie=hashlib.sha256(f'{seed}:{role}:{pid}'.encode()).hexdigest()
            return (-need,-practiced,tie)
        best=min(remaining,key=key)
        remaining.remove(best)
        relevant=skills[role]
        needs=sorted(relevant & children[best]['needs'])
        done=sorted(relevant & children[best]['done'])
        reason=('Occasion de pratiquer : '+', '.join(needs)) if needs else (
            'Expérience liée : '+', '.join(done) if done else 'Proposition de répartition, à revoir')
        proposals.append({'role_code':role,'eleve_ref':best,'raison':reason})
    return {'format':'kompose.school-role-proposals/1',
            'mission_ref':mission['id'],'teacher_approval_required':True,
            'runtime_admitted':False,'dispatch_allowed':False,
            'propositions':proposals}
