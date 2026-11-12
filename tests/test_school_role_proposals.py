import json
from pathlib import Path
import pytest
from kompose.school_role_proposals import propose_roles

ROOT=Path(__file__).resolve().parents[2]/'Kontexte'
# Do not require Kontexte repo in Kompose's independent tests.
MISSION={'format':'kontexte.mission/1','id':'demo','synthetic':True,'safety':{'publication_default':'private'},
         'roles':['fermier','boulanger'],'steps':[{'role':'fermier','curriculum_ids':['qc-math']},
                                                 {'role':'boulanger','curriculum_ids':['qc-fr']}]}
PEOPLE=[{'eleve_ref':'pupil-1','pratique_souhaitee':['qc-fr'],'deja_pratique':[]},
        {'eleve_ref':'pupil-2','pratique_souhaitee':['qc-math'],'deja_pratique':[]}]

def test_complementary_and_not_authoritative():
    out=propose_roles(MISSION,PEOPLE)
    chosen={p['role_code']:p['eleve_ref'] for p in out['propositions']}
    assert chosen=={'fermier':'pupil-2','boulanger':'pupil-1'}
    assert out['dispatch_allowed'] is False and out['teacher_approval_required']
    assert out==propose_roles(MISSION,PEOPLE)

def test_rejects_unapproved_profile_fields():
    with pytest.raises(ValueError):propose_roles(MISSION,[{**PEOPLE[0],'real_name':'Alice'}])

def test_leave_unfilled_roles_to_teacher():
    out=propose_roles(MISSION,[PEOPLE[0]])
    assert len(out['propositions'])==2
    assert any(p['eleve_ref'] is None for p in out['propositions'])
