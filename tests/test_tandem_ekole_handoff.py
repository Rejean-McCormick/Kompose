"""P1 isolated conformance tests, no school accounts or Orgo calls."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from kompose.tandem_handoff import verify_teacher_preview,load_teacher_preview,TandemHandoffError

FIXTURE=ROOT/'examples/integrations/ekole-fete-sorciere.synthetic.json'

class EkolePreviewGateTest(unittest.TestCase):
    def setUp(self):self.value=json.loads(FIXTURE.read_text(encoding='utf8'))
    def test_compatible_contract(self):
        result=verify_teacher_preview(self.value)
        self.assertTrue(result['valid']);self.assertFalse(result['runtime_admitted'])
        self.assertFalse(result['permissions_verified']);self.assertFalse(result['world_release_verified'])
    def test_no_secrets_or_children(self):
        raw=json.dumps(self.value,ensure_ascii=False)
        self.assertNotIn('Une feuille produit',raw)
        self.assertNotIn('55 Klownkoins',raw)
        self.assertTrue(all(set(t)=={'task_ref','role_code','state','fragment_refs'} for t in self.value['tasks']))
    def test_reject_personal_field(self):
        self.value['student_name']='Enfant'
        with self.assertRaises(TandemHandoffError):verify_teacher_preview(self.value)
    def test_reject_embedded_clue(self):
        self.value['tasks'][0]['fragment_text']='secret'
        with self.assertRaises(TandemHandoffError):verify_teacher_preview(self.value)
    def test_reject_false_authority(self):
        self.value['authority']='kompose'
        with self.assertRaises(TandemHandoffError):verify_teacher_preview(self.value)
    def test_reject_real_mode(self):
        self.value['mode']='live'
        with self.assertRaises(TandemHandoffError):verify_teacher_preview(self.value)
    def test_reject_unknown_scope(self):
        for key in ('tenant_id','world_id','world_release_id'):
            p=copy.deepcopy(self.value);p[key]=''
            with self.subTest(key=key),self.assertRaises(TandemHandoffError):verify_teacher_preview(p)
    def test_reject_wrong_release_format(self):
        self.value['world_release_id']='33333333333343338333333333333333'
        with self.assertRaises(TandemHandoffError):verify_teacher_preview(self.value)
    def test_reject_duplicate_tasks(self):
        self.value['tasks'].append(copy.deepcopy(self.value['tasks'][0]))
        with self.assertRaises(TandemHandoffError):verify_teacher_preview(self.value)
    def test_reject_fragment_bodies_as_refs(self):
        self.value['tasks'][0]['fragment_refs']=['Une feuille produit 2 invitations']
        with self.assertRaises(TandemHandoffError):verify_teacher_preview(self.value)
    def test_reject_bad_states(self):
        self.value['tasks'][0]['state']='teacher_authorized'
        with self.assertRaises(TandemHandoffError):verify_teacher_preview(self.value)
    def test_strict_file_contract_agrees_with_memory_verifier(self):
        self.assertEqual(load_teacher_preview(FIXTURE),self.value)

    def test_duplicate_json_top_level_keys_fail_closed(self):
        original=FIXTURE.read_text(encoding='utf-8')
        duplicate=original.replace('"mode": "synthetic",','"mode": "synthetic", "mode": "live",',1)
        with tempfile.TemporaryDirectory() as directory:
            file=Path(directory)/'duplicate.json';file.write_text(duplicate,encoding='utf-8')
            with self.assertRaisesRegex(TandemHandoffError,'dupliquée'):
                load_teacher_preview(file)

    def test_duplicate_json_nested_task_keys_fail_closed(self):
        original=FIXTURE.read_text(encoding='utf-8')
        duplicate=original.replace('"state": "ready",','"state": "ready", "state": "done",',1)
        with tempfile.TemporaryDirectory() as directory:
            file=Path(directory)/'duplicate.json';file.write_text(duplicate,encoding='utf-8')
            with self.assertRaisesRegex(TandemHandoffError,'dupliquée'):
                load_teacher_preview(file)

    def test_oversized_preview_rejected_before_parsing(self):
        with tempfile.TemporaryDirectory() as directory:
            file=Path(directory)/'huge.json';file.write_bytes(b' '*131073)
            with self.assertRaisesRegex(TandemHandoffError,'volumineuse'):
                load_teacher_preview(file)

    def test_invalid_utf8_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            file=Path(directory)/'bad.json';file.write_bytes(b'\xff\xfe{}')
            with self.assertRaises(TandemHandoffError):load_teacher_preview(file)

    def test_symlink_refused_even_when_target_is_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            link=Path(directory)/'link.json'
            try:link.symlink_to(FIXTURE)
            except (OSError,NotImplementedError):self.skipTest('symlinks require privileges on this OS')
            with self.assertRaises(TandemHandoffError):load_teacher_preview(link)

    def test_cli_rejects_duplicate_json_keys(self):
        original=FIXTURE.read_text(encoding='utf-8')
        with tempfile.TemporaryDirectory() as directory:
            file=Path(directory)/'dupe.json'
            file.write_text(original.replace('"mode": "synthetic",','"mode": "synthetic", "mode": "synthetic",',1),encoding='utf-8')
            import os
            result=subprocess.run([sys.executable,'-m','kompose.cli','verify-ekole-preview',str(file)],
                env=dict(os.environ,PYTHONPATH=str(ROOT/'src')),cwd=ROOT,text=True,capture_output=True)
            self.assertNotEqual(result.returncode,0)
            self.assertNotIn('Traceback',result.stderr)

    def test_cli(self):
        import os
        cp=subprocess.run([sys.executable,'-m','kompose.cli','verify-ekole-preview',str(FIXTURE)],
                env=dict(os.environ,PYTHONPATH=str(ROOT/'src')),cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(cp.returncode,0,cp.stderr)
        self.assertFalse(json.loads(cp.stdout)['runtime_admitted'])

if __name__=='__main__':unittest.main()
