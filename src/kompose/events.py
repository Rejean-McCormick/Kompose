"""Sélection de messages prédéfinis. Pas de texte généré."""

def select_prompts(prompt_definitions, event_name, audience, event_id, recipient_id, delivered=None):
    """Renvoie (messages, nouvel_ensemble_de_clés), sans effet réseau.

    En production, la déduplication doit être transactionnelle et durable.
    """
    if not event_id or not recipient_id:
        raise ValueError('Identifiants requis pour idempotence')
    seen=set(delivered or set())
    out=[]
    for p in prompt_definitions:
        if p.get('on_event') != event_name or p.get('audience') != audience:
            continue
        # Le prototype n'exécute pas de conditions `requires` dynamiques.
        if p.get('requires'):
            continue
        key=(event_id,p['id'],recipient_id)
        if key in seen:
            continue
        seen.add(key)
        out.append({'prompt_id':p['id'],'recipient_id':recipient_id,
                    'body':p['body'],'action':p['action']})
    return out,seen
