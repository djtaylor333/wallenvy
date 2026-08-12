"""
Wall Envy - Static Site Builder
Generates all HTML pages from a base template + page content.
Run: python scripts/build-pages.py
Output: all pages are written to their respective paths in the repo root.
"""

import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# /wallenvy/  -> GitHub Pages subdirectory (djtaylor333.github.io/wallenvy/)
# /           -> Custom domain root (wallenvy.com.au)
BASE_HREF = '/'

# ─── Shared HTML Fragments ──────────────────────────────────────────────────

NAV = """
<nav class="site-nav" id="site-nav">
  <div class="container">
    <div class="nav-inner">
      <a href="./" class="nav-logo">WALL ENVY</a>
      <ul class="nav-links">
        <li><a href="./" class="nav-link" data-path="/">Home</a></li>
        <li>
          <a href="services.html" class="nav-link" data-path="/services">Services <span class="arrow">&#9660;</span></a>
          <div class="dropdown">
            <a href="services/commercial.html">Commercial &amp; Office</a>
            <a href="services/residential.html">Residential &amp; Interior</a>
            <a href="services/healthcare.html">Healthcare &amp; Clinics</a>
            <a href="services/schools.html">Schools &amp; Education</a>
            <a href="services/hospitality.html">Hospitality, Cafes &amp; Retail</a>
            <a href="services/sports.html">Sports &amp; Sponsorship</a>
          </div>
        </li>
        <li>
          <a href="printing.html" class="nav-link" data-path="/printing">Printing <span class="arrow">&#9660;</span></a>
          <div class="dropdown">
            <a href="printing.html">Print Surfaces</a>
            <a href="printing/embossed-relief.html">Embossed &amp; Relief</a>
            <a href="printing/vehicle-branding.html">Vehicle Branding</a>
          </div>
        </li>
        <li><a href="how-it-works.html" class="nav-link" data-path="/how-it-works">How It Works</a></li>
        <li><a href="why-choose-us.html" class="nav-link" data-path="/why-choose-us">Why Choose Us</a></li>
        <li><a href="projects.html" class="nav-link" data-path="/projects">Projects</a></li>
        <li><a href="faqs.html" class="nav-link" data-path="/faqs">FAQs</a></li>
        <li><a href="contact.html" class="nav-link" data-path="/contact" style="color:var(--cyan);font-weight:600;">Contact</a></li>
      </ul>
      <button class="theme-toggle" aria-label="Toggle theme">
        <span class="icon-sun">&#9728;&#65039;</span>
        <span class="icon-moon">&#127769;</span>
      </button>
      <button class="burger" id="nav-burger" aria-label="Open menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</nav>
<div class="mobile-menu" id="mobile-menu">
  <a href="/">Home</a>
  <div class="mobile-section-label">Services</div>
  <a href="services.html">All Services</a>
  <a href="services/commercial.html" style="padding-left:1.75rem">Commercial &amp; Office</a>
  <a href="services/residential.html" style="padding-left:1.75rem">Residential &amp; Interior</a>
  <a href="services/healthcare.html" style="padding-left:1.75rem">Healthcare &amp; Clinics</a>
  <a href="services/schools.html" style="padding-left:1.75rem">Schools &amp; Education</a>
  <a href="services/hospitality.html" style="padding-left:1.75rem">Hospitality, Cafes &amp; Retail</a>
  <a href="services/sports.html" style="padding-left:1.75rem">Sports &amp; Sponsorship</a>
  <hr>
  <div class="mobile-section-label">Printing</div>
  <a href="printing.html">Print Surfaces</a>
  <a href="printing/embossed-relief.html" style="padding-left:1.75rem">Embossed &amp; Relief</a>
  <a href="printing/vehicle-branding.html" style="padding-left:1.75rem">Vehicle Branding</a>
  <hr>
  <a href="how-it-works.html">How It Works</a>
  <a href="why-choose-us.html">Why Choose Us</a>
  <a href="projects.html">Projects</a>
  <a href="faqs.html">FAQs</a>
  <a href="contact.html" style="color:var(--cyan);font-weight:700;">Contact Us</a>
</div>
"""

FOOTER = """
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="./" class="footer-logo">WALL ENVY</a>
        <p>Any Design. Any Surface. Print the Impossible.<br>
           Serving the Central Coast &amp; Hunter regions of NSW, Australia.</p>
        <div class="footer-social">
          <a href="https://www.facebook.com/people/Wallenvy/61592586241845/" target="_blank" rel="noopener" aria-label="Facebook">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
          </a>
          <a href="https://www.instagram.com/wallenvy.au" target="_blank" rel="noopener" aria-label="Instagram">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
          </a>
        </div>
      </div>
      <div class="footer-col">
        <h5>Services</h5>
        <ul>
          <li><a href="services/commercial.html">Commercial &amp; Office</a></li>
          <li><a href="services/residential.html">Residential</a></li>
          <li><a href="services/healthcare.html">Healthcare</a></li>
          <li><a href="services/schools.html">Schools &amp; Education</a></li>
          <li><a href="services/hospitality.html">Hospitality &amp; Retail</a></li>
          <li><a href="services/sports.html">Sports &amp; Sponsorship</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h5>Printing</h5>
        <ul>
          <li><a href="printing.html">Print Surfaces</a></li>
          <li><a href="printing/embossed-relief.html">Embossed &amp; Relief</a></li>
          <li><a href="printing/vehicle-branding.html">Vehicle Branding</a></li>
          <li><a href="how-it-works.html">How It Works</a></li>
          <li><a href="why-choose-us.html">Why Choose Us</a></li>
          <li><a href="projects.html">Projects</a></li>
        </ul>
      </div>
      <div class="footer-col footer-contact">
        <h5>Get In Touch</h5>
        <p>&#128222; <a href="tel:0414698448" style="color:inherit;">0414 698 448</a></p>
        <p>&#9993;&#65039; <a href="mailto:info@wallenvy.com.au" style="color:inherit;">info@wallenvy.com.au</a></p>
        <p>&#128205; Central Coast &amp; Hunter, NSW</p>
        <a href="contact.html" class="btn btn-primary btn-sm" style="margin-top:1rem;display:inline-flex;">Get Free Quote</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 Wall Envy Aus. All Rights Reserved.</span>
      <span><a href="faqs.html" style="color:inherit;">FAQs</a> &nbsp;&middot;&nbsp; <a href="contact.html" style="color:inherit;">Contact</a></span>
    </div>
  </div>
</footer>

<div class="cookie-banner" id="cookie-banner" role="dialog" aria-label="Cookie preferences">
  <p>&#127850; We use cookies to enhance your experience and enable social media features. By continuing, you agree to their use.</p>
  <div class="cookie-actions">
    <button class="btn btn-primary cookie-accept" id="cookie-accept">Accept All</button>
    <button class="btn btn-ghost cookie-decline" id="cookie-decline">Decline</button>
  </div>
</div>
"""

THEME_SCRIPT = """<script>(function(){var t=localStorage.getItem('wallenvy_theme');if(!t)t=window.matchMedia('(prefers-color-scheme:light)').matches?'light':'dark';document.documentElement.setAttribute('data-theme',t);})();</script>"""

def page(title, desc, content, path=""):
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
</head>
<body>
{NAV}
{content}
{FOOTER}
<script src="assets/js/main.js"></script>
</body>
</html>"""

# ─── Shared "Print the Impossible" CTA used on all service/printing pages ──

def cta_strip(kicker="Ready to Get Started?", headline="Print the Impossible", sub="", cta_label="Book Free Consultation", cta_link="/contact.html"):
    sub_html = f"<p>{sub}</p>" if sub else "<p>Whether you have a finished design ready to print or just a rough idea, we&#8217;re here to help. Book your free consultation and site measure today.</p>"
    return f"""
<section class="cta-strip">
  <img src="/assets/images/cta-banner.jpg" alt="" class="cta-bg-img" aria-hidden="true">
  <div class="container inner">
    <span class="cta-kicker">{kicker}</span>
    <h2>{headline}</h2>
    {sub_html}
    <div class="cta-btns">
      <a href="{cta_link}" class="btn btn-primary btn-lg">{cta_label}</a>
      <a href="projects.html" class="btn btn-outline btn-lg">See Our Work</a>
    </div>
  </div>
</section>"""

def inner_hero(label, h1, desc):
    return f"""
<section class="hero-inner-page page-content">
  <div class="container">
    <div class="page-hero-label reveal">{label}</div>
    <h1 class="reveal reveal-delay-1">{h1}</h1>
    <p class="hero-desc reveal reveal-delay-2">{desc}</p>
  </div>
</section>"""

# ─── Page definitions ────────────────────────────────────────────────────────

PAGES = {}

# ── services.html ──────────────────────────────────────────────────────────

PAGES["services.html"] = page(
    "Services",
    "We provide direct-to-wall printing for commercial offices, residential homes, healthcare clinics, schools, hospitality venues, and sports facilities across the Central Coast & Hunter regions.",
    inner_hero("What We Offer", 'Our <span class="gradient-text">Services</span>', "We print on any surface for any industry. Explore what we can do for your space.") + """
