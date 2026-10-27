"""B6 isolated tests: no Orgo server, no pupil data and no network."""
from __future__ import annotations
import copy
import json
import tempfile
import unittest
from pathlib import Path
from subprocess import run
import sys

from kompose.kontexte_preview import (
    ScenarioPreviewError,compile_preview,role_projection,
    ready_preview_steps,propose_absence_fallback,
)
from kompose.mission_replay import replay_receipts

ROOT=Path(__file__).resolve().parents[1]
EX=ROOT/'examples'/'kontexte-boulangerie'


def load(path):return json.loads(path.read_text(encoding='utf-8'))

class PreviewBoulangerie(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mission=load(EX/'data'/'missions'/'boulangerie.json')
        cls.roles=[load(x) for x in sorted((EX/'data'/'roles').glob('*.json'))]
        cls.receipts=load(EX/'mock-orgo-receipts.json')['receipts']
        cls.plan=compile_preview(cls.mission,cls.roles,target_course_id='qc-pri-ma-008')

    def test_source_is_unchanged_and_plan_is_non_executable(self):
        self.assertEqual(self.mission['format'],'kontexte.mission/1')
        self.assertEqual(self.plan['scenario']['source_status'],'scenario_skeleton_requires_pedagogical_review')
        self.assertEqual(self.plan['format'],'kompose.kontexte-preview/1')
        self.assertTrue(self.plan['preview_only'])
        self.assertEqual(self.plan['canonical_runtime'],'orgo')
        self.assertFalse(self.plan['dispatch_allowed'])
        self.assertEqual(self.plan['handoff']['mode'],'review_only')

    def test_no_silent_curriculum_remapping(self):
        self.assertEqual(self.plan['curriculum']['source_ids'],['qc-pri-ma-006'])
        self.assertEqual(self.plan['curriculum']['target_course_id'],'qc-pri-ma-008')
        self.assertIs(self.plan['curriculum']['target_mapped'],False)
        self.assertIn('Écart de référentiel',' '.join(self.plan['warnings']))
        self.assertIs(self.plan['curriculum']['mastery_evaluated'],False)

    def test_deterministic_source_hash_and_no_mutation(self):
        first=copy.deepcopy(self.mission)
        result=compile_preview(first,copy.deepcopy(self.roles),target_course_id='qc-pri-ma-008')
        self.assertEqual(result,self.plan)
        self.assertEqual(first,self.mission)
        changed=copy.deepcopy(self.mission)
        changed['steps'][0]['instruction']['fr-CA']+=' (test)'
        again=compile_preview(changed,self.roles,target_course_id='qc-pri-ma-008')
        self.assertNotEqual(self.plan['scenario']['sha256'],again['scenario']['sha256'])

    def test_role_projection_contains_only_own_steps_and_no_clue(self):
        for rid in ('boulanger','fermier','comptable'):
            view=role_projection(self.plan,rid)
            self.assertEqual(len(view['steps']),1)
            self.assertEqual(view['role_id'],rid)
            txt=json.dumps(view,ensure_ascii=False)
            for forbidden in ('indice-un','indice-deux','Le premier groupe détient','Le deuxième groupe détient', 'teacher_approval'):
                self.assertNotIn(forbidden,txt)
            self.assertTrue(view['not_authorization'])
        with self.assertRaises(ScenarioPreviewError):role_projection(self.plan,'eleve-inconnu')

    def test_steps_locked_by_dependencies_and_join(self):
        self.assertEqual(ready_preview_steps(self.plan,set(),set()),['phase-1'])
        self.assertEqual(ready_preview_steps(self.plan,{'phase-1'},set()),['phase-2'])
        self.assertEqual(ready_preview_steps(self.plan,{'phase-1','phase-2'},set()),[])
        self.assertEqual(ready_preview_steps(self.plan,{'phase-1','phase-2'},{'indice-un'}),[])
        self.assertEqual(ready_preview_steps(self.plan,{'phase-1','phase-2'},{'indice-un','indice-deux'}),['phase-3'])

    def test_full_mock_replay_and_duplicate_idempotence(self):
        result=replay_receipts(self.plan,self.receipts)
        self.assertEqual(result['format'],'kompose.orgo-mock-replay/1')
        self.assertEqual(result['completed_steps'],['phase-1','phase-2','phase-3'])
        self.assertEqual(result['duplicate_count'],1)
        self.assertEqual(result['accepted_event_count'],7)
        self.assertEqual(result['orgo_operations_performed'],0)
        self.assertIsNone(result['evidence']['school_competencies_mastered'])
        self.assertFalse(result['evidence']['validated_by_teacher_in_real_system'])
        self.assertEqual(result['session_state'],'preview_open')

    def test_replay_rejects_out_of_order_and_skipped_steps(self):
        evt={'event_id':'x','sequence':1,'source':'orgo_mock_fixture','synthetic':True,
             'kind':'step_completed','step_id':'phase-3','role_id':'comptable','human_reviewed':True}
        with self.assertRaises(ScenarioPreviewError):replay_receipts(self.plan,[evt])
        evt['step_id']='phase-1';evt['role_id']='boulanger';evt['sequence']=2
        with self.assertRaises(ScenarioPreviewError):replay_receipts(self.plan,[evt])

    def test_replay_rejects_missing_review_and_wrong_role(self):
        evt={'event_id':'x','sequence':1,'source':'orgo_mock_fixture','synthetic':True,
             'kind':'step_completed','step_id':'phase-1','role_id':'boulanger','human_reviewed':False}
        with self.assertRaises(ScenarioPreviewError):replay_receipts(self.plan,[evt])
        evt['human_reviewed']=True;evt['role_id']='comptable'
        with self.assertRaises(ScenarioPreviewError):replay_receipts(self.plan,[evt])

    def test_replay_rejects_fragment_to_wrong_recipient_or_without_review(self):
        evt={'event_id':'x','sequence':1,'source':'orgo_mock_fixture','synthetic':True,
             'kind':'fragment_authorized','fragment_id':'indice-un',
             'role_id':'fermier','teacher_authorized':True}
        with self.assertRaises(ScenarioPreviewError):replay_receipts(self.plan,[evt])
        evt['role_id']='boulanger';evt['teacher_authorized']=False
        with self.assertRaises(ScenarioPreviewError):replay_receipts(self.plan,[evt])

    def test_replay_rejects_real_events_and_pii(self):
        item=copy.deepcopy(self.receipts[0]);item['source']='orgo';
        with self.assertRaises(ScenarioPreviewError):replay_receipts(self.plan,[item])
        item=copy.deepcopy(self.receipts[0]);item['student_name']='Enfant';
        with self.assertRaises(ScenarioPreviewError):replay_receipts(self.plan,[item])
        item=copy.deepcopy(self.receipts[0]);item['synthetic']=False
        with self.assertRaises(ScenarioPreviewError):replay_receipts(self.plan,[item])

    def test_duplicate_conflicting_receipt_rejected(self):
        a=copy.deepcopy(self.receipts[0]);b=copy.deepcopy(a);b['role_id']='fermier'
        with self.assertRaises(ScenarioPreviewError):replay_receipts(self.plan,[a,b])

    def test_paused_prevents_completion_and_duplicate_resume(self):
        a=copy.deepcopy(self.receipts[0]);b=copy.deepcopy(self.receipts[1]);
        third=copy.deepcopy(self.receipts[3]);third['sequence']=3
        with self.assertRaises(ScenarioPreviewError):replay_receipts(self.plan,[a,b,third])
        with self.assertRaises(ScenarioPreviewError):replay_receipts(self.plan,[a,copy.deepcopy(self.receipts[2])])

    def test_absence_proposal_is_not_a_permission(self):
        result=propose_absence_fallback(self.plan,'fermier')
        self.assertEqual(result['affected_steps'],['phase-2'])
        self.assertEqual(result['affected_fragment_ids'],['indice-deux'])
        self.assertEqual(result['granted_fragments'],[])
        self.assertEqual(result['automatically_assigned_roles'],[])
        self.assertEqual(result['orgo_mutations'],0)
        self.assertEqual(result['status'],'teacher_and_orgo_approval_required')
        with self.assertRaises(ScenarioPreviewError):propose_absence_fallback(self.plan,'fantome')

    def test_validation_unknown_role_and_cycles(self):
        bad=copy.deepcopy(self.mission);bad['steps'][0]['role']='autre'
        with self.assertRaises(ScenarioPreviewError):compile_preview(bad,self.roles)
        bad=copy.deepcopy(self.mission);bad['steps'][0]['depends_on']=['phase-3']
        with self.assertRaises(ScenarioPreviewError):compile_preview(bad,self.roles)
        bad=copy.deepcopy(self.mission);bad['steps'][0]['depends_on']=['fantome']
        with self.assertRaises(ScenarioPreviewError):compile_preview(bad,self.roles)

    def test_validation_non_synthetic_and_secret_release(self):
        bad=copy.deepcopy(self.mission);bad['synthetic']=False
        with self.assertRaises(ScenarioPreviewError):compile_preview(bad,self.roles)
        bad=copy.deepcopy(self.mission);bad['fragments'][0]['release']='immediate'
        with self.assertRaises(ScenarioPreviewError):compile_preview(bad,self.roles)
        bad=copy.deepcopy(self.mission);bad['joins'][0]['fragment_ids']=['missing']
        with self.assertRaises(ScenarioPreviewError):compile_preview(bad,self.roles)

    def test_optional_json_schemas_validate_real_outputs(self):
        try:import jsonschema
        except ImportError:self.skipTest('jsonschema facultatif non installé')
        schemas=ROOT/'contracts'/'schemas'
        replay=replay_receipts(self.plan,self.receipts)
        jsonschema.Draft202012Validator(load(schemas/'kontexte-preview.schema.json')).validate(self.plan)
        jsonschema.Draft202012Validator(load(schemas/'orgo-mock-replay.schema.json')).validate(replay)

    def test_cli_role_view_and_absence_fallback(self):
        role=run([sys.executable,'-m','kompose.cli','preview-kontexte',
                  str(EX/'data'/'missions'/'boulangerie.json'),str(EX/'data'/'roles'),
                  '--role','boulanger'],stdout=-1,stderr=-1,text=True)
        self.assertEqual(role.returncode,0,role.stderr)
        self.assertEqual(len(json.loads(role.stdout)['steps']),1)
        proposal=run([sys.executable,'-m','kompose.cli','preview-kontexte',
                      str(EX/'data'/'missions'/'boulangerie.json'),str(EX/'data'/'roles'),
                      '--absent-role','fermier'],stdout=-1,stderr=-1,text=True)
        self.assertEqual(proposal.returncode,0,proposal.stderr)
        self.assertEqual(json.loads(proposal.stdout)['fallback']['orgo_mutations'],0)

    def test_kontexte_orgo_bootstrap_is_review_only(self):
        fixture=load(EX/'orgo-bootstrap-review.example.json')
        self.assertEqual(fixture['schema_version'],'orgo.scenario.v1')
        self.assertEqual([x['op'] for x in fixture['operations']],['create_case','create_task'])
        self.assertTrue(fixture['scenario']['synthetic'])
        self.assertIn('réviser la mission',fixture['operations'][1]['input']['title'].lower())
        self.assertNotIn('Le premier groupe détient',json.dumps(fixture,ensure_ascii=False))
        self.assertNotIn('Le deuxième groupe détient',json.dumps(fixture,ensure_ascii=False))
        self.assertFalse(fixture['operations'][1]['input']['metadata']['private_fragments_embedded'])

    def test_cli_exports_preview_and_mock_simulation(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'preview.json'
            result=run([sys.executable,'-m','kompose.cli','preview-kontexte',
                        str(EX/'data'/'missions'/'boulangerie.json'),str(EX/'data'/'roles'),
                        '--replay',str(EX/'mock-orgo-receipts.json'),'--out',str(p)],
                       stdout=-1,stderr=-1,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            doc=load(p)
            self.assertEqual(doc['replay']['completed_steps'],['phase-1','phase-2','phase-3'])
            self.assertNotIn('Le premier groupe détient',p.read_text(encoding='utf-8'))

if __name__=='__main__':unittest.main()
