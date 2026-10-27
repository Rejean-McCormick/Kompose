"""Structured contract validation when optional dev dependencies are present."""
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
SC=ROOT/'contracts'/'schemas'
EX=ROOT/'examples'

class SchemaValidationTests(unittest.TestCase):
    @unittest.skipUnless(importlib.util.find_spec('jsonschema'), 'Installer .[dev] pour valider JSON Schema')
    def test_every_json_schema_is_valid(self):
        import jsonschema
        for p in SC.glob('*.schema.json'):
            with self.subTest(schema=p.name):
                jsonschema.Draft202012Validator.check_schema(json.loads(p.read_text(encoding="utf-8")))

    @unittest.skipUnless(importlib.util.find_spec('jsonschema'), 'Installer .[dev] pour valider JSON Schema')
    def test_examples_follow_public_schemas(self):
        import jsonschema
        schema_names={'capsule':'capsule.json','role':'roles.json','kristal':'kristals.json',
                      'mission':'missions.json','prompt':'prompts.json','session':'session.example.json',
                      'diagnostic-blueprint':'diagnostic.json','teacher-constraint':'teacher-constraints.PRIVE-DEMO.json',
                      'phase':'phases.json','event':'event.example.json'}
        single={'capsule','session','diagnostic-blueprint','event'}
        roots={'role':'roles','kristal':'kristals','mission':'missions','prompt':'prompts',
               'teacher-constraint':'constraints','phase':'phases'}
        for key, filename in schema_names.items():
            schema=json.loads((SC/f'{key}.schema.json').read_text(encoding="utf-8"))
            data=json.loads((EX/'capsule-rivieres'/filename).read_text(encoding="utf-8"))
            values = [data] if key in single else data[roots[key]]
            for i, value in enumerate(values):
                with self.subTest(type=key, index=i):
                    jsonschema.validate(value,schema)
        schema=json.loads((SC/'integration-manifest.schema.json').read_text(encoding="utf-8"))
        manifest=json.loads((EX/'integrations/kor.adapter.example.json').read_text(encoding="utf-8"))
        jsonschema.validate(manifest,schema)

    @unittest.skipUnless(importlib.util.find_spec('yaml'), 'Installer .[dev] pour valider OpenAPI')
    def test_openapi_parses_and_paths_are_well_formed(self):
        import yaml
        spec=yaml.safe_load((ROOT/'contracts/openapi.yaml').read_text(encoding="utf-8"))
        self.assertEqual(spec['openapi'],'3.1.0')
        self.assertTrue(spec['info']['title'].startswith('KOMPOSE'))
        ids=[]
        for path, operations in spec['paths'].items():
            tokens=set(re.findall(r'\{([^}]+)\}', path))
            for method,op in operations.items():
                if method not in {'get','post','put','delete','patch'}: continue
                ids.append(op['operationId'])
                params={p.get('name') or p['$ref'].split('/')[-1] for p in op.get('parameters',[])}
                self.assertTrue(tokens <= params, f'{path} missing path parameters')
        self.assertEqual(len(ids),len(set(ids)))

    def test_document_links_resolve(self):
        docs=[ROOT/'README.md',*ROOT.glob('docs/**/*.md'),ROOT/'contracts/README.md',
              ROOT/'examples/capsule-rivieres/README.md']
        for file in docs:
            txt=file.read_text(encoding="utf-8")
            for link in re.findall(r'\[[^\]]+\]\(([^)#]+)(?:#[^)]*)?\)',txt):
                if link.startswith(('https://','http://','mailto:')): continue
                if link.startswith('#'): continue
                resolved=(file.parent/link).resolve()
                with self.subTest(file=file.name,target=link):
                    self.assertTrue(resolved.exists(),f'{file}: broken link {link}')

if __name__=='__main__':unittest.main()
