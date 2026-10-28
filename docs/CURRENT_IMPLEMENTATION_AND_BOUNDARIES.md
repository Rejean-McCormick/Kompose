# Current Implementation and Operational Boundaries

**Checked against the supplied KOMPOSE `0.2.0` source snapshot on 2026-10-27.**

This is an implementation inventory, not a new release, a production certification, or proof of any external repository's current behavior. For machine-readable contracts use `contracts/`; for decisions use ADRs. Where design documents describe orchestration, read them as **proposed responsibilities or local simulations**, not as a live Tandem task engine.

## Implemented and exercised locally

| Capability | Source files | Scope |
|---|---|---|
| Fictional capsule validation | `src/kompose/validation.py`, `tests/test_reference.py` | Cross-reference consistency and publication safeguards; no verified real educational source |
| Session-state examples | `src/kompose/lifecycle.py`, `src/kompose/entry.py` | Pure state transitions and entry-rule checks; no deployed identity service or database |
| Mission phases/dependencies, guardian-transfer proposals | `src/kompose/coordination.py`, `tests/test_orchestration.py` | Pure functions and teacher-approval assumptions; **not real Orgo operations** |
| Deterministic prompts and Kristal lookup | `src/kompose/events.py`, `src/kompose/reader.py` | Fictional, preapproved demo responses; no live authorized content registry |
| Kontexte B6 planning preview | `src/kompose/kontexte_preview.py`, `src/kompose/mission_replay.py` | Synthetic plan, role projection, fallback proposal, mock-receipt replay; **zero Orgo operations** |
| Ekole P1 preview verification | `src/kompose/tandem_handoff.py`, `tests/test_tandem_ekole_handoff.py` | Strict local JSON structure/field gate, not permission or release verification |
| CLI and examples | `src/kompose/cli.py`, `examples/` | Commands for demos and validation, no hosted API |
| Proposed API / schemas | `contracts/openapi.yaml`, `contracts/schemas/` | Contract definitions, not a deployed service |

## Authority and data ownership

- **Orgo owns operational Tandem Case/Task/Signal workflows**, real task transitions, dispatch, authorization decisions, and reconciliation. `lifecycle.py` does not compete with Orgo; its simulated state names are **not** Orgo state or evidence.
- **Kontexte owns scenario sources.** KOMPOSE may compile explicitly synthetic definitions into a preview; it does not alter source curriculum references or replace human pedagogical review.
- **Ekole owns authorized teacher/learning projections.** The local preview gate only verifies the exact supported synthetic shape; neither grades nor competencies are inferred from a `done` task.
- **Orgo_Worlds / authoritative platform owns World and WorldRelease.** UUID parsing in the preview verifier does not establish scope membership, release existence, or signature validity.
- **KOR may be an optional UI client**; KOMPOSE is independent of KOR (ADR 0006), while Orgo operational ownership is an additional and separate constraint (ADR 0008).

## Explicit non-guarantees

- No real school users, child records, SSO, teacher sessions, deployment, HTTP integration, or live Task creation.
- No remote fragment disclosure, durable transaction, message outbox, signed approval, or actual WorldRelease admission.
- B6 receipts with `source: orgo_mock_fixture` are **fictional fixtures**; their `teacher_authorized` and `human_reviewed` flags are assertions, **not authentication**.
- Ekole P1 preview results include `runtime_admitted: false`, `permissions_verified: false`, and `world_release_verified: false` even for a valid synthetic fixture.
- No full constraint solver or psychometrically validated diagnostic, accessibility validation, or classroom-ready audit.

## How to verify locally

From the repository root (Linux/macOS shell):

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m kompose.cli validate examples/capsule-rivieres
PYTHONPATH=src python3 -m kompose.cli preview-kontexte examples/kontexte-boulangerie/data/missions/boulangerie.json examples/kontexte-boulangerie/data/roles
PYTHONPATH=src python3 -m kompose.cli verify-ekole-preview examples/integrations/ekole-fete-sorciere.synthetic.json
```

On Windows PowerShell use `$env:PYTHONPATH='src'` then `py -m ...`.

The wiki is a **separate optional checkout** at `../Kompose.wiki/`; without it, wiki tests are skipped. Do not describe skipped checks as passed.

## Primary references

- [ADR 0008: Orgo operational authority](adr/0008-tandem-orgo-operational-authority.md)
- [Tandem P1 alignment and privacy gate](TANDEM_P1_ORGO_EKOLE_ALIGNMENT.md)
- [Kontexte B6 proposal and dry-run boundaries](b6/ARCHITECTURE.md)
- [ADR 0006: independence from KOR](adr/0006-kompose-application-autonome.md)

Changes to operational authority, student data, or contract semantics require separate review and new tests; documentation updates do not authorize a runtime integration.
