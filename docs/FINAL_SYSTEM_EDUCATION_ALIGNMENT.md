# Final-system education boundary — Kompose

**Scope:** `FC-10`; preparation, local simulation and verification. **Authority:** Orgo is the sole owner of actual operational Cases/Tasks.

## Implemented review-only checks

`src/kompose/tandem_handoff.py` retains `verify_teacher_preview`, the schema-level gate for `ekole.tandem-teacher-preview/1.0`. It additionally supplies **`verify_initial_design_preview(preview, mission)`**, an exact Kontexte source-to-preview conformance check:

1. Confirm the preview is a bounded, closed, synthetic Ekole object.
2. Confirm the original `kontexte.mission/1` is explicitly synthetic, its roles are unique and all step dependencies refer only to earlier steps.
3. Confirm task order, IDs, roles, initial states and absence of released fragment references agree with the original source.
4. Return only a constrained `kompose.initial-design-check/1.0` proof with `dispatch_allowed=false` and `teacher_authorized=false`.

The new proof is **not** an IK, Orgo admission or education grading contract; it only ensures honest initial preview fidelity. Akor calls this owner validator before creating P2/P3 requests, and duplicate progress or fabricated private fragments are rejected.

## Tests and follow-ups

Run `PYTHONPATH=src python -m unittest discover -s tests -v`. Separate cross-owner tests use the actual Kontexte, Ékole and Akor modules in the branch harness. The open teacher/learner, Orgo effect, Moodle and signed release interfaces remain **TBD** and require bilateral owner approval with negative fixtures before any live data or authorization. Existing local demos remain practice-only.
