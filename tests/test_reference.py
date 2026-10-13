"""Vérifications de la spécification. Aucune donnée réelle d'élève."""
import copy
import unittest
from pathlib import Path
from kompose.validation import validate_directory, load_json, publication_ready, ReferenceError
from kompose.reader import read_answer
from kompose.events import select_prompts
from kompose.allocation_policy import first_choice_quota, order_for_choice

ROOT=Path(__file__).resolve().parents[1]
EX=ROOT/'examples'/'capsule-rivieres'

class ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kristals=load_json(EX/'kristals.json')['kristals']
        cls.prompts=load_json(EX/'prompts.json')['prompts']
        cls.roles=load_json(EX/'roles.json')['roles']

    def test_demo_is_cross_reference_consistent(self):
        self.assertEqual(validate_directory(EX), [])

    def test_20_roles_and_quota_7(self):
        self.assertEqual(len(self.roles),20)
        self.assertEqual(len(set(r['id'] for r in self.roles)),20)
        self.assertEqual(first_choice_quota(20),7)
        self.assertEqual(first_choice_quota(3),1)
        self.assertEqual(first_choice_quota(1),1)
        self.assertEqual(first_choice_quota(0),0)

    def test_fraction_invalid(self):
        for n,fraction in [(-1,1/3),(20,0),(20,2)]:
            with self.assertRaises(ValueError):first_choice_quota(n,fraction)

    def test_reader_refuses_unauthorized_access_even_in_demo(self):
        with self.assertRaises(PermissionError):
            read_answer(self.kristals,'KR-ARCHIVES','TERRITOIRE','OCCUPANTS',demo=True)

    def test_reader_refuses_unpublished_without_demo_flag(self):
        with self.assertRaises(PermissionError):
            read_answer(self.kristals,'KR-ARCHIVES','TERRITOIRE','OCCUPANTS',access_granted=True)

    def test_reader_exact_answer(self):
        original=self.kristals[0]['topics'][0]['questions'][0]
        response=read_answer(self.kristals,'KR-ARCHIVES','TERRITOIRE','OCCUPANTS',access_granted=True,demo=True)
        self.assertEqual(response['answer'],original['answer'])
        self.assertEqual(response['source_refs'],original['source_refs'])
        self.assertTrue(response['demo'])

    def test_reader_rejects_unknown_question_and_topic(self):
        with self.assertRaises(ReferenceError):
            read_answer(self.kristals,'KR-ARCHIVES','TERRITOIRE','QUESTION_INVENTEE',access_granted=True,demo=True)
        with self.assertRaises(ReferenceError):
            read_answer(self.kristals,'KR-ARCHIVES','THEME_INCONNU','OCCUPANTS',access_granted=True,demo=True)

    def test_no_published_demo_documents(self):
        self.assertTrue(all(k['status']=='demo' for k in self.kristals))
        self.assertTrue(all(not publication_ready(k) for k in self.kristals))

    def test_publication_guard_requires_sources_and_review(self):
        item=copy.deepcopy(self.kristals[0])
        item['status']='published'
        self.assertFalse(publication_ready(item))
        item['sources'][0]['verified']=True
        item['sources'][0]['rights_cleared']=True
        item['sources'][0]['citation']='Référence revue en test (fictive)'
        item['editorial_review']['status']='approved'
        item['editorial_review']['reviewed_at']='2026-10-12T12:00:00Z'
        self.assertTrue(publication_ready(item))
        item['perspective']['type']='nation_autochtone_identifiee'
        self.assertFalse(publication_ready(item))
        item['editorial_review']['community_review_status']='approved'
        self.assertTrue(publication_ready(item))

    def test_prompt_dispatch_and_idempotence(self):
        first,seen=select_prompts(self.prompts,'kristal.acces_accorde','demandeur','e-1','P-001')
        self.assertEqual(len(first),1)
        self.assertEqual(first[0]['body'],self.prompts[3]['body'])
        again,seen2=select_prompts(self.prompts,'kristal.acces_accorde','demandeur','e-1','P-001',seen)
        self.assertEqual(again,[])
        self.assertEqual(seen,seen2)
        other,_=select_prompts(self.prompts,'kristal.acces_accorde','gardien','e-1','P-001')
        self.assertEqual(other,[])

    def test_order_never_runs_on_incomparable_scores(self):
        with self.assertRaises(ValueError):
            order_for_choice({'P-001':50,'P-002':90},comparable=False,seed='test-only')

    def test_order_stable_and_private(self):
        scores={'P-001':80,'P-002':90,'P-003':80}
        a=order_for_choice(scores,comparable=True,seed='secret-session-seed')
        b=order_for_choice(scores,comparable=True,seed='secret-session-seed')
        self.assertEqual(a,b)
        self.assertEqual(a[0],'P-002')

    def test_prompt_requires_blocked_in_minimal_demonstrator(self):
        more=self.prompts+[dict(self.prompts[0],id='PR-BLOQUE',requires=['condition_privée'])]
        out,_=select_prompts(more,'session.roles_publies','participant','evt','P-007')
        self.assertEqual([p['prompt_id'] for p in out],['PR-DEPART'])

if __name__ == '__main__':unittest.main()
