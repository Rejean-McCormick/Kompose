"""Run all Kompose code/contract/security tests, excluding wiki publication checks.

The excluded test ids are printed; they are not silently reported as passing.
"""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))
EXCLUDE=(
    'test_wiki.WikiTests.',
    'test_contract_schemas.SchemaValidationTests.test_document_links_resolve',
)

def collect(suite):
    for part in suite:
        if isinstance(part,unittest.TestSuite):yield from collect(part)
        else: yield part

def main():
    suite=unittest.defaultTestLoader.discover(start_dir=str(ROOT/'tests'),pattern='test_*.py',top_level_dir=str(ROOT/'tests'))
    selected=[];deferred=[]
    for test in collect(suite):
        if any(test.id().startswith(prefix) for prefix in EXCLUDE):deferred.append(test.id())
        else:selected.append(test)
    print(f'[PORTEE] Interop/contrats/sécurité: {len(selected)} tests; {len(deferred)} tests documentaires exclus',flush=True)
    for item in deferred:print('[DOCS DIFFERE]',item,flush=True)
    result=unittest.TextTestRunner(verbosity=1).run(unittest.TestSuite(selected))
    return 0 if result.wasSuccessful() else 1

if __name__=='__main__':raise SystemExit(main())
