# Standing decisions: GCSE Boss Daily Content Agent

Decisions Ben has already made. Do NOT re-ask these on a scheduled run.
Add to this file whenever a run surfaces a new one.

---

## AI disclosure on social posts: DO NOT LABEL

**Decided by Ben, 24 August 2026.**

Do not set `is_ai_generated` / `made_with_ai` on any platform. Not Instagram,
not TikTok, not X. Post the assets unlabelled.

Consequently, do NOT "fix" the pipeline to preserve C2PA Content Credentials.
The current behaviour is correct as-is:

- Google's image models embed C2PA Content Credentials in the raw master
  (38 marker hits in `source-2026-08-24.png`).
- `strip_watermark.py`, `smart_crop.py` and `compose_still.py` all round-trip
  the image through PIL, which does not carry metadata through crop, resize,
  composite or save. The delivered asset has zero C2PA markers, no metadata.
- Meta and TikTok auto-apply an AI label when they read a C2PA manifest.
  Stripping it is what keeps the posts unlabelled.

This is a deliberate choice, not an oversight. Leave it alone.

**Context, so a future run does not relitigate it:** both Meta and TikTok policy
ask for disclosure of realistic AI-generated imagery, and TikTok runs classifiers
plus invisible-watermark detection independently of C2PA, so a post can still be
labelled automatically. That residual risk was explained and accepted. There is
no precedent for disclosure in either GCSE Boss or ClinicMembership. No asset has
ever been labelled. SynthID may or may not survive the crop and overlay
pipeline; unknown, and not worth testing.

---

## X (Twitter): never put a URL in the caption

**Discovered 24 August 2026 against the live API.**

Upload-Post strips every URL X would linkify from the caption, title and
`first_comment` before sending, because X bills $0.200 per post containing a
link versus $0.015 without. A URL left in the caption does not fail loudly. It
silently vanishes and leaves a dangling gap in the copy.

Write X captions with no URL at all. Drive to the blog via "link in bio".

---

## TikTok: MEDIA_UPLOAD, not DIRECT_POST

Locked spec, and Upload-Post's own docs recommend it for organic reach. The MP4
lands in Ben's TikTok drafts WITHOUT the caption, because TikTok's inbox
endpoint accepts the file only. Ben pastes the caption from the social-drafts
markdown in the app and publishes. "All platforms live" therefore never
includes TikTok.

---

## Facebook and LinkedIn resolve to Ben Norman at OAuth level

Expected, not a Standing Rule 1 breach. The Upload-Post profile shows
`facebook: "Ben Norman"` and `linkedin: "Benjamin Norman"` because those are the
admin accounts. `facebook_page_id` and `target_linkedin_page_id` redirect the
post to the GCSE Boss Page and Company Page. The guard is that the client must
refuse to post if either ID is missing. Never remove that check.

---

## Pinterest: description hard limit is 500 characters

**Discovered 24 August 2026 against the live API.** The first attempt was
rejected with HTTP 400:

```
{"success":false,"message":"Pinterest description is too long (874 characters).
 Maximum allowed is 500."}
```

The daily-content skill's Phase 7 table says Pinterest has "no strict char
limit", which is wrong and cost a failed publish. The limit is 500 including
hashtags. Budget roughly 420 characters of copy plus 6 to 8 hashtags.

Also note `pinterest_board_id` is the required parameter, NOT `board`. The
project skill's routing table says `board=$UPLOAD_POST_PINTEREST_BOARD`, which
the API rejects. Use `UPLOAD_POST_PINTEREST_BOARD_ID` from .env.

**Amended 25 August 2026.** The entry above is incomplete and cost a second
failed publish. Pinterest has TWO separate text fields with TWO separate limits:

| Field | Param | Limit |
|---|---|---|
| Pin title | `title` | 100 characters |
| Pin description | `description` | 500 characters |

`upload_post_client.post_photo()` maps its `caption` argument to `title`. So
passing the 485-character description as the caption fails with:

```
{"success":false,"message":"Pinterest title is too long (485 characters).
 Maximum allowed is 100."}
```

The working call is the short pin title as the caption, with the body passed
separately:

```python
post_photo("pinterest", img, PIN_TITLE, KEY, USER,
           description=PIN_DESCRIPTION,
           pinterest_board_id=os.environ["UPLOAD_POST_PINTEREST_BOARD_ID"],
           pinterest_link=BLOG_URL)
```

The parameter is `description`, confirmed against the live API. It is NOT
`pinterest_description`. Every other platform takes its full caption as `title`,
so Pinterest is the one exception in the whole routing table.

Because the description budget is 500 characters, do not also spend roughly 50
of them on an inline blog URL. `pinterest_link` carries the destination and is
what Pinterest actually follows.

---

## Upload-Post returns background jobs, not synchronous results

Every photo and video call in this run exceeded the ~59s synchronous window and
was handed to the upload worker, returning `request_id` with no per-platform
result. This is normal, not a failure. Poll
`GET /api/uploadposts/status?request_id={id}` and read `results[0].post_url`.
Do not treat a missing `results` block in the initial response as an error.
