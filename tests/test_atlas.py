import copy, importlib.util, json, sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("build", ROOT / "scripts/build.py")
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)
DATA = json.loads((ROOT / "assets/example.json").read_text())
ATLAS = json.loads((ROOT / "examples/atlas-intro/content.json").read_text())


class AtlasTests(unittest.TestCase):
    def test_atlas_builds_standalone_css(self):
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "a.json"
            src.write_text(json.dumps(ATLAS))
            build.build(src, Path(temp) / "out")
            css = (Path(temp) / "out/style.css").read_bytes()
            self.assertEqual(css, (ROOT / "assets/theme-atlas.css").read_bytes())
            html = (Path(temp) / "out/page-01.html").read_text()
            self.assertIn('class="sheet atlas layout-cover"', html)

    def test_legacy_content_renders_in_atlas(self):
        with tempfile.TemporaryDirectory() as temp:
            build.build(ROOT / "assets/example.json", Path(temp) / "out", "atlas")
            self.assertIn("legacy flow", (Path(temp) / "out/page-01.html").read_text())

    def test_atlas_kinds_rejected_in_light(self):
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "a.json"
            src.write_text(json.dumps(ATLAS))
            for theme in ("light", "dark"):
                with self.assertRaises(ValueError):
                    build.build(src, Path(temp) / theme, theme)

    def test_escapes_text(self):
        data = copy.deepcopy(ATLAS)
        data["pages"][0]["title"] = "<script>x</script>"
        with tempfile.TemporaryDirectory() as temp:
            src = Path(temp) / "a.json"
            src.write_text(json.dumps(data))
            build.build(src, Path(temp) / "out")
            self.assertNotIn("<script>x", (Path(temp) / "out/page-01.html").read_text())

    def test_invalid_atlas_fields(self):
        def first(data, kind):
            return next(b for p in data["pages"] for b in p["blocks"] if b["kind"] == kind)
        bad = copy.deepcopy(ATLAS)
        first(bad, "steps")["actions"] = ["too", "many", "gaps", "for", "steps", "!"]
        with self.assertRaises(ValueError):
            build.atlas.validate(build.validate(bad))
        bad = copy.deepcopy(ATLAS)
        first(bad, "table")["trows"][0]["state"] = "<b>"
        with self.assertRaises(ValueError):
            build.atlas.validate(build.validate(bad))


if __name__ == "__main__":
    unittest.main()
