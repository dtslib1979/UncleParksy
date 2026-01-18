/**
 * ═══════════════════════════════════════════════════════════════
 * FLOOR SYSTEM - Broadcasting Station Navigation
 * Navigate from lobby to each floor (channel, studio, console)
 * ═══════════════════════════════════════════════════════════════
 */

(function() {
  'use strict';

  // ─────────────────────────────────────────────────────────────
  // Configuration
  // ─────────────────────────────────────────────────────────────
  const FLOORS = {
    1: { code: '1', name: 'B1 · Channels' },
    2: { code: '2', name: 'B2 · Studio' },
    3: { code: 'parksy', name: 'B3 · Console' }
  };

  const PERSONAS = [
    { id: 'philosopher', name: 'Philosopher', icon: '🤔', desc: 'Deep thinking & insight', archiveUrl: '/category/Philosopher-Parksy/' },
    { id: 'blogger', name: 'Blogger', icon: '📝', desc: 'Daily essays & stories', archiveUrl: '/category/Blogger-Parksy/' },
    { id: 'visualizer', name: 'Visualizer', icon: '🎨', desc: 'Data & concept visuals', archiveUrl: '/category/Visualizer-Parksy/' },
    { id: 'musician', name: 'Musician', icon: '🎵', desc: 'Music curation & experience', archiveUrl: '/category/Musician-Parksy/' },
    { id: 'technician', name: 'Technician', icon: '🔧', desc: 'Tech tutorials & tools', archiveUrl: '/category/Technician-Parksy/' },
    { id: 'tester', name: 'Tester', icon: '🧪', desc: 'Testing & experiments', archiveUrl: '/category/Tester-Parksy/' },
    { id: 'protocol', name: 'Protocol', icon: '📋', desc: 'Systems & frameworks', archiveUrl: '/category/Protocol-Parksy/' },
    { id: 'orbit', name: 'Orbit-Log', icon: '🌌', desc: 'Analytics & tracking', archiveUrl: '/category/Orbit-Log/' }
  ];

  const MERITS = [
    { id: 'bluff', name: 'Bluff', desc: 'Bold overstatement style' },
    { id: 'halfblood', name: 'Halfblood', desc: 'Borderline perspective' },
    { id: 'aggro', name: 'Aggro', desc: 'Aggressive directness' },
    { id: 'shaman', name: 'Shaman', desc: 'Mystical & spiritual' }
  ];

  const FORMATS = [
    { id: 'panel', name: 'Panel Comment', desc: 'TV panel discussion style' },
    { id: 'news', name: 'News Style', desc: 'Broadcast news format' },
    { id: 'debate', name: 'Debate Point', desc: 'Structured argument' },
    { id: 'summary', name: 'Summary', desc: 'Concise key points' }
  ];

  const STORAGE_KEY = 'parksy-unlocked-floors';

  // ─────────────────────────────────────────────────────────────
  // State
  // ─────────────────────────────────────────────────────────────
  let unlockedFloors = new Set();
  let currentFloor = null;
  let pendingFloor = null;
  let selectedPersona = null;
  let selectedMerit = null;
  let selectedFormat = 'panel';
  let lastOutput = '';

  // ─────────────────────────────────────────────────────────────
  // DOM Elements
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
  // Initialization
  // ─────────────────────────────────────────────────────────────
  function init() {
    loadUnlockedFloors();
    updateGateVisuals();
    setupFloorGates();
    setupGateModal();
    setupBackButtons();
    createParticles();
    setupStudio();
    setupFormatSelector();
    initAmbientAudio();

    // Check URL hash
    const hash = window.location.hash;
    if (hash && hash.startsWith('#floor-')) {
      const floorNum = parseInt(hash.replace('#floor-', ''));
      if (unlockedFloors.has(floorNum)) {
        navigateToFloor(floorNum);
      }
    }
  }

  // ─────────────────────────────────────────────────────────────
  // Unlock State Management
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
  // Floor Gate Setup
  // ─────────────────────────────────────────────────────────────
  function setupFloorGates() {
    floorGates.forEach(gate => {
      gate.addEventListener('click', () => {
        const floorNum = parseInt(gate.dataset.floor);

        if (unlockedFloors.has(floorNum)) {
          // Already unlocked - navigate directly
          navigateToFloor(floorNum);
        } else {
          // Show gate modal
          showGateModal(floorNum, gate.dataset.hint);
        }
      });
    });
  }

  // ─────────────────────────────────────────────────────────────
  // Gate Modal
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
      // Correct
      unlockFloor(pendingFloor);
      hideGateModal();
      navigateToFloor(pendingFloor);
    } else {
      // Wrong
      gateError.textContent = 'Invalid code';
      gateInput.classList.add('shake');
      setTimeout(() => gateInput.classList.remove('shake'), 500);
    }
  }

  // ─────────────────────────────────────────────────────────────
  // Floor Navigation
  // ─────────────────────────────────────────────────────────────
  function navigateToFloor(floorNum) {
    currentFloor = floorNum;

    // Hide entrance
    entrance.classList.add('hidden');

    // Hide all floors
    floors.forEach(f => f.classList.add('floor-hidden'));

    // Show target floor
    const floor = document.getElementById(`floor-${floorNum}`);
    if (floor) {
      floor.classList.remove('floor-hidden');
      window.scrollTo(0, 0);
      history.pushState(null, '', `#floor-${floorNum}`);
    }
  }

  function navigateToEntrance() {
    currentFloor = null;

    // Hide all floors
    floors.forEach(f => f.classList.add('floor-hidden'));

    // Show entrance
    entrance.classList.remove('hidden');
    window.scrollTo(0, 0);
    history.pushState(null, '', '/');
  }

  function setupBackButtons() {
    backButtons.forEach(btn => {
      btn.addEventListener('click', navigateToEntrance);
    });

    // Browser back button handling
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
  // Particle Effects
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
  // Format Selector
  // ─────────────────────────────────────────────────────────────
  function setupFormatSelector() {
    const formatBtns = document.querySelectorAll('.format-btn');
    formatBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        formatBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        selectedFormat = btn.dataset.format;
      });
    });
  }

  // ─────────────────────────────────────────────────────────────
  // Studio (B2) - Viewer Curation
  // ─────────────────────────────────────────────────────────────
  function setupStudio() {
    const personasGrid = document.querySelector('.selector-grid.personas');
    const meritsGrid = document.querySelector('.selector-grid.merits');
    const textarea = document.querySelector('.lab-textarea');
    const processBtn = document.querySelector('.lab-process-btn');
    const output = document.querySelector('.lab-output');
    const copyBtn = document.querySelector('[data-action="copy"]');
    const downloadBtn = document.querySelector('[data-action="download"]');

    if (!personasGrid || !meritsGrid) return;

    // Create Persona buttons
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

    // Create Merit buttons
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
        processBtn.textContent = `Curate as ${selectedPersona.name} × ${selectedMerit.name}`;
      }
    }

    // Process transformation
    if (processBtn) {
      processBtn.addEventListener('click', () => {
        if (!selectedPersona || !selectedMerit || !textarea) return;

        const inputText = textarea.value.trim();
        if (!inputText) {
          output.innerHTML = '<p class="curation-empty">Enter text to curate.</p>';
          return;
        }

        // Transform text
        const transformed = transformText(inputText, selectedPersona, selectedMerit, selectedFormat);

        lastOutput = transformed;
        output.innerHTML = `<p>${transformed.replace(/\n/g, '</p><p>')}</p>`;

        // Enable action buttons
        if (copyBtn) copyBtn.disabled = false;
        if (downloadBtn) downloadBtn.disabled = false;
      });
    }

    // Copy button
    if (copyBtn) {
      copyBtn.addEventListener('click', async () => {
        if (!lastOutput) return;
        try {
          await navigator.clipboard.writeText(lastOutput);
          copyBtn.textContent = 'Copied!';
          setTimeout(() => {
            copyBtn.textContent = 'Copy to Clipboard';
          }, 2000);
        } catch (e) {
          console.error('Copy failed:', e);
        }
      });
    }

    // Download button
    if (downloadBtn) {
      downloadBtn.addEventListener('click', () => {
        if (!lastOutput) return;

        const html = generateHTML(lastOutput, selectedPersona, selectedMerit, selectedFormat);
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

  function transformText(text, persona, merit, format) {
    let transformed = text;

    // Format-based transformation
    switch (format) {
      case 'panel':
        transformed = `[${persona.name}]: "${text}"`;
        break;
      case 'news':
        transformed = `BREAKING: ${text.split('.')[0]}. According to ${persona.name}, ${text.substring(text.indexOf('.') + 1).trim() || text}`;
        break;
      case 'debate':
        transformed = `POINT: ${text}\n\nCONTEXT: As ${persona.name} would argue, this perspective represents...`;
        break;
      case 'summary':
        const sentences = text.split('.').filter(s => s.trim());
        transformed = `KEY POINTS:\n${sentences.slice(0, 3).map((s, i) => `${i + 1}. ${s.trim()}`).join('\n')}`;
        break;
    }

    // Merit-based style transformation
    switch (merit.id) {
      case 'bluff':
        transformed = transformed.replace(/\./g, '... obviously.');
        break;
      case 'halfblood':
        transformed = `[From the borderline]\n\n${transformed}\n\n— watching from the edge`;
        break;
      case 'aggro':
        transformed = transformed.toUpperCase().replace(/\./g, '!');
        break;
      case 'shaman':
        transformed = `✦ ${transformed.split('.').join('.\n✦ ')}`;
        break;
    }

    return transformed;
  }

  function generateHTML(content, persona, merit, format) {
    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${persona.name} × ${merit.name} | PARKSY Broadcasting</title>
  <style>
    :root {
      --bg: #0a0a0a;
      --text: #e8e4dc;
      --accent: #e63946;
    }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
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
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .badge {
      background: var(--accent);
      color: white;
      padding: 0.2rem 0.5rem;
      font-size: 0.7rem;
    }
    .content {
      white-space: pre-wrap;
    }
  </style>
</head>
<body>
  <div class="meta">
    <span class="badge">${format.toUpperCase()}</span>
    ${persona.name} × ${merit.name} | Generated by PARKSY Broadcasting
  </div>
  <div class="content">${content}</div>
</body>
</html>`;
  }

  // ─────────────────────────────────────────────────────────────
  // Ambient Audio
  // ─────────────────────────────────────────────────────────────
  let audioContext = null;
  let isAudioStarted = false;

  function initAmbientAudio() {
    // Start on user interaction
    document.addEventListener('click', startAudio, { once: true });
    document.addEventListener('touchstart', startAudio, { once: true });
  }

  function startAudio() {
    if (isAudioStarted) return;

    try {
      audioContext = new (window.AudioContext || window.webkitAudioContext)();

      // Low frequency drone
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
  // Run
  // ─────────────────────────────────────────────────────────────
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
