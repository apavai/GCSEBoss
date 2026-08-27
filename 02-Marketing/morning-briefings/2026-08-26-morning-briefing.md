# GCSE Boss Morning Briefing: Wednesday 26 August 2026

**Generated:** 07:25 BST by CEO Agent
**Agent team status:** ⚠️ 2.5 of 3. Research Lite ✅ 05:21. Daily Content Agent ⚠️ partial, produced blog + all 6 social assets + captions (05:45 to 05:52) then stopped before writing the approval page and the self-QA log. CEO Agent ✅ 07:25.

---

## 🎯 Today's Priority

**The bundle is complete and looks good, but there is no approval page to click through.** Everything else shipped. You either approve from the raw files listed below, or re-run the Daily Content Agent's approval-page phase to rebuild `2026-08-26-approval.html`. Given the course-change window is live and search intent falls off from about 1 September, do not let this slide to tomorrow.

---

## 📋 Approval Queue

### Blog Post

- **Title:** Changing A Level Subjects After GCSE Results: How Late Is Too Late
- **Target keyword:** changing a level subjects after gcse results
- **QA Status:** ✅ PASS on CEO spot-checks. No agent QA log exists, see below.
- **Word count:** 1,377. **Above the 1,000 to 1,250 band.** Not publish-blocking, but flagging it as the first overrun this week.
- **Audience:** Student (Mon/Wed/Fri rotation) ✅
- **Action needed:** Approve, then commit the working-tree edit and push. Commit `1f30ff9` is already in the log, but the file has since been modified.
- **Direct link:** `/Users/ben/GCSEBoss/blog/posts/changing-a-level-subjects-after-gcse-results.html`

**Git state needs a second look.** `1f30ff9 Add blog post: changing-a-level-subjects-after-gcse-results` is committed, but the file is modified in the working tree: one `<h2>` was rewritten from "How late is too late to change A level subjects after GCSE results" to "Changing A level subjects after GCSE results: how late is too late". The newer version is the better one, it front-loads the exact keyword. It is just not committed, so a push right now ships the older heading. `blog/index.html` is clean and the card is in.

### Social bundle

- **TikTok**: ready. MP4 verified 1080×1920, h264, 450 frames, exactly 15.000s. Still PNG present. Caption 1,119/1,500, paste manually in the app.
- **Instagram (portrait)**: ready. 1080×1350, caption 1,763/2,200.
- **Facebook**: ready. 1080×1080, routes to GCSE Boss Page 925540653986300.
- **LinkedIn**: ready. 1080×1080, routes to GCSE Boss Company Page 112469982.
- **X**: ready. 1200×675, caption **278/280**. Two characters of headroom, so do not touch it. No URL in the caption as specified, add the blog link as the first comment.
- **Pinterest**: ready. 1000×1500, description 458/800, pin title 62 chars. Yesterday's HTTP 400 was a title-length rejection, this one is comfortably inside.
- **QA status:** ✅ PASS on CEO spot-checks, ⚠️ no agent QA log.

**What I actually verified, since the self-QA log is missing:** zero em dash hits and zero banned substitutes across the blog HTML and all six captions (Standing Rule 9 clean). No competitor names anywhere (Rule 2). No grade-outcome claims (Rule 3). Brand name correct throughout, one-word form only in hashtags (Rule 5). No quantified stats in any caption, so no `Source:` line is required today (Rule 6). All six asset dimensions correct. Visual check on the Facebook and TikTok stills: student in frame, blue accent line, URL pill, dog-only watermark bottom right, palette clean, overlay strings match the captions word for word.

**What I could not verify:** the TikTok fade timing frame by frame, and the four remaining images beyond a dimension check. Duration and frame count are right, which is the usual failure surface, so the risk is low.

**How to approve without the approval page:**

