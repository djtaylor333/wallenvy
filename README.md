# Wall Envy Website

Modern static website for [Wall Envy](https://www.wallenvy.com.au) — Any Design. Any Surface. Print the Impossible.

## Local Development

Serve locally with Python (root-relative paths require a local server):
`bash
python -m http.server 8000
`
Then open http://localhost:8000

## Rebuild Pages

All pages are generated from scripts/build-pages.py. After editing the template or page content:
`bash
python scripts/build-pages.py
`

## Add New Assets

Run python scripts/download-assets.py to re-download images from the source site.

Place additional images in ssets/images/ and videos in ssets/videos/.

## YouTube Integration

On the Projects page, find the commented-out <section id="videos"> block.
Uncomment it and replace YOUR_PLAYLIST_ID_HERE with your YouTube playlist ID.

## GitHub Pages

1. Push to main branch
2. In repo Settings → Pages → Source: Deploy from branch main / / (root)
3. Once DNS is pointed: add CNAME record pointing to djtaylor333.github.io

## Domain Setup (wallenvy.com.au)

In your DNS provider, add:
- Type: CNAME
- Name: www
- Value: djtaylor333.github.io
- Type: A records for apex domain pointing to GitHub Pages IPs:
  185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
