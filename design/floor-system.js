/**
 * ═══════════════════════════════════════════════════════════════
 * FLOOR SYSTEM - 층 기반 네비게이션
 * 입구에서 각 층으로 이동하는 구조
 * ═══════════════════════════════════════════════════════════════
 */

(function() {
  'use strict';

  // ─────────────────────────────────────────────────────────────
  // 설정
  // ─────────────────────────────────────────────────────────────
  const FLOORS = {
    1: { code: '1', name: 'B1 · 쇼룸' },
    2: { code: '2', name: 'B2 · 실험실' },
    3: { code: 'parksy', name: 'B3 · 콘솔' }
  };

  const PERSONAS = [
    { id: 'philosopher', name: '철학자 박씨', icon: '🤔', desc: '본질을 파고드는 사유', archiveUrl: '/category/Philosopher-Parksy/' },
    { id: 'blogger', name: '블로거 박씨', icon: '📝', desc: '일상의 기록과 에세이', archiveUrl: '/category/Blogger-Parksy/' },
    { id: 'visualizer', name: '시각화사 박씨', icon: '🎨', desc: '데이터와 개념의 시각화', archiveUrl: '/category/Visualizer-Parksy/' },
    { id: 'musician', name: '뮤지션 박씨', icon: '🎵', desc: '음악 큐레이션과 감상', archiveUrl: '/category/Musician-Parksy/' },
    { id: 'technician', name: '기능인 박씨', icon: '🔧', desc: '기술 튜토리얼과 도구', archiveUrl: '/category/Technician-Parksy/' }
  ];

  const MERITS = [
    { id: 'bluff', name: 'Bluff', desc: '허세와 과장의 미학' },
    { id: 'halfblood', name: 'Halfblood', desc: '경계인의 관점' },
    { id: 'aggro', name: 'Aggro', desc: '공격적 직설화법' },
    { id: 'shaman', name: 'Shaman', desc: '영적이고 신비로운' }
  ];

  const STORAGE_KEY = 'parksy-unlocked-floors';

  // ─────────────────────────────────────────────────────────────
  // 상태
  // ─────────────────────────────────────────────────────────────
  let unlockedFloors = new Set();
  let currentFloor = null;
  let pendingFloor = null;
  let selectedPersona = null;
  let selectedMerit = null;
  let lastOutput = '';

  // ─────────────────────────────────────────────────────────────
  // DOM 요소
  // ─────────────────────────────────────────────────────────────
  const entrance = document.getElementById('entrance');
  const floors = document.querySelectorAll('.floor');
  const floorGates = document.querySelectorAll('.floor-gate');
  const gateOverlay = document.getElementById('gate-overlay');
  const gateInput = document.getElementById('gate-input');
  const gateError = document.getElementById('gate-error');
  const gateFloorTarget = document.querySelector('.gate-floor-target');
  const gateHintText = document.querySelector('.gate-hint-text');
  const gateSubmit = document.querySelector('.gate-submit');
  const gateCancel = document.querySelector('.gate-cancel');
  const backButtons = document.querySelectorAll('.back-to-entrance');
  const particles = document.querySelector('.particles');

  // ─────────────────────────────────────────────────────────────
  // 초기화
  // ─────────────────────────────────────────────────────────────
  function init() {
    loadUnlockedFloors();
    updateGateVisuals();
    setupFloorGates();
    setupGateModal();
    setupBackButtons();
    createParticles();
    setupLaboratory();
    initAmbientAudio();

    // URL hash 체크
    const hash = window.location.hash;
    if (hash && hash.startsWith('#floor-')) {
      const floorNum = parseInt(hash.replace('#floor-', ''));
      if (unlockedFloors.has(floorNum)) {
        navigateToFloor(floorNum);
      }
    }
  }

  // ─────────────────────────────────────────────────────────────
  // 잠금 상태 관리
  // ─────────────────────────────────────────────────────────────
  function loadUnlockedFloors() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        unlockedFloors = new Set(parsed);
      }
    } catch (e) {
      console.warn('Failed to load unlocked floors:', e);
    }
  }

  function saveUnlockedFloors() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify([...unlockedFloors]));
    } catch (e) {
      console.warn('Failed to save unlocked floors:', e);
    }
  }

  function unlockFloor(floorNum) {
    unlockedFloors.add(floorNum);
    saveUnlockedFloors();
    updateGateVisuals();
  }

  function updateGateVisuals() {
    floorGates.forEach(gate => {
      const floorNum = parseInt(gate.dataset.floor);
      if (unlockedFloors.has(floorNum)) {
        gate.classList.add('unlocked');
      } else {
        gate.classList.remove('unlocked');
      }
    });
  }

  // ─────────────────────────────────────────────────────────────
  // 층 게이트 설정
  // ─────────────────────────────────────────────────────────────
  function setupFloorGates() {
    floorGates.forEach(gate => {
      gate.addEventListener('click', () => {
        const floorNum = parseInt(gate.dataset.floor);

        if (unlockedFloors.has(floorNum)) {
          // 이미 해제됨 - 바로 이동
          navigateToFloor(floorNum);
        } else {
          // 게이트 모달 표시
          showGateModal(floorNum, gate.dataset.hint);
        }
      });
    });
  }

  // ─────────────────────────────────────────────────────────────
  // 게이트 모달
  // ─────────────────────────────────────────────────────────────
  function setupGateModal() {
    gateSubmit.addEventListener('click', submitGate);
    gateCancel.addEventListener('click', hideGateModal);

    gateInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        submitGate();
      } else if (e.key === 'Escape') {
        hideGateModal();
      }
    });

    gateOverlay.addEventListener('click', (e) => {
      if (e.target === gateOverlay) {
        hideGateModal();
      }
    });
  }

  function showGateModal(floorNum, hint) {
    pendingFloor = floorNum;
    gateFloorTarget.textContent = `B${floorNum}`;
    gateHintText.textContent = hint || '';
    gateInput.value = '';
    gateError.textContent = '';

    gateOverlay.classList.add('visible');
    gateOverlay.setAttribute('aria-hidden', 'false');
    setTimeout(() => gateInput.focus(), 100);
  }

  function hideGateModal() {
    gateOverlay.classList.remove('visible');
    gateOverlay.setAttribute('aria-hidden', 'true');
    pendingFloor = null;
  }

  function submitGate() {
    if (!pendingFloor) return;

    const floor = FLOORS[pendingFloor];
    const input = gateInput.value.toLowerCase().trim();

    if (input === floor.code.toLowerCase()) {
      // 정답
      unlockFloor(pendingFloor);
      hideGateModal();
      navigateToFloor(pendingFloor);
    } else {
      // 오답
      gateError.textContent = '잘못된 암호입니다';
      gateInput.classList.add('shake');
      setTimeout(() => gateInput.classList.remove('shake'), 500);
    }
  }

  // ─────────────────────────────────────────────────────────────
  // 층 네비게이션
  // ─────────────────────────────────────────────────────────────
  function navigateToFloor(floorNum) {
    currentFloor = floorNum;

    // 입구 숨기기
    entrance.classList.add('hidden');

    // 모든 층 숨기기
    floors.forEach(f => f.classList.add('floor-hidden'));

    // 해당 층 표시
    const floor = document.getElementById(`floor-${floorNum}`);
    if (floor) {
      floor.classList.remove('floor-hidden');
      window.scrollTo(0, 0);
      history.pushState(null, '', `#floor-${floorNum}`);
    }
  }

  function navigateToEntrance() {
    currentFloor = null;

    // 모든 층 숨기기
    floors.forEach(f => f.classList.add('floor-hidden'));

    // 입구 표시
    entrance.classList.remove('hidden');
    window.scrollTo(0, 0);
    history.pushState(null, '', '/');
  }

  function setupBackButtons() {
    backButtons.forEach(btn => {
      btn.addEventListener('click', navigateToEntrance);
    });

    // 브라우저 뒤로가기 처리
    window.addEventListener('popstate', () => {
      const hash = window.location.hash;
      if (hash && hash.startsWith('#floor-')) {
        const floorNum = parseInt(hash.replace('#floor-', ''));
        if (unlockedFloors.has(floorNum)) {
          navigateToFloor(floorNum);
        } else {
          navigateToEntrance();
        }
      } else {
        navigateToEntrance();
      }
    });
  }

  // ─────────────────────────────────────────────────────────────
  // 파티클 효과
  // ─────────────────────────────────────────────────────────────
  function createParticles() {
    if (!particles) return;

    const count = 15;
    for (let i = 0; i < count; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.left = `${Math.random() * 100}%`;
      particle.style.animationDelay = `${Math.random() * 8}s`;
      particle.style.animationDuration = `${6 + Math.random() * 4}s`;
      particles.appendChild(particle);
    }
  }

  // ─────────────────────────────────────────────────────────────
  // 실험실 기능
  // ─────────────────────────────────────────────────────────────
  function setupLaboratory() {
    const personasGrid = document.querySelector('.selector-grid.personas');
    const meritsGrid = document.querySelector('.selector-grid.merits');
    const textarea = document.querySelector('.lab-textarea');
    const processBtn = document.querySelector('.lab-process-btn');
    const outputArea = document.querySelector('.lab-output-area');
    const output = document.querySelector('.lab-output');
    const outputMeta = document.querySelector('.lab-output-meta');
    const copyBtn = document.querySelector('[data-action="copy"]');
    const downloadBtn = document.querySelector('[data-action="download"]');

    if (!personasGrid || !meritsGrid) return;

    // Persona 버튼 생성
    PERSONAS.forEach(p => {
      const btn = document.createElement('button');
      btn.className = 'selector-btn';
      btn.dataset.persona = p.id;
      btn.innerHTML = `
        <span class="btn-icon">${p.icon}</span>
        ${p.name}
        <span class="btn-sub">${p.desc}</span>
      `;

      btn.addEventListener('click', () => {
        personasGrid.querySelectorAll('.selector-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        selectedPersona = p;
        updateProcessButton();
      });

      btn.addEventListener('dblclick', () => {
        window.location.href = p.archiveUrl;
      });

      personasGrid.appendChild(btn);
    });

    // Merit 버튼 생성
    MERITS.forEach(m => {
      const btn = document.createElement('button');
      btn.className = 'selector-btn';
      btn.dataset.merit = m.id;
      btn.innerHTML = `
        ${m.name}
        <span class="btn-sub">${m.desc}</span>
      `;

      btn.addEventListener('click', () => {
        meritsGrid.querySelectorAll('.selector-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        selectedMerit = m;
        updateProcessButton();
      });

      meritsGrid.appendChild(btn);
    });

    function updateProcessButton() {
      if (selectedPersona && selectedMerit) {
        processBtn.disabled = false;
        processBtn.textContent = `${selectedPersona.name} × ${selectedMerit.name}로 변환`;
      }
    }

    // 변환 처리
    if (processBtn) {
      processBtn.addEventListener('click', () => {
        if (!selectedPersona || !selectedMerit || !textarea) return;

        const inputText = textarea.value.trim();
        if (!inputText) {
          output.textContent = '변환할 텍스트를 입력하세요.';
          outputArea.classList.add('has-content');
          return;
        }

        // 간단한 변환 로직 (실제로는 더 정교한 변환이 필요)
        const transformed = transformText(inputText, selectedPersona, selectedMerit);

        lastOutput = transformed;
        output.textContent = transformed;
        outputMeta.textContent = `${selectedPersona.name} × ${selectedMerit.name} | ${new Date().toLocaleTimeString()}`;
        outputArea.classList.add('has-content');

        // 액션 버튼 활성화
        if (copyBtn) copyBtn.disabled = false;
        if (downloadBtn) downloadBtn.disabled = false;
      });
    }

    // 복사 버튼
    if (copyBtn) {
      copyBtn.addEventListener('click', async () => {
        if (!lastOutput) return;
        try {
          await navigator.clipboard.writeText(lastOutput);
          copyBtn.textContent = '복사됨!';
          setTimeout(() => {
            copyBtn.textContent = '클립보드에 복사';
          }, 2000);
        } catch (e) {
          console.error('Copy failed:', e);
        }
      });
    }

    // 다운로드 버튼
    if (downloadBtn) {
      downloadBtn.addEventListener('click', () => {
        if (!lastOutput) return;

        const html = generateHTML(lastOutput, selectedPersona, selectedMerit);
        const blob = new Blob([html], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `parksy-${selectedPersona.id}-${selectedMerit.id}-${Date.now()}.html`;
        a.click();
        URL.revokeObjectURL(url);
      });
    }
  }

  function transformText(text, persona, merit) {
    // 간단한 변환 예시
    let transformed = text;

    // Merit에 따른 스타일 변환
    switch (merit.id) {
      case 'bluff':
        transformed = text.split('.').map(s => s.trim()).filter(s => s)
          .map(s => `${s}... 그렇다.`).join(' ');
        break;
      case 'halfblood':
        transformed = `[${persona.name}의 시선으로]\n\n${text}\n\n— 경계에서 바라보며`;
        break;
      case 'aggro':
        transformed = text.toUpperCase().replace(/\./g, '!');
        break;
      case 'shaman':
        transformed = `✦ ${text.split('.').join('.\n✦ ')}`;
        break;
      default:
        transformed = text;
    }

    return transformed;
  }

  function generateHTML(content, persona, merit) {
    return `<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${persona.name} × ${merit.name} | Parksy Engine</title>
  <style>
    :root {
      --bg: #0a0a0a;
      --text: #e8e4dc;
      --accent: #ff6b35;
    }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'Noto Serif KR', serif;
      max-width: 800px;
      margin: 0 auto;
      padding: 2rem;
      line-height: 1.8;
    }
    .meta {
      font-size: 0.8rem;
      color: var(--accent);
      margin-bottom: 2rem;
      font-family: monospace;
    }
    .content {
      white-space: pre-wrap;
    }
  </style>
</head>
<body>
  <div class="meta">${persona.name} × ${merit.name} | Generated by Parksy Engine</div>
  <div class="content">${content}</div>
</body>
</html>`;
  }

  // ─────────────────────────────────────────────────────────────
  // 앰비언트 오디오
  // ─────────────────────────────────────────────────────────────
  let audioContext = null;
  let isAudioStarted = false;

  function initAmbientAudio() {
    // 사용자 인터랙션 시 시작
    document.addEventListener('click', startAudio, { once: true });
    document.addEventListener('touchstart', startAudio, { once: true });
  }

  function startAudio() {
    if (isAudioStarted) return;

    try {
      audioContext = new (window.AudioContext || window.webkitAudioContext)();

      // 저주파 드론
      const drone = audioContext.createOscillator();
      drone.type = 'sine';
      drone.frequency.value = 55; // A1

      const droneGain = audioContext.createGain();
      droneGain.gain.value = 0.02;

      // LFO for subtle movement
      const lfo = audioContext.createOscillator();
      lfo.frequency.value = 0.1;
      const lfoGain = audioContext.createGain();
      lfoGain.gain.value = 5;
      lfo.connect(lfoGain);
      lfoGain.connect(drone.frequency);

      drone.connect(droneGain);
      droneGain.connect(audioContext.destination);

      drone.start();
      lfo.start();

      isAudioStarted = true;
    } catch (e) {
      console.warn('Audio not supported:', e);
    }
  }

  // ─────────────────────────────────────────────────────────────
  // 실행
  // ─────────────────────────────────────────────────────────────
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