1. Captions: `/Users/ben/GCSEBoss/02-Marketing/social-drafts/2026-08-26-changing-a-level-subjects-after-gcse-results.md`
2. Assets: `/Users/ben/GCSEBoss/02-Marketing/social-drafts/2026-08-26-*.png|mp4`
3. Blog: open the HTML above in a browser

---

## 📊 Quick Stats

- **Blog posts live:** 64 (63 pushed, 1 awaiting your approval)
- **Social posts shipped, last 7 days:** 11. Yesterday's run went 6 for 6, including the Pinterest retry. TikTok is in the drafts inbox, not live, so it still needs you in the app.
- **Upload-Post quota used this month:** within plan, no limit hit
- **Gemini cost this month, estimate:** under £1.10. Today's run about £0.02.

---

## 🔍 Research swap-in flag

**No swap-in today.** Research Lite recommends proceeding with the scheduled angle and the timing argues for it: the course-change window is open right now and closes as term starts. Agreed, no swap.

Forward notes:

- **Friday:** November resit entries close 4 October 2026, English Language and Maths only, results mid January 2027. Boards vary by a few days, so the copy should say "confirm with your exam centre".
- **Thursday:** unchanged.

---

## 📰 Today's Research Lite headline

Nothing material broke overnight. Results day plus six, peak enrolment. The Ofqual 20 August picture still stands (67.3% at grade 4/C or above, maths 53.8% at grade 5+) and is available if a future post needs a grade-threshold anchor. The competitor surface on course-change content is thin, mostly forum threads and tutoring blogs rather than a practical sequence, so today's angle sits in a real gap.

---

## 🤖 Agent Activity Log

| Agent | Status | Output |
|---|---|---|
| Research Lite | ✅ 05:21 | Daily brief, no swap-in |
| Daily Content Agent | ⚠️ 05:45 to 05:52, partial | Blog + 6 social assets + TikTok MP4 + captions. **No approval page, no QA log.** |
| CEO Agent | ✅ 07:25 | This briefing, plus substitute QA spot-checks |

---

## ⏳ Carry-forward open items

1. **🆕 Daily Content Agent stopped before Phase 8/9 today.** Approval page and QA log both missing. Yesterday the same two files landed at 08:49 and 08:51, well after the 07:15 CEO slot, so this may be a recurring late-phase stall rather than a one-off. Worth a look at where the run is dropping.
2. **🆕 Blog word count 1,377 against a 1,000 to 1,250 spec.** First overrun this week. Either trim or widen the band.
3. **🆕 Uncommitted `<h2>` edit** sitting on top of commit `1f30ff9`. Commit it before pushing or the older heading ships.
4. **Imagen 4 Fast still returning HTTP 404.** Cascade self-heals to `gemini-3.1-flash-image`, so nothing breaks, but every run burns a failed call. Open since 24 August. Decision needed on reordering MODELS.
5. **`content-bank-v1.xlsx` still does not exist.** Open since Sunday 23 August. The planner can draft a ~30 row rebuild next Sunday if you want that automated.
6. **Research Lite skill body still missing** at `/Users/ben/GCSEBoss/.claude/skills/gcse-boss-research-lite/SKILL.md`. Now open four days. The scheduled task effectively points at itself and the agent is running on its prompt plus the plugin copy of the project skill. This is the most fragile thing in the stack.
7. **Stale hard-coded sandbox paths** in `gemini_background.py` and `compose_still.py` defaults. One-line fix each.
8. **gcseboss.com homepage em dash sweep still outstanding.** Open since 21 August.
9. **`blog-drafts/` archive not tracking the site.** Today's draft did land there, which is an improvement.
10. **No `social-performance/dashboard-data.js`.** Dashboard update skipped, as specified.

**Resolved since yesterday:** the full 25 August bundle published, 6 for 6 across all platforms, and the Pinterest title/description split is now documented in commit `6ad2423`.

---

*CEO Agent autonomous Wednesday compile. Nothing approved, nothing published, no drafts modified. No approval page exists for today, so approve from the raw files listed above or rebuild the page, then commit the working-tree edit and push.*
