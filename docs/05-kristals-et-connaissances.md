# 05 — Kristals, gardiens, acquisition et transmission

## Définition

Un **Kristal** est une unité de savoir documentaire *versionnée* et *située*. Il contient un sujet, une perspective attribuée à des documents/auteurs précisément identifiés, des sources consultables, des questions prédéfinies, des réponses rédigées et des limites explicites. Il n'est ni un personnage, ni une IA, ni une vérité sans contexte.

Un **gardien** est un élève temporairement responsable de guider l'accès ou la transmission : c'est un rôle de jeu et une responsabilité pédagogique, pas une propriété intellectuelle ni un privilège permanent. Le système conserve l'accès au contenu même en cas d'absence du gardien.

## Modes d'acquisition (configurables par capsule)

| Mode | Déclencheur | Mécanique | Risque / atténuation |
|---|---|---|---|
| `confie` | succès à une épreuve adaptée, rotation ou décision enseignant | octroi de garde | ne pas réserver systématiquement les savoirs valorisés aux « meilleurs » |
| `decouvert` | enquête, énigme, indice de carte | ouverture d'un accès | alternatives accessibles |
| `transmis` | rencontre et demande au gardien | partage d'un jeton d'accès à durée limitée | éviter la dépendance sociale ou l'exclusion |
| `reconstitue` | combinaison de plusieurs preuves | nouvel accès après vérification de conditions | ne pas confondre consensus entre élèves et preuve historique |

## Protocole hybride (mode recommandé)

1. Un événement de mission rend un Kristal **recherchable** et indique un indice public.
2. Le gardien reçoit une mission personnelle de médiation (sans données privées des autres élèves).
3. Le demandeur entre en contact avec le gardien selon les règles de la classe. Dans KOMPOSE, il peut soumettre une **demande d'accès** plutôt qu'un chat libre.
4. Le gardien valide une interaction, ou l'enseignant peut l'attester; le système émet un `AccessGrant` court, associé à la session, au demandeur et au Kristal.
5. Le demandeur ouvre le lecteur de Kristal. La réponse affichée vient du contenu validé, pas de la parole ni d'une improvisation forcée du gardien.
6. Un événement de consultation peut déclencher un prompt de mission ou débloquer une comparaison entre sources.

**Plan de secours :** expiration/réassignation de garde, accès enseignant, temps maximum avant déblocage alternatif, adaptation pour enfant isolé ou absent. L'acquisition ne doit pas permettre au gardien de retenir le savoir indéfiniment ni de demander une contrepartie personnelle.

## Perspectives historiques et Kristals croisés

Une capsule peut confronter des archives produites par des colons et des sources documentant l'expérience d'une nation autochtone **nommée**. Ce n'est pas « deux côtés égaux » par principe. Chaque entrée indique : période, territoire, auteur/communauté, type de source, statut de traduction, datation, biais probables, connaissances absentes et droit de diffusion.

Une comparaison peut conduire à :
- distinguer faits documentés et interprétations;
- constater que certains documents sont des sources de pouvoir, d'autres des témoignages;
- comprendre pourquoi des archives de colons peuvent sous-représenter les voix autochtones;
- identifier ce qui ne peut pas être conclu.

**Interdit éditorial :** inventer un témoignage à la première personne d'une nation, publier un savoir restreint, présenter une culture comme homogène, ou utiliser un « document fictif » comme archive vérifiée. Des partenaires et responsables autochtones doivent pouvoir fixer les permissions et restrictions pertinentes aux contenus les concernant.

## Versionnage & publication

`Kristal` : `id` stable, `version` immuable, `status`, `perspective`, `source_refs`, `editorial_review`, `questions`. Tout changement des réponses crée une nouvelle version; les séances existantes demeurent épinglées à leur version approuvée. Il faut un workflow explicite : brouillon → revue → publié → retiré. Le démonstrateur n'a que des données `demo`.

## Lecture minimale

La lecture ne déclenche pas une génération. Le triplet `(kristal_id, topic_id, question_id)` identifie exactement une réponse; réponse inconnue → refus neutre et liste de questions disponibles. Les détails sont dans [06](06-moteur-regles-sans-ia.md).
