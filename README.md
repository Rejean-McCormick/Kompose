# KOMPOSE

**Educational capsule design, validation, and local simulation. Orgo is the sole authority for operational Tandem tasks.**

**Version:** `0.2.0` (reference package) · **Documentation:** English README; design documents also include French · **Status:** executable technical reference, **not a school-ready product**.

KOMPOSE and **KOR are separate applications**. KOR may provide an optional narrative interface; it is not the KOMPOSE engine. **KOMPOSE and Orgo also have distinct responsibilities:** KOMPOSE prepares and checks educational plans and runs local simulations; **Orgo alone owns real Cases, Tasks, operational transitions, dispatch, permissions, and reconciliation** under the adopted [ADR 0008](docs/adr/0008-tandem-orgo-operational-authority.md).

> **Source of truth:** executable behavior is in `src/kompose/` and its tests; proposed API and data contracts are in `contracts/`; architectural decisions and restrictions are in `docs/`. Neither a wiki page nor a successful simulation is evidence of deployed school authorization.

## What is included

- A **pure Python reference model** for joining a fictional capsule, session state changes, pause/resume, mission dependencies, phase coordination, role-selection quota, prompts, and teacher-supervised transfer proposals.
- Versioned **OpenAPI and JSON Schema specifications**; the OpenAPI endpoints are **illustrative, not hosted**.
- A **deterministic, non-generative Kristal reader** using predefined questions and responses. Demo content is fictional and is not verified historical material.
- A sample **Rivers capsule** with role, mission, phase, diagnostic, Kristal, prompt, and event fixtures.
- A **Kontexte B6 planning preview** (`preview-kontexte`), including optional role projection, proposed absence fallback, and replay of fictional Orgo receipts. It does not create real Tasks or deliver secret fragments.
- A strict **Ekole P1 synthetic teacher-preview verifier** (`verify-ekole-preview`), which checks a local JSON file and refuses unexpected or sensitive fields. Its results always indicate that runtime admission, permission checks, and WorldRelease validation are **not established**.
- Unit and contract tests, including security and non-disclosure checks for the synthetic previews.

**Not included:** a web application or teacher console, school SSO, deployed API, transactional store, real Orgo client, verified permissions, operational dispatch, globally optimized role assignment, validated adaptive assessment, certified historical content, or classroom-ready infrastructure.

## Quick start (Python 3.10+)

Run these commands **from the repository root**. The reference CLI has no mandatory third-party runtime dependencies.

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m kompose.cli validate examples/capsule-rivieres
PYTHONPATH=src python3 -m kompose.cli demo-flow examples/capsule-rivieres
PYTHONPATH=src python3 -m kompose.cli quota 20
PYTHONPATH=src python3 -m kompose.cli ready-missions examples/capsule-rivieres/missions.json
PYTHONPATH=src python3 -m kompose.cli read examples/capsule-rivieres/kristals.json KR-ARCHIVES TERRITOIRE OCCUPANTS --demo
PYTHONPATH=src python3 -m kompose.cli trigger examples/capsule-rivieres/prompts.json kristal.acces_accorde --audience demandeur --demo
```

On **Windows PowerShell**, set `$env:PYTHONPATH='src'` once, then use `py -m ...` instead of the `PYTHONPATH=src python3 -m ...` prefix. Alternatively, install locally with `python -m pip install -e '.[dev]'` and use `kompose` as the CLI executable. Optional `dev` requirements provide schema-validation tooling; the core reference functions use the Python standard library.

> **Safety:** `--demo` only permits explicitly fictional local examples. It is not a school login or authorization check. A prompt produced by the simulator is not a dispatched student message.

## Kontexte B6 — plan and mock replay only

The B6 demonstrator transforms a **synthetic** Kontexte mission and role definitions into a **non-executable educational plan**. Example:

```bash
PYTHONPATH=src python3 -m kompose.cli preview-kontexte \
  examples/kontexte-boulangerie/data/missions/boulangerie.json \
  examples/kontexte-boulangerie/data/roles
```

Optional CLI flags: `--role ROLE_ID` for a restricted role projection, `--absent-role ROLE_ID` to propose (not perform) a fallback, `--replay FILE` to process mock Orgo receipts in a teacher-level view, and `--out FILE` to write JSON. `--role` cannot be combined with `--replay` or `--absent-role`.

The bakery fixture has **3 roles, 3 review-required steps, and 2 fragment references**. Its source curriculum IDs remain `qc-pri-ma-006`; supplying the optional target-course value `qc-pri-ma-008` **does not remap them or certify alignment**. The plan includes identifiers and decision points, **not secret fragment text or pupil records**. See [B6 architecture](docs/b6/ARCHITECTURE.md) and [the bakery example](examples/kontexte-boulangerie/README.md).

`LANCER_DEMO_B6.bat` is an optional Windows local demonstration. It does not launch an Orgo server.

## Tandem P1 — Ekole teacher preview verification

```bash
PYTHONPATH=src python3 -m kompose.cli verify-ekole-preview \
  examples/integrations/ekole-fete-sorciere.synthetic.json
