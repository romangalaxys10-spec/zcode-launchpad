#!/usr/bin/env python3
"""changelog_from_git.py -- draft a grouped changelog from git history.

Stdlib only. Python 3.8+. Cross-OS (uses subprocess, pathlib).

Groups commits since a ref (tag, branch, or date) into:
  * Breaking  -- subjects/footers contain "BREAKING CHANGE" / "BREAKING:" or
                 the conventional-commits "!" marker
  * Added     -- feat(...)
  * Fixed     -- fix(...)
  * Perf      -- perf(...)
  * Docs      -- docs(...) / ci(...) / test(...) / chore(...) / refactor(...)
  * Other     -- everything else

Usage:
  python3 changelog_from_git.py <ref> [--repo PATH] [--version TAG]
    <ref> a git rev range end: a tag, commit, branch, or date like 2026-01-01.
          With a tag or rev, we read log ref..HEAD. With a date, log --since.

Exit codes:
  0 success (markdown changelog on stdout)
  1 not a git repo / ref does not resolve
  2 bad arguments
"""

import argparse
import re
import subprocess
import sys


def fail(code, msg):
    print(msg, file=sys.stderr)
    sys.exit(code)


def git(repo, *args, allow_fail=False):
    cmd = ["git", "-C", repo] + list(args)
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0 and not allow_fail:
        fail(1, "git error: %s\n%s" % (" ".join(args), p.stderr.strip()))
    return p


def is_date(s):
    return re.fullmatch(r"\d{4}(-\d{2}(-\d{2})?)?", s) is not None


def collect(repo, ref, version):
    if is_date(ref):
        p = git(repo, "log", "--since=%s" % ref, "--no-merges",
                "--pretty=format:%h\t%s", allow_fail=False)
    else:
        p = git(repo, "log", "%s..HEAD" % ref, "--no-merges",
                "--pretty=format:%h\t%s", allow_fail=False)
        if p.returncode != 0:
            fail(1, "cannot resolve ref %r: %s" % (ref, p.stderr.strip()))
    entries = []
    for line in p.stdout.splitlines():
        if "\t" not in line:
            continue
        sha, subject = line.split("\t", 1)
        entries.append((sha, subject))
    return entries


CONV = re.compile(r"^(\w+)(\(([^)]*)\))?(!)?:\s*(.*)$")


def classify(subject):
    """Return group key for a subject. Breaking wins over everything else."""
    m = CONV.match(subject)
    if m:
        t = m.group(1).lower()
        bang = m.group(4)
        rest = m.group(5).lower()
        if bang or "breaking" in rest:
            return "breaking"
        if t == "feat":
            return "added"
        if t == "fix":
            return "fixed"
        if t == "perf":
            return "perf"
        if t in ("docs", "ci", "test", "chore", "refactor"):
            return "docs"
    low = subject.lower()
    if "breaking" in low:
        return "breaking"
    if low.startswith(("feat", "feature")) or low.startswith("add"):
        return "added"
    if low.startswith(("fix", "patch", "bug")):
        return "fixed"
    return "other"


GROUPS = [
    ("breaking", "Breaking Changes"),
    ("added", "Added"),
    ("fixed", "Fixed"),
    ("perf", "Performance"),
    ("docs", "Docs, Test, Chore"),
    ("other", "Other"),
]


def main():
    ap = argparse.ArgumentParser(
        description="Draft a grouped changelog from git log since a ref or date.")
    ap.add_argument("ref", help="tag, rev range end, or date (YYYY-MM-DD)")
    ap.add_argument("--repo", default=".", help="path to repo root (default .)")
    ap.add_argument("--version", default=None,
                    help="version label for the changelog header")
    a = ap.parse_args()

    try:
        git(a.repo, "rev-parse", "--git-dir")
    except SystemExit:
        raise
    except Exception as e:
        fail(1, "not a git repo: %s" % e)

    entries = collect(a.repo, a.ref, a.version)
    if not entries:
        fail(1, "no commits found for ref %r. Nothing to draft." % a.ref)

    buckets = {k: [] for k, _ in GROUPS}
    for sha, subject in entries:
        buckets[classify(subject)].append((sha, subject))

    out = []
    header = "# Changelog"
    if a.version:
        header += " %s" % a.version
    out.append(header)
    out.append("")
    out.append("Draft from %d commits since %s. Verify each line against the "
               "diff before shipping. (commit shortsha) suffix = source." %
               (len(entries), a.ref))
    out.append("")
    for key, title in GROUPS:
        if not buckets[key]:
            continue
        out.append("## %s" % title)
        out.append("")
        for sha, subject in buckets[key]:
            out.append("- %s (%s)" % (subject, sha))
        out.append("")
    print("\n".join(out))
    sys.exit(0)


if __name__ == "__main__":
    main()
