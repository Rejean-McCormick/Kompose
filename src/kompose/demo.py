"""Reproducible fake end-to-end narrative — no real students or live auth."""
from pathlib import Path
from datetime import datetime, timedelta, timezone
from .validation import load_json
from .entry import may_join
from .lifecycle import apply_session_command
from .coordination import ready_missions, advance_phase, guardian_fallback
from .allocation_policy import first_choice_quota
from .events import select_prompts
from .reader import read_answer


def run_demo(capsule_directory: Path):
    base = Path(capsule_directory)
    s = load_json(base / 'session.example.json')
    missions = load_json(base / 'missions.json')['missions']
    prompts = load_json(base / 'prompts.json')['prompts']
    kristals = load_json(base / 'kristals.json')['kristals']
    now = datetime(2026, 10, 12, 12, tzinfo=timezone.utc)
    actions = [
        ('prepare', {'content_ready': True}),  # demo-only editorial bypass in simulation
        ('open', {}),
        ('close_enrollment', {}),
        ('close_diagnostic', {'diagnostics_reviewed': True}),
        ('preview_assignment', {'plan_checked': True}),
    ]
    events = []
    valid_entry = False
    for action, guards in actions:
        s, event = apply_session_command(s, action, actor_role='teacher',
                                         expected_version=s.get('version', 0), guards=guards)
        events.append(event['name'])
        if action == 'open':
            valid_entry = may_join(submitted_code='DEMO-2026', code_on_server='DEMO-2026',
                                   now=now, expires_at=now + timedelta(minutes=10),
                                   authenticated=True, enrolled=True, seats_available=True,
                                   session_state=s['state'])
    s['teacher_approval'] = True  # demo fixture only; approval in real system is audited
    s, event = apply_session_command(s, 'publish_assignment', actor_role='teacher',
                expected_version=s['version'], guards={'hard_constraints_satisfied': True,
                'roles_complete': True, 'accessibility_checked': True})
    events.append(event['name'])
    messages, _ = select_prompts(prompts, 'session.roles_publies', 'participant',
                                 'event-demo-roles', 'P-001')
    ready = ready_missions(missions, set())
    phase = advance_phase(current_phase='exploration', next_phase='enquete',
                          ordered_phases=['exploration', 'enquete', 'synthese'],
                          pending_blockers=[], teacher_override=False)
    s, event = apply_session_command(s, 'pause', actor_role='teacher',
                                     expected_version=s['version'])
    events.append(event['name'])
    s, event = apply_session_command(s, 'resume', actor_role='teacher',
                                     expected_version=s['version'])
    events.append(event['name'])
    answer = read_answer(kristals, 'KR-ARCHIVES', 'TERRITOIRE', 'OCCUPANTS',
                         access_granted=True, demo=True)
    fallback = guardian_fallback('KR-ARCHIVES', 'P-001', 'P-002', {'P-002', 'P-003'})
    s, event = apply_session_command(s, 'finish', actor_role='teacher',
                                     expected_version=s['version'])
    events.append(event['name'])
    return {
        'notice': 'SIMULATION FICTIVE : ni authentification, ni approbation éditoriale, ni allocation réelle',
        'entry_allowed_in_demo': valid_entry,
        'first_choice_quota_for_20': first_choice_quota(20),
        'final_state': s['state'],
        'session_version': s['version'],
        'event_names': events,
        'messages_sent': [x['prompt_id'] for x in messages],
        'initial_ready_missions': ready,
        'phase_change': phase['name'],
        'guardian_fallback_proposal': fallback['name'],
        'verified_historical_answer': False,
        'demo_documentary_answer_id': answer['question_id'],
    }
