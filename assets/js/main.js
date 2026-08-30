/* =====================================================
   WALL ENVY — JavaScript
   Theme toggle · Nav · Lightbox · Cookie consent
   Scroll reveal · FAQ accordion
   ===================================================== */

(function () {
  'use strict';

  /* ---- Theme ---- */
  const THEME_KEY = 'wallenvy_theme';

  function getPreferredTheme() {
    const stored = localStorage.getItem(THEME_KEY);
    if (stored) return stored;
    return 'dark'; // Default to midnight theme
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);
  }

  // Apply immediately to avoid FOUC (called before DOMContentLoaded via inline script)
  applyTheme(getPreferredTheme());

  /* ---- Cookie Consent ---- */
  const CONSENT_KEY = 'wallenvy_consent';

  function getConsent() { return localStorage.getItem(CONSENT_KEY); }

  function setConsent(value) {
    localStorage.setItem(CONSENT_KEY, value);
    hideCookieBanner();
    if (value === 'accepted') enableThirdParty();
  }

  function enableThirdParty() {
    // Load FB SDK lazily if consent is given
    document.querySelectorAll('[data-fb-lazy]').forEach(el => {
      el.removeAttribute('data-fb-lazy');
    });
    loadFbSdk();
  }

  function loadFbSdk() {
    if (document.getElementById('fb-sdk')) return;
    const js = document.createElement('script');
    js.id = 'fb-sdk';
    js.async = true;
    js.defer = true;
    js.crossOrigin = 'anonymous';
    js.src = 'https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v19.0';
    document.body.appendChild(js);
  }

  function showCookieBanner() {
    const banner = document.getElementById('cookie-banner');
    if (banner) {
      requestAnimationFrame(() => banner.classList.add('visible'));
    }
  }

  function hideCookieBanner() {
    const banner = document.getElementById('cookie-banner');
    if (banner) {
      banner.classList.remove('visible');
      setTimeout(() => banner.remove(), 500);
    }
  }

  /* ---- FAQ Accordion ---- */
  function initFaq() {
    document.querySelectorAll('.faq-question').forEach(btn => {
      btn.addEventListener('click', () => {
        const item = btn.closest('.faq-item');
        const isOpen = item.classList.contains('open');
        // Close all
        document.querySelectorAll('.faq-item.open').forEach(el => el.classList.remove('open'));
        // Toggle clicked
        if (!isOpen) item.classList.add('open');
      });
    });
  }

  /* ---- Gallery Lightbox ---- */
  let galleryImages = [];
  let currentIndex  = 0;

  function initLightbox() {
    const lightbox  = document.getElementById('lightbox');
    if (!lightbox) return;
    const lbImg     = document.getElementById('lb-img');
    const lbClose   = document.getElementById('lb-close');
    const lbPrev    = document.getElementById('lb-prev');
    const lbNext    = document.getElementById('lb-next');

    galleryImages = Array.from(document.querySelectorAll('.gallery-item img'));

    document.querySelectorAll('.gallery-item').forEach((item, idx) => {
      item.addEventListener('click', () => openLightbox(idx));
    });

    lbClose.addEventListener('click', closeLightbox);
    lbPrev.addEventListener('click',  () => navigate(-1));
    lbNext.addEventListener('click',  () => navigate(1));
    lightbox.addEventListener('click', e => { if (e.target === lightbox) closeLightbox(); });

    document.addEventListener('keydown', e => {
      if (!lightbox.classList.contains('open')) return;
      if (e.key === 'Escape')     closeLightbox();
      if (e.key === 'ArrowLeft')  navigate(-1);
      if (e.key === 'ArrowRight') navigate(1);
    });
  }

  function openLightbox(idx) {
    currentIndex = idx;
    const lightbox = document.getElementById('lightbox');
    const lbImg    = document.getElementById('lb-img');
    lbImg.src = galleryImages[idx].src;
    lbImg.alt = galleryImages[idx].alt || 'Wall Envy Project';
    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    document.getElementById('lightbox').classList.remove('open');
    document.body.style.overflow = '';
  }

  function navigate(dir) {
    currentIndex = (currentIndex + dir + galleryImages.length) % galleryImages.length;
    const lbImg = document.getElementById('lb-img');
    lbImg.style.opacity = '0';
    setTimeout(() => {
      lbImg.src = galleryImages[currentIndex].src;
      lbImg.style.opacity = '1';
    }, 150);
  }

  /* ---- Nav Dropdowns (hover with delay prevents accidental close) ---- */
  function initDropdowns() {
    document.querySelectorAll('.nav-links > li').forEach(li => {
      const dropdown = li.querySelector('.dropdown');
      if (!dropdown) return;
      let hideTimer;
      const show = () => { clearTimeout(hideTimer); dropdown.style.display = 'block'; };
      const hide = () => { hideTimer = setTimeout(() => { dropdown.style.display = ''; }, 150); };
      li.addEventListener('mouseenter', show);
      li.addEventListener('mouseleave', hide);
      dropdown.addEventListener('mouseenter', show);
      dropdown.addEventListener('mouseleave', hide);
    });
  }

  /* ---- Tally Form Theme Sync ---- */
  function syncTallyForms() {
    const darkWrap  = document.querySelector('.tally-dark');
    const lightWrap = document.querySelector('.tally-light');
    if (!darkWrap || !lightWrap) return;

    const theme     = document.documentElement.getAttribute('data-theme') || 'dark';
    const isLight   = theme === 'light';
    const toShow    = isLight ? lightWrap : darkWrap;
    const toHide    = isLight ? darkWrap  : lightWrap;

    // Force hide with inline style (overrides any Tally-injected styles)
    toHide.style.cssText  = 'display:none!important;height:0;overflow:hidden;';
    toShow.style.cssText  = 'display:block;';

    // Reload the newly-visible iframe so Tally calculates its full height
    const iframe = toShow.querySelector('iframe');
    if (iframe) {
      const src = iframe.src || iframe.dataset.tallySrc;
      if (src) {
        iframe.src = '';
        requestAnimationFrame(() => { iframe.src = src; });
      }
    }
  }

  /* ---- Nav ---- */
  function initNav() {
    const burger     = document.getElementById('nav-burger');
    const mobileMenu = document.getElementById('mobile-menu');
    const themeBtn   = document.querySelector('.theme-toggle');
    const nav        = document.getElementById('site-nav');

    // Mark active link — strip base href prefix so works at /wallenvy/ or /
    const baseEl  = document.querySelector('base');
    const baseHref = baseEl ? baseEl.getAttribute('href') : '/';
    const basePath = new URL(baseHref, window.location.origin).pathname.replace(/\/$/, '');
    const path = window.location.pathname.replace(basePath, '').replace(/\/$/, '') || '/';
    document.querySelectorAll('.nav-link[data-path], .mobile-menu a[data-path]').forEach(link => {
      const lp = link.getAttribute('data-path').replace(/\/$/, '');
      if (path === lp || (lp !== '/' && path.startsWith(lp))) {
        link.classList.add('active');
      }
    });

    // Burger toggle
    if (burger && mobileMenu) {
      burger.addEventListener('click', () => {
        burger.classList.toggle('open');
        mobileMenu.classList.toggle('open');
      });
      // Close on link click
      mobileMenu.querySelectorAll('a').forEach(a => {
        a.addEventListener('click', () => {
          burger.classList.remove('open');
          mobileMenu.classList.remove('open');
        });
      });
    }

    // Theme toggle
    if (themeBtn) {
      themeBtn.addEventListener('click', () => {
        const cur = document.documentElement.getAttribute('data-theme') || 'dark';
        applyTheme(cur === 'dark' ? 'light' : 'dark');
        syncTallyForms(); // swap Tally form to match new theme
      });
    }

    // Nav scroll shadow
    if (nav) {
      window.addEventListener('scroll', () => {
        nav.style.borderBottomColor = window.scrollY > 10
          ? 'var(--border)'
          : 'transparent';
      }, { passive: true });
    }
  }

  /* ---- Scroll Reveal ---- */
  function initReveal() {
    const els = document.querySelectorAll('.reveal');
    if (!els.length) return;
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    els.forEach(el => io.observe(el));
  }

  /* ---- Init on DOM Ready ---- */
  document.addEventListener('DOMContentLoaded', () => {
    initNav();
    initFaq();
    initLightbox();
    initReveal();
    syncTallyForms(); // show correct Tally form for current theme on page load

    // Cookie consent
    const consent = getConsent();
    if (!consent) {
      showCookieBanner();
    } else if (consent === 'accepted') {
      enableThirdParty();
    }

    // Cookie banner buttons
    const acceptBtn  = document.getElementById('cookie-accept');
    const declineBtn = document.getElementById('cookie-decline');
    if (acceptBtn)  acceptBtn.addEventListener('click',  () => setConsent('accepted'));
    if (declineBtn) declineBtn.addEventListener('click', () => setConsent('declined'));

    // Smooth anchor scroll offset for fixed nav
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', e => {
        const target = document.querySelector(anchor.getAttribute('href'));
        if (!target) return;
        e.preventDefault();
        const top = target.getBoundingClientRect().top + window.scrollY - 88;
        window.scrollTo({ top, behavior: 'smooth' });
      });
    });
  });

})();
