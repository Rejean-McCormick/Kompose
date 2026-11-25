import unittest

from kompose.school_role_proposals import propose_roles

# Keep these fixtures independent of a Kontexte checkout.
MISSION={'format':'kontexte.mission/1','id':'demo','synthetic':True,'safety':{'publication_default':'private'},
         'roles':['fermier','boulanger'],'steps':[{'role':'fermier','curriculum_ids':['qc-math']},
                                                 {'role':'boulanger','curriculum_ids':['qc-fr']}]}
PEOPLE=[{'eleve_ref':'pupil-1','pratique_souhaitee':['qc-fr'],'deja_pratique':[]},
        {'eleve_ref':'pupil-2','pratique_souhaitee':['qc-math'],'deja_pratique':[]}]


class SchoolRoleProposalTests(unittest.TestCase):
    def test_complementary_and_not_authoritative(self):
        out = propose_roles(MISSION, PEOPLE)
        chosen = {p['role_code']: p['eleve_ref'] for p in out['propositions']}
        self.assertEqual(chosen, {'fermier': 'pupil-2', 'boulanger': 'pupil-1'})
        self.assertIs(out['dispatch_allowed'], False)
        self.assertTrue(out['teacher_approval_required'])
        self.assertEqual(out, propose_roles(MISSION, PEOPLE))

    def test_rejects_unapproved_profile_fields(self):
        with self.assertRaises(ValueError):
            propose_roles(MISSION, [{**PEOPLE[0], 'real_name': 'Alice'}])

    def test_leave_unfilled_roles_to_teacher(self):
        out = propose_roles(MISSION, [PEOPLE[0]])
        self.assertEqual(len(out['propositions']), 2)
        self.assertTrue(any(p['eleve_ref'] is None for p in out['propositions']))
