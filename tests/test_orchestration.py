"""No sensitive learner fixtures. Deterministic orchestration unit tests."""
import copy
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
from kompose.validation import validate_directory, load_json
from kompose.lifecycle import apply_session_command, SessionTransitionError
from kompose.entry import may_join, EntryError
from kompose.coordination import (
    ready_missions, validate_dependencies, CoordinationError,
    advance_phase, guardian_fallback,
)
from kompose.demo import run_demo

EX = Path(__file__).resolve().parents[1] / 'examples' / 'capsule-rivieres'

class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.session = load_json(EX / 'session.example.json')

    def go(self, action, flags=None):
        self.session, event = apply_session_command(self.session, action,
            actor_role='teacher', expected_version=self.session.get('version', 0),
            guards=flags)
        return event

    def test_requires_teacher(self):
        with self.assertRaises(PermissionError):
            apply_session_command(self.session, 'prepare', actor_role='student',
                                  expected_version=0, guards={'content_ready': True})

    def test_prepare_requires_review_and_does_not_mutate(self):
        previous = copy.deepcopy(self.session)
        with self.assertRaises(SessionTransitionError): self.go('prepare')
        self.assertEqual(self.session, previous)
        self.assertEqual(self.go('prepare', {'content_ready': True})['name'], 'session.prete')

    def test_stale_version_is_rejected(self):
        self.go('prepare', {'content_ready': True})
        with self.assertRaises(SessionTransitionError):
            apply_session_command(self.session, 'open', actor_role='teacher', expected_version=0)

    def test_cannot_publish_without_approval(self):
        self.session['state'] = 'validation'
        with self.assertRaises(SessionTransitionError):
            self.go('publish_assignment', {'hard_constraints_satisfied': True,
                   'roles_complete': True, 'accessibility_checked': True})
        self.session['teacher_approval'] = True
        with self.assertRaises(SessionTransitionError):
            self.go('publish_assignment', {'hard_constraints_satisfied': True,
                   'roles_complete': True})
        event = self.go('publish_assignment', {'hard_constraints_satisfied': True,
                   'roles_complete': True, 'accessibility_checked': True})
        self.assertEqual(event['name'], 'session.roles_publies')
        self.assertEqual(self.session['state'], 'aventure')

    def test_pause_resume_then_finish(self):
        self.session['state'] = 'aventure'
        self.go('pause')
        self.assertEqual(self.session['state'], 'suspendue')
        self.assertEqual(self.session['paused_from'], 'aventure')
        with self.assertRaises(SessionTransitionError): self.go('finish')
        self.go('resume')
        self.assertNotIn('paused_from', self.session)
        self.go('finish')
        with self.assertRaises(SessionTransitionError): self.go('resume')

    def test_cancel_from_any_active_state(self):
        self.go('cancel')
        with self.assertRaises(SessionTransitionError): self.go('open')

class EntryTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2026, 10, 12, 12, tzinfo=timezone.utc)
        self.kw = dict(submitted_code='KOMPOSE-26', code_on_server='KOMPOSE-26',
                       expires_at=self.now + timedelta(minutes=5), now=self.now,
                       authenticated=True, enrolled=True, seats_available=True, session_state='inscriptions')

    def test_join_requires_code_and_external_authentication(self):
        self.assertTrue(may_join(**self.kw))
        with self.assertRaises(EntryError): may_join(**dict(self.kw, submitted_code='BAD'))
        with self.assertRaises(PermissionError): may_join(**dict(self.kw, authenticated=False))
        with self.assertRaises(PermissionError): may_join(**dict(self.kw, enrolled=False))
        with self.assertRaises(EntryError): may_join(**dict(self.kw, seats_available=False))

    def test_closed_session_rejected(self):
        with self.assertRaises(EntryError):
            may_join(**dict(self.kw, session_state='diagnostic'))

    def test_expiry_timezone_required(self):
        with self.assertRaises(EntryError): may_join(**dict(self.kw, now=self.kw['expires_at']))
        with self.assertRaises(EntryError): may_join(**dict(self.kw, now=datetime(2026,10,12)))

class CoordinationTests(unittest.TestCase):
    def setUp(self):
        self.missions = load_json(EX/'missions.json')['missions']

    def test_dependency_graph_and_unlocks(self):
        self.assertEqual(ready_missions(self.missions, []), ['MIS-RECHERCHE', 'MIS-DEMANDE'])
        self.assertEqual(ready_missions(self.missions, ['MIS-RECHERCHE','MIS-DEMANDE']), ['MIS-COMPARAISON'])
        self.assertEqual(ready_missions(self.missions, ['MIS-RECHERCHE','MIS-DEMANDE','MIS-COMPARAISON']), ['MIS-SYNTHESE'])
        self.assertEqual(validate_directory(EX), [])

    def test_cycle_and_unknown_dependency_rejected(self):
        copy_missions = copy.deepcopy(self.missions)
        copy_missions[0]['depends_on'] = ['MIS-SYNTHESE']
        with self.assertRaises(CoordinationError): validate_dependencies(copy_missions)
        copy_missions[0]['depends_on'] = ['MISSING']
        with self.assertRaises(CoordinationError): validate_dependencies(copy_missions)

    def test_advancing_phases(self):
        args = dict(current_phase='exploration',next_phase='enquete',
                    ordered_phases=['exploration','enquete','synthese'])
        with self.assertRaises(CoordinationError): advance_phase(**args, pending_blockers=['MIS-RECHERCHE'])
        event = advance_phase(**args, pending_blockers=['MIS-RECHERCHE'], teacher_override=True)
        self.assertEqual(event['payload']['pending_count'], 1)
        with self.assertRaises(CoordinationError):
            advance_phase(current_phase='exploration',next_phase='synthese',
                          ordered_phases=['exploration','enquete','synthese'], pending_blockers=[])

    def test_guardian_transfer_requires_available_new_guardian(self):
        with self.assertRaises(CoordinationError): guardian_fallback('K1','P1','P3',['P2'])
        event=guardian_fallback('K1','P1','P2',['P2'])
        self.assertTrue(event['payload']['requires_teacher_approval'])

    def test_demo_entire_flow(self):
        result=run_demo(EX)
        self.assertEqual(result['final_state'], 'terminee')
        self.assertEqual(result['first_choice_quota_for_20'],7)
        self.assertEqual(len(result['event_names']),9)
        self.assertFalse(result['verified_historical_answer'])

if __name__ == '__main__': unittest.main()
