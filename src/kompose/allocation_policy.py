"""Règles d'entrée : ceci n'est PAS un solveur d'attribution sous contraintes."""
import math
import hashlib

def first_choice_quota(n, fraction=1/3):
    if not isinstance(n, int) or n < 0:
        raise ValueError('n doit être entier et positif ou nul')
    if not 0 < fraction <= 1:
        raise ValueError('fraction invalide')
    return math.ceil(n * fraction - 1e-12)

def order_for_choice(scores, *, comparable, seed):
    """Ordre privé et reproductible, seulement si comparabilité attestée.

    La validité psychométrique et les aménagements ne sont PAS évalués ici.
    """
    if comparable is not True:
        raise ValueError('Classement interdit sans résultats comparables; utiliser attribution_guidee')
    if not seed or len(set(scores)) != len(scores):
        raise ValueError('Seed requis et participants uniques attendus')
    for pid,score in scores.items():
        if not isinstance(pid,str) or not pid or not isinstance(score,(float,int)) or isinstance(score,bool) or not math.isfinite(score):
            raise ValueError('Identifiant ou score invalide')
    def tie(pid):
        return hashlib.sha256((str(seed)+':'+pid).encode()).hexdigest()
    return sorted(scores,key=lambda pid:(-scores[pid],tie(pid)))