<section class="section page-content" style="padding-top:3rem;">
  <div class="container">
    <p class="reveal" style="max-width:720px;margin-bottom:3rem;">We provide printing services on a variety of surfaces to a variety of businesses. We aren't limited to commercial — we can do residential, small businesses, hospitals, restaurants, schools, stadiums — anywhere you can think of. Or if you need a custom design, we can work with you on something that perfectly suits your space.</p>
    <div class="services-grid">
      <a href="services/commercial.html" class="service-card reveal">
        <div class="service-icon">&#127970;</div>
        <h3>Commercial &amp; Office Spaces</h3>
        <p>German-engineered UV printing that transforms reception walls, boardrooms, and retail spaces with powerful, permanent brand imagery.</p>
        <span class="service-card-link">Learn more &#8594;</span>
      </a>
      <a href="services/residential.html" class="service-card reveal reveal-delay-1">
        <div class="service-icon">&#127968;</div>
        <h3>Residential &amp; Interior Design</h3>
        <p>Bespoke architectural finishes for your home. Backed by carpentry expertise and interior design know-how for a flawless result.</p>
        <span class="service-card-link">Learn more &#8594;</span>
      </a>
      <a href="services/healthcare.html" class="service-card reveal reveal-delay-2">
        <div class="service-icon">&#127973;</div>
        <h3>Healthcare &amp; Clinics</h3>
        <p>Seamless, hygienic, low-VOC wall art that calms patients and elevates your practice without compromising clinical standards.</p>
        <span class="service-card-link">Learn more &#8594;</span>
      </a>
      <a href="services/schools.html" class="service-card reveal">
        <div class="service-icon">&#127891;</div>
        <h3>Schools &amp; Education</h3>
        <p>Pick-proof, 100% child-safe murals that inspire learning — durable enough for classrooms and safe enough for nurseries.</p>
        <span class="service-card-link">Learn more &#8594;</span>
      </a>
      <a href="services/hospitality.html" class="service-card reveal reveal-delay-1">
        <div class="service-icon">&#9749;</div>
        <h3>Hospitality, Cafes &amp; Retail</h3>
        <p>Create Instagram-worthy walls that drive organic word-of-mouth. Zero downtime — trade again the very next day.</p>
        <span class="service-card-link">Learn more &#8594;</span>
      </a>
      <a href="services/sports.html" class="service-card reveal reveal-delay-2">
        <div class="service-icon">&#127942;</div>
        <h3>Sports &amp; Sponsorship</h3>
        <p>The Direct-to-Wall Sponsorship Model — premium, permanent sponsor placements that generate ongoing revenue for your club.</p>
        <span class="service-card-link">Learn more &#8594;</span>
      </a>
    </div>
  </div>
</section>""" + cta_strip()
)

# ── services/commercial.html ───────────────────────────────────────────────

PAGES["services/commercial.html"] = page(
    "Commercial & Office Printing",
    "Transform your office or retail space with permanent, UV-cured direct-to-wall branding. High-impact corporate murals, logos, and signage on any surface.",
    inner_hero("Services", 'Commercial &amp; <span class="gradient-text">Office Spaces</span>', "Branding that means business — from boardroom backdrops to retail feature walls.") + """
<section class="section page-content" style="padding-top:3rem;">
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:start;">
      <div>
        <p class="reveal" style="font-size:1.05rem;margin-bottom:2rem;">First impressions matter. When a client walks into your office, your environment speaks volumes about your brand's professionalism, culture, and success. At Wall Envy, we help businesses transform blank, uninspiring walls into powerful branding tools using advanced, German-engineered direct-to-wall printing technology.</p>
        <div class="feature-list">
          <div class="feature-item reveal">
            <div class="feature-icon">&#127775;</div>
            <div><h4>High-Impact Corporate Branding</h4><p>Razor-sharp logos, mission statements, and brand imagery — in brand-accurate colours, directly on your wall.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-1">
            <div class="feature-icon">&#128170;</div>
            <div><h4>Ultimate Durability</h4><p>Hard-coat UV ink is scratch-resistant, water-resistant, and easy to clean — built for high-traffic commercial areas.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-2">
            <div class="feature-icon">&#9889;</div>
            <div><h4>Zero Disruption</h4><p>Eco-friendly, low-VOC inks mean we can print after hours. Your staff returns to a transformed workspace the next morning.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-3">
            <div class="feature-icon">&#127959;</div>
            <div><h4>Any Surface</h4><p>Plasterboard, raw brick, glass, concrete, metal panels — our technology adapts flawlessly to any commercial surface.</p></div>
          </div>
        </div>
      </div>
      <div class="reveal reveal-delay-2">
        <img src="/assets/images/projects/proj-06.jpg" alt="Commercial wall printing project" style="width:100%;border-radius:var(--card-r);box-shadow:var(--sh-lg);">
      </div>
    </div>
    <div style="margin-top:3rem;">
      <h3 class="reveal" style="margin-bottom:1.25rem;">Perfect For</h3>
      <div class="perfect-for-grid">
        <div class="perfect-for-item reveal"><div class="pf-dot"></div><p>Corporate Offices &amp; Boardrooms — impressive reception backdrops and mission statement walls</p></div>
        <div class="perfect-for-item reveal reveal-delay-1"><div class="pf-dot"></div><p>Retail Stores &amp; Showrooms — eye-catching seasonal displays and permanent brand imagery</p></div>
        <div class="perfect-for-item reveal reveal-delay-2"><div class="pf-dot"></div><p>Gyms &amp; Fitness Centres — highly durable, motivating graphics that won't peel in humid environments</p></div>
        <div class="perfect-for-item reveal reveal-delay-3"><div class="pf-dot"></div><p>Wayfinding &amp; Directional Signage — permanent, scuff-proof signage for buildings and warehouses</p></div>
      </div>
    </div>
  </div>
</section>""" + cta_strip("Ready to Upgrade Your Workspace?", "Print the <span class='gradient-text'>Impossible</span>", "Your business is unique, and your workspace should reflect that. From subtle, elegant designs to bold, floor-to-ceiling statements — let's discuss your brand's vision.", "Book Free Commercial Consultation")
)

# ── services/residential.html ──────────────────────────────────────────────

PAGES["services/residential.html"] = page(
    "Residential & Interior Design",
    "Bespoke direct-to-wall printing for homes. Custom murals, feature walls, and architectural finishes. Safe for nurseries, durable outdoors, and beautiful everywhere.",
    inner_hero("Services", 'Residential &amp; <span class="gradient-text">Interior Design</span>', "Bespoke architectural finishes that transform your home into a personal masterpiece.") + """
<section class="section page-content" style="padding-top:3rem;">
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:start;">
      <div>
        <p class="reveal" style="font-size:1.05rem;margin-bottom:2rem;">Your home is your ultimate sanctuary. For decades, homeowners have been limited to standard paint colours, repetitive wallpapers, or expensive hand-painted art. Wall Envy is changing residential design — delivering premium, direct-to-wall printing that creates breathtaking, bespoke features you simply can't get anywhere else.</p>
        <div class="feature-list">
          <div class="feature-item reveal">
            <div class="feature-icon">&#127775;</div>
            <div><h4>Flawless Preparation</h4><p>Backed by years of professional carpentry experience, we ensure walls are perfectly prepared and primed before a drop of ink is applied.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-1">
            <div class="feature-icon">&#127775;</div>
            <div><h4>Curated Interior Design</h4><p>Nicole's background in interior styling means we don't just execute your vision — we can help you curate the perfect design for your space.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-2">
            <div class="feature-icon">&#128164;</div>
            <div><h4>No Peeling, No Seams</h4><p>Our UV ink bonds directly to the surface, creating a seamless, permanent finish that looks like it's part of the architecture itself.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-3">
            <div class="feature-icon">&#127807;</div>
            <div><h4>Safe for Your Family</h4><p>Eco-friendly, non-toxic, low-VOC inks cure instantly. 100% safe for nurseries, bedrooms, and living areas the moment we finish printing.</p></div>
          </div>
        </div>
      </div>
      <div class="reveal reveal-delay-2">
        <img src="/assets/images/projects/proj-09.jpg" alt="Residential wall printing" style="width:100%;border-radius:var(--card-r);box-shadow:var(--sh-lg);">
      </div>
    </div>
    <div style="margin-top:3rem;">
      <h3 class="reveal" style="margin-bottom:1.25rem;">Perfect For</h3>
      <div class="perfect-for-grid">
        <div class="perfect-for-item reveal"><div class="pf-dot"></div><p>Luxury Living Spaces — breathtaking feature walls, custom staircase backdrops, home theatre designs</p></div>
        <div class="perfect-for-item reveal reveal-delay-1"><div class="pf-dot"></div><p>Nurseries &amp; Children&#8217;s Rooms — beautiful, scratch-resistant murals safe for the whole family</p></div>
        <div class="perfect-for-item reveal reveal-delay-2"><div class="pf-dot"></div><p>Alfresco &amp; Outdoor Entertaining — direct print onto exterior brick, rendered concrete, and stone</p></div>
        <div class="perfect-for-item reveal reveal-delay-3"><div class="pf-dot"></div><p>Bathrooms &amp; Kitchens — glass splashbacks, tiles, and moisture-rich environments</p></div>
      </div>
    </div>
    <div class="highlight-box reveal" style="margin-top:2.5rem;">
      <h4 style="margin-bottom:0.5rem;">Partnering with Interior Designers &amp; Architects</h4>
      <p style="margin:0;">We collaborate directly with interior designers, architects, and custom home builders across the Central Coast and Hunter regions. Wall Envy provides a unique, cutting-edge tool to offer your clients — large-scale custom imagery and textures without the limitations of traditional materials.</p>
    </div>
  </div>
