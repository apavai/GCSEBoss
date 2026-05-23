# GCSE Boss Website

Marketing site for [gcseboss.com](https://gcseboss.com).

## Adding blog posts

1. Create a new HTML file in `blog/posts/` (copy `welcome-to-gcse-boss.html` as a template — includes the App Store CTA banner).
2. Add a card to `blog/index.html` linking to the new post.
3. Link to the post using root-relative URLs (e.g. `/blog/posts/my-post-slug`) — do not use `.html` paths or `_redirects` rules.

Push to `main` — Cloudflare deploys automatically.

