---
name: launchpad
description: Turn recent git history into launch content the user can actually ship (changelog, blog post, X thread, LinkedIn post, Reddit post, Product Hunt copy). Use when asked to write launch posts, changelogs, release announcements, or anything marketing the last version of a repo. Collects raw material from git, interviews the user on audience/tone/limits, then drafts each artifact grounded in real diffs and the user's words.
---

# launchpad

Produce launch content for a repo release. Every claim in the output traces to
one of two places: a commit/diff, or the user's own words from the interview.
If a claim has neither source, it does not go in the draft.

## Voice rules (apply to all drafts)
- Short sentences. Concrete facts. No hype words ("revolutionary", "game-changing", "unleash", "supercharge", "seamless").
- No em dashes. Use commas, periods, parentheses.
- No invented metrics ("10x faster", "99% of users"). If the repo has no benchmark
  the user ran, do not invent one. If the user states a number, use it and mark
  it as the user's own figure in the manifest.
- No fake user quotes. If no customer testimonial is provided, the post has
  none. Do not write `> "This is amazing" -- some user`.
- Write in the user's voice. The interview answers define tense, pronouns,
  and register (first-person founder post vs third-person team post).

## Step 1. Collect raw material
Pick the range:
```bash
# since a tag (recommended)
git log <tag>..HEAD --no-merges --pretty=format:'%h%x09%ad%x09%s' --date=short
git diff --stat <tag>..HEAD
# since a date
git log --since=2026-01-01 --no-merges --pretty=format:'%h%x09%ad%x09%s' --date=short
```
For each interesting commit, read the actual diff (not just the subject line):
```bash
git show <sha> --stat
git show <sha> -- <important-file>
```
Record a fact sheet (internal, not shipped): each fact as
`fact | source (commit sha + file, or user statement)`. This fact sheet is
what every draft below quotes from.

Optionally run the helper for a grouped starting point:
```bash
python3 scripts/changelog_from_git.py <ref-or-date>
```
It groups commits into feat / fix / breaking and prints a changelog draft.
It is a starting point, not the final changelog. Curate it.

## Step 2. Interview the user (keep it to 3 questions)
1. Who is the audience, and what should they do after reading (install, read docs,
   just know it exists)?
2. What register: first-person founder ("I shipped"), team ("we"), or neutral
   ("v2.3 adds")?
3. What must NOT be claimed (stability, uptime numbers, enterprise support,
   "no bugs", anything not tested)? Write each down. Drafts treat the list
   as a hard filter.

If the user says "just draft it" to the interview, assume: audience is existing
users of the tool, first-person, nothing untested gets claimed. Say so in the
manifest.

## Step 3. Produce the drafts
Create `launch/` (or the out dir the user named) with one file per artifact:

- `launch/changelog.md`
  Version, date, groups: Breaking, Added, Fixed. Every line ends with
  `(commit shortsha)` or `(reported issue N)` when the source is a commit.
- `launch/blog.md`
  Title + outline + full draft. Outline first, draft second, so the user can
  reorder. Opening line states what shipped in one sentence. Each section
  claims only facts from the fact sheet.
- `launch/x-thread.md`
  3 to 6 tweets, numbered 1/6 style. First tweet is the announcement. Middle
  tweets are features with one concrete detail each. Last tweet is the link.
  270 chars or fewer per tweet (count them).
- `launch/linkedin.md`
  150 to 250 words. No hashtag wall (max 3), no "excited to announce".
- `launch/reddit.md`
  Target a subreddit the user named (r/programming, r/developers, r/selfhosted,
  a language subreddit). Match its norms: r/selfhosted wants setup steps,
  r/programming wants the why, r/devops wants operations detail. Show the
  assumed norms at the top of the file as one line: `Norms assumed: ...`.
  Default to self-hosting/subreddit-agnostic technical post if none chosen.
- `launch/product-hunt.md`
  Tagline (under 60 chars), description (under 250 chars), first comment
  (the founder story in 80 to 150 words).
- `launch/manifest.md`
  One table per fact used across drafts: fact, source (sha or user quote),
  artifacts it appears in. Plus a "not claimed" list of anything the user said
  not to claim, so a future run does not accidentally claim it.

## Step 4. Self-check before returning the folder
For each draft, verify:
- No sentence states a number that is not in the fact sheet.
- No quote is attributed to anyone other than the user (unless the user
  provided a real quote in the interview).
- X thread tweets are each under 270 characters.
- "Not claimed" list items do not appear anywhere in the drafts.

Return: the manifest path, and the "not claimed" violations found (ideally none).

## Honest limits
- A commit subject line is weaker evidence than the diff. If the subject
  says "improve performance" and the diff shows a renamed variable, the fact
  is a rename, not a performance win.
- This skill cannot verify that the launch will be received well. It verifies
  that every claim is grounded.
- Reddit and LinkedIn norms are approximations. The user should read the
  target subreddit's rules before posting.
