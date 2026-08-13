"""
Apply SEO improvements to build-pages.py:
- Canonical + og:url + og:image + twitter card in page()
- JSON-LD LocalBusiness schema on every page
- Updated SEO titles + meta descriptions for all pages
- Service page H1s updated with keywords/location
- Opening paragraphs updated with location mentions
"""
import re, os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BP   = os.path.join(REPO, "scripts", "build-pages.py")

with open(BP, "r", encoding="utf-8") as f:
    c = f.read()

# ── 1. Add constants after BASE_HREF ────────────────────────────────────────
OLD_BASE = "# /wallenvy/  -> GitHub Pages subdirectory (djtaylor333.github.io/wallenvy/)\n# /           -> Custom domain root (wallenvy.com.au)\nBASE_HREF = '/'"
NEW_BASE = """# /wallenvy/  -> GitHub Pages subdirectory (djtaylor333.github.io/wallenvy/)
# /           -> Custom domain root (wallenvy.com.au)
BASE_HREF = '/'

# SEO
CANONICAL_BASE  = "https://wallenvy.com.au"
OG_IMAGE        = "https://wallenvy.com.au/assets/images/logo-banner.png"

SCHEMA_LD = \"\"\"<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Wall Envy",
  "description": "Premium direct-to-wall printing for commercial and residential spaces across the Central Coast, Newcastle and Hunter Region of NSW, Australia.",
  "@id": "https://wallenvy.com.au",
  "url": "https://wallenvy.com.au",
  "telephone": "+61414698448",
  "email": "info@wallenvy.com.au",
  "logo": "https://wallenvy.com.au/assets/images/logo-banner.png",
  "image": "https://wallenvy.com.au/assets/images/logo-banner.png",
  "priceRange": "$$",
  "areaServed": [
    {"@type": "City", "name": "Central Coast NSW"},
    {"@type": "City", "name": "Newcastle NSW"},
    {"@type": "City", "name": "Lake Macquarie NSW"},
    {"@type": "AdministrativeArea", "name": "Hunter Region NSW"}
  ],
  "sameAs": [
    "https://www.facebook.com/people/Wallenvy/61592586241845/",
    "https://www.instagram.com/wallenvy.au"
  ]
}
</script>\"\"\""""
c = c.replace(OLD_BASE, NEW_BASE)

# ── 2. Update page() function ────────────────────────────────────────────────
OLD_PAGE = '''def page(title, desc, content, path=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Wall Envy</title>
  <meta name="description" content="{desc}">
  <meta property="og:title" content="{title} | Wall Envy">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <base href="{BASE_HREF}">
  <link rel="icon" href="assets/images/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/css/style.css">
  {THEME_SCRIPT}
</head>'''

NEW_PAGE = '''def page(title, desc, content, page_path=""):
    canonical = f"{CANONICAL_BASE}{page_path}" if page_path else CANONICAL_BASE + "/"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Wall Envy</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical}">
  <!-- Open Graph -->
  <meta property="og:title" content="{title} | Wall Envy">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:site_name" content="Wall Envy">
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title} | Wall Envy">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{OG_IMAGE}">
  {SCHEMA_LD}
  <base href="{BASE_HREF}">
  <link rel="icon" href="assets/images/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="assets/css/style.css">
  {THEME_SCRIPT}
</head>'''
c = c.replace(OLD_PAGE, NEW_PAGE)