</section>""" + cta_strip("Transform Your Home Today", "Print the <span class='gradient-text'>Impossible</span>", "Your home deserves better than off-the-shelf decor. Let's create a bespoke finish that is exclusively yours.", "Book Residential Design Consultation")
)

# ── services/healthcare.html ───────────────────────────────────────────────

PAGES["services/healthcare.html"] = page(
    "Healthcare & Clinics Wall Printing",
    "Hygienic, seamless, low-VOC wall art for medical centres, dental clinics, pediatric wards, and aged care facilities. Safe for patients immediately after printing.",
    inner_hero("Services", 'Healthcare &amp; <span class="gradient-text">Clinics</span>', "Hygienic, calming environments that improve patient experience without compromising clinical standards.") + """
<section class="section page-content" style="padding-top:3rem;">
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:start;">
      <div>
        <p class="reveal" style="font-size:1.05rem;margin-bottom:2rem;">In healthcare, interior design goes far beyond aesthetics. The environment you create directly impacts patient anxiety, perceived professionalism, and clinical hygiene. Wall Envy provides the ultimate solution — stunning, calming, and highly professional murals directly on your clinic's walls. No peeling seams, no trapped bacteria, no lingering chemical odours.</p>
        <div class="feature-list">
          <div class="feature-item reveal">
            <div class="feature-icon">&#129529;</div>
            <div><h4>100% Seamless &amp; Hygienic</h4><p>No wallpaper seams, no vinyl edges — our UV ink creates a flat, non-porous surface that leaves nowhere for pathogens to hide.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-1">
            <div class="feature-icon">&#128170;</div>
            <div><h4>Medical-Grade Durability</h4><p>Our hard-coat UV finish withstands aggressive daily wipe-downs and sanitisation protocols without fading or degrading.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-2">
            <div class="feature-icon">&#127807;</div>
            <div><h4>Safe, Low-VOC &amp; Odourless</h4><p>German-engineered eco-inks, non-toxic and odourless. Zero off-gassing — patients can be treated safely the very next day.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-3">
            <div class="feature-icon">&#128149;</div>
            <div><h4>Transform Patient Anxiety</h4><p>A beautifully printed nature scene or calming geometric pattern dramatically improves patient experience and reduces clinical anxiety.</p></div>
          </div>
        </div>
      </div>
      <div class="reveal reveal-delay-2">
        <img src="/assets/images/projects/proj-15.jpg" alt="Healthcare wall printing" style="width:100%;border-radius:var(--card-r);box-shadow:var(--sh-lg);">
      </div>
    </div>
    <div style="margin-top:3rem;">
      <h3 class="reveal" style="margin-bottom:1.25rem;">Perfect For</h3>
      <div class="perfect-for-grid">
        <div class="perfect-for-item reveal"><div class="pf-dot"></div><p>Dental Clinics — calming ceiling murals above treatment chairs, professional reception branding</p></div>
        <div class="perfect-for-item reveal reveal-delay-1"><div class="pf-dot"></div><p>Medical Centres &amp; Allied Health — welcoming waiting room graphics and wayfinding signage</p></div>
        <div class="perfect-for-item reveal reveal-delay-2"><div class="pf-dot"></div><p>Paediatric Wards &amp; Kids&#8217; Clinics — vibrant, engaging murals that make doctor visits less intimidating</p></div>
        <div class="perfect-for-item reveal reveal-delay-3"><div class="pf-dot"></div><p>Hospitals &amp; Aged Care — high-durability finishes that withstand wheelchairs and medical carts</p></div>
      </div>
    </div>
  </div>
</section>""" + cta_strip("Upgrade Your Practice Environment", "Print the <span class='gradient-text'>Impossible</span>", "Elevate your clinic from a sterile room to a modern, welcoming practice without compromising your rigorous health standards. We print on plaster, glass partitions, doors, and brick.", "Book Clinical Site Consultation")
)

# ── services/schools.html ─────────────────────────────────────────────────

PAGES["services/schools.html"] = page(
    "Schools & Education Wall Printing",
    "Pick-proof, 100% child-safe direct-to-wall murals for schools, preschools, and daycares. Inspiring, permanent artwork that won't peel, fade, or off-gas.",
    inner_hero("Services", 'Schools &amp; <span class="gradient-text">Education</span>', "Inspiring spaces that are built to last — because children deserve better than peeling vinyl.") + """
<section class="section page-content" style="padding-top:3rem;">
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:start;">
      <div>
        <p class="reveal" style="font-size:1.05rem;margin-bottom:2rem;">The physical environment of a school plays a massive role in how children learn, play, and feel. Blank, institutional walls don't inspire creativity — but traditional methods like vinyl decals rarely survive a classroom environment before curious hands peel them off. At Wall Envy, we provide vibrant, educational murals that bond directly to your walls. No peeling edges, no toxic fumes, no maintenance required.</p>
        <div class="feature-list">
          <div class="feature-item reveal">
            <div class="feature-icon">&#128170;</div>
            <div><h4>Pick-Proof &amp; Ultra-Durable</h4><p>Our UV ink bonds directly to the wall surface, leaving zero seams or edges to peel. It becomes a permanent, scratch-resistant part of the wall.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-1">
            <div class="feature-icon">&#127807;</div>
            <div><h4>100% Child-Safe &amp; Odourless</h4><p>Low-VOC, completely non-toxic inks cure instantly. We can print on a Sunday — completely safe and odourless for students on Monday morning.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-2">
            <div class="feature-icon">&#129531;</div>
            <div><h4>Hygienic &amp; Easy to Clean</h4><p>Our hard-coat finish is water-resistant and highly durable. Cleaning staff can wipe down and sanitise aggressively without fading the artwork.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-3">
            <div class="feature-icon">&#128218;</div>
            <div><h4>Transform Educational Outcomes</h4><p>Turn a corridor into a history timeline, print giant alphabet walls in preschools, or showcase school values and mascots larger-than-life.</p></div>
          </div>
        </div>
      </div>
      <div class="reveal reveal-delay-2">
        <img src="/assets/images/projects/proj-16.jpg" alt="School wall printing" style="width:100%;border-radius:var(--card-r);box-shadow:var(--sh-lg);">
      </div>
    </div>
    <div style="margin-top:3rem;">
      <h3 class="reveal" style="margin-bottom:1.25rem;">Perfect For</h3>
      <div class="perfect-for-grid">
        <div class="perfect-for-item reveal"><div class="pf-dot"></div><p>Preschools &amp; Daycares — engaging sensory walls, calming murals, interactive learning graphics</p></div>
        <div class="perfect-for-item reveal reveal-delay-1"><div class="pf-dot"></div><p>Primary &amp; High Schools — school crests, house mascots, inspirational quotes, durable wayfinding</p></div>
        <div class="perfect-for-item reveal reveal-delay-2"><div class="pf-dot"></div><p>School Libraries — immersive reading nooks and storybook murals that encourage literacy</p></div>
        <div class="perfect-for-item reveal reveal-delay-3"><div class="pf-dot"></div><p>Outdoor &amp; Undercover Areas — direct print onto exterior brick, concrete playgrounds, and sports halls</p></div>
      </div>
    </div>
  </div>
</section>""" + cta_strip("Inspire Your Students", "Print the <span class='gradient-text'>Impossible</span>", "Whether you want to brighten a single classroom or completely rebrand your school's outdoor quadrangle, Wall Envy delivers vibrant, permanent results.", "Book Free School Site Consultation")
)

# ── services/hospitality.html ─────────────────────────────────────────────

PAGES["services/hospitality.html"] = page(
    "Hospitality, Cafes & Retail Wall Printing",
    "Create Instagram-worthy feature walls for cafes, restaurants, bars, and retail spaces. Zero downtime, no seams, built to last in high-humidity venues.",
    inner_hero("Services", 'Hospitality, Cafes <br>&amp; <span class="gradient-text">Retail</span>', "Create spaces people want to photograph, share, and return to — over and over.") + """
