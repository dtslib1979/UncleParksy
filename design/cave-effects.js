/* ═══════════════════════════════════════════════════════════════
   CAVE UI - EFFECTS ENGINE
   Awwwards-level interactions
   ═══════════════════════════════════════════════════════════════ */

class CaveEffects {
  constructor(options = {}) {
    this.options = {
      cursor: true,
      torchLight: true,
      smoothScroll: true,
      textReveal: true,
      scrollReveal: true,
      magnetic: true,
      pageTransition: true,
      ...options
    };

    this.cursor = null;
    this.cursorGlow = null;
    this.torchLight = null;
    this.mouse = { x: 0, y: 0 };
    this.smoothMouse = { x: 0, y: 0 };

    this.init();
  }

  init() {
    // Wait for DOM
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.setup());
    } else {
      this.setup();
    }
  }

  setup() {
    // Add texture class to body
    document.body.classList.add('cave-texture');

    if (this.options.cursor) this.initCursor();
    if (this.options.torchLight) this.initTorchLight();
    if (this.options.smoothScroll) this.initSmoothScroll();
    if (this.options.textReveal) this.initTextReveal();
    if (this.options.scrollReveal) this.initScrollReveal();
    if (this.options.magnetic) this.initMagnetic();
    if (this.options.pageTransition) this.initPageTransition();

    // Start animation loop
    this.animate();
  }

  /* ─────────────────────────────────────────────────────────────
     CUSTOM CURSOR
     ───────────────────────────────────────────────────────────── */
  initCursor() {
    // Create cursor elements
    this.cursor = document.createElement('div');
    this.cursor.className = 'cave-cursor';
    document.body.appendChild(this.cursor);

    this.cursorGlow = document.createElement('div');
    this.cursorGlow.className = 'cave-cursor-glow';
    document.body.appendChild(this.cursorGlow);

    // Add class to body
    document.body.classList.add('cave-cursor-active');

    // Track mouse
    document.addEventListener('mousemove', (e) => {
      this.mouse.x = e.clientX;
      this.mouse.y = e.clientY;
    });

    // Hover states
    const hoverElements = document.querySelectorAll('a, button, .cave-door, .magnetic, [data-cursor="hover"]');
    hoverElements.forEach(el => {
      el.addEventListener('mouseenter', () => this.cursor.classList.add('hover'));
      el.addEventListener('mouseleave', () => this.cursor.classList.remove('hover'));
    });

    // Hide cursor when leaving window
    document.addEventListener('mouseleave', () => {
      this.cursor.style.opacity = '0';
      this.cursorGlow.style.opacity = '0';
    });

    document.addEventListener('mouseenter', () => {
      this.cursor.style.opacity = '1';
      this.cursorGlow.style.opacity = '1';
    });
  }

  /* ─────────────────────────────────────────────────────────────
     TORCH LIGHT
     ───────────────────────────────────────────────────────────── */
  initTorchLight() {
    this.torchLight = document.createElement('div');
    this.torchLight.className = 'torch-light flicker';
    document.body.appendChild(this.torchLight);
  }

  /* ─────────────────────────────────────────────────────────────
     SMOOTH SCROLL (Lenis-like)
     ───────────────────────────────────────────────────────────── */
  initSmoothScroll() {
    // Simple smooth scroll implementation
    // For production, use Lenis library
    document.documentElement.style.scrollBehavior = 'smooth';

    // Smooth anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(anchor.getAttribute('href'));
        if (target) {
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  /* ─────────────────────────────────────────────────────────────
     TEXT REVEAL - Split text into chars
     ───────────────────────────────────────────────────────────── */
  initTextReveal() {
    document.querySelectorAll('.text-reveal').forEach(el => {
      const text = el.textContent;
      el.innerHTML = '';

      [...text].forEach((char, i) => {
        const span = document.createElement('span');
        span.className = 'char';
        span.textContent = char === ' ' ? '\u00A0' : char;
        span.style.animationDelay = `${i * 0.05}s`;
        el.appendChild(span);
      });
    });

    // Line reveal
    document.querySelectorAll('.line-reveal').forEach(el => {
      const lines = el.innerHTML.split('<br>');
      el.innerHTML = '';

      lines.forEach((line, i) => {
        const div = document.createElement('div');
        div.className = 'line';
        div.innerHTML = line;
        div.style.animationDelay = `${i * 0.15}s`;
        el.appendChild(div);
      });
    });
  }

  /* ─────────────────────────────────────────────────────────────
     SCROLL REVEAL - Intersection Observer
     ───────────────────────────────────────────────────────────── */
  initScrollReveal() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          // Optional: unobserve after reveal
          // observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    });

    document.querySelectorAll('.scroll-reveal').forEach(el => {
      observer.observe(el);
    });
  }

  /* ─────────────────────────────────────────────────────────────
     MAGNETIC BUTTONS
     ───────────────────────────────────────────────────────────── */
  initMagnetic() {
    document.querySelectorAll('.magnetic').forEach(el => {
      el.addEventListener('mousemove', (e) => {
        const rect = el.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;

        el.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
      });

      el.addEventListener('mouseleave', () => {
        el.style.transform = 'translate(0, 0)';
      });
    });
  }

  /* ─────────────────────────────────────────────────────────────
     PAGE TRANSITIONS
     ───────────────────────────────────────────────────────────── */
  initPageTransition() {
    // Create transition element
    const transition = document.createElement('div');
    transition.className = 'page-transition';
    document.body.appendChild(transition);

    // Intercept link clicks
    document.querySelectorAll('a[href]').forEach(link => {
      const href = link.getAttribute('href');

      // Only internal links
      if (href && !href.startsWith('#') && !href.startsWith('http') && !href.startsWith('mailto')) {
        link.addEventListener('click', (e) => {
          e.preventDefault();

          // Start transition
          transition.classList.add('entering');

          setTimeout(() => {
            window.location.href = href;
          }, 600);
        });
      }
    });

    // On page load, animate out
    window.addEventListener('load', () => {
      transition.classList.add('leaving');
      setTimeout(() => {
        transition.classList.remove('entering', 'leaving');
      }, 600);
    });
  }

  /* ─────────────────────────────────────────────────────────────
     ANIMATION LOOP
     ───────────────────────────────────────────────────────────── */
  animate() {
    // Smooth cursor following
    const lerp = (a, b, n) => (1 - n) * a + n * b;

    this.smoothMouse.x = lerp(this.smoothMouse.x, this.mouse.x, 0.15);
    this.smoothMouse.y = lerp(this.smoothMouse.y, this.mouse.y, 0.15);

    if (this.cursor) {
      this.cursor.style.left = `${this.mouse.x}px`;
      this.cursor.style.top = `${this.mouse.y}px`;
    }

    if (this.cursorGlow) {
      this.cursorGlow.style.left = `${this.smoothMouse.x}px`;
      this.cursorGlow.style.top = `${this.smoothMouse.y}px`;
    }

    if (this.torchLight) {
      this.torchLight.style.left = `${this.smoothMouse.x}px`;
      this.torchLight.style.top = `${this.smoothMouse.y}px`;
    }

    requestAnimationFrame(() => this.animate());
  }

  /* ─────────────────────────────────────────────────────────────
     UTILITY METHODS
     ───────────────────────────────────────────────────────────── */

  // Add parallax to element
  addParallax(selector, speed = 0.5) {
    const el = document.querySelector(selector);
    if (!el) return;

    window.addEventListener('scroll', () => {
      const scrolled = window.pageYOffset;
      el.style.transform = `translateY(${scrolled * speed}px)`;
    });
  }

  // Create entrance overlay
  createEntrance(text = '朴') {
    const overlay = document.createElement('div');
    overlay.className = 'entrance-overlay';
    overlay.innerHTML = `<span class="monument">${text}</span>`;
    document.body.appendChild(overlay);
  }

  // Add glitch effect to element
  addGlitch(selector) {
    const el = document.querySelector(selector);
    if (!el) return;

    el.classList.add('glitch', 'glitch-hover');
    el.setAttribute('data-text', el.textContent);
  }
}

/* ─────────────────────────────────────────────────────────────
   GSAP ANIMATIONS (if GSAP is loaded)
   ───────────────────────────────────────────────────────────── */
if (typeof gsap !== 'undefined') {
  // Register ScrollTrigger if available
  if (typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);
  }

  // Entrance animation
  const entranceTimeline = gsap.timeline();

  entranceTimeline
    .from('.monument', {
      opacity: 0,
      scale: 0.8,
      filter: 'blur(20px)',
      duration: 1.2,
      ease: 'power3.out'
    })
    .from('.statement', {
      opacity: 0,
      y: 30,
      duration: 0.8,
      ease: 'power2.out'
    }, '-=0.5')
    .from('.cave-door', {
      opacity: 0,
      y: 20,
      duration: 0.6,
      ease: 'power2.out'
    }, '-=0.3');
}

/* ─────────────────────────────────────────────────────────────
   AUTO INIT
   ───────────────────────────────────────────────────────────── */
// Auto-initialize if data attribute present
if (document.querySelector('[data-cave-effects]')) {
  window.caveEffects = new CaveEffects();
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CaveEffects;
}

// Export for ES modules
if (typeof window !== 'undefined') {
  window.CaveEffects = CaveEffects;
}