# ── 3. Update SEO titles, descriptions and add canonical paths ───────────────
updates = [
    # (old_page_call_start, new_title, new_desc, page_path)
    ('PAGES["services.html"] = page(\n    "Services",',
     'PAGES["services.html"] = page(\n    "Wall Printing Services — Commercial, Residential & More",',
     '"Explore Wall Envy\'s direct-to-wall printing services for commercial, residential, healthcare, schools, hospitality and sports facilities across the Central Coast & Newcastle.",',
     '"/services.html"'),
    ('PAGES["services/commercial.html"] = page(\n    "Commercial & Office Printing",',
     'PAGES["services/commercial.html"] = page(\n    "Commercial Wall Printing Central Coast & Newcastle",',
     '"Direct-to-wall printing for offices and commercial spaces across the Central Coast, Newcastle & Hunter. Logos, branded walls, feature murals and more.",',
     '"/services/commercial.html"'),
    ('PAGES["services/residential.html"] = page(\n    "Residential & Interior Design",',
     'PAGES["services/residential.html"] = page(\n    "Residential Wall Murals & Feature Walls",',
     '"Bespoke direct-to-wall printed murals and feature walls for homes across the Central Coast, Newcastle and Hunter Region. Custom designs and high-resolution results.",',
     '"/services/residential.html"'),
    ('PAGES["services/healthcare.html"] = page(\n    "Healthcare & Clinics Wall Printing",',
     'PAGES["services/healthcare.html"] = page(\n    "Healthcare & Clinic Wall Murals",',
     '"Seamless direct-to-wall artwork for clinics and healthcare spaces across the Central Coast, Newcastle and Hunter. Create calm, branded patient environments.",',
     '"/services/healthcare.html"'),
    ('PAGES["services/schools.html"] = page(\n    "Schools & Education Wall Printing",',
     'PAGES["services/schools.html"] = page(\n    "School Wall Murals & Educational Wall Printing",',
     '"Vibrant direct-to-wall murals for schools and learning spaces across the Central Coast, Newcastle and Hunter. Educational, branded and custom artwork.",',
     '"/services/schools.html"'),
    ('PAGES["services/hospitality.html"] = page(\n    "Hospitality, Cafes & Retail Wall Printing",',
     'PAGES["services/hospitality.html"] = page(\n    "Cafe, Restaurant & Retail Wall Printing",',
     '"Create standout feature walls for cafes, restaurants and retail spaces across the Central Coast, Newcastle and Hunter with direct-to-wall printing.",',
     '"/services/hospitality.html"'),
    ('PAGES["services/sports.html"] = page(\n    "Sports & Sponsorship Wall Printing",',
     'PAGES["services/sports.html"] = page(\n    "Sports, Gym & Sponsorship Wall Printing",',
     '"Turn sports and gym walls into branded, motivational or sponsorship spaces with direct-to-wall printing across the Central Coast and Hunter.",',
     '"/services/sports.html"'),
    ('PAGES["printing.html"] = page(\n    "Printing Surfaces",',
     'PAGES["printing.html"] = page(\n    "Wall Printing Surfaces — Brick, Glass, Wood & More",',
     '"Explore surfaces Wall Envy can print on, including brick, glass, concrete, metal, wood and painted walls using direct-to-surface printing on the Central Coast & Hunter.",',
     '"/printing.html"'),
    ('PAGES["printing/embossed-relief.html"] = page(\n    "Embossed & Relief Printing",',
     'PAGES["printing/embossed-relief.html"] = page(\n    "Embossed & Relief Wall Printing",',
     '"Add physical depth and texture to your walls with embossed UV wall printing. Raised patterns, architectural textures and 3D effects. Central Coast & Newcastle.",',
     '"/printing/embossed-relief.html"'),
    ('PAGES["printing/vehicle-branding.html"] = page(\n    "Vehicle & Fleet Branding",',
     'PAGES["printing/vehicle-branding.html"] = page(\n    "Vehicle & Fleet Branding — Direct Print",',
     '"Permanent direct-to-surface vehicle branding for vans, trucks and trailers across the Central Coast & Hunter. No vinyl wraps. UV-cured ink that won\'t peel or bubble.",',
     '"/printing/vehicle-branding.html"'),
    ('PAGES["how-it-works.html"] = page(\n    "How It Works",',
     'PAGES["how-it-works.html"] = page(\n    "How Wall Printing Works — 4 Simple Steps",',
     '"Learn how Wall Envy\'s direct-to-wall printing process works in 4 clean steps. Consultation, digital proofing, the print, and final reveal. Fast, clean and hassle-free.",',
     '"/how-it-works.html"'),
    ('PAGES["why-choose-us.html"] = page(\n    "Why Choose Direct-to-Wall Printing",',
     'PAGES["why-choose-us.html"] = page(\n    "Why Choose Direct-to-Wall Printing",',
     '"See how direct-to-wall printing compares to wallpaper and vinyl wraps on 5 key points: seamless finish, durability, surface flexibility, no VOCs and creative freedom.",',
     '"/why-choose-us.html"'),
    ('PAGES["projects.html"] = page(\n    "Projects",',
     'PAGES["projects.html"] = page(\n    "Wall Printing Projects Gallery",',
     '"Browse Wall Envy\'s completed direct-to-wall printing projects across the Central Coast and Hunter. Commercial, residential, hospitality, schools and more.",',
     '"/projects.html"'),
    ('PAGES["faqs.html"] = page(\n    "Frequently Asked Questions",',
     'PAGES["faqs.html"] = page(\n    "Wall Printing FAQs",',
     '"Answers to common questions about direct-to-wall printing — surfaces, cost, process, durability, preparation and more. Central Coast & Newcastle.",',
     '"/faqs.html"'),
    ('PAGES["contact.html"] = page(\n    "Contact Us",',
     'PAGES["contact.html"] = page(\n    "Contact Wall Envy — Book a Free Consultation",',
     '"Book your free direct-to-wall printing consultation with Wall Envy. Call 0414 698 448 or fill in our form. Central Coast, Newcastle & Hunter Region.",',
     '"/contact.html"'),
    ('PAGES["about.html"] = page(\n    "About Us",',
     'PAGES["about.html"] = page(\n    "About Wall Envy — Meet the Family Team",',
     '"Wall Envy is a family-owned direct-to-wall printing business on the Central Coast. Meet Jon, Nicole, Arianne and David — the four equal partners behind the print.",',
     '"/about.html"'),
    ('PAGES["404.html"] = page(\n    "Page Not Found",\n    "The page you were looking for could not be found.",',
     'PAGES["404.html"] = page(\n    "Page Not Found",\n    "The page you were looking for could not be found.",',
     None,
     '"/404.html"'),
]