<section class="section page-content" style="padding-top:3rem;">
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:start;">
      <div>
        <p class="reveal" style="font-size:1.05rem;margin-bottom:2rem;">In the hospitality industry, the ambiance of your venue is just as important as the food on the plate. Today's customers are looking for an experience — and a striking, unique environment is the fastest way to turn a first-time visitor into a loyal regular. Wall Envy helps cafes, restaurants, bars, and boutique hotels create stunning, large-scale feature walls that people want to photograph and share.</p>
        <div class="feature-list">
          <div class="feature-item reveal">
            <div class="feature-icon">&#128247;</div>
            <div><h4>The &#8220;Instagram&#8221; Factor</h4><p>A stunning, photogenic feature wall encourages patrons to take photos and tag your venue. Free, organic marketing driven by your interior design.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-1">
            <div class="feature-icon">&#128164;</div>
            <div><h4>Zero Seams, Zero Peeling</h4><p>Steam from coffee machines and kitchen heat cause traditional wallpaper to peel. Our UV ink bonds to the surface — a flawless, seam-free finish that lasts.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-2">
            <div class="feature-icon">&#9889;</div>
            <div><h4>Minimal Downtime</h4><p>Fast, efficient, and using low-VOC odourless inks — you can often trade the very next day without disrupting staff or customers.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-3">
            <div class="feature-icon">&#127759;</div>
            <div><h4>Backed by Carpentry Expertise</h4><p>We ensure your walls are perfectly prepped before a single drop of ink is applied, guaranteeing a high-end architectural finish.</p></div>
          </div>
        </div>
      </div>
      <div class="reveal reveal-delay-2">
        <img src="/assets/images/projects/proj-17.jpg" alt="Hospitality wall printing" style="width:100%;border-radius:var(--card-r);box-shadow:var(--sh-lg);">
      </div>
    </div>
    <div style="margin-top:3rem;">
      <h3 class="reveal" style="margin-bottom:1.25rem;">Perfect For</h3>
      <div class="perfect-for-grid">
        <div class="perfect-for-item reveal"><div class="pf-dot"></div><p>Cafes &amp; Coffee Shops — accent walls, menu board surrounds, or local community-focused art</p></div>
        <div class="perfect-for-item reveal reveal-delay-1"><div class="pf-dot"></div><p>Restaurants &amp; Bars — moody atmospheric graphics, brand logos, or immersive floor-to-ceiling designs</p></div>
        <div class="perfect-for-item reveal reveal-delay-2"><div class="pf-dot"></div><p>Boutique Hotels &amp; Airbnbs — unique room features that make your online listings stand out</p></div>
        <div class="perfect-for-item reveal reveal-delay-3"><div class="pf-dot"></div><p>Retail Spaces — bold branding, wayfinding, and seasonal promotional walls</p></div>
      </div>
    </div>
  </div>
</section>""" + cta_strip("Ready to Transform Your Venue?", "Print the <span class='gradient-text'>Impossible</span>", "From subtle elegant designs to bold floor-to-ceiling statements — let's discuss your venue's vision.", "Book Free Venue Consultation")
)

# ── services/sports.html ──────────────────────────────────────────────────

PAGES["services/sports.html"] = page(
    "Sports & Sponsorship Wall Printing",
    "The Direct-to-Wall Sponsorship Model — premium permanent sponsor placements that generate revenue for your club. Impact-resistant, UV-cured ink for sports facilities.",
    inner_hero("Services", 'Sports &amp; <span class="gradient-text">Sponsorship</span>', "Build your legacy — and your revenue — with the Direct-to-Wall Sponsorship Model.") + """
<section class="section page-content" style="padding-top:3rem;">
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:start;">
      <div>
        <p class="reveal" style="font-size:1.05rem;margin-bottom:2rem;">For local sports clubs, gyms, and community centres, sponsorships are the lifeblood of the organisation. But traditional sponsorship advertising — sagging vinyl banners and peeling stickers — makes your facility look cluttered and unprofessional. At Wall Envy, we offer the <strong>Direct-to-Wall Sponsorship Model</strong>: print your sponsors' logos directly onto your facility's walls, creating premium, permanent advertising real estate that sponsors are proud to pay for.</p>
        <div class="feature-list">
          <div class="feature-item reveal">
            <div class="feature-icon">&#128170;</div>
            <div><h4>Impact &amp; Scuff Resistant</h4><p>Our UV ink is cured with ultraviolet light, creating a hard-coat finish that resists basketballs, pickleballs, and gym bags — unlike vinyl that tears and dents.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-1">
            <div class="feature-icon">&#128167;</div>
            <div><h4>Sweat &amp; Humidity Proof</h4><p>Our ink bonds directly to the surface — impervious to peeling in high-humidity gyms, locker rooms, and aquatic centres where adhesives fail.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-2">
            <div class="feature-icon">&#127959;</div>
            <div><h4>Print on Raw Materials</h4><p>We don't need a perfectly smooth painted wall. Vibrant, high-definition branding directly onto raw cinderblock, brick, concrete, and corrugated metal.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-3">
            <div class="feature-icon">&#9940;</div>
            <div><h4>Zero Hanging Hazards</h4><p>Eliminate the safety risks and maintenance hassles of hanging large banners from high ceilings or fences — permanently.</p></div>
          </div>
        </div>
      </div>
      <div class="reveal reveal-delay-2">
        <img src="/assets/images/projects/proj-18.jpg" alt="Sports facility wall printing" style="width:100%;border-radius:var(--card-r);box-shadow:var(--sh-lg);">
        <div class="highlight-box" style="margin-top:1.5rem;">
          <h4 style="margin-bottom:0.5rem;">The Sponsorship Wall Revenue Generator</h4>
          <p style="margin:0;font-size:0.9rem;">We partner with facilities like indoor sports centres and community hubs to create dedicated &#8220;Sponsor Walls.&#8221; You sell premium, tiered logo placements — we print them permanently, creating a stunning architectural feature wall that generates <strong>continuous revenue</strong> for your club.</p>
        </div>
      </div>
    </div>
    <div style="margin-top:3rem;">
      <h3 class="reveal" style="margin-bottom:1.25rem;">Perfect For</h3>
      <div class="perfect-for-grid">
        <div class="perfect-for-item reveal"><div class="pf-dot"></div><p>Indoor Sports Stadiums &amp; Courts — team logos, sideline branding, and permanent sponsor placements</p></div>
        <div class="perfect-for-item reveal reveal-delay-1"><div class="pf-dot"></div><p>Gyms &amp; Fitness Centres — floor-to-ceiling motivational quotes and high-energy murals</p></div>
        <div class="perfect-for-item reveal reveal-delay-2"><div class="pf-dot"></div><p>Community Hubs &amp; Schools — Hall of Fame walls, donor recognition trees, durable wayfinding</p></div>
        <div class="perfect-for-item reveal reveal-delay-3"><div class="pf-dot"></div><p>Locker Rooms &amp; Clubhouses — immersive team branding that builds culture and intimidates the opposition</p></div>
      </div>
    </div>
  </div>
</section>""" + cta_strip("Maximise Your Wall Space", "Print the <span class='gradient-text'>Impossible</span>", "Stop settling for cheap banners. Upgrade your facility with permanent, impact-resistant graphics that reflect the pride of your club and the value of your sponsors.", "Book Free Facility Consultation")
)

# ── printing.html ─────────────────────────────────────────────────────────

PAGES["printing.html"] = page(
    "Printing Surfaces",
    "Direct-to-wall printing on any surface — walls, glass, metal, wood, tile, canvas, vehicles, and more. No Wall? No Problem. We print the impossible.",
    inner_hero("Printing", 'Print on <span class="gradient-text">Any Surface</span>', "We're called 'direct-to-wall' — but we're certainly not limited to walls.") + """
<section class="section page-content" style="padding-top:3rem;">
  <div class="container">
    <p class="reveal" style="font-size:1.05rem;max-width:720px;margin-bottom:3rem;">We can print on all kinds of surfaces — it doesn't have to be a blank white wall. We can print on glass, wood, canvas, metal, walls, and floors. If a surface is flat and vertical (or can be propped up vertically), there is a very good chance we can print stunning, high-definition art right onto it.</p>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:start;margin-bottom:3rem;">
      <div>
        <span class="section-label">No Wall? No Problem!</span>
        <h3 class="reveal" style="margin-bottom:1.25rem;">Think Outside the Wall</h3>
        <div class="feature-list">
          <div class="feature-item reveal">
            <div class="feature-icon">&#128682;</div>
            <div><h4>Doors &amp; Wardrobes</h4><p>Transform boring internal doors or flat-panel wardrobe doors into pieces of art, wood-grain illusions, or custom kids&#8217; room themes.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-1">
            <div class="feature-icon">&#128444;&#65039;</div>
            <div><h4>Custom Canvases</h4><p>Museum-quality art prints on large-scale stretched canvases that you can move whenever you like.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-2">
            <div class="feature-icon">&#127795;</div>
            <div><h4>Timber Panels &amp; Room Dividers</h4><p>Intricate, high-res designs on freestanding timber panels, acoustic boards, or room dividers for cafes and open-plan offices.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-3">
            <div class="feature-icon">&#127968;</div>
            <div><h4>Tiles &amp; Splashbacks</h4><p>Custom kitchen splashbacks or bathroom feature elements — UV-cured ink is highly water and scratch-resistant.</p></div>
          </div>
        </div>
      </div>
      <div class="reveal reveal-delay-2">
        <img src="/assets/images/projects/proj-19.jpg" alt="Surface printing examples" style="width:100%;border-radius:var(--card-r);box-shadow:var(--sh-lg);">
      </div>
    </div>
    <div class="services-grid">
      <a href="services/commercial.html" class="service-card reveal">
        <div class="service-icon">&#127970;</div>
        <h3>Commercial &amp; Office Spaces</h3>
        <p>Walls, glass partitions, reception counters, and more.</p>
        <span class="service-card-link">Learn more &#8594;</span>
      </a>
      <a href="printing/embossed-relief.html" class="service-card reveal reveal-delay-1">
        <div class="service-icon">&#9632;&#65039;</div>
        <h3>Embossed &amp; Relief Printing</h3>
        <p>True 3D tactile textures built up with layers of UV-curable ink. You can actually feel the design.</p>
        <span class="service-card-link">Learn more &#8594;</span>
      </a>
      <a href="printing/vehicle-branding.html" class="service-card reveal reveal-delay-2">
        <div class="service-icon">&#128663;</div>
        <h3>Vehicle Branding</h3>
        <p>Permanent, seamless branding directly onto vans, trucks, trailers — no vinyl, no peeling.</p>
        <span class="service-card-link">Learn more &#8594;</span>
      </a>
    </div>
  </div>
