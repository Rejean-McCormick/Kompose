"""Offline validation of the English GitHub wiki."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Le wiki est un dépôt distinct; une copie embarquée historique reste acceptée.
EXTERNAL_WIKI = ROOT.parent / 'Kompose.wiki'
WIKI = EXTERNAL_WIKI if EXTERNAL_WIKI.is_dir() else ROOT / 'wiki'


@unittest.skipUnless(WIKI.is_dir(), "Wiki facultatif non livré : cloner Kompose.wiki à côté du dépôt")
class WikiTests(unittest.TestCase):
    def test_navigation_files_present(self):
        for name in ('Home', '_Sidebar', '_Footer', 'Quick-Start', 'API-and-Contracts', 'Security-Privacy-and-Fairness'):
            self.assertTrue((WIKI / f'{name}.md').is_file(), name)

    def test_internal_wikilinks_resolve(self):
        available = {p.stem for p in WIKI.glob('*.md')}
        for path in WIKI.glob('*.md'):
            if path.name == 'README-WIKI-SOURCE.md':
                continue
            with self.subTest(page=path.name):
                for slug in re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', path.read_text(encoding='utf-8')):
                    self.assertIn(slug, available)

    def test_required_status_disclaimers(self):
        home = (WIKI / 'Home.md').read_text(encoding='utf-8').lower()
        kristals = (WIKI / 'Kristals.md').read_text(encoding='utf-8').lower()
        self.assertIn('not a product ready', home)
        self.assertIn('no generative ai', kristals)
        self.assertIn('status: demo', kristals)

    def test_wiki_pages_have_titles(self):
        for path in WIKI.glob('*.md'):
            if path.name.startswith('_'):
                continue
            with self.subTest(page=path.name):
                self.assertRegex(path.read_text(encoding='utf-8'), r'(?m)^# .+')

    def test_sidebar_lists_major_pages(self):
        sidebar = (WIKI / '_Sidebar.md').read_text(encoding='utf-8')
        for slug in ('Home', 'Entry-Door', 'Diagnostic-and-Role-Casting', 'Kristals', 'Architecture',
                     'Security-Privacy-and-Fairness', 'FAQ', 'Roadmap'):
            self.assertIn(f'[[{slug}', sidebar)


if __name__ == '__main__':
    unittest.main()