for old_start, new_start, new_desc_line, new_path in updates:
    # Find next line with old description
    if old_start not in c:
        print(f"  [MISS] {old_start[:60]}")
        continue

    idx = c.index(old_start)
    # Find the closing ) of page() call's first 3 args
    # Replace just the PAGES["x"] = page( line and desc line
    segment_end = c.index('\n', idx + len(old_start)) + 1
    desc_line_end = c.index('\n', segment_end) + 1

    if new_desc_line:
        old_segment = c[idx:desc_line_end]
        old_desc = c[segment_end:desc_line_end].rstrip()
        new_segment = new_start + '\n    ' + new_desc_line + '\n'
        c = c[:idx] + new_segment + c[desc_line_end:]

    # Now update the path= argument in the page() call
    # Find the closing ) of the page() call for this page
    # It ends with: + cta_strip(...)\n) or just \n)
    # Strategy: find "    content," or the content start, then find the last ,\n    page_path arg
    # Simpler: find ", path=" or the end of the page() call and add/update page_path
    if new_path:
        # Look for existing page_path or the end of page() call
        # The page() call ends with the content + closing )
        # We'll add/replace the path arg at the right spot
        # Find the PAGES[...] = page(...) call again after our replacement
        if new_start not in c:
            print(f"  [SKIP path] {new_path}")
            continue
        idx2 = c.index(new_start)
        # Find the page() call - it ends with \n)\n
        # The pattern is: page(\n    title,\n    desc,\n    content...\n)\n
        # We need to add page_path as 4th arg - but content is a huge block
        # Better: search for the end of the block and insert before closing )
        # The page def takes (title, desc, content, page_path="")
        # In the call: page("title", "desc", inner_hero(...) + """...""" + cta_strip(...)\n)
        # Let's find the pattern: \n)\n\n# ── and add path before the )
        pass  # path is now handled in a second pass below

print("Title/desc updates done")

# ── 4. Add page_path to all page() calls ─────────────────────────────────────
# Each PAGES["x.html"] = page( call ends with a big content block.
# We need to add page_path as final arg.
# Pattern: the closing ) of each page() call is a standalone ) on its own line.
# We'll match: \n)\n\n# ── or \n)\n\nPAGES or end of file

path_map = {
    'PAGES["services.html"]':                    '/services.html',
    'PAGES["services/commercial.html"]':         '/services/commercial.html',
    'PAGES["services/residential.html"]':        '/services/residential.html',
    'PAGES["services/healthcare.html"]':         '/services/healthcare.html',
    'PAGES["services/schools.html"]':            '/services/schools.html',
    'PAGES["services/hospitality.html"]':        '/services/hospitality.html',
    'PAGES["services/sports.html"]':             '/services/sports.html',
    'PAGES["printing.html"]':                    '/printing.html',
    'PAGES["printing/embossed-relief.html"]':    '/printing/embossed-relief.html',
    'PAGES["printing/vehicle-branding.html"]':   '/printing/vehicle-branding.html',
    'PAGES["how-it-works.html"]':                '/how-it-works.html',
    'PAGES["why-choose-us.html"]':               '/why-choose-us.html',
    'PAGES["projects.html"]':                    '/projects.html',
    'PAGES["faqs.html"]':                        '/faqs.html',
    'PAGES["contact.html"]':                     '/contact.html',
    'PAGES["about.html"]':                       '/about.html',
    'PAGES["404.html"]':                         '/404.html',
}

