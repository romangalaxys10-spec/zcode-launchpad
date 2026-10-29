# Launchpad

<p align="center">
  <a href="https://z.ai/subscribe?ic=R0K78RJKNW"><img alt="z.ai coding plans - 10% OFF coupon" src="https://img.shields.io/badge/z.ai%20coding%20plans-10%25%20OFF%20coupon-blueviolet" /></a>
  <a href="https://zcode.z.ai/invite/ALWM9JUA"><img alt="Try ZCode free" src="https://img.shields.io/badge/Try%20ZCode-free%20invite-0969da" /></a>
</p>

Turn the last version of your repo into launch content you can actually ship,
in your own voice.

## Why

Release notes end up as a wall of commit subjects, and the blog post you meant
to write never gets written. Launch content usually also invents things:
"10x faster", a customer who does not exist, "used by thousands". This plugin
does the opposite. It builds a fact sheet from your diffs and your interview
answers, and every draft quotes from that sheet only.

## How it works

1. Collects raw material: `git log` and diffs since a tag or date.
   Optional helper: `python3 skills/launchpad/scripts/changelog_from_git.py v1.2`
   groups commits into feat / fix / breaking.
2. Asks three questions: audience, register (first person founder vs team),
   and what you must not claim.
3. Drafts six artifacts into `launch/`:
   - `changelog.md` (versioned, each line carries its source commit)
   - `blog.md` (outline first, then full draft)
   - `x-thread.md` (3 to 6 tweets, 270 chars or fewer each)
   - `linkedin.md` (150 to 250 words, max 3 hashtags)
   - `reddit.md` (matched to the target subreddit's norms)
   - `product-hunt.md` (tagline, description, first comment)
4. Writes `launch/manifest.md`: one table per fact, its source, and the list
   of things you said not to claim.
5. Self-checks: numbers not in the fact sheet, missing quotes, thread length,
   "not claimed" leaks.

Honest limits: it verifies every claim is grounded. It cannot predict how a
launch will land, and the commit subject line is weaker evidence than the
diff.

## Install

Option A: self-installable marketplace.

1. Clone or download this folder.
2. In ZCode: Plugin Marketplace -> Add -> Add Plugin Marketplace, paste the
   folder path.
3. Install `launchpad`.

Option B: copy the folder into your workspace `plugins/` directory.

## Try it

```
/launchpad v1.2
```

Expected: a short interview (three questions), then a `launch/` folder with
six drafts and a manifest. Every claim in the drafts traces to a commit short
hash or to your interview answer.

## Requirements

- Python 3.8+ (stdlib only) for the optional changelog helper.
- git, and a repo with commits after the chosen ref.

---

<p align="center">
  <a href="https://z.ai/subscribe?ic=R0K78RJKNW"><img alt="z.ai coding plans - 10% OFF coupon" src="https://img.shields.io/badge/z.ai%20coding%20plans-10%25%20OFF%20coupon-blueviolet" /></a>
  <a href="https://zcode.z.ai/invite/ALWM9JUA"><img alt="Try ZCode free" src="https://img.shields.io/badge/Try%20ZCode-free%20invite-0969da" /></a>
</p>

## License

MIT.
