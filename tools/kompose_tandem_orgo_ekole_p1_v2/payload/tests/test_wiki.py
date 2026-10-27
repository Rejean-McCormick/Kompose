"""Offline validation of the English GitHub wiki."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def wiki_directory(root: Path) -> Path:
    """Resolve the separate Kompose.wiki checkout, with legacy in-repo fallback."""
    sibling = root.parent / 'Kompose.wiki'
    legacy = root / 'wiki'
    if sibling.is_dir() and not sibling.is_symlink():
        return sibling
    if legacy.is_dir() and not legacy.is_symlink():
        return legacy
    return sibling  # Existing tests fail visibly if no wiki is present.

WIKI = wiki_directory(ROOT)


class WikiTests(unittest.TestCase):
    def test_external_wiki_and_legacy_fallback(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            repo = parent / 'Kompose'
            repo.mkdir()
            self.assertEqual(wiki_directory(repo), parent / 'Kompose.wiki')
            (repo / 'wiki').mkdir()
            self.assertEqual(wiki_directory(repo), repo / 'wiki')
            (parent / 'Kompose.wiki').mkdir()
            self.assertEqual(wiki_directory(repo), parent / 'Kompose.wiki')

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