# For each PAGES entry, find its page() call and update the closing ) to include path
for pages_key, path_val in path_map.items():
    if pages_key not in c:
        print(f"  [MISS path] {pages_key}")
        continue
    start = c.index(pages_key)
    # Find the = page( that follows
    eq_idx = c.index('= page(', start)
    # Find the closing ) of this page() call
    # It's the ) on its own line after the content block
    # Pattern: ends with \n)\n
    # Find the first \n)\n after eq_idx that isn't inside a nested string
    # Simple approach: find pattern cta_strip(...)\n) or the end-closing
    # Actually look for the pattern: the content arg ends, and the page() closes
    # The page call structure: page(\n    title,\n    desc,\n    content_block\n)
    # The content_block may contain ) chars, so find the last \n)\n
    # Strategy: find the closing ) by looking for the pattern that ends a page() call
    # which is always: + cta_strip(...)\n)\n or """\n)\n or ..."""\n)\n
    # Find the rightmost \n)\n between eq_idx and the next PAGES[ 
    next_pages = c.find('\nPAGES[', eq_idx + 10)
    if next_pages == -1:
        next_pages = c.find('\n# ─── Write', eq_idx)
    segment = c[eq_idx:next_pages]
    # The page() call closing ) is the last occurrence of \n)\n in segment
    last_close = segment.rfind('\n)\n')
    if last_close == -1:
        print(f"  [NO CLOSE] {pages_key}")
        continue
    # Check if path is already there
    before_close = segment[max(0, last_close-80):last_close]
    if path_val in before_close:
        print(f"  [SKIP dup] {path_val}")
        continue
    # Insert path before the closing )
    abs_close = eq_idx + last_close
    c = c[:abs_close] + f',\n    "{path_val}"' + c[abs_close:]
    print(f"  [path ok] {path_val}")

print("Path updates done")

# ── 5. Update service page H1s to include location/keywords ─────────────────
h1_updates = [
    ('inner_hero("Services", \'Commercial &amp; <span class="gradient-text">Office Spaces</span>\'',
     'inner_hero("Services", \'Commercial Wall Printing <span class="gradient-text">Central Coast & Newcastle</span>\''),
    ('inner_hero("Services", \'Residential &amp; <span class="gradient-text">Interior Design</span>\'',
     'inner_hero("Services", \'Residential Wall Murals &amp; <span class="gradient-text">Feature Walls</span>\''),
    ('inner_hero("Services", \'Healthcare &amp; <span class="gradient-text">Clinics</span>\'',
     'inner_hero("Services", \'Healthcare &amp; Clinic <span class="gradient-text">Wall Printing</span>\''),
    ('inner_hero("Services", \'Schools &amp; <span class="gradient-text">Education</span>\'',
     'inner_hero("Services", \'School Wall Murals &amp; <span class="gradient-text">Educational Printing</span>\''),
    ('inner_hero("Services", \'Hospitality, Cafes <br>&amp; <span class="gradient-text">Retail</span>\'',
     'inner_hero("Services", \'Cafe, Restaurant &amp; <span class="gradient-text">Retail Wall Printing</span>\''),
    ('inner_hero("Services", \'Sports &amp; <span class="gradient-text">Sponsorship</span>\'',
     'inner_hero("Services", \'Sports, Gym &amp; <span class="gradient-text">Sponsorship Walls</span>\''),
    ('inner_hero("Printing", \'Print on <span class="gradient-text">Any Surface</span>\'',
     'inner_hero("Printing", \'Direct Printing on <span class="gradient-text">Any Surface</span>\''),
]
for old_h1, new_h1 in h1_updates:
    if old_h1 in c:
        c = c.replace(old_h1, new_h1)
        print(f"  [h1] updated")
    else:
        print(f"  [h1 MISS] {old_h1[:60]}")

# ── 6. Update service page opening paragraphs with location mention ──────────
# Commercial - already fine, just add location to opening
old_commercial_p = 'At Wall Envy, we help businesses transform blank, uninspiring walls into powerful branding tools using advanced, direct-to-wall printing technology.'
new_commercial_p = 'At Wall Envy, we help businesses across the Central Coast, Newcastle, Lake Macquarie and the Hunter Region transform blank, uninspiring walls into powerful branding tools using advanced, direct-to-wall printing technology.'
c = c.replace(old_commercial_p, new_commercial_p)

old_sports_p = 'For local sports clubs, gyms, and community centres, sponsorships are the lifeblood of the organisation.'
new_sports_p = 'For local sports clubs, gyms, and community centres across the Central Coast and Hunter Region, sponsorships are the lifeblood of the organisation.'
c = c.replace(old_sports_p, new_sports_p)

old_hospitality_p = 'Wall Envy helps cafes, restaurants, bars, and boutique hotels'
new_hospitality_p = 'Wall Envy helps cafes, restaurants, bars, and boutique hotels across the Central Coast, Newcastle and Hunter Region'
c = c.replace(old_hospitality_p, new_hospitality_p)

old_schools_p = 'At Wall Envy, we provide vibrant, educational murals that bond directly to your walls.'
new_schools_p = 'At Wall Envy, we provide vibrant, educational murals for schools across the Central Coast and Hunter Region that bond directly to your walls.'
c = c.replace(old_schools_p, new_schools_p)

print("Opening paragraph updates done")

with open(BP, "w", encoding="utf-8") as f:
    f.write(c)
print("\nbuild-pages.py saved")