</section>""" + cta_strip("Have a Unique Surface?", "Print the <span class='gradient-text'>Impossible</span>", "From custom tabletops to giant event signage — if we can put it in front of the printer, we can bring your vision to life. Don't be afraid to ask!", "Book Free Surface Consultation")
)

# ── printing/embossed-relief.html ─────────────────────────────────────────

PAGES["printing/embossed-relief.html"] = page(
    "Embossed & Relief Printing",
    "True 3D tactile wall printing. We build up layers of UV-curable ink to create raised patterns, textures, and architectural features you can actually feel.",
    inner_hero("Printing", 'Embossed &amp; <span class="gradient-text">Relief Printing</span>', "Add physical depth and touch to your walls — a multi-sensory experience unlike anything else.") + """
<section class="section page-content" style="padding-top:3rem;">
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:start;">
      <div>
        <p class="reveal" style="font-size:1.05rem;margin-bottom:2rem;">Standard printing gives you colour and imagery. But what if you could actually <em>feel</em> the design? At Wall Envy, we push the boundaries of spatial design with advanced Embossed and Relief Wall Printing. By building up layers of UV-curable ink, we create striking, three-dimensional textures, raised patterns, and tactile architectural features directly onto your vertical surfaces. This isn't an optical illusion — it's a true dimensional finish.</p>
        <div class="feature-list">
          <div class="feature-item reveal">
            <div class="feature-icon">&#128400;</div>
            <div><h4>A Multi-Sensory Experience</h4><p>Interior design is no longer just visual. A tactile wall invites people to reach out, touch, and interact with the space — creating an unforgettable impression.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-1">
            <div class="feature-icon">&#127775;</div>
            <div><h4>Luxurious Architectural Textures</h4><p>Replicate the look and feel of hand-carved stone, raised Venetian plaster, or subtle geometric ribs — without the massive labour costs of traditional trades.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-2">
            <div class="feature-icon">&#128164;</div>
            <div><h4>Flawless Integration</h4><p>Just like our standard printing, relief effects are printed seamlessly onto the surface. No heavy panels to mount, no peeling layers, no structural compromises.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-3">
            <div class="feature-icon">&#127775;</div>
            <div><h4>Complete Customisation</h4><p>From subtle corporate logos that literally stand out from a boardroom wall to bold organic relief patterns in a luxury hotel foyer — any depth, any texture, any design.</p></div>
          </div>
        </div>
      </div>
      <div class="reveal reveal-delay-2">
        <img src="/assets/images/projects/proj-20.jpg" alt="Embossed wall printing" style="width:100%;border-radius:var(--card-r);box-shadow:var(--sh-lg);">
      </div>
    </div>
    <div style="margin-top:3rem;">
      <h3 class="reveal" style="margin-bottom:1.25rem;">Perfect For</h3>
      <div class="perfect-for-grid">
        <div class="perfect-for-item reveal"><div class="pf-dot"></div><p>Luxury Residential Feature Walls — tactile dimension behind a bedhead or in a grand entryway</p></div>
        <div class="perfect-for-item reveal reveal-delay-1"><div class="pf-dot"></div><p>High-End Corporate Offices — striking 3D company logos and dimensional brand elements</p></div>
        <div class="perfect-for-item reveal reveal-delay-2"><div class="pf-dot"></div><p>Boutique Hospitality &amp; Hotels — custom architectural depth that standard paint simply can't achieve</p></div>
        <div class="perfect-for-item reveal reveal-delay-3"><div class="pf-dot"></div><p>Retail Displays &amp; Showrooms — raised textures that catch the light and elevate perceived product value</p></div>
      </div>
    </div>
  </div>
</section>""" + cta_strip("Ready to Add Physical Depth?", "Print the <span class='gradient-text'>Impossible</span>", "Combine colour, imagery, and physical dimension into a single seamless application. Let's discuss your tactile design ideas.", "Book Free Design Consultation")
)

# ── printing/vehicle-branding.html ────────────────────────────────────────

PAGES["printing/vehicle-branding.html"] = page(
    "Vehicle & Fleet Branding",
    "Permanent, seamless vehicle branding printed directly onto vans, trucks, and trailers. No vinyl wrap bubbling or peeling — ever.",
    inner_hero("Printing", 'Vehicle &amp; Fleet <span class="gradient-text">Branding</span>', "The end of peeling vinyl wraps — permanent, seamless branding direct to your vehicle.") + """
<section class="section page-content" style="padding-top:3rem;">
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:3rem;align-items:start;">
      <div>
        <p class="reveal" style="font-size:1.05rem;margin-bottom:2rem;">Your business vehicle is a moving billboard, seen by thousands of potential customers every day. But traditional vehicle signage has a major flaw: vinyl wraps and stickers inevitably bubble, fade, and peel at the edges, making your brand look tired and unprofessional. Wall Envy uses advanced, German-engineered direct-to-surface printing technology to bypass vinyl completely — printing your high-definition logos, contact details, and graphics directly onto the side of your van, truck, or trailer. Permanent, seamless, and built to withstand harsh Australian conditions.</p>
        <div class="feature-list">
          <div class="feature-item reveal">
            <div class="feature-icon">&#10060;</div>
            <div><h4>Zero Peeling or Bubbling</h4><p>No adhesives or vinyl sheets means no edges to catch the wind, peel in the heat, or bubble under the sun. The ink becomes a permanent part of the vehicle.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-1">
            <div class="feature-icon">&#9728;&#65039;</div>
            <div><h4>UV Hard-Coat Durability</h4><p>Our eco-inks create a scratch-resistant, water-resistant hard coat. It handles road grime, high-pressure washing, and intense Australian sunlight far better than standard decals.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-2">
            <div class="feature-icon">&#128663;</div>
            <div><h4>Flawless on Corrugated Surfaces</h4><p>Vinyl wrappers struggle with deep grooves and rivets. Our print head adjusts to surface contours, delivering razor-sharp imagery on flat or deeply textured panels.</p></div>
          </div>
          <div class="feature-item reveal reveal-delay-3">
            <div class="feature-icon">&#127775;</div>
            <div><h4>The Premium Aesthetic</h4><p>Direct printing looks like a high-end, custom factory paint job — elevating the perceived value of your business the moment you pull up to a client's site.</p></div>
          </div>
        </div>
      </div>
      <div class="reveal reveal-delay-2">
        <img src="/assets/images/projects/proj-21.jpg" alt="Vehicle branding project" style="width:100%;border-radius:var(--card-r);box-shadow:var(--sh-lg);">
      </div>
    </div>
    <div style="margin-top:3rem;">
      <h3 class="reveal" style="margin-bottom:1.25rem;">Perfect For</h3>
      <div class="perfect-for-grid">
        <div class="perfect-for-item reveal"><div class="pf-dot"></div><p>Tradie Vans &amp; Utes — clean, professional branding for plumbers, electricians, builders, and landscapers</p></div>
        <div class="perfect-for-item reveal reveal-delay-1"><div class="pf-dot"></div><p>Food Trucks &amp; Coffee Trailers — vibrant, high-resolution graphics that withstand heat and humidity</p></div>
        <div class="perfect-for-item reveal reveal-delay-2"><div class="pf-dot"></div><p>Corporate Box Trucks &amp; Delivery Fleets — large-scale edge-to-edge advertising on massive blank panels</p></div>
        <div class="perfect-for-item reveal reveal-delay-3"><div class="pf-dot"></div><p>Enclosed Toy Haulers &amp; Motorsport Trailers — custom graphics and sponsor logos that won't tear from highway debris</p></div>
      </div>
    </div>
    <div class="highlight-box reveal" style="margin-top:2rem;">
      <p style="margin:0;">We print directly onto <strong>painted automotive metal, bare aluminium, fibreglass, and composite trailer panelling</strong>. Stop replacing tired stickers and invest in permanent, professional branding for your fleet.</p>
    </div>
  </div>
