import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(args, cwd=None):
    return subprocess.run(
        [sys.executable, str(ROOT / "straylog.py")] + args,
        capture_output=True, text=True, cwd=cwd,
    )


def test_clean_file(tmp_path):
    f = tmp_path / "clean.py"
    f.write_text("x = 1\ny = x + 2\n")
    r = run([str(tmp_path)])
    assert r.returncode == 0
    assert "No stray debug" in r.stdout


def test_detects_print(tmp_path):
    f = tmp_path / "a.py"
    f.write_text("print('hi')\n")
    r = run([str(tmp_path)])
    assert r.returncode == 1
    assert "a.py:1" in r.stdout
    assert "[print]" in r.stdout


def test_json_output(tmp_path):
    f = tmp_path / "b.js"
    f.write_text("console.log('x');\n")
    r = run([str(tmp_path), "--json"])
    assert r.returncode == 1
    data = json.loads(r.stdout)
    assert len(data) == 1
    assert data[0]["kind"] == "console"


def test_ignore_dir(tmp_path):
    d = tmp_path / "node_modules"
    d.mkdir()
    (d / "x.js").write_text("console.log('x');\n")
    r = run([str(tmp_path)])
    assert r.returncode == 0
