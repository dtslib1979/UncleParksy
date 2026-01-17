/* ═══════════════════════════════════════════════════════════════
   DEPTH SYSTEM - 수직 지층 인터랙션
   "스크롤 = 더 깊이, 클릭 = 이동"
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
    labOutput: null
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
      transform: (text) => `[사유]\n${text}\n\n→ 이것이 의미하는 바는...`
    },
    blogger: {
      name: '블로거 박씨',
      icon: '📱',
      desc: 'PWA, 웹앱, 실험',
      transform: (text) => `## 오늘의 발견\n\n${text}\n\n---\n*GitHub Pages에서 확인*`
    },
    visualizer: {
      name: '시각화사 박씨',
      icon: '🎨',
      desc: '다이어그램, 프레임',
      transform: (text) => `┌─────────────┐\n│ ${text.substring(0, 20)}... │\n└─────────────┘`
    },
    musician: {
      name: '뮤지션 박씨',
      icon: '🎵',
      desc: '소리, 리듬, 캐스트',
      transform: (text) => `♪ ${text} ♪\n\n[tempo: 자유롭게]\n[mood: 실험적]`
    },
    technician: {
      name: '기능인 박씨',
      icon: '🔧',
      desc: '디바이스, 세팅, 해킹',
      transform: (text) => `[설정]\n- 입력: ${text.substring(0, 30)}...\n- 적용: 즉시\n- 결과: 확인 필요`
    }
  };

  const MERITS = {
    bluff: {
      name: 'Bluff',
      desc: '허세 · 과장',
      transform: (text) => text.toUpperCase() + '!!!'
    },
    halfblood: {
      name: 'Halfblood',
      desc: '반쪽 언어',
      transform: (text) => {
        // 간단한 한영 혼용 시뮬레이션
        const words = text.split(' ');
        return words.map((w, i) => i % 3 === 0 ? w : w).join(' ') + ' (반쪽)';
      }
    },
    aggro: {
      name: 'Aggro',
      desc: '어그로 · 직격',
      transform: (text) => `[직격]\n\n${text}\n\n그래서 어쩌라고?`
    },
    shaman: {
      name: 'Shaman',
      desc: '무속 · 신비',
      transform: (text) => `···\n\n${text}\n\n···\n\n(알 수 없는 기운이 감돈다)`
    }
  };

  /* ─────────────────────────────────────────────────────────────
     INIT: 초기화
     ───────────────────────────────────────────────────────────── */

  function init() {
    setupIntersectionObserver();
    setupSelectors();
    setupLaboratory();
    setupOutputActions();
    setupSurfaceButton();
    updateHUD();
  }

  /* ─────────────────────────────────────────────────────────────
     INTERSECTION OBSERVER: 현재 층 감지
     ───────────────────────────────────────────────────────────── */

  function setupIntersectionObserver() {
    const depths = document.querySelectorAll('.depth');

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && entry.intersectionRatio > 0.5) {
          const depthIndex = parseInt(entry.target.dataset.depth, 10);
          if (depthIndex !== state.currentDepth) {
            state.currentDepth = depthIndex;
            updateHUD();
          }
        }
      });
    }, {
      threshold: [0.5],
      rootMargin: '-10% 0px -10% 0px'
    });

    depths.forEach(depth => observer.observe(depth));
  }

  /* ─────────────────────────────────────────────────────────────
     HUD: 상단 표시 업데이트
     ───────────────────────────────────────────────────────────── */

  function updateHUD() {
    const indicator = document.querySelector('.depth-indicator');
    const surfaceBtn = document.querySelector('.surface-btn');
    const depth = DEPTHS[state.currentDepth];

    if (indicator && depth) {
      indicator.innerHTML = `
        <span class="current-depth">Depth ${state.currentDepth}</span>
        <span class="depth-name">/ ${depth.name}</span>
      `;
    }

    // Surface 버튼: Depth 0에서는 숨김
    if (surfaceBtn) {
      if (state.currentDepth > 0) {
        surfaceBtn.classList.add('visible');
      } else {
        surfaceBtn.classList.remove('visible');
      }
    }

    // body에 현재 depth 표시
    document.body.dataset.currentDepth = state.currentDepth;
  }

  function setupSurfaceButton() {
    const btn = document.querySelector('.surface-btn');
    if (!btn) return;

    btn.addEventListener('click', () => {
      const entrance = document.querySelector('#entrance');
      if (entrance) {
        entrance.scrollIntoView({ behavior: 'smooth' });
      }
    });
  }

  /* ─────────────────────────────────────────────────────────────
     SELECTORS: 페르소나 & 메리트 선택
     ───────────────────────────────────────────────────────────── */

  function setupSelectors() {
    // 페르소나 버튼 생성
    const personaGrid = document.querySelector('.selector-grid.personas');
    if (personaGrid) {
      personaGrid.innerHTML = '';
      Object.entries(PERSONAS).forEach(([key, persona]) => {
        const btn = document.createElement('button');
        btn.className = 'selector-btn';
        btn.dataset.persona = key;
        btn.innerHTML = `
          <span class="btn-icon">${persona.icon}</span>
          ${persona.name}
          <span class="btn-sub">${persona.desc}</span>
        `;
        btn.addEventListener('click', () => selectPersona(key, btn));
        personaGrid.appendChild(btn);
      });
    }

    // 메리트 버튼 생성
    const meritGrid = document.querySelector('.selector-grid.merits');
    if (meritGrid) {
      meritGrid.innerHTML = '';
      Object.entries(MERITS).forEach(([key, merit]) => {
        const btn = document.createElement('button');
        btn.className = 'selector-btn';
        btn.dataset.merit = key;
        btn.innerHTML = `
          ${merit.name}
          <span class="btn-sub">${merit.desc}</span>
        `;
        btn.addEventListener('click', () => selectMerit(key, btn));
        meritGrid.appendChild(btn);
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

    updateLabState();
  }

  function selectMerit(key, btn) {
    document.querySelectorAll('.selector-grid.merits .selector-btn').forEach(b => {
      b.classList.remove('selected');
    });

    btn.classList.add('selected');
    state.selectedMerit = key;
    document.body.dataset.merit = key;

    updateLabState();
  }

  /* ─────────────────────────────────────────────────────────────
     LABORATORY: 변환 실험실
     ───────────────────────────────────────────────────────────── */

  function setupLaboratory() {
    const processBtn = document.querySelector('.lab-process-btn');
    const textarea = document.querySelector('.lab-textarea');

    if (processBtn) {
      processBtn.addEventListener('click', processInput);
    }

    if (textarea) {
      textarea.addEventListener('input', updateLabState);
    }

    updateLabState();
  }

  function updateLabState() {
    const processBtn = document.querySelector('.lab-process-btn');
    const textarea = document.querySelector('.lab-textarea');

    if (!processBtn || !textarea) return;

    const hasInput = textarea.value.trim().length > 0;
    const hasSelection = state.selectedPersona && state.selectedMerit;

    processBtn.disabled = !(hasInput && hasSelection);

    if (!hasSelection) {
      processBtn.textContent = '↑ 먼저 위에서 선택하세요';
    } else if (!hasInput) {
      processBtn.textContent = '입력을 기다리는 중...';
    } else {
      processBtn.textContent = '변환하기';
    }
  }

  function processInput() {
    const textarea = document.querySelector('.lab-textarea');
    const outputArea = document.querySelector('.lab-output-area');
    const outputEl = document.querySelector('.lab-output');
    const outputMeta = document.querySelector('.lab-output-meta');

    if (!textarea || !outputArea || !outputEl) return;

    const input = textarea.value.trim();
    if (!input || !state.selectedPersona || !state.selectedMerit) return;

    const persona = PERSONAS[state.selectedPersona];
    const merit = MERITS[state.selectedMerit];

    // 변환 적용: Persona → Merit 순서
    let result = persona.transform(input);
    result = merit.transform(result);

    state.labOutput = result;

    // 출력 표시
    outputEl.textContent = result;
    outputArea.classList.add('has-content');

    if (outputMeta) {
      outputMeta.textContent = `${persona.name} × ${merit.name}`;
    }

    // Output 버튼 활성화
    updateOutputButtons();
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
      font-family: -apple-system, sans-serif;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 2rem;
    }
    .content {
      max-width: 600px;
      line-height: 1.8;
      white-space: pre-wrap;
    }
    .meta {
      margin-top: 2rem;
      font-size: 0.8rem;
      color: #666;
      border-top: 1px solid #333;
      padding-top: 1rem;
    }
  </style>
</head>
<body>
  <div class="content">${escapeHTML(state.labOutput)}<div class="meta">Generated by Parksy Engine<br>${persona.name} × ${merit.name}</div></div>
</body>
</html>`;

    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `parksy-${state.selectedPersona}-${state.selectedMerit}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
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
    });
  }

  function escapeHTML(str) {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  /* ─────────────────────────────────────────────────────────────
     BOOTSTRAP
     ───────────────────────────────────────────────────────────── */

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // 외부 접근용
  window.DepthSystem = {
    getState: () => ({ ...state }),
    getDepths: () => [...DEPTHS],
    scrollToDepth: (index) => {
      const depth = document.querySelector(`[data-depth="${index}"]`);
      if (depth) depth.scrollIntoView({ behavior: 'smooth' });
    }
  };

})();
