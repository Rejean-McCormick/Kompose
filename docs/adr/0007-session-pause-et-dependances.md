# ADR 0007 — Pause/reprise et graphe de missions

**Décision : acceptée le 2026-10-12.**

Une session possède un état versionné, un état `suspendue` temporaire et un ancien état de reprise. La progression collective utilise un graphe acyclique de `depends_on` et des transitions séquentielles de phases. Les exceptions pédagogiques sont possibles avec trace enseignante, sans dérogation aux règles de sécurité et de droits.

## Conséquences

- Transactions optimistes obligatoires en production.
- Définitions de missions validées contre références manquantes et cycles.
- Cas de secours pour gardien absent; transfert proposé, non automatique.
