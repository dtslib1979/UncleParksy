/**
 * ═══════════════════════════════════════════════════════════════
 * ELEVATOR SYSTEM - Broadcasting Station Navigation
 * Vertical floor navigation with elevator panel mechanics
 * ═══════════════════════════════════════════════════════════════
 */

(function() {
  'use strict';

  // ─────────────────────────────────────────────────────────────
  // Configuration
  // ─────────────────────────────────────────────────────────────
  const FLOORS = {
    lobby: { level: '1F', name: 'Lobby', locked: false },
    channels: { level: 'B1', name: 'Channels', locked: false },
    studio: { level: 'B2', name: 'Studio', locked: false },
    console: { level: 'B3', name: 'Console', locked: false },
    office: { level: 'B4', name: 'Office', locked: true, code: 'parksy' }
  };

  const PERSONAS = [
    { id: 'philosopher', name: 'Philosopher', icon: '🤔' },
    { id: 'blogger', name: 'Blogger', icon: '📝' },
    { id: 'visualizer', name: 'Visualizer', icon: '🎨' },
    { id: 'musician', name: 'Musician', icon: '🎵' },
    { id: 'technician', name: 'Technician', icon: '🔧' },
    { id: 'tester', name: 'Tester', icon: '🧪' },
    { id: 'protocol', name: 'Protocol', icon: '📋' },
    { id: 'orbit', name: 'Orbit-Log', icon: '🌌' }
  ];

  const MERITS = [
    { id: 'bluff', name: 'Bluff', desc: 'Bold overstatement' },
    { id: 'halfblood', name: 'Halfblood', desc: 'Borderline view' },
    { id: 'aggro', name: 'Aggro', desc: 'Direct & aggressive' },
    { id: 'shaman', name: 'Shaman', desc: 'Mystical tone' }
  ];

  const STORAGE_KEY = 'parksy-unlocked-floors';

  // ─────────────────────────────────────────────────────────────
  // State
  // ─────────────────────────────────────────────────────────────
  let currentFloor = 'lobby';
  let unlockedFloors = new Set(['lobby', 'channels', 'studio', 'console']);
  let selectedPersona = null;
  let selectedMerit = null;
  let lastOutput = '';

  // ─────────────────────────────────────────────────────────────
  // DOM Elements
  // ─────────────────────────────────────────────────────────────
  const elevatorBtns = document.querySelectorAll('.elevator-btn');
  const floorIndicator = document.querySelector('.current-floor');
  const floorSections = document.querySelectorAll('.floor-section');
  const quickCards = document.querySelectorAll('.quick-card[data-goto]');

  // ─────────────────────────────────────────────────────────────
  // Initialization
  // ─────────────────────────────────────────────────────────────
  function init() {
    loadUnlockedFloors();
    setupElevatorButtons();
    setupQuickAccess();
    setupCarousel();
    setupStudioWorkspace();
    setupOfficeUnlock();

    // Check URL hash
    const hash = window.location.hash.replace('#floor-', '');
    if (hash && FLOORS[hash] && (unlockedFloors.has(hash) || !FLOORS[hash].locked)) {
      navigateToFloor(hash);
    }
  }

  // ─────────────────────────────────────────────────────────────
  // Floor Unlock Management
  // ─────────────────────────────────────────────────────────────
  function loadUnlockedFloors() {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        parsed.forEach(f => unlockedFloors.add(f));
      }
    } catch (e) {
      console.warn('Failed to load unlocked floors:', e);
    }
    updateElevatorButtons();
  }

  function saveUnlockedFloors() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify([...unlockedFloors]));
    } catch (e) {
      console.warn('Failed to save unlocked floors:', e);
    }
  }

  function unlockFloor(floorId) {
    unlockedFloors.add(floorId);
    saveUnlockedFloors();
    updateElevatorButtons();
  }

  function updateElevatorButtons() {
    elevatorBtns.forEach(btn => {
      const floorId = btn.dataset.floor;
      const floor = FLOORS[floorId];

      if (floor.locked && !unlockedFloors.has(floorId)) {
        btn.classList.add('locked');
        btn.querySelector('.btn-icon').textContent = '🔒';
      } else {
        btn.classList.remove('locked');
        // Restore original icon
        const icons = { lobby: '🏛️', channels: '📺', studio: '🎬', console: '🖥️', office: '📋' };
        btn.querySelector('.btn-icon').textContent = icons[floorId] || '📋';
      }
    });
  }

  // ─────────────────────────────────────────────────────────────
  // Elevator Navigation
  // ─────────────────────────────────────────────────────────────
  function setupElevatorButtons() {
    elevatorBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        const floorId = btn.dataset.floor;
        const floor = FLOORS[floorId];

        if (floor.locked && !unlockedFloors.has(floorId)) {
          // Scroll to locked floor to show lock screen
          navigateToFloor(floorId);
        } else {
          navigateToFloor(floorId);
        }
      });
    });
  }

  function navigateToFloor(floorId) {
    if (!FLOORS[floorId]) return;

    currentFloor = floorId;
    const floor = FLOORS[floorId];

    // Update indicator
    if (floorIndicator) {
      floorIndicator.textContent = floor.level;
    }

    // Update elevator buttons
    elevatorBtns.forEach(btn => {
      btn.classList.toggle('active', btn.dataset.floor === floorId);
    });

    // Show/hide floor sections
    floorSections.forEach(section => {
      const sectionId = section.id.replace('floor-', '');
      section.classList.toggle('active', sectionId === floorId);
    });

    // Update URL
    history.pushState(null, '', `#floor-${floorId}`);

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // ─────────────────────────────────────────────────────────────
  // Quick Access Links
  // ─────────────────────────────────────────────────────────────
  function setupQuickAccess() {
    quickCards.forEach(card => {
      card.addEventListener('click', (e) => {
        const goto = card.dataset.goto;
        if (goto && FLOORS[goto]) {
          e.preventDefault();
          navigateToFloor(goto);
        }
      });
    });
  }

  // ─────────────────────────────────────────────────────────────
  // News Carousel
  // ─────────────────────────────────────────────────────────────
  function setupCarousel() {
    const track = document.querySelector('.carousel-track');
    const prevBtn = document.querySelector('.carousel-btn.prev');
    const nextBtn = document.querySelector('.carousel-btn.next');

    if (!track || !prevBtn || !nextBtn) return;

    const cardWidth = 296; // 280px + 16px gap

    prevBtn.addEventListener('click', () => {
      track.scrollBy({ left: -cardWidth, behavior: 'smooth' });
    });

    nextBtn.addEventListener('click', () => {
      track.scrollBy({ left: cardWidth, behavior: 'smooth' });
    });
  }

  // ─────────────────────────────────────────────────────────────
  // Studio Workspace
  // ─────────────────────────────────────────────────────────────
  function setupStudioWorkspace() {
    const personasGrid = document.querySelector('.selector-grid.personas');
    const meritsGrid = document.querySelector('.selector-grid.merits');
    const transformBtn = document.querySelector('.transform-btn');
    const transformInput = document.querySelector('.transform-input');
    const transformOutput = document.querySelector('.transform-output');
    const copyBtn = document.querySelector('[data-action="copy"]');
    const downloadBtn = document.querySelector('[data-action="download"]');
    const launchBtn = document.querySelector('[data-action="open-transform"]');
    const workspace = document.getElementById('transform-workspace');
    const closeBtn = document.querySelector('.workspace-close');

    if (!personasGrid || !meritsGrid) return;

    // Generate persona buttons
    PERSONAS.forEach(p => {
      const btn = document.createElement('button');
      btn.className = 'selector-btn';
      btn.dataset.persona = p.id;
      btn.innerHTML = `${p.icon} ${p.name}`;

      btn.addEventListener('click', () => {
        personasGrid.querySelectorAll('.selector-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        selectedPersona = p;
        updateTransformButton();
      });

      personasGrid.appendChild(btn);
    });

    // Generate merit buttons
    MERITS.forEach(m => {
      const btn = document.createElement('button');
      btn.className = 'selector-btn';
      btn.dataset.merit = m.id;
      btn.innerHTML = `${m.name}`;

      btn.addEventListener('click', () => {
        meritsGrid.querySelectorAll('.selector-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        selectedMerit = m;
        updateTransformButton();
      });

      meritsGrid.appendChild(btn);
    });

    function updateTransformButton() {
      if (selectedPersona && selectedMerit && transformBtn) {
        transformBtn.disabled = false;
        transformBtn.textContent = `Transform as ${selectedPersona.name} × ${selectedMerit.name}`;
      }
    }

    // Transform button
    if (transformBtn) {
      transformBtn.addEventListener('click', () => {
        if (!selectedPersona || !selectedMerit || !transformInput) return;

        const input = transformInput.value.trim();
        if (!input) {
          transformOutput.innerHTML = '<p class="output-placeholder">Enter text to transform.</p>';
          return;
        }

        const transformed = transformText(input, selectedPersona, selectedMerit);
        lastOutput = transformed;
        transformOutput.innerHTML = `<p>${transformed.replace(/\n/g, '</p><p>')}</p>`;

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
          setTimeout(() => { copyBtn.textContent = 'Copy'; }, 2000);
        } catch (e) {
          console.error('Copy failed:', e);
        }
      });
    }

    // Download button
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

    // Launch workspace button
    if (launchBtn && workspace) {
      launchBtn.addEventListener('click', () => {
        workspace.scrollIntoView({ behavior: 'smooth' });
      });
    }
  }

  function transformText(text, persona, merit) {
    let transformed = text;

    // Persona prefix
    transformed = `[${persona.name}]: "${text}"`;

    // Merit style
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

  function generateHTML(content, persona, merit) {
    return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${persona.name} × ${merit.name} | PARKSY Broadcasting</title>
  <style>
    body {
      background: #0a0a0a;
      color: #e8e8e8;
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
      max-width: 800px;
      margin: 0 auto;
      padding: 2rem;
      line-height: 1.8;
    }
    .meta {
      font-size: 0.8rem;
      color: #f4a261;
      margin-bottom: 2rem;
      font-family: monospace;
    }
    .content { white-space: pre-wrap; }
  </style>
</head>
<body>
  <div class="meta">${persona.name} × ${merit.name} | PARKSY Broadcasting</div>
  <div class="content">${content}</div>
</body>
</html>`;
  }

  // ─────────────────────────────────────────────────────────────
  // Office Unlock
  // ─────────────────────────────────────────────────────────────
  function setupOfficeUnlock() {
    const lockInput = document.querySelector('.lock-input');
    const lockSubmit = document.querySelector('.lock-submit');
    const lockScreen = document.getElementById('office-lock');
    const officeContent = document.querySelector('.office-content');
    const officeSection = document.getElementById('floor-office');

    if (!lockInput || !lockSubmit) return;

    // Check if already unlocked
    if (unlockedFloors.has('office')) {
      if (lockScreen) lockScreen.style.display = 'none';
      if (officeContent) officeContent.style.display = 'block';
      if (officeSection) officeSection.classList.remove('locked');
    }

    lockSubmit.addEventListener('click', attemptUnlock);
    lockInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') attemptUnlock();
    });

    function attemptUnlock() {
      const code = lockInput.value.toLowerCase().trim();

      if (code === FLOORS.office.code) {
        unlockFloor('office');

        if (lockScreen) lockScreen.style.display = 'none';
        if (officeContent) officeContent.style.display = 'block';
        if (officeSection) officeSection.classList.remove('locked');
      } else {
        lockInput.classList.add('shake');
        setTimeout(() => lockInput.classList.remove('shake'), 500);
        lockInput.value = '';
        lockInput.placeholder = 'Invalid code';
      }
    }
  }

  // ─────────────────────────────────────────────────────────────
  // PO Dispatch System (Flag/Placeholder)
  // ─────────────────────────────────────────────────────────────
  function setupPODispatch() {
    const openPOBtn = document.querySelector('[data-action="open-po"]');
    const poPanel = document.getElementById('po-panel');
    const poTypeBtns = document.querySelectorAll('.po-type-btn');
    const poPriorityBtns = document.querySelectorAll('.po-priority-btn');
    const dispatchBtn = document.querySelector('[data-action="dispatch"]');
    const saveDraftBtn = document.querySelector('[data-action="save-draft"]');

    let selectedType = null;
    let selectedPriority = 'normal';

    if (!poPanel) return;

    // Open PO Panel
    if (openPOBtn) {
      openPOBtn.addEventListener('click', () => {
        poPanel.scrollIntoView({ behavior: 'smooth' });
      });
    }

    // Type Selection
    poTypeBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        poTypeBtns.forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        selectedType = btn.dataset.type;
        updateDispatchButton();
      });
    });

    // Priority Selection
    poPriorityBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        poPriorityBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        selectedPriority = btn.dataset.priority;
      });
    });

    function updateDispatchButton() {
      if (dispatchBtn) {
        // For now, keep disabled as system is pending
        // In future: dispatchBtn.disabled = !selectedType;
        dispatchBtn.disabled = true;
      }
    }

    // Save Draft (placeholder)
    if (saveDraftBtn) {
      saveDraftBtn.addEventListener('click', () => {
        const poData = collectPOData();
        console.log('PO Draft:', poData);
        alert('Draft saved locally. Full dispatch requires studio-engine setup.');
      });
    }

    // Dispatch (placeholder)
    if (dispatchBtn) {
      dispatchBtn.addEventListener('click', () => {
        const poData = collectPOData();
        console.log('PO Dispatch Request:', poData);
        alert('Dispatch pending. Connect studio-engine repository to enable.');
      });
    }

    function collectPOData() {
      const now = new Date();
      const dateStr = now.toISOString().slice(0, 10).replace(/-/g, '');
      const seq = String(Math.floor(Math.random() * 10000)).padStart(4, '0');

      return {
        id: `PO-${dateStr}-${seq}`,
        type: selectedType,
        priority: selectedPriority,
        channel: document.getElementById('po-channel')?.value || 'all',
        status: 'draft',
        created_at: now.toISOString(),
        payload: {
          title: document.getElementById('po-title')?.value || '',
          description: document.getElementById('po-payload')?.value || ''
        },
        target_repo: 'dtslib1979/studio-engine'
      };
    }
  }

  // Initialize PO System
  setupPODispatch();

  // ─────────────────────────────────────────────────────────────
  // Handle Browser Navigation
  // ─────────────────────────────────────────────────────────────
  window.addEventListener('popstate', () => {
    const hash = window.location.hash.replace('#floor-', '');
    if (hash && FLOORS[hash]) {
      navigateToFloor(hash);
    } else {
      navigateToFloor('lobby');
    }
  });

  // ─────────────────────────────────────────────────────────────
  // Run
  // ─────────────────────────────────────────────────────────────
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
