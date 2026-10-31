"""Verify hook plumbing in a temporary directory, without real secrets or Git writes."""
import os
from pathlib import Path
import subprocess
import tempfile

hook = Path(__file__).resolve().parents[1] / "skills/git-quality-hooks/assets/pre-commit"
subprocess.run(["/bin/sh", "-n", str(hook)], check=True)
with tempfile.TemporaryDirectory(prefix="agent-skills-hook-") as tmp:
    root = Path(tmp)
    bin_dir = root / "bin"
    bin_dir.mkdir()
    args = root / "args.txt"
    env = {**os.environ, "PATH": str(bin_dir), "TEST_SCANNER_ARGS": str(args)}
    missing = subprocess.run(["/bin/sh", str(hook)], env=env, capture_output=True, text=True)
    assert missing.returncode == 1 and "gitleaks is required" in missing.stderr

    scanner = bin_dir / "gitleaks"
    scanner.write_text('#!/bin/sh\nprintf "%s\\n" "$@" > "$TEST_SCANNER_ARGS"\nexit "$TEST_SCANNER_EXIT"\n')
    scanner.chmod(0o755)
    expected = ["protect", "--staged", "--redact=100", "--no-banner", "--no-color"]
    for code in (0, 1, 42):
        result = subprocess.run(
            ["/bin/sh", str(hook)], env={**env, "TEST_SCANNER_EXIT": str(code)},
            capture_output=True, text=True,
        )
        assert result.returncode == code, (code, result.returncode)
        assert args.read_text().splitlines() == expected
print("Hook syntax, missing scanner, exact staged/redacted arguments, and exit codes 0/1/42 passed.")
