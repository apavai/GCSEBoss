# GCSE Boss Morning Briefing: Friday 28 August 2026

**Generated:** 07:15 BST by CEO Agent
**Agent team status:** ✅ 3 of 3. Research Lite ✅ 05:22. Daily Content Agent ✅ 05:40 to 05:59, full run including approval page and self-QA log. CEO Agent ✅ 07:15.

---

## 🎯 Today's Priority

**Commit the QA fixes before you push, then approve the bundle.** The blog post was committed at 05:58 as `7f5bfc3`, but six of today's QA auto-fixes landed in the file *after* that commit. `blog/posts/november-gcse-resit-revision.html` currently sits 22 lines ahead of the committed version, including the og:title rewrite and the keyword H2. **A `git push` right now would publish the pre-fix draft.** Same pattern as the 26 August post. Commit the working tree first, then push.

Then approve: `/Users/ben/GCSEBoss/02-Marketing/approval-pages/2026-08-28-approval.html`

The angle is the last weekday of the holiday and resit search intent climbs from here to late September, so the window is wide but today is the natural publish day.

---

## 📋 Approval Queue

### Blog Post

- **Title:** Revising for November GCSE Resits: What the Next Ten Weeks Should Look Like
- **Target keyword:** november gcse resit revision
- **QA Status:** ✅ PASS (23 checks: 16 PASS, 1 N/A, 6 auto-fixed in-run, 0 unresolved FAIL)
- **Word count:** 1,249, inside the 1,000 to 1,250 band
- **Audience:** Student (Mon/Wed/Fri rotation) ✅
- **Action needed:** `git add` the modified post and the three re-composed crops, commit, then push. Untracked QA report and blog draft to add too.
- **Direct link:** `/Users/ben/GCSEBoss/blog/posts/november-gcse-resit-revision.html`

CEO spot-checks: 7 H2 sections, keyword present in title, meta description, og:title, first paragraph and H2 #1 after the fix. Index card patched at the top of `blog/index.html` and already committed. Zero em dashes and zero banned substitutes across blog, index card, all six captions and all twelve overlay strings.

### Social bundle

- **TikTok**: ready. 1080×1920 MP4 verified h264, 30/1 fps, 450 frames, exactly 15.000s. Still PNG present. Caption 1,268/1,500, paste manually in the app.
- **Instagram (portrait)**: ready. 1080×1350, caption 1,809/2,200.
- **Facebook**: ready. 1080×1080, routes to GCSE Boss Page 925540653986300.
- **LinkedIn**: ready. 1080×1080, routes to GCSE Boss Company Page 112469982. Caption 1,452/3,000.
- **X**: ready. 1200×675, caption 272/280 after an auto-fix down from 309. No URL in the caption, add the blog link as the first comment.
- **Pinterest**: ready. 1000×1500, pin title 67/100, description 462/500.
- **QA status:** ✅ PASS
- **One-click approval:** `/Users/ben/GCSEBoss/02-Marketing/approval-pages/2026-08-28-approval.html` (13.4 MB, all 6 stills plus the MP4 embedded inline)

**Recorded deviation worth knowing about.** The master is a single student sitting left of centre with the head low in frame, so the skill's default focal points printed the headline across her face on the 1:1 and 16:9 crops. Facebook, LinkedIn and X were re-cropped and re-composed (fy 0.44→0.58 on 1:1, 0.42→0.50 on 16:9). Logged as a deviation, nothing changed in the skill. TikTok MP4 unaffected, no re-render.

**One item a reader could catch us on.** Today's brief gives the November series as 2 to 11 November, but our existing `gcse-resits-november` post says 2 to 18 November. Neither is sourced to a board timetable in our files. Today's copy hedges to "early November" and "the first half of November" on every surface, with exact dates left to the exam centre. **The two posts still contradict each other on the live site.** Worth resolving against the JCQ common timetable and correcting whichever is wrong.

**Stat deliberately withheld.** The Tes pass-rate figure from this morning's brief (English and maths down a fifth straight year) was left out of blog and captions on safeguarding grounds. Agreed call on a resit post.

---

## 📊 Quick Stats

- **Blog posts live:** 66 (65 pushed, 1 awaiting your approval and a re-commit)
- **Social posts shipped, last 7 days:** 22 across the 24 to 27 August bundles. The 27 August run went 5 for 5 on photos, TikTok in the drafts inbox as usual.
- **Upload-Post quota used this month:** within plan, no limit hit
- **Gemini cost this month, estimate:** under £1.20. Today's run about £0.02, one wasted 404 then a success on prompt variant 1, no safety block.