</section>""" + cta_strip("Ready to Upgrade Your Fleet?", "Print the <span class='gradient-text'>Impossible</span>", "Let's discuss your vehicle branding requirements and book a free vehicle quote and measure.", "Book Free Vehicle Quote")
)

# ── how-it-works.html ─────────────────────────────────────────────────────

PAGES["how-it-works.html"] = page(
    "How It Works",
    "4 simple steps: Design & Consultation, Preparation, The Print, Final Reveal. Clean, fast, and completely hassle-free direct-to-wall printing.",
    inner_hero("Our Process", 'How It <span class="gradient-text">Works</span>', "Turning your blank walls into masterpieces in 4 simple steps.") + """
<section class="section page-content" style="padding-top:3rem;">
  <div class="container">
    <p class="reveal" style="font-size:1.05rem;max-width:720px;margin-bottom:3rem;">At Wall Envy, we combine advanced vertical printing technology with a family-owned commitment to exceptional craftsmanship. Whether you're a business looking to create an unforgettable Instagram wall or a homeowner wanting a custom mural, our process is clean, fast, and completely hassle-free. Here's how we bring your vision to life on the Central Coast and surrounding regions.</p>
    <div style="display:flex;flex-direction:column;gap:2rem;">
      <div style="display:grid;grid-template-columns:80px 1fr;gap:2rem;align-items:start;" class="reveal">
        <div style="text-align:center;">
          <div style="width:64px;height:64px;border-radius:16px;background:var(--grad-brand);display:flex;align-items:center;justify-content:center;font-family:'Bebas Neue',sans-serif;font-size:2rem;color:#fff;margin:0 auto;">1</div>
        </div>
        <div class="card">
          <h3 style="margin-bottom:0.75rem;">Design &amp; Consultation — Your Vision, Our Expertise</h3>
          <div class="feature-list" style="margin-top:0.75rem;">
            <div class="feature-item"><div class="feature-icon">&#128161;</div><div><h4>Collaborate with Us</h4><p>Share your ideas, reference images, corporate logos, or room dimensions. If you need inspiration, Nicole and our design team can help you curate the perfect artwork, pattern, or texture.</p></div></div>
            <div class="feature-item"><div class="feature-icon">&#128269;</div><div><h4>Surface Check</h4><p>We verify your wall material (plaster, brick, concrete, timber, glass, or tile) to ensure it's suitable for printing.</p></div></div>
            <div class="feature-item"><div class="feature-icon">&#128444;&#65039;</div><div><h4>Digital Proofing</h4><p>We provide a digital mockup so you can see exactly how the artwork will look in your specific space before a single drop of ink touches your wall.</p></div></div>
          </div>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:80px 1fr;gap:2rem;align-items:start;" class="reveal reveal-delay-1">
        <div style="text-align:center;">
          <div style="width:64px;height:64px;border-radius:16px;background:var(--grad-brand);display:flex;align-items:center;justify-content:center;font-family:'Bebas Neue',sans-serif;font-size:2rem;color:#fff;margin:0 auto;">2</div>
        </div>
        <div class="card">
          <h3 style="margin-bottom:0.75rem;">Preparation &amp; Setup — Quick, Clean, and Non-Invasive</h3>
          <div class="feature-list" style="margin-top:0.75rem;">
            <div class="feature-item"><div class="feature-icon">&#10024;</div><div><h4>Zero Mess</h4><p>Unlike traditional wallpaper installation or messy hand-painting, our vertical printing process requires minimal site preparation.</p></div></div>
            <div class="feature-item"><div class="feature-icon">&#128295;</div><div><h4>Precision Calibration</h4><p>Our team arrives on-site and sets up our state-of-the-art vertical printer directly against your wall.</p></div></div>
            <div class="feature-item"><div class="feature-icon">&#128258;</div><div><h4>Laser-Accurate Alignment</h4><p>The machine automatically calibrates to your wall's exact height, level, and contours — accommodating heights of up to 4 metres.</p></div></div>
          </div>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:80px 1fr;gap:2rem;align-items:start;" class="reveal reveal-delay-2">
        <div style="text-align:center;">
          <div style="width:64px;height:64px;border-radius:16px;background:var(--grad-brand);display:flex;align-items:center;justify-content:center;font-family:'Bebas Neue',sans-serif;font-size:2rem;color:#fff;margin:0 auto;">3</div>
        </div>
        <div class="card">
          <h3 style="margin-bottom:0.75rem;">The Print — Watch the Magic Happen in Real-Time</h3>
          <div class="feature-list" style="margin-top:0.75rem;">
            <div class="feature-item"><div class="feature-icon">&#127912;</div><div><h4>High-Definition Direct Printing</h4><p>Our eco-friendly, non-toxic UV-cured inks are sprayed directly onto the vertical surface with incredible precision.</p></div></div>
            <div class="feature-item"><div class="feature-icon">&#9889;</div><div><h4>Instant Dry &amp; Durable</h4><p>The UV light instantly cures the ink as it prints. Dry the second it leaves the print head — no smudging, no running, and no strong chemical odours.</p></div></div>
            <div class="feature-item"><div class="feature-icon">&#127775;</div><div><h4>Flawless Finish</h4><p>Watch as high-resolution images, rich textures, or crisp branding emerge seamlessly onto your plaster, brick, or wood with vibrant, long-lasting colour.</p></div></div>
          </div>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:80px 1fr;gap:2rem;align-items:start;" class="reveal reveal-delay-3">
        <div style="text-align:center;">
          <div style="width:64px;height:64px;border-radius:16px;background:var(--grad-brand);display:flex;align-items:center;justify-content:center;font-family:'Bebas Neue',sans-serif;font-size:2rem;color:#fff;margin:0 auto;">4</div>
        </div>
        <div class="card">
          <h3 style="margin-bottom:0.75rem;">Final Reveal &amp; Enjoyment — Ready to Impress Instantly</h3>
          <div class="feature-list" style="margin-top:0.75rem;">
            <div class="feature-item"><div class="feature-icon">&#9889;</div><div><h4>Zero Downtime</h4><p>Once the print run finishes, we pack up our equipment immediately. No curing wait time, no peeling edges, and no messy cleanup left behind.</p></div></div>
            <div class="feature-item"><div class="feature-icon">&#128170;</div><div><h4>Built to Last</h4><p>Your new custom feature wall is scratch-resistant, water-resistant, and easy to maintain — ready for daily life in a bustling caf&#233;, corporate office, or residential living room.</p></div></div>
            <div class="feature-item"><div class="feature-icon">&#128247;</div><div><h4>Ready to Share</h4><p>Step back, admire your transformed space, and get ready for the compliments — and the tags on social media!</p></div></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>""" + cta_strip("Ready to Begin?", "Print the <span class='gradient-text'>Impossible</span>", "Whether you have a finished design or just a rough idea — we're here to help every step of the way. Book your free design consultation and quote today.", "Book Free Design Consultation")
)

# ── why-choose-us.html ────────────────────────────────────────────────────

