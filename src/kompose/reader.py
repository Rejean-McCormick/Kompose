"""Lecteur non-IA, strictement fondé sur des identifiants de questions."""
from .validation import publication_ready, ReferenceError

def read_answer(kristals, kristal_id, topic_id, question_id, *, access_granted=False, demo=False):
    """Retourne une réponse préécrite, jamais générée.

    `access_granted` doit découler d'un contrôle serveur en production;
    ce prototype n'émet ni ne vérifie un véritable jeton d'accès.
    """
    if not access_granted:
        raise PermissionError('Accès à ce Kristal non autorisé')
    k = next((k for k in kristals if k.get('id')==kristal_id), None)
    if k is None:
        raise ReferenceError('Kristal inconnu')
    if not publication_ready(k) and not (demo and k.get('status')=='demo'):
        raise PermissionError('Contenu non publié ou non vérifié')
    t=next((t for t in k.get('topics',[]) if t.get('id')==topic_id),None)
    if t is None:
        raise ReferenceError('Thème inconnu : choisir un thème disponible')
    q=next((q for q in t.get('questions',[]) if q.get('id')==question_id),None)
    if q is None:
        raise ReferenceError('Question inconnue : choisir une question disponible')
    source_ids={s.get('id') for s in k.get('sources',[])}
    if not q.get('source_refs') or not set(q['source_refs']).issubset(source_ids):
        raise ReferenceError('Réponse non traçable')
    return {'kristal_id':kristal_id,'version':k['version'],'question_id':q['id'],
            'question':q['label'],'answer':q['answer'],
            'source_refs':list(q['source_refs']),'limitations':q['limitations'],
            'demo':k.get('status')=='demo'}
