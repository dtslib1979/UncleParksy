/* ═══════════════════════════════════════════════════════════════
   DEPTH SYSTEM - 수직 지층 인터랙션 v2.0
   "스크롤 = 더 깊이, 클릭 = 이동"
   Apple Design Award 급 구현
   ═══════════════════════════════════════════════════════════════ */

(function() {
  'use strict';

  /* ─────────────────────────────────────────────────────────────
     STATE: 시스템 상태
     ───────────────────────────────────────────────────────────── */

  const state = {
    currentDepth: 0,
    selectedPersona: null,
    selectedMerit: null,
    labOutput: null,
    isAnimating: false,
    isMobile: window.innerWidth <= 768,
    reducedMotion: window.matchMedia('(prefers-reduced-motion: reduce)').matches
  };

  const DEPTHS = [
    { id: 'entrance', name: 'Entrance', label: '입구' },
    { id: 'selector', name: 'Selector', label: '선택' },
    { id: 'laboratory', name: 'Laboratory', label: '실험실' },
    { id: 'output', name: 'Output', label: '출력' }
  ];

  const PERSONAS = {
    philosopher: {
      name: '철학자 박씨',
      icon: '🤔',
      desc: '사고 실험, 반론, 구조화',
      color: '#6b8e9f',
      archiveUrl: '/category/Philosopher-Parksy/',
      transform: (text) => `[사유]\n\n${text}\n\n→ 이것이 의미하는 바는...\n→ 그러나 반론하자면...\n→ 결국 핵심은...`
    },
    blogger: {
      name: '블로거 박씨',
      icon: '📱',
      desc: 'PWA, 웹앱, 실험',
      color: '#8b7355',
      archiveUrl: '/category/Blogger-Parksy/',
      transform: (text) => `## 오늘의 발견\n\n${text}\n\n---\n\n### 다음 단계\n- [ ] 프로토타입 만들기\n- [ ] GitHub에 올리기\n- [ ] 피드백 받기`
    },
    visualizer: {
      name: '시각화사 박씨',
      icon: '🎨',
      desc: '다이어그램, 프레임',
      color: '#7a8b6b',
      archiveUrl: '/category/Visualizer-Parksy/',
      transform: (text) => {
        const lines = text.split('\n').filter(l => l.trim());
        const boxed = lines.map(l => `│ ${l.substring(0, 40).padEnd(40)} │`).join('\n');
        return `┌──────────────────────────────────────────┐\n${boxed}\n└──────────────────────────────────────────┘`;
      }
    },
    musician: {
      name: '뮤지션 박씨',
      icon: '🎵',
      desc: '소리, 리듬, 캐스트',
      color: '#8b6b7a',
      archiveUrl: '/category/Musician-Parksy/',
      transform: (text) => `♪ ♫ ♪\n\n${text}\n\n♪ ♫ ♪\n\n[tempo: rubato]\n[mood: 실험적]\n[key: 자유조]`
    },
    technician: {
      name: '기능인 박씨',
      icon: '🔧',
      desc: '디바이스, 세팅, 해킹',
      color: '#6b6b8b',
      archiveUrl: '/category/Technician-Parksy/',
      transform: (text) => `[SYSTEM LOG]\n\n> 입력 감지됨\n> 분석 중...\n\n${text}\n\n> 처리 완료\n> 적용: 즉시\n> 상태: READY`
    }
  };

  const MERITS = {
    bluff: {
      name: 'Bluff',
      desc: '허세 · 과장',
      transform: (text) => {
        return text.toUpperCase().replace(/\./g, '!!!').replace(/,/g, ' —') + '\n\n(이게 바로 진짜다)';
      }
    },
    halfblood: {
      name: 'Halfblood',
      desc: '반쪽 언어',
      transform: (text) => {
        // 한영 혼용 느낌
        const additions = [' (honestly)', ' 진짜로', ' you know', ' 솔직히'];
        let result = text;
        additions.forEach((add, i) => {
          const pos = Math.floor(result.length * (i + 1) / (additions.length + 1));
          result = result.slice(0, pos) + add + result.slice(pos);
        });
        return result;
      }
    },
    aggro: {
      name: 'Aggro',
      desc: '어그로 · 직격',
      transform: (text) => `[직격]\n\n${text}\n\n---\n\n근데 솔직히 말해서,\n이거 안 하면 어쩔 건데?\n\n할 거야, 말 거야?`
    },
    shaman: {
      name: 'Shaman',
      desc: '무속 · 신비',
      transform: (text) => `· · ·\n\n\n${text}\n\n\n· · ·\n\n\n(알 수 없는 기운이 감돈다)\n(무언가가 다가오고 있다)\n(준비하라)`
    }
  };

  // DOM 요소 캐시
  let elements = {};

  /* ─────────────────────────────────────────────────────────────
     INIT: 초기화
     ───────────────────────────────────────────────────────────── */

  function init() {
    cacheElements();
    setupDepthGauge();
    setupIntersectionObserver();
    setupSelectors();
    setupLaboratory();
    setupOutputActions();
    setupSurfaceButton();
    setupKeyboardNav();

    if (!state.reducedMotion) {
      setupTorchLight();
      setupParticles();
      setupTextAnimations();
      setupAmbientAudio();
    }

    // 초기 상태
    updateHUD();
    showInitialDepth();

    // 리사이즈 대응
    window.addEventListener('resize', debounce(handleResize, 200));
  }

  function cacheElements() {
    elements = {
      hud: document.querySelector('.depth-hud'),
      indicator: document.querySelector('.depth-indicator'),
      surfaceBtn: document.querySelector('.surface-btn'),
      depths: document.querySelectorAll('.depth'),
      personaGrid: document.querySelector('.selector-grid.personas'),
      meritGrid: document.querySelector('.selector-grid.merits'),
      labTextarea: document.querySelector('.lab-textarea'),
      labProcessBtn: document.querySelector('.lab-process-btn'),
      labOutputArea: document.querySelector('.lab-output-area'),
      labOutput: document.querySelector('.lab-output'),
      labOutputMeta: document.querySelector('.lab-output-meta')
    };
  }

  function showInitialDepth() {
    // 첫 번째 층 바로 보이기
    setTimeout(() => {
      const firstDepth = document.querySelector('[data-depth="0"]');
      if (firstDepth) {
        firstDepth.classList.add('visible');
      }
    }, 100);
  }

  /* ─────────────────────────────────────────────────────────────
     DEPTH GAUGE: 우측 깊이 인디케이터
     ───────────────────────────────────────────────────────────── */

  function setupDepthGauge() {
    // 이미 있으면 스킵
    if (document.querySelector('.depth-gauge')) return;

    const gauge = document.createElement('nav');
    gauge.className = 'depth-gauge';
    gauge.setAttribute('aria-label', 'Depth navigation');

    DEPTHS.forEach((depth, index) => {
      if (index > 0) {
        const line = document.createElement('div');
        line.className = 'depth-gauge-line';
        gauge.appendChild(line);
      }

      const dot = document.createElement('button');
      dot.className = 'depth-gauge-dot';
      dot.dataset.depth = index;
      dot.setAttribute('aria-label', `Go to ${depth.name}`);
      dot.title = depth.name;

      if (index === 0) dot.classList.add('active');

      dot.addEventListener('click', () => scrollToDepth(index));

      gauge.appendChild(dot);
    });

    document.body.appendChild(gauge);
  }

  function updateDepthGauge() {
    const dots = document.querySelectorAll('.depth-gauge-dot');
    dots.forEach((dot, index) => {
      dot.classList.toggle('active', index === state.currentDepth);
    });
  }

  /* ─────────────────────────────────────────────────────────────
     INTERSECTION OBSERVER: 현재 층 감지
     ───────────────────────────────────────────────────────────── */

  function setupIntersectionObserver() {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const depthIndex = parseInt(entry.target.dataset.depth, 10);

        // 층 전환 효과
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');

          if (entry.intersectionRatio > 0.5 && depthIndex !== state.currentDepth) {
            state.currentDepth = depthIndex;
            updateHUD();
            updateDepthGauge();
            onDepthChange(depthIndex);
          }
        }
      });
    }, {
      threshold: [0, 0.25, 0.5, 0.75, 1],
      rootMargin: '-5% 0px -5% 0px'
    });

    elements.depths.forEach(depth => observer.observe(depth));
  }

  function onDepthChange(index) {
    // 깊이 변경 시 추가 효과
    document.body.dataset.currentDepth = index;

    // 진동 피드백 (모바일)
    if (navigator.vibrate && state.isMobile) {
      navigator.vibrate(10);
    }

    // 앰비언트 사운드 볼륨 조절
    updateAmbientVolume(index);
  }

  /* ─────────────────────────────────────────────────────────────
     HUD: 상단 표시 업데이트
     ───────────────────────────────────────────────────────────── */

  function updateHUD() {
    const depth = DEPTHS[state.currentDepth];

    if (elements.indicator && depth) {
      elements.indicator.innerHTML = `
        <span class="current-depth">Depth ${state.currentDepth}</span>
        <span class="depth-name">/ ${depth.name}</span>
      `;
    }

    // Surface 버튼
    if (elements.surfaceBtn) {
      elements.surfaceBtn.classList.toggle('visible', state.currentDepth > 0);
    }
  }

  function setupSurfaceButton() {
    if (!elements.surfaceBtn) return;

    elements.surfaceBtn.addEventListener('click', () => {
      scrollToDepth(0);
    });
  }

  function scrollToDepth(index) {
    const depth = document.querySelector(`[data-depth="${index}"]`);
    if (depth) {
      depth.scrollIntoView({ behavior: state.reducedMotion ? 'auto' : 'smooth' });
    }
  }

  /* ─────────────────────────────────────────────────────────────
     KEYBOARD NAVIGATION
     ───────────────────────────────────────────────────────────── */

  function setupKeyboardNav() {
    document.addEventListener('keydown', (e) => {
      // Arrow keys for depth navigation
      if (e.key === 'ArrowDown' && state.currentDepth < DEPTHS.length - 1) {
        e.preventDefault();
        scrollToDepth(state.currentDepth + 1);
      } else if (e.key === 'ArrowUp' && state.currentDepth > 0) {
        e.preventDefault();
        scrollToDepth(state.currentDepth - 1);
      }

      // Escape to go to surface
      if (e.key === 'Escape' && state.currentDepth > 0) {
        scrollToDepth(0);
      }
    });
  }

  /* ─────────────────────────────────────────────────────────────
     SELECTORS: 페르소나 & 메리트 선택
     ───────────────────────────────────────────────────────────── */

  function setupSelectors() {
    // 페르소나 버튼 생성
    if (elements.personaGrid) {
      elements.personaGrid.innerHTML = '';
      Object.entries(PERSONAS).forEach(([key, persona], index) => {
        const btn = document.createElement('button');
        btn.className = 'selector-btn';
        btn.dataset.persona = key;
        btn.dataset.archiveUrl = persona.archiveUrl;
        btn.style.animationDelay = `${index * 0.1}s`;
        btn.innerHTML = `
          <span class="btn-icon">${persona.icon}</span>
          ${persona.name}
          <span class="btn-sub">${persona.desc}</span>
        `;
        btn.addEventListener('click', () => selectPersona(key, btn));
        // 더블클릭으로 아카이브 이동
        btn.addEventListener('dblclick', () => {
          if (persona.archiveUrl) {
            window.location.href = persona.archiveUrl;
          }
        });
        elements.personaGrid.appendChild(btn);
      });
    }

    // 메리트 버튼 생성
    if (elements.meritGrid) {
      elements.meritGrid.innerHTML = '';
      Object.entries(MERITS).forEach(([key, merit], index) => {
        const btn = document.createElement('button');
        btn.className = 'selector-btn';
        btn.dataset.merit = key;
        btn.style.animationDelay = `${index * 0.1}s`;
        btn.innerHTML = `
          ${merit.name}
          <span class="btn-sub">${merit.desc}</span>
        `;
        btn.addEventListener('click', () => selectMerit(key, btn));
        elements.meritGrid.appendChild(btn);
      });
    }
  }

  function selectPersona(key, btn) {
    // 기존 선택 해제
    document.querySelectorAll('.selector-grid.personas .selector-btn').forEach(b => {
      b.classList.remove('selected');
    });

    // 새 선택
    btn.classList.add('selected');
    state.selectedPersona = key;
    document.body.dataset.persona = key;

    // 선택 피드백 - 파티클 burst
    if (!state.reducedMotion) {
      createSelectionBurst(btn);
    }

    // 진동
    if (navigator.vibrate) navigator.vibrate(20);

    updateLabState();
  }

  function selectMerit(key, btn) {
    document.querySelectorAll('.selector-grid.merits .selector-btn').forEach(b => {
      b.classList.remove('selected');
    });

    btn.classList.add('selected');
    state.selectedMerit = key;
    document.body.dataset.merit = key;

    if (!state.reducedMotion) {
      createSelectionBurst(btn);
    }

    if (navigator.vibrate) navigator.vibrate(20);

    updateLabState();
  }

  // 선택 시 파티클 burst 효과
  function createSelectionBurst(element) {
    const rect = element.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;

    for (let i = 0; i < 8; i++) {
      const particle = document.createElement('div');
      particle.style.cssText = `
        position: fixed;
        left: ${centerX}px;
        top: ${centerY}px;
        width: 4px;
        height: 4px;
        background: var(--flame-edge);
        border-radius: 50%;
        pointer-events: none;
        z-index: 10000;
      `;

      const angle = (i / 8) * Math.PI * 2;
      const distance = 50 + Math.random() * 30;
      const duration = 400 + Math.random() * 200;

      document.body.appendChild(particle);

      particle.animate([
        {
          transform: 'translate(-50%, -50%) scale(1)',
          opacity: 1
        },
        {
          transform: `translate(calc(-50% + ${Math.cos(angle) * distance}px), calc(-50% + ${Math.sin(angle) * distance}px)) scale(0)`,
          opacity: 0
        }
      ], {
        duration: duration,
        easing: 'cubic-bezier(0.16, 1, 0.3, 1)',
        fill: 'forwards'
      }).onfinish = () => particle.remove();
    }
  }

  /* ─────────────────────────────────────────────────────────────
     LABORATORY: 변환 실험실
     ───────────────────────────────────────────────────────────── */

  function setupLaboratory() {
    if (elements.labProcessBtn) {
      elements.labProcessBtn.addEventListener('click', processInput);
    }

    if (elements.labTextarea) {
      elements.labTextarea.addEventListener('input', updateLabState);

      // 포커스 시 효과
      elements.labTextarea.addEventListener('focus', () => {
        elements.labTextarea.parentElement.classList.add('focused');
      });

      elements.labTextarea.addEventListener('blur', () => {
        elements.labTextarea.parentElement.classList.remove('focused');
      });
    }

    updateLabState();
  }

  function updateLabState() {
    if (!elements.labProcessBtn || !elements.labTextarea) return;

    const hasInput = elements.labTextarea.value.trim().length > 0;
    const hasSelection = state.selectedPersona && state.selectedMerit;

    elements.labProcessBtn.disabled = !(hasInput && hasSelection);

    if (!hasSelection) {
      elements.labProcessBtn.textContent = '↑ 먼저 위에서 선택하세요';
    } else if (!hasInput) {
      elements.labProcessBtn.textContent = '입력을 기다리는 중...';
    } else {
      elements.labProcessBtn.textContent = '변환하기';
    }
  }

  function processInput() {
    if (!elements.labTextarea || !elements.labOutputArea || !elements.labOutput) return;

    const input = elements.labTextarea.value.trim();
    if (!input || !state.selectedPersona || !state.selectedMerit) return;

    const persona = PERSONAS[state.selectedPersona];
    const merit = MERITS[state.selectedMerit];

    // 처리 중 표시
    elements.labProcessBtn.textContent = '처리 중...';
    elements.labProcessBtn.disabled = true;

    // 약간의 딜레이로 "처리 중" 느낌
    setTimeout(() => {
      // 변환 적용: Persona → Merit 순서
      let result = persona.transform(input);
      result = merit.transform(result);

      state.labOutput = result;

      // 타이핑 효과로 출력
      if (!state.reducedMotion) {
        typeText(elements.labOutput, result, () => {
          elements.labOutputArea.classList.add('has-content');
          if (elements.labOutputMeta) {
            elements.labOutputMeta.textContent = `${persona.name} × ${merit.name}`;
          }
          updateOutputButtons();
          updateLabState();
        });
      } else {
        elements.labOutput.textContent = result;
        elements.labOutputArea.classList.add('has-content');
        if (elements.labOutputMeta) {
          elements.labOutputMeta.textContent = `${persona.name} × ${merit.name}`;
        }
        updateOutputButtons();
        updateLabState();
      }

    }, 500);
  }

  // 타이핑 효과
  function typeText(element, text, callback) {
    element.textContent = '';
    let index = 0;
    const speed = Math.max(5, 20 - text.length / 50); // 긴 텍스트는 빠르게

    function type() {
      if (index < text.length) {
        element.textContent += text.charAt(index);
        index++;
        setTimeout(type, speed);
      } else if (callback) {
        callback();
      }
    }

    type();
  }

  /* ─────────────────────────────────────────────────────────────
     OUTPUT: 저장/배포 액션
     ───────────────────────────────────────────────────────────── */

  function setupOutputActions() {
    const downloadBtn = document.querySelector('[data-action="download"]');
    const copyBtn = document.querySelector('[data-action="copy"]');

    if (downloadBtn) {
      downloadBtn.addEventListener('click', downloadAsHTML);
    }

    if (copyBtn) {
      copyBtn.addEventListener('click', copyToClipboard);
    }

    updateOutputButtons();
  }

  function updateOutputButtons() {
    const hasOutput = !!state.labOutput;
    document.querySelectorAll('.output-btn[data-action]').forEach(btn => {
      btn.disabled = !hasOutput;
    });
  }

  function downloadAsHTML() {
    if (!state.labOutput) return;

    const persona = PERSONAS[state.selectedPersona];
    const merit = MERITS[state.selectedMerit];

    const html = `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${persona.name} × ${merit.name} | Parksy Engine</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: #0a0a0a;
      color: #e8e8e8;
      font-family: 'Pretendard', -apple-system, sans-serif;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 2rem;
    }
    .container {
      max-width: 600px;
      width: 100%;
    }
    .content {
      line-height: 1.8;
      white-space: pre-wrap;
      font-size: 1.1rem;
    }
    .meta {
      margin-top: 3rem;
      font-size: 0.8rem;
      color: #666;
      border-top: 1px solid #222;
      padding-top: 1rem;
    }
    .meta a {
      color: #f7931e;
      text-decoration: none;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="content">${escapeHTML(state.labOutput)}</div>
    <div class="meta">
      Generated by <a href="https://parksy.kr" target="_blank">Parksy Engine</a><br>
      ${persona.name} × ${merit.name}
    </div>
  </div>
</body>
</html>`;

    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `parksy-${state.selectedPersona}-${state.selectedMerit}-${Date.now()}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    // 피드백
    showToast('HTML 파일 다운로드 완료');
  }

  function copyToClipboard() {
    if (!state.labOutput) return;

    navigator.clipboard.writeText(state.labOutput).then(() => {
      const btn = document.querySelector('[data-action="copy"]');
      if (btn) {
        const original = btn.innerHTML;
        btn.innerHTML = '복사됨! <span class="btn-arrow">✓</span>';
        setTimeout(() => { btn.innerHTML = original; }, 2000);
      }
      showToast('클립보드에 복사됨');
    });
  }

  // 토스트 메시지
  function showToast(message) {
    const existing = document.querySelector('.depth-toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'depth-toast';
    toast.textContent = message;
    toast.style.cssText = `
      position: fixed;
      bottom: 80px;
      left: 50%;
      transform: translateX(-50%) translateY(20px);
      background: rgba(247, 147, 30, 0.9);
      color: #0a0a0a;
      padding: 12px 24px;
      border-radius: 4px;
      font-size: 0.9rem;
      font-weight: 600;
      z-index: 10001;
      opacity: 0;
      transition: all 0.3s ease;
    `;

    document.body.appendChild(toast);

    requestAnimationFrame(() => {
      toast.style.opacity = '1';
      toast.style.transform = 'translateX(-50%) translateY(0)';
    });

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(-50%) translateY(20px)';
      setTimeout(() => toast.remove(), 300);
    }, 2000);
  }

  function escapeHTML(str) {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  /* ─────────────────────────────────────────────────────────────
     TORCH LIGHT: 마우스/터치 따라다니는 횃불 조명
     ───────────────────────────────────────────────────────────── */

  let torchLight = null;
  let mouseX = window.innerWidth / 2;
  let mouseY = window.innerHeight / 2;
  let currentX = mouseX;
  let currentY = mouseY;

  function setupTorchLight() {
    torchLight = document.createElement('div');
    torchLight.className = 'torch-light-effect';

    if (state.isMobile) {
      // 모바일: 터치 포인트에 반짝이는 효과
      setupMobileTorchLight();
    } else {
      // 데스크탑: 마우스 따라다니는 효과
      setupDesktopTorchLight();
    }
  }

  function setupDesktopTorchLight() {
    torchLight.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 400px;
      height: 400px;
      border-radius: 50%;
      pointer-events: none;
      z-index: 1;
      background: radial-gradient(
        circle,
        rgba(255, 107, 53, 0.08) 0%,
        rgba(247, 147, 30, 0.04) 30%,
        transparent 60%
      );
      filter: blur(40px);
      mix-blend-mode: screen;
      will-change: transform;
      transform: translate(-50%, -50%);
    `;
    document.body.appendChild(torchLight);

    document.addEventListener('mousemove', (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    }, { passive: true });

    // 부드러운 따라다니기 + 깜빡임
    function animateTorch() {
      // Lerp
      currentX += (mouseX - currentX) * 0.1;
      currentY += (mouseY - currentY) * 0.1;

      // 자연스러운 깜빡임
      const flicker = 0.9 + Math.random() * 0.15;

      torchLight.style.transform = `translate(${currentX - 200}px, ${currentY - 200}px)`;
      torchLight.style.opacity = flicker;

      requestAnimationFrame(animateTorch);
    }

    animateTorch();
  }

  function setupMobileTorchLight() {
    // 모바일: 터치 시 해당 위치에 일시적 조명 효과
    document.addEventListener('touchstart', (e) => {
      const touch = e.touches[0];
      createTouchGlow(touch.clientX, touch.clientY);
    }, { passive: true });

    document.addEventListener('touchmove', (e) => {
      const touch = e.touches[0];
      createTouchGlow(touch.clientX, touch.clientY, true);
    }, { passive: true });
  }

  function createTouchGlow(x, y, isMove = false) {
    const glow = document.createElement('div');
    glow.style.cssText = `
      position: fixed;
      left: ${x}px;
      top: ${y}px;
      width: ${isMove ? 150 : 250}px;
      height: ${isMove ? 150 : 250}px;
      border-radius: 50%;
      pointer-events: none;
      z-index: 1;
      background: radial-gradient(
        circle,
        rgba(255, 107, 53, ${isMove ? 0.06 : 0.12}) 0%,
        rgba(247, 147, 30, 0.04) 40%,
        transparent 70%
      );
      filter: blur(30px);
      mix-blend-mode: screen;
      transform: translate(-50%, -50%);
      opacity: 1;
      transition: opacity 0.8s ease-out, transform 0.8s ease-out;
    `;
    document.body.appendChild(glow);

    // 페이드 아웃
    requestAnimationFrame(() => {
      glow.style.opacity = '0';
      glow.style.transform = 'translate(-50%, -50%) scale(1.5)';
    });

    setTimeout(() => glow.remove(), 800);
  }

  /* ─────────────────────────────────────────────────────────────
     PARTICLES: 떠다니는 불씨/먼지
     ───────────────────────────────────────────────────────────── */

  function setupParticles() {
    const container = document.createElement('div');
    container.className = 'depth-particles';
    document.body.appendChild(container);

    const particleCount = state.isMobile ? 8 : 15;

    function createParticle() {
      const particle = document.createElement('div');
      particle.className = 'particle';

      const startX = Math.random() * 100;
      const size = 1 + Math.random() * 2;
      const duration = 6 + Math.random() * 4;
      const delay = Math.random() * 5;

      particle.style.cssText = `
        left: ${startX}vw;
        bottom: -10px;
        width: ${size}px;
        height: ${size}px;
        animation-duration: ${duration}s;
        animation-delay: ${delay}s;
      `;

      container.appendChild(particle);

      // 애니메이션 끝나면 재생성
      setTimeout(() => {
        particle.remove();
        createParticle();
      }, (duration + delay) * 1000);
    }

    for (let i = 0; i < particleCount; i++) {
      setTimeout(() => createParticle(), i * 300);
    }
  }

  /* ─────────────────────────────────────────────────────────────
     TEXT ANIMATIONS: 글자별 등장 효과
     ───────────────────────────────────────────────────────────── */

  function setupTextAnimations() {
    // entrance-monument 텍스트 애니메이션
    const monument = document.querySelector('.entrance-monument');
    if (monument) {
      const html = monument.innerHTML;

      // HTML 태그와 텍스트를 분리
      const tokens = html.split(/(<[^>]+>)/g).filter(Boolean);
      let charIndex = 0;

      const animated = tokens.map(token => {
        // HTML 태그는 그대로 유지
        if (token.startsWith('<')) {
          return token;
        }

        // 텍스트는 글자별로 애니메이션
        return token.split('').map(char => {
          if (char === ' ' || char === '\n') {
            return char;
          }

          const delay = charIndex * 0.08;
          charIndex++;

          return `<span class="char-animate" style="animation-delay:${delay}s">${char}</span>`;
        }).join('');
      }).join('');

      monument.innerHTML = animated;

      // 스타일 주입
      if (!document.querySelector('#char-reveal-style')) {
        const style = document.createElement('style');
        style.id = 'char-reveal-style';
        style.textContent = `
          .char-animate {
            display: inline-block;
            opacity: 0;
            transform: translateY(30px) rotate(-5deg);
            animation: charReveal 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
          }
          @keyframes charReveal {
            to {
              opacity: 1;
              transform: translateY(0) rotate(0deg);
            }
          }
        `;
        document.head.appendChild(style);
      }
    }

    // entrance-statement도 애니메이션 적용
    const statement = document.querySelector('.entrance-statement');
    if (statement) {
      statement.style.opacity = '0';
      statement.style.transform = 'translateY(20px)';
      statement.style.transition = 'opacity 1s ease 1.5s, transform 1s ease 1.5s';

      setTimeout(() => {
        statement.style.opacity = '1';
        statement.style.transform = 'translateY(0)';
      }, 100);
    }
  }

  /* ─────────────────────────────────────────────────────────────
     AMBIENT AUDIO: Web Audio API 프로시저럴 동굴 사운드
     ───────────────────────────────────────────────────────────── */

  let audioContext = null;
  let ambientNodes = {
    drone: null,
    noise: null,
    masterGain: null
  };
  let audioInitialized = false;

  function setupAmbientAudio() {
    // 사용자 인터랙션 후 시작
    const initOnInteraction = () => {
      if (!audioInitialized) {
        initAudio();
        audioInitialized = true;
      }
    };
    document.addEventListener('click', initOnInteraction, { once: true });
    document.addEventListener('touchstart', initOnInteraction, { once: true });
  }

  function initAudio() {
    try {
      audioContext = new (window.AudioContext || window.webkitAudioContext)();

      // 마스터 게인
      ambientNodes.masterGain = audioContext.createGain();
      ambientNodes.masterGain.gain.value = 0.08;
      ambientNodes.masterGain.connect(audioContext.destination);

      // 1. 저주파 드론 (동굴 울림)
      const droneOsc = audioContext.createOscillator();
      droneOsc.type = 'sine';
      droneOsc.frequency.value = 55; // 저주파

      const droneGain = audioContext.createGain();
      droneGain.gain.value = 0.3;

      const droneFilter = audioContext.createBiquadFilter();
      droneFilter.type = 'lowpass';
      droneFilter.frequency.value = 100;

      droneOsc.connect(droneFilter);
      droneFilter.connect(droneGain);
      droneGain.connect(ambientNodes.masterGain);
      droneOsc.start();
      ambientNodes.drone = { osc: droneOsc, gain: droneGain };

      // 2. 필터드 노이즈 (바람/공기)
      const bufferSize = 2 * audioContext.sampleRate;
      const noiseBuffer = audioContext.createBuffer(1, bufferSize, audioContext.sampleRate);
      const output = noiseBuffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        output[i] = Math.random() * 2 - 1;
      }

      const noise = audioContext.createBufferSource();
      noise.buffer = noiseBuffer;
      noise.loop = true;

      const noiseFilter = audioContext.createBiquadFilter();
      noiseFilter.type = 'bandpass';
      noiseFilter.frequency.value = 400;
      noiseFilter.Q.value = 0.5;

      const noiseGain = audioContext.createGain();
      noiseGain.gain.value = 0.15;

      noise.connect(noiseFilter);
      noiseFilter.connect(noiseGain);
      noiseGain.connect(ambientNodes.masterGain);
      noise.start();
      ambientNodes.noise = { source: noise, gain: noiseGain, filter: noiseFilter };

      // 3. LFO로 미묘한 변화 (숨쉬는 느낌)
      const lfo = audioContext.createOscillator();
      lfo.type = 'sine';
      lfo.frequency.value = 0.1; // 아주 느리게

      const lfoGain = audioContext.createGain();
      lfoGain.gain.value = 0.02;

      lfo.connect(lfoGain);
      lfoGain.connect(ambientNodes.masterGain.gain);
      lfo.start();

      // 페이드 인
      ambientNodes.masterGain.gain.setValueAtTime(0, audioContext.currentTime);
      ambientNodes.masterGain.gain.linearRampToValueAtTime(0.08, audioContext.currentTime + 2);

    } catch (e) {
      console.log('Audio not supported');
    }
  }

  function updateAmbientVolume(depthIndex) {
    if (!ambientNodes.masterGain || !audioContext) return;

    // 깊이에 따라 특성 변화
    const baseVolume = 0.05 + (depthIndex * 0.03);
    const targetVolume = Math.min(baseVolume, 0.15);

    ambientNodes.masterGain.gain.linearRampToValueAtTime(
      targetVolume,
      audioContext.currentTime + 0.5
    );

    // 깊을수록 드론 주파수 낮아짐
    if (ambientNodes.drone) {
      const droneFreq = 55 - (depthIndex * 10);
      ambientNodes.drone.osc.frequency.linearRampToValueAtTime(
        droneFreq,
        audioContext.currentTime + 0.5
      );
    }

    // 깊을수록 노이즈 필터 좁아짐 (더 먹먹해짐)
    if (ambientNodes.noise) {
      const noiseFreq = 400 - (depthIndex * 50);
      ambientNodes.noise.filter.frequency.linearRampToValueAtTime(
        noiseFreq,
        audioContext.currentTime + 0.5
      );
    }
  }

  /* ─────────────────────────────────────────────────────────────
     UTILITIES
     ───────────────────────────────────────────────────────────── */

  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  function handleResize() {
    state.isMobile = window.innerWidth <= 768;
  }

  /* ─────────────────────────────────────────────────────────────
     BOOTSTRAP
     ───────────────────────────────────────────────────────────── */

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // 외부 접근용 API
  window.DepthSystem = {
    getState: () => ({ ...state }),
    getDepths: () => [...DEPTHS],
    scrollToDepth: scrollToDepth,
    getCurrentDepth: () => state.currentDepth
  };

})();