PAGES["why-choose-us.html"] = page(
    "Why Choose Direct-to-Wall Printing",
    "5 reasons why direct-to-wall printing beats wallpaper and vinyl wraps: seamless finish, no peeling, any surface, no VOCs, and unlimited creative freedom.",
    inner_hero("The Wall Envy Advantage", 'Why Choose <span class="gradient-text">Direct-to-Wall?</span>', "For decades, custom wall art meant messy glues and peeling vinyl. Our technology eliminates those headaches permanently.") + """
<section class="section page-content" style="padding-top:3rem;">
  <div class="container">
    <p class="reveal" style="font-size:1.05rem;max-width:720px;margin-bottom:3rem;">For decades, adding custom artwork or branding to a wall meant dealing with messy glues, peeling vinyl, or repetitive wallpaper. Our direct-to-wall printing technology eliminates those headaches, delivering a seamless, permanent, and high-end finish that traditional methods simply cannot match.</p>
    <h3 class="reveal" style="margin-bottom:1.5rem;">Direct-to-Wall Printing vs. Wallpaper &amp; Vinyl Wraps</h3>
    <div class="comparison-grid">
      <div class="comparison-item reveal">
        <div class="comparison-header"><div class="ci-num">1</div><h3>100% Seamless Finish</h3></div>
        <div class="comparison-body">
          <div class="ci-problem"><strong>The Problem</strong>Large format vinyl and wallpaper are applied in panels. No matter how skilled the installer, there are always visible seams that disrupt the image and accumulate dust over time.</div>
          <div class="ci-advantage"><strong>The Wall Envy Advantage</strong>Our technology prints directly onto the wall as one continuous, edge-to-edge image. No seams, no overlaps — just a flawless, uninterrupted masterpiece that looks like a luxury hand-painted mural.</div>
        </div>
      </div>
      <div class="comparison-item reveal reveal-delay-1">
        <div class="comparison-header"><div class="ci-num">2</div><h3>Zero Peeling, Bubbling, or Fading</h3></div>
        <div class="comparison-body">
          <div class="ci-problem"><strong>The Problem</strong>Adhesives are vulnerable. Changes in humidity, temperature, and general wear inevitably lead to lifting edges, unsightly bubbles, and yellowing over time.</div>
          <div class="ci-advantage"><strong>The Wall Envy Advantage</strong>No physical material stuck to your wall means nothing to peel or bubble. Premium, UV-resistant inks cure instantly, bonding permanently with the surface. Brilliant colour for a decade or more.</div>
        </div>
      </div>
      <div class="comparison-item reveal reveal-delay-2">
        <div class="comparison-header"><div class="ci-num">3</div><h3>Ultimate Surface Flexibility</h3></div>
        <div class="comparison-body">
          <div class="ci-problem"><strong>The Problem</strong>Traditional methods require perfectly smooth, prepped surfaces. Applying vinyl or wallpaper to textured surfaces like brick or raw concrete is often impossible or fails quickly.</div>
          <div class="ci-advantage"><strong>The Wall Envy Advantage</strong>We print precisely onto almost any vertical surface — rough brick, concrete, timber, glass, tile, or standard plasterboard. Our technology adapts flawlessly to underlying texture.</div>
        </div>
      </div>
      <div class="comparison-item reveal">
        <div class="comparison-header"><div class="ci-num">4</div><h3>Healthier, Odour-Free Environments</h3></div>
        <div class="comparison-body">
          <div class="ci-problem"><strong>The Problem</strong>Wallpaper glues and vinyl adhesives often release strong chemical odours and Volatile Organic Compounds (VOCs) that require the space to be aired out for days.</div>
          <div class="ci-advantage"><strong>The Wall Envy Advantage</strong>Our eco-friendly, UV-cured inks are completely non-toxic and odourless. The moment printing stops, the room is 100% safe to occupy — perfect for homes, schools, caf&#233;s, and healthcare facilities.</div>
        </div>
      </div>
      <div class="comparison-item reveal reveal-delay-1">
        <div class="comparison-header"><div class="ci-num">5</div><h3>Infinite Creative Freedom</h3></div>
        <div class="comparison-body">
          <div class="ci-problem"><strong>The Problem</strong>You're often limited to repeating, mass-produced geometric patterns found in a supplier's catalogue. Custom designs are expensive and slow to produce.</div>
          <div class="ci-advantage"><strong>The Wall Envy Advantage</strong>Your space should reflect your unique vision. Custom corporate logos, high-resolution local landscapes, intricate art pieces, or tactile 3D architectural textures — if you can imagine it, we can print it.</div>
        </div>
      </div>
    </div>
  </div>
</section>""" + cta_strip("Convinced?", "Print the <span class='gradient-text'>Impossible</span>", "Let's discuss your specific material and space. Book a free site measure and surface consultation today.", "Book Free Site Measure")
)

# ── projects.html ─────────────────────────────────────────────────────────

proj_items = "".join(
    f'<a class="gallery-item reveal" href="#" onclick="return false;" aria-label="View project image {i+1}">'
    f'<img src="/assets/images/projects/proj-{str(i+2).zfill(2)}.jpg" alt="Wall Envy project {i+1}" loading="lazy"></a>'
    for i in range(19)
    if i != 6 and i != 11 and i != 12  # skip failed downloads (proj-01,07,10,11,12,13,14 were some that failed)
)

PAGES["projects.html"] = page(
    "Projects",
    "Browse Wall Envy's project gallery — stunning direct-to-wall printing installations across the Central Coast & Hunter regions.",
    inner_hero("Our Work", 'Project <span class="gradient-text">Gallery</span>', "A showcase of walls transformed — commercial, residential, healthcare, schools, hospitality, and sports.") + f"""
<section class="section page-content" style="padding-top:2rem;">
  <div class="container">
    <p class="reveal" style="max-width:680px;margin-bottom:2.5rem;">Every project tells a story. From bold commercial branding to intimate residential murals, we bring walls to life across the Central Coast and Hunter regions. Click any image to view it full-size.</p>
    <div class="gallery-grid">
      <a class="gallery-item reveal" href="#" onclick="return false;" aria-label="View project"><img src="/assets/images/projects/proj-02.jpg" alt="Wall Envy project" loading="lazy"></a>
      <a class="gallery-item reveal" href="#" onclick="return false;" aria-label="View project"><img src="/assets/images/projects/proj-03.jpg" alt="Wall Envy project" loading="lazy"></a>
      <a class="gallery-item reveal reveal-delay-1" href="#" onclick="return false;" aria-label="View project"><img src="/assets/images/projects/proj-05.jpg" alt="Wall Envy project" loading="lazy"></a>
      <a class="gallery-item reveal reveal-delay-2" href="#" onclick="return false;" aria-label="View project"><img src="/assets/images/projects/proj-06.jpg" alt="Wall Envy project" loading="lazy"></a>
      <a class="gallery-item reveal" href="#" onclick="return false;" aria-label="View project"><img src="/assets/images/projects/proj-08.jpg" alt="Wall Envy project" loading="lazy"></a>
      <a class="gallery-item reveal reveal-delay-1" href="#" onclick="return false;" aria-label="View project"><img src="/assets/images/projects/proj-09.jpg" alt="Wall Envy project" loading="lazy"></a>
      <a class="gallery-item reveal reveal-delay-2" href="#" onclick="return false;" aria-label="View project"><img src="/assets/images/projects/proj-15.jpg" alt="Wall Envy project" loading="lazy"></a>
      <a class="gallery-item reveal" href="#" onclick="return false;" aria-label="View project"><img src="/assets/images/projects/proj-16.jpg" alt="Wall Envy project" loading="lazy"></a>
      <a class="gallery-item reveal reveal-delay-1" href="#" onclick="return false;" aria-label="View project"><img src="/assets/images/projects/proj-17.jpg" alt="Wall Envy project" loading="lazy"></a>
      <a class="gallery-item reveal reveal-delay-2" href="#" onclick="return false;" aria-label="View project"><img src="/assets/images/projects/proj-18.jpg" alt="Wall Envy project" loading="lazy"></a>
      <a class="gallery-item reveal" href="#" onclick="return false;" aria-label="View project"><img src="/assets/images/projects/proj-19.jpg" alt="Wall Envy project" loading="lazy"></a>
      <a class="gallery-item reveal reveal-delay-1" href="#" onclick="return false;" aria-label="View project"><img src="/assets/images/projects/proj-20.jpg" alt="Wall Envy project" loading="lazy"></a>
      <a class="gallery-item reveal reveal-delay-2" href="#" onclick="return false;" aria-label="View project"><img src="/assets/images/projects/proj-21.jpg" alt="Wall Envy project" loading="lazy"></a>
      <a class="gallery-item reveal" href="#" onclick="return false;" aria-label="View project"><img src="/assets/images/projects/proj-22.jpg" alt="Wall Envy project" loading="lazy"></a>
      <a class="gallery-item reveal reveal-delay-1" href="#" onclick="return false;" aria-label="View project"><img src="/assets/images/projects/proj-23.jpg" alt="Wall Envy project" loading="lazy"></a>
      <a class="gallery-item reveal reveal-delay-2" href="#" onclick="return false;" aria-label="View project"><img src="/assets/images/projects/proj-24.jpg" alt="Wall Envy project" loading="lazy"></a>
    </div>
    <!-- Lightbox -->
    <div class="lightbox" id="lightbox" role="dialog" aria-label="Image viewer">
      <div class="lightbox-inner">
        <button class="lightbox-close" id="lb-close" aria-label="Close">&#x2715;</button>
        <img class="lightbox-img" id="lb-img" src="" alt="">
      </div>
      <button class="lightbox-prev" id="lb-prev" aria-label="Previous">&#8249;</button>
      <button class="lightbox-next" id="lb-next" aria-label="Next">&#8250;</button>
    </div>
  </div>
</section>

<!-- YouTube Section — Uncomment and add your playlist/video ID to activate -->
<!--
<section class="section" style="background:var(--bg2);" id="videos">
  <div class="container text-center">
    <span class="section-label">Watch Us Work</span>
    <h2 style="margin-bottom:2rem;">Wall Envy on <span class="gradient-text">YouTube</span></h2>
    <div style="max-width:800px;margin:0 auto;border-radius:var(--card-r);overflow:hidden;box-shadow:var(--sh-lg);">
      <iframe
        src="https://www.youtube.com/embed/videoseries?list=YOUR_PLAYLIST_ID_HERE"
        width="100%"
        height="450"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
        title="Wall Envy YouTube playlist"
        style="display:block;">
      </iframe>
    </div>
    <p style="margin-top:1rem;font-size:0.875rem;">Subscribe to our YouTube channel for time-lapses, project tours, and tips.</p>
  </div>
</section>
-->""" + cta_strip("Love What You See?", "Print the <span class='gradient-text'>Impossible</span>", "Ready to transform your own space? Book your free consultation and site measure today — no obligation.", "Book Free Consultation")
)

# ── faqs.html ─────────────────────────────────────────────────────────────

