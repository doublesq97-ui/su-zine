import copy, importlib.util, json, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build", ROOT / "scripts/build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)
DATA = json.loads((ROOT / "assets/example.json").read_text())

class ThemeTests(unittest.TestCase):
    def test_selection_and_default_regression(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name, theme, cli in [("default", None, None), ("light", "light", None), ("dark", "dark", None), ("cli", None, "dark"), ("override", "dark", "light")]:
                data = copy.deepcopy(DATA)
                if theme is not None: data["theme"] = theme
                source = root / f"{name}.json"
                source.write_text(json.dumps(data))
                build.build(source, root / name, cli)
            for name in ("default", "light", "override"):
                self.assertEqual((ROOT / "assets/style.css").read_bytes(), (root / name / "style.css").read_bytes())
            self.assertEqual((root / "dark/style.css").read_bytes(), (root / "cli/style.css").read_bytes())
            for name in ("light", "dark", "cli", "override"):
                self.assertEqual((root / "default/page-01.html").read_bytes(), (root / name / "page-01.html").read_bytes())

    def test_invalid_theme(self):
        for invalid in (None, 1, [], {}, "sepia", "<script>"):
            with self.assertRaises(ValueError): build.validate(dict(DATA, theme=invalid))
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "invalid"
            with self.assertRaises(ValueError): build.build(ROOT / "assets/example.json", out, "invalid")
            self.assertFalse(out.exists())