```

The verifier requires the exact `ekole.tandem-teacher-preview/1.0` format with `mode: synthetic` and `authority: orgo`. It rejects duplicate JSON keys, unknown fields, symlinks, non-UTF-8 input, files larger than **128 KiB**, malformed scope UUIDs, invalid task identifiers, and unauthorized data-bearing fields. The included fixture represents **11 synthetic tasks**, not Tasks created in Orgo.

A successful result contains `runtime_admitted: false`, `permissions_verified: false`, and `world_release_verified: false`. An `orgo` authority declaration is a **label in the fixture**, not proof of an authenticated Orgo decision. No network, teacher session, child identity, WorldRelease lookup, or fragment delivery is performed. See [Tandem alignment](docs/TANDEM_P1_ORGO_EKOLE_ALIGNMENT.md).

## Responsibility boundaries

| Area | Actual owner / responsibility | What this repository provides |
|---|---|---|
| Kontexte missions, roles, steps, source references | **Kontexte** | Validation and non-executable B6 projection of explicitly synthetic definitions |
| Real Case / Task / Signal / workflow, transitions, idempotent dispatch | **Orgo** | Local rules, mock receipts, no mutation of Orgo state |
| Tenant, World, WorldRelease | **Orgo_Worlds / authoritative platform** | Structural UUID checks in synthetic preview, **not existence or authorization** |
| Teacher and learning projections | **Ekole / authorized institutional services** | Strict synthetic teacher-preview format checks; no deployed teacher UI |
| School login, child permissions, private assessments | **School services / future adapters** | Design contracts and examples; no identity backend |
| Narrative experience | **KOR or another optional client** | Example adapter manifest; no live integration |
| Kristal content and editorial rights | **Content owner / editorial authority** | Demonstration-only deterministic lookup and publication guards |

The functions in `lifecycle.py` and `coordination.py` are **reference simulations**. They must **not** be used to advance real Tandem missions when Orgo owns the operational workflow. See [ADR 0006](docs/adr/0006-kompose-application-autonome.md) (independence from KOR) and [ADR 0008](docs/adr/0008-tandem-orgo-operational-authority.md) (operational ownership by Orgo).

## Nine functional responsibilities (design scope, not nine deployed services)

| Responsibility | Role in the model | Design document |
|---|---|---|
| Entry Door | Temporary capsule code plus *external* authenticated identity | [15](docs/15-entry-door.md) |
| Diagnostic | Assessment design, accommodation and comparability constraints | [04](docs/04-diagnostic-et-attribution.md) |
| Role casting | Optional first-third choices, suggested assignments, teacher approval | [04](docs/04-diagnostic-et-attribution.md) |
| Coordination | **Local simulation** of state, events, dependencies, and phases | [16](docs/16-orchestration-et-dependances.md) |
| Kristals | Versioned editorial knowledge, permissions model, supervised custody | [05](docs/05-kristals-et-connaissances.md) |
| Interactions | Guided cooperative prompts and exchanges in fictional examples | [14](docs/14-recette-narrative.md) |
| Adaptation | Accessible alternatives, pacing, non-stigmatizing choices | [07](docs/07-interfaces.md) |
| Supervision | Proposed teacher interventions and private constraints | [17](docs/17-supervision-et-continuite.md) |
| Closure | Proposed session closeout and limited retention | [17](docs/17-supervision-et-continuite.md) |

## Non-negotiable safeguards

1. A capsule code **never substitutes for school authentication**.
2. No public ranking, private assessment disclosure, or permanent labelling of children.
3. Safety, accessibility, and authorization override preference optimization.
4. Private collaboration constraints and pupil information are excluded from narrative events and preview exports.
5. A Kristal and its temporary guardian are distinct; source, editorial version, and access policy are tracked separately.
6. Documentary answers are **prewritten, attributable, and non-generative**; unknown questions do not trigger invented facts.
7. Historical perspectives require identifiable sources and appropriate community/editorial review. **Demo history is fictional.**
8. Any real role assignment or sensitive transition requires a properly authenticated, authorized human workflow.
9. Dependencies must not form cycles; a simulated absence fallback is never an automatic real reassignment.
10. Schema validation, fixture flags, and passing unit tests do **not** prove real-world authorization or deployment readiness.

## Documentation, wiki, and contribution

- [Documentation index](docs/INDEX.md) and [current implementation boundary](docs/CURRENT_IMPLEMENTATION_AND_BOUNDARIES.md)
- [Data contracts](contracts/README.md) and [illustrative OpenAPI](contracts/openapi.yaml)
- [Security and fairness](docs/09-protection-et-equite.md), [integration plan](docs/20-plan-d-integration.md)
- [Decisions](docs/adr/), [changelog](CHANGELOG.md), [contributing](CONTRIBUTING.md)

The **English wiki is a separate, optional Git repository**, normally cloned next to this source checkout as `../Kompose.wiki/`. Start with `../Kompose.wiki/Home.md` and its `_Sidebar.md`; its absence causes wiki-specific tests to be **skipped**, not passed. Normative contracts remain in `contracts/` and `docs/`. The collected archive is not evidence that the wiki has been published online.

No redistribution license has been selected; see [LICENSE-TO-DECIDE.md](LICENSE-TO-DECIDE.md). All examples are fictional and must never be presented as approved classroom content.