---

## 🔍 Research swap-in flag

**No swap-in today.** Research Lite recommends the scheduled angle and the publication window is at its widest. No exam board announcement landed overnight, which was the one trigger the weekly plan named for a Friday swap.

**Forward note for Monday:** the week of 24 August plan runs out today. Next week's plan is due from the Sunday Planner at 17:00 on 30 August, and it still has no content bank to draw from. See carry-forward item 1.

---

## 📰 Today's Research Lite headline

Nothing material broke overnight. Three live threads, none forcing a change: English and maths pass rates down a fifth straight year (handle with care, needs a Source line if it ever reaches a caption), Ofqual keeping the maths and science formula sheets to 2030 or 2031 (usable in the maths weeks), and September policy changes that are teacher-facing background only. The free revision surface has already moved onto November resit content, but almost none of it separates resit revision from first-time revision, so the half-known-content premise sits in a real gap.

---

## 🤖 Agent Activity Log

| Agent | Status | Output |
|---|---|---|
| Research Lite | ✅ 05:22 | Daily brief, no swap-in |
| Daily Content Agent | ✅ 05:40 to 05:59 | Blog + 6 social assets + TikTok MP4 + captions + approval page + QA log |
| CEO Agent | ✅ 07:15 | This briefing |

---

## ⏳ Carry-forward open items

1. **🔴 `content-bank-v1.xlsx` still does not exist.** Sixth day open and now genuinely blocking. Today is the last angle in the current plan, so Sunday's Planner at 17:00 on 30 August has nothing to draw from for the week of 31 August. Either rebuild it this weekend or tell the Planner to improvise. The 24 August plan already listed five candidate September angles you could seed it with.
2. **🔴 Uncommitted QA fixes on the day's blog post, twice this week.** The Daily Content Agent commits in Phase 9 and then auto-fixes after, so the committed version is stale by the time you see it. Worth a Phase 9 ordering fix in the daily-content skill: commit last, after the fix pass.
3. **Research Lite skill body still missing** at `/Users/ben/GCSEBoss/.claude/skills/gcse-boss-research-lite/SKILL.md`. Six days open. The scheduled task points at itself and the agent has reused the 24 to 27 August brief structure every morning since. Still the most fragile thing in the stack.
4. **Project skill bodies are not in the repo.** Neither `gcse-boss/SKILL.md` nor `gcse-boss-daily-content/SKILL.md` nor `gcse-boss-ceo-agent/SKILL.md` is under `/Users/ben/GCSEBoss/.claude/skills/`. Only `DECISIONS.md` and `scripts/` are there. Every agent loads from the plugin cache, so the documented folder structure does not match reality and the repo copy could go silently stale. Second day open.
5. **November window contradiction between two live posts.** New today, detail in the approval queue above. 2 to 11 vs 2 to 18 November.
6. **Imagen 4 Fast still returning HTTP 404.** Five days running. The cascade self-heals to `gemini-3.1-flash-image` immediately so nothing breaks, but every run burns a failed call. Reordering MODELS is a one-line decision.
7. **QA harness note still unwritten.** Yesterday's finding: the em dash grep should run on prose only, after markdown structure and HTML attributes are stripped. Today it again flagged 7 `---` horizontal rules as double hyphens. Harmless but it costs a manual dismissal every morning.
8. **Git identity not configured in the run environment.** Today's commit again needed explicit `-c user.name` / `-c user.email`. A repo-local identity removes the workaround permanently.
9. **gcseboss.com homepage em dash sweep still outstanding.** Open since 21 August.
10. **Stale hard-coded sandbox paths** in `gemini_background.py` and `compose_still.py` defaults. One-line fix each.
11. **No `02-Marketing/social-performance/dashboard-data.js`.** Dashboard update skipped, as specified.
12. **Stray file still on disk.** `_gcseboss_captions_tmp.py` is still in `/Users/ben/Claude/Membership website/`, 14 bytes, one placeholder line. Safe to delete by hand.

**Resolved since yesterday:**

- Blog `<title>` double colon on the 27 August post was fixed and committed as `2854cc3`.
- The Daily Content Agent again completed Phases 8 and 9 cleanly, landing at 05:59, inside the CEO slot.
- Over-applied hyphen sweep caught in-run this morning (`re reading`, `ten week plans`, `first time revision` and others). Rule 9's "keep compounds" clause held, at the cost of one X re-render.

---

*CEO Agent autonomous Friday compile. Nothing approved, nothing published, no drafts modified. Commit the working tree, push, then approve via `/02-Marketing/approval-pages/2026-08-28-approval.html`.*