faqs = [
    ("What Is Wall Printing?", "Wall printing is an innovative technology that allows us to print high-quality, intricate designs directly onto your walls. It's a new alternative to traditional methods like painting or wallpapering."),
    ("What is the Wall Printing Process?", "The process begins with a consultation where we discuss your ideas, preferences, and specifics of the space. Then our designers create high-resolution art. We use advanced wall printing machines to translate the design onto your wall with meticulous attention to detail."),
    ("What Can Be Printed On?", "Yes, we can print on a diverse range of surfaces, including Sheetrock (drywall), Plaster Walls, Brick Walls, Glass Walls, Metal Walls, and Wood Walls. This also includes floors. We do not however print on ceilings."),
    ("What Designs Can Be Printed?", "We can print a virtually unlimited range of designs, from subtle patterns to vibrant, large-scale murals."),
    ("Can I Use My Own Design or Image?", "Absolutely! We work closely with each client to understand their vision, and we can use any high-resolution image you provide. If the image is not high resolution, our design team can try and enhance the image for your size requirements. Vector art can be set to any size you want."),
    ("How Long Does the Wall Printing Process Take?", "The duration of the process depends on the size of the wall and the complexity of the design. We can provide a more accurate estimate after the initial consultation."),
    ("Is the Wall Damaged From the Printing?", "No, wall printing does not cause any damage to the wall. If you want to change or remove the design, all you have to do is simply paint right over it."),
    ("How Is the Cost of Wall Printing Determined?", "The cost is determined based on several factors, including the travel & setup time, size of the print, the complexity of the design & print job, and the type of wall surface."),
    ("Can You Help with Design Ideas?", "Absolutely! Our skilled designers can work with you to come up with a design that suits your space and personal style. Our team will send you proofs which you will provide an approval on before we start any work."),
    ("How Far in Advance Do I Need to Schedule?", "The lead time can vary depending on our current schedule and the size of your project. We are taking on projects now and we can consult with you on scheduling."),
    ("How Long Does the Print Last?", "With proper care, a wall print can last for many years. Typically, indoor prints can last 12 years and outdoor 5 years. For outdoor prints we suggest adding a protective layer of clear coat which would extend the lifespan outdoors."),
]

faq_html = '\n'.join(
    f'''<div class="faq-item">
  <button class="faq-question"><span>{q}</span><span class="faq-icon">&#9660;</span></button>
  <div class="faq-answer"><div class="faq-answer-inner">{a}</div></div>
</div>'''
    for q, a in faqs
)

PAGES["faqs.html"] = page(
    "Frequently Asked Questions",
    "Answers to common questions about wall printing — process, surfaces, cost, designs, lifespan, and how to get started with Wall Envy.",
    inner_hero("Got Questions?", 'Frequently Asked <span class="gradient-text">Questions</span>', "Everything you need to know about direct-to-wall printing.") + f"""
<section class="section page-content" style="padding-top:3rem;">
  <div class="container">
    <div style="max-width:820px;margin:0 auto;">
      <div class="faq-list">
{faq_html}
      </div>
      <div class="highlight-box reveal" style="margin-top:3rem;text-align:center;">
        <h4 style="margin-bottom:0.5rem;">Still have questions?</h4>
        <p style="margin-bottom:1.25rem;">We're happy to help. Reach out directly and we'll get back to you quickly.</p>
        <a href="contact.html" class="btn btn-primary">Contact Us</a>
      </div>
    </div>
  </div>
</section>""" + cta_strip()
)

# ── contact.html ──────────────────────────────────────────────────────────

PAGES["contact.html"] = page(
    "Contact Us",
    "Book your free Wall Envy consultation. Call 0414 698 448, email info@wallenvy.com.au, or fill in our quick contact form — we'll be in touch shortly.",
    inner_hero("Let's Talk", 'Get in <span class="gradient-text">Touch</span>', "Book your free consultation and site measure today. No obligation, no pressure — just great ideas.") + """
<section class="section page-content" style="padding-top:3rem;">
  <div class="container">
    <div class="contact-grid">
      <!-- LEFT: contact details -->
      <div>
        <div class="contact-info">
          <div class="contact-info-item">
            <div class="ci-icon">&#128222;</div>
            <div>
              <h4 style="margin-bottom:0.2rem;">Phone</h4>
              <a href="tel:0414698448" style="font-size:1.1rem;font-weight:600;color:var(--cyan);">0414 698 448</a>
            </div>
          </div>
          <div class="contact-info-item">
            <div class="ci-icon">&#9993;&#65039;</div>
            <div>
              <h4 style="margin-bottom:0.2rem;">Email</h4>
              <a href="mailto:info@wallenvy.com.au" style="font-size:1rem;font-weight:500;color:var(--cyan);">info@wallenvy.com.au</a>
            </div>
          </div>
          <div class="contact-info-item">
            <div class="ci-icon">&#128205;</div>
            <div>
              <h4 style="margin-bottom:0.2rem;">Service Area</h4>
              <p style="margin:0;">Central Coast &amp; Hunter regions, NSW, Australia</p>
            </div>
          </div>
        </div>
        <div class="contact-social-row" style="margin-top:2rem;">
          <a href="https://www.facebook.com/people/Wallenvy/61592586241845/" target="_blank" rel="noopener" class="social-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
            Facebook
          </a>
          <a href="https://www.instagram.com/wallenvy.au" target="_blank" rel="noopener" class="social-btn">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
            Instagram
          </a>
        </div>

        <!-- Facebook Page Widget (shown only if consent accepted) -->
        <div class="fb-widget-wrap" id="fb-widget-section" style="margin-top:2rem;">
          <h4>&#128077; Follow Us on Facebook</h4>
          <div id="fb-root"></div>
          <div class="fb-page"
            data-href="https://www.facebook.com/people/Wallenvy/61592586241845/"
            data-tabs="timeline"
            data-width="380"
            data-height="400"
            data-small-header="true"
            data-adapt-container-width="true"
            data-hide-cover="false"
            data-show-facepile="false">
          </div>
        </div>

        <!-- Instagram Follow Card -->
        <a href="https://www.instagram.com/wallenvy.au" target="_blank" rel="noopener" class="insta-card" style="text-decoration:none;margin-top:1.5rem;display:flex;">
          <div class="insta-icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="url(#ig-grad)">
              <defs>
                <linearGradient id="ig-grad" x1="0%" y1="100%" x2="100%" y2="0%">
                  <stop offset="0%" style="stop-color:#f09433"/>
                  <stop offset="25%" style="stop-color:#e6683c"/>
                  <stop offset="50%" style="stop-color:#dc2743"/>
                  <stop offset="75%" style="stop-color:#cc2366"/>
                  <stop offset="100%" style="stop-color:#bc1888"/>
                </linearGradient>
              </defs>
              <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
            </svg>
          </div>
          <div>
            <h4>Follow @wallenvy.au</h4>
            <p>See our latest projects, behind-the-scenes clips, and inspiration on Instagram.</p>
          </div>
        </a>
      </div>

      <!-- RIGHT: Tally Form -->
      <div>
        <h3 style="margin-bottom:1.5rem;">Reach out to Begin Your Free Consultation</h3>
        <div class="tally-wrapper">
          <iframe data-tally-src="https://tally.so/embed/b5XJM2?alignLeft=1&hideTitle=1&transparentBackground=1&dynamicHeight=1" loading="lazy" width="100%" height="867" frameborder="0" marginheight="0" marginwidth="0" title="Reach out to Begin Your Free Consultation"></iframe>
        </div>
        <script>var d=document,w="https://tally.so/widgets/embed.js",v=function(){"undefined"!=typeof Tally?Tally.loadEmbeds():d.querySelectorAll("iframe[data-tally-src]:not([src])").forEach((function(e){e.src=e.dataset.tallySrc}))};if("undefined"!=typeof Tally)v();else if(d.querySelector('script[src="'+w+'"]')==null){var s=d.createElement("script");s.src=w,s.onload=v,s.onerror=v,d.body.appendChild(s);}</script>
      </div>
    </div>
  </div>
</section>"""
)

# ── 404.html ──────────────────────────────────────────────────────────────

PAGES["404.html"] = page(
    "Page Not Found",
    "The page you were looking for could not be found.",
    """
<section style="min-height:70vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:4rem 1rem;">
  <div>
    <div style="font-family:'Bebas Neue',sans-serif;font-size:8rem;line-height:1;background:var(--grad-text);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">404</div>
    <h2 style="margin-bottom:1rem;">Oops — that wall is blank!</h2>
    <p style="max-width:420px;margin:0 auto 2rem;">The page you're looking for doesn't exist, but we can definitely print something here. Let's get you back on track.</p>
    <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
      <a href="/" class="btn btn-primary">Back to Home</a>
      <a href="contact.html" class="btn btn-outline">Contact Us</a>
    </div>
  </div>
</section>"""
)

# ─── Write all pages ─────────────────────────────────────────────────────────

def write_page(rel_path, html):
    full_path = os.path.join(ROOT, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  [ok] {rel_path}")

if __name__ == "__main__":
    print("\n=== Wall Envy Page Builder ===\n")
    for rel_path, html in PAGES.items():
        write_page(rel_path, html)
    print(f"\n=== Done: {len(PAGES)} pages built ===\n")
