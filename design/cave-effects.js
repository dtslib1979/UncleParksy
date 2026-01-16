/* ═══════════════════════════════════════════════════════════════
   CAVE UI - EFFECTS ENGINE v2.0
   실제로 Awwwards 급으로 다시 짬
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

    // State
    this.cursor = null;
    this.cursorGlow = null;
    this.torchLight = null;
    this.mouse = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
    this.smoothMouse = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
    this.isRunning = false;
    this.rafId = null;

    // Scroll state (for real smooth scroll)
    this.scroll = {
      current: 0,
      target: 0,
      ease: 0.075,
      isSmooth: true
    };

    // Bound methods for cleanup
    this._onMouseMove = this._onMouseMove.bind(this);
    this._onResize = this._onResize.bind(this);

    this.init();
  }

  init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.setup());
    } else {
      this.setup();
    }
  }

  setup() {
    document.body.classList.add('cave-texture');

    if (this.options.cursor) this.initCursor();
    if (this.options.torchLight) this.initTorchLight();
    if (this.options.smoothScroll) this.initSmoothScroll();
    if (this.options.textReveal) this.initTextReveal();
    if (this.options.scrollReveal) this.initScrollReveal();
    if (this.options.magnetic) this.initMagnetic();
    if (this.options.pageTransition) this.initPageTransition();

    // Global listeners
    window.addEventListener('mousemove', this._onMouseMove, { passive: true });
    window.addEventListener('resize', this._onResize, { passive: true });

    // Start render loop
    this.start();
  }

  /* ─────────────────────────────────────────────────────────────
     RENDER LOOP - 제대로 된 애니메이션 루프
     ───────────────────────────────────────────────────────────── */
  start() {
    if (this.isRunning) return;
    this.isRunning = true;
    this.render();
  }

  stop() {
    this.isRunning = false;
    if (this.rafId) {
      cancelAnimationFrame(this.rafId);
      this.rafId = null;
    }
  }

  render() {
    if (!this.isRunning) return;

    // Lerp helper
    const lerp = (a, b, n) => a + (b - a) * n;

    // Smooth mouse (for cursor + torch)
    this.smoothMouse.x = lerp(this.smoothMouse.x, this.mouse.x, 0.15);
    this.smoothMouse.y = lerp(this.smoothMouse.y, this.mouse.y, 0.15);

    // Update cursor position with transform (GPU accelerated)
    if (this.cursor) {
      this.cursor.style.transform = `translate3d(${this.mouse.x}px, ${this.mouse.y}px, 0) translate(-50%, -50%)`;
    }

    if (this.cursorGlow) {
      this.cursorGlow.style.transform = `translate3d(${this.smoothMouse.x}px, ${this.smoothMouse.y}px, 0) translate(-50%, -50%)`;
    }

    if (this.torchLight) {
      this.torchLight.style.transform = `translate3d(${this.smoothMouse.x}px, ${this.smoothMouse.y}px, 0) translate(-50%, -50%)`;
    }

    // Smooth scroll update
    if (this.options.smoothScroll && this.scroll.isSmooth && this.scrollContainer) {
      this.scroll.current = lerp(this.scroll.current, this.scroll.target, this.scroll.ease);

      // Round to prevent subpixel rendering
      const roundedScroll = Math.round(this.scroll.current * 100) / 100;

      this.scrollContainer.style.transform = `translate3d(0, ${-roundedScroll}px, 0)`;
    }

    this.rafId = requestAnimationFrame(() => this.render());
  }

  _onMouseMove(e) {
    this.mouse.x = e.clientX;
    this.mouse.y = e.clientY;
  }

  _onResize() {
    if (this.scrollContainer) {
      document.body.style.height = `${this.scrollContainer.getBoundingClientRect().height}px`;
    }
  }

  /* ─────────────────────────────────────────────────────────────
     CUSTOM CURSOR - GPU 가속 + will-change
     ───────────────────────────────────────────────────────────── */
  initCursor() {
    // Create cursor
    this.cursor = document.createElement('div');
    this.cursor.className = 'cave-cursor';
    this.cursor.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      pointer-events: none;
      z-index: 10000;
      mix-blend-mode: difference;
      background: #e8e8e8;
      will-change: transform;
    `;
    document.body.appendChild(this.cursor);

    // Create glow
    this.cursorGlow = document.createElement('div');
    this.cursorGlow.className = 'cave-cursor-glow';
    this.cursorGlow.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 300px;
      height: 300px;
      border-radius: 50%;
      pointer-events: none;
      z-index: -1;
      background: radial-gradient(circle, rgba(255,107,53,0.08) 0%, transparent 70%);
      will-change: transform;
    `;
    document.body.appendChild(this.cursorGlow);

    // Hide default cursor
    document.body.style.cursor = 'none';

    // Hover states with scale transition
    const hoverElements = document.querySelectorAll('a, button, .cave-door, .magnetic, [data-cursor="hover"]');
    hoverElements.forEach(el => {
      el.style.cursor = 'none';

      el.addEventListener('mouseenter', () => {
        this.cursor.style.transform += ' scale(3)';
        this.cursor.style.mixBlendMode = 'normal';
        this.cursor.style.background = 'rgba(255,107,53,0.3)';
      });

      el.addEventListener('mouseleave', () => {
        this.cursor.style.mixBlendMode = 'difference';
        this.cursor.style.background = '#e8e8e8';
      });
    });

    // Visibility
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
     TORCH LIGHT - 진짜 횃불 느낌
     ───────────────────────────────────────────────────────────── */
  initTorchLight() {
    this.torchLight = document.createElement('div');
    this.torchLight.className = 'torch-light';
    this.torchLight.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 500px;
      height: 500px;
      border-radius: 50%;
      pointer-events: none;
      z-index: 1;
      background: radial-gradient(
        circle,
        rgba(255, 107, 53, 0.12) 0%,
        rgba(247, 147, 30, 0.06) 30%,
        transparent 60%
      );
      filter: blur(40px);
      mix-blend-mode: screen;
      will-change: transform;
    `;
    document.body.appendChild(this.torchLight);

    // Flicker effect
    this.flickerTorch();
  }

  flickerTorch() {
    if (!this.torchLight) return;

    const flicker = () => {
      const intensity = 0.9 + Math.random() * 0.2;
      this.torchLight.style.opacity = intensity;

      // Random interval for natural feel
      setTimeout(flicker, 50 + Math.random() * 100);
    };

    flicker();
  }

  /* ─────────────────────────────────────────────────────────────
     SMOOTH SCROLL - 진짜 Lenis 스타일
     ───────────────────────────────────────────────────────────── */
  initSmoothScroll() {
    // Check if Lenis is available - use it if so
    if (typeof Lenis !== 'undefined') {
      this.lenis = new Lenis({
        duration: 1.2,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
        orientation: 'vertical',
        smoothWheel: true
      });

      const lenisRaf = (time) => {
        this.lenis.raf(time);
        requestAnimationFrame(lenisRaf);
      };
      requestAnimationFrame(lenisRaf);

      return;
    }

    // Fallback: Custom smooth scroll implementation
    // Wrap content
    const body = document.body;
    const html = document.documentElement;

    // Check if already has scroll container
    if (document.querySelector('.cave-scroll-container')) {
      this.scrollContainer = document.querySelector('.cave-scroll-container');
    } else {
      // Create scroll container
      this.scrollContainer = document.createElement('div');
      this.scrollContainer.className = 'cave-scroll-container';
      this.scrollContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        will-change: transform;
      `;

      // Move body children to container
      while (body.firstChild) {
        this.scrollContainer.appendChild(body.firstChild);
      }
      body.appendChild(this.scrollContainer);
    }

    // Set body height
    setTimeout(() => {
      body.style.height = `${this.scrollContainer.getBoundingClientRect().height}px`;
    }, 100);

    // Listen for scroll
    window.addEventListener('scroll', () => {
      this.scroll.target = window.scrollY;
    }, { passive: true });

    // Smooth anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', (e) => {
        const href = anchor.getAttribute('href');
        if (href === '#') return;

        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
          const offset = target.getBoundingClientRect().top + this.scroll.current;
          this.scroll.target = offset;
          window.scrollTo(0, offset);
        }
      });
    });
  }

  /* ─────────────────────────────────────────────────────────────
     TEXT REVEAL - GSAP SplitText 스타일
     ───────────────────────────────────────────────────────────── */
  initTextReveal() {
    document.querySelectorAll('.text-reveal').forEach(el => {
      const text = el.textContent;
      const chars = text.split('');

      el.innerHTML = '';
      el.style.position = 'relative';

      chars.forEach((char, i) => {
        const span = document.createElement('span');
        span.className = 'char';
        span.textContent = char === ' ' ? '\u00A0' : char;
        span.style.cssText = `
          display: inline-block;
          opacity: 0;
          transform: translateY(100%) rotateX(-90deg);
          transform-origin: top center;
          animation: charReveal 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
          animation-delay: ${i * 0.03}s;
        `;
        el.appendChild(span);
      });
    });

    // Add keyframes if not exists
    if (!document.querySelector('#cave-text-reveal-styles')) {
      const style = document.createElement('style');
      style.id = 'cave-text-reveal-styles';
      style.textContent = `
        @keyframes charReveal {
          to {
            opacity: 1;
            transform: translateY(0) rotateX(0);
          }
        }
      `;
      document.head.appendChild(style);
    }
  }

  /* ─────────────────────────────────────────────────────────────
     SCROLL REVEAL - Intersection Observer + 스타일
     ───────────────────────────────────────────────────────────── */
  initScrollReveal() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          // Add stagger delay based on index
          const index = Array.from(entry.target.parentNode.children)
            .filter(el => el.classList.contains('scroll-reveal'))
            .indexOf(entry.target);

          entry.target.style.transitionDelay = `${index * 0.1}s`;
          entry.target.classList.add('revealed');
        }
      });
    }, {
      threshold: 0.15,
      rootMargin: '0px 0px -10% 0px'
    });

    document.querySelectorAll('.scroll-reveal').forEach(el => {
      // Initial state
      el.style.cssText += `
        opacity: 0;
        transform: translateY(60px);
        transition: opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1),
                    transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
      `;
      observer.observe(el);
    });

    // Add revealed styles
    if (!document.querySelector('#cave-scroll-reveal-styles')) {
      const style = document.createElement('style');
      style.id = 'cave-scroll-reveal-styles';
      style.textContent = `
        .scroll-reveal.revealed {
          opacity: 1 !important;
          transform: translateY(0) !important;
        }
      `;
      document.head.appendChild(style);
    }
  }

  /* ─────────────────────────────────────────────────────────────
     MAGNETIC BUTTONS - 제대로 된 구현
     ───────────────────────────────────────────────────────────── */
  initMagnetic() {
    document.querySelectorAll('.magnetic').forEach(el => {
      // Store original position
      const rect = el.getBoundingClientRect();

      el.style.cssText += `
        transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      `;

      el.addEventListener('mousemove', (e) => {
        const rect = el.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        const deltaX = e.clientX - centerX;
        const deltaY = e.clientY - centerY;

        // Magnetic pull (30% of distance)
        const moveX = deltaX * 0.3;
        const moveY = deltaY * 0.3;

        el.style.transform = `translate3d(${moveX}px, ${moveY}px, 0)`;
      });

      el.addEventListener('mouseleave', () => {
        el.style.transform = 'translate3d(0, 0, 0)';
      });
    });
  }

  /* ─────────────────────────────────────────────────────────────
     PAGE TRANSITIONS - 뒤로가기 지원
     ───────────────────────────────────────────────────────────── */
  initPageTransition() {
    // Create transition overlay
    const overlay = document.createElement('div');
    overlay.className = 'page-transition-overlay';
    overlay.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: #0a0a0a;
      z-index: 10001;
      pointer-events: none;
      transform: translateY(100%);
      transition: transform 0.6s cubic-bezier(0.7, 0, 0.3, 1);
    `;
    document.body.appendChild(overlay);

    // Intercept internal links
    document.querySelectorAll('a[href]').forEach(link => {
      const href = link.getAttribute('href');

      if (href &&
          !href.startsWith('#') &&
          !href.startsWith('http') &&
          !href.startsWith('mailto') &&
          !href.startsWith('tel')) {

        link.addEventListener('click', (e) => {
          e.preventDefault();

          // Start transition
          overlay.style.transform = 'translateY(0)';

          setTimeout(() => {
            window.location.href = href;
          }, 600);
        });
      }
    });

    // Handle page load (animate out)
    window.addEventListener('load', () => {
      // Check if coming from internal navigation
      if (document.referrer.includes(window.location.hostname) || sessionStorage.getItem('cave-transitioning')) {
        overlay.style.transform = 'translateY(0)';
        overlay.style.transition = 'none';

        requestAnimationFrame(() => {
          overlay.style.transition = 'transform 0.6s cubic-bezier(0.7, 0, 0.3, 1)';
          overlay.style.transform = 'translateY(-100%)';
        });

        sessionStorage.removeItem('cave-transitioning');
      }
    });

    // Handle back/forward
    window.addEventListener('pageshow', (e) => {
      if (e.persisted) {
        // Page was restored from cache
        overlay.style.transform = 'translateY(-100%)';
      }
    });

    // Mark as transitioning before unload
    window.addEventListener('beforeunload', () => {
      sessionStorage.setItem('cave-transitioning', 'true');
    });
  }

  /* ─────────────────────────────────────────────────────────────
     CLEANUP
     ───────────────────────────────────────────────────────────── */
  destroy() {
    this.stop();
    window.removeEventListener('mousemove', this._onMouseMove);
    window.removeEventListener('resize', this._onResize);

    // Remove created elements
    if (this.cursor) this.cursor.remove();
    if (this.cursorGlow) this.cursorGlow.remove();
    if (this.torchLight) this.torchLight.remove();

    document.body.style.cursor = '';
  }
}

/* ─────────────────────────────────────────────────────────────
   AUTO INIT
   ───────────────────────────────────────────────────────────── */
if (document.querySelector('[data-cave-effects]')) {
  window.caveEffects = new CaveEffects();
}

// Export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CaveEffects;
}

if (typeof window !== 'undefined') {
  window.CaveEffects = CaveEffects;
}
