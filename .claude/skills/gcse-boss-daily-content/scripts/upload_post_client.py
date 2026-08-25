#!/usr/bin/env python3
"""Upload-Post client for GCSE Boss. Publishes ONLY on explicit instruction.

Standing Rule 1 (post-identity lock) is enforced in code here:
Facebook and LinkedIn refuse to post without their page IDs, because without
them the API would default to Ben's personal feed. Never remove those guards.

Standing decision 24 Aug 2026: never set is_ai_generated / made_with_ai.
See DECISIONS.md adjacent to this scripts/ folder.
"""
import json, mimetypes, os, ssl, time, urllib.request, urllib.error, uuid
from pathlib import Path

API = "https://api.upload-post.com"
PHOTO_EP, VIDEO_EP = "/api/upload_photos", "/api/upload"
BANNED_IDENTITIES = {"ben norman", "benjamin norman"}


def load_env(p="/sessions/serene-funny-hawking/mnt/GCSEBoss/.env"):
    for line in Path(p).read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def _multipart(fields, files):
    """fields: list of (name, value). files: list of (name, path)."""
    b = f"----gcseboss{uuid.uuid4().hex}"
    out = bytearray()
    for k, v in fields:
        out += f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    for k, p in files:
        p = Path(p)
        mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        out += (f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"; "
                f"filename=\"{p.name}\"\r\nContent-Type: {mime}\r\n\r\n").encode()
        out += p.read_bytes() + b"\r\n"
    out += f"--{b}--\r\n".encode()
    return bytes(out), f"multipart/form-data; boundary={b}"


def _post(endpoint, fields, files, key, timeout=300):
    body, ctype = _multipart(fields, files)
    req = urllib.request.Request(API + endpoint, data=body, method="POST",
        headers={"Authorization": f"Apikey {key}", "Content-Type": ctype,
                 "Idempotency-Key": f"gcseboss-{uuid.uuid4().hex[:16]}"})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=timeout).read())
    except urllib.error.HTTPError as e:
        return {"success": False, "_http": e.code, "_body": e.read().decode()[:600]}


def status(request_id, key):
    req = urllib.request.Request(
        f"{API}/api/uploadposts/status?request_id={request_id}",
        headers={"Authorization": f"Apikey {key}"})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=60).read())
    except urllib.error.HTTPError as e:
        return {"success": False, "_http": e.code, "_body": e.read().decode()[:400]}


def guard(platform, fields):
    """Standing Rule 1. Raise rather than post to a personal identity."""
    d = dict(fields)
    if d.get("user", "").strip().lower() in BANNED_IDENTITIES:
        raise RuntimeError(f"{platform}: refusing, profile resolves to a personal identity")
    if platform == "facebook" and not d.get("facebook_page_id"):
        raise RuntimeError("facebook: refusing to post, would default to personal feed")
    if platform == "linkedin" and not d.get("target_linkedin_page_id"):
        raise RuntimeError("linkedin: refusing to post, would default to personal profile")
    if platform == "pinterest" and not d.get("pinterest_board_id"):
        raise RuntimeError("pinterest: refusing to post, no board id")


def post_photo(platform, image, caption, key, user, **extra):
    f = [("user", user), ("platform[]", platform), ("title", caption)]
    # Instagram: media_type must be ABSENT. Any explicit value is rejected
    # ("Unknown media type"). The server defaults to IMAGE. Do not add it.
    for k, v in extra.items():
        if v not in (None, ""):
            f.append((k, str(v)))
    guard(platform, f)
    return _post(PHOTO_EP, f, [("photos[]", image)], key)


def post_video(platform, video, caption, key, user, **extra):
    f = [("user", user), ("platform[]", platform), ("title", caption)]
    for k, v in extra.items():
        if v not in (None, ""):
            f.append((k, str(v)))
    guard(platform, f)
    return _post(VIDEO_EP, f, [("video", video)], key)
