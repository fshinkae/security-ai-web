/* AEMS — Swipe Quiz Engine */
(() => {
  'use strict';

  const container = document.getElementById('quiz-container');
  if (!container) return;

  const questaoInicial = container.dataset.questaoInicial;
  const allCards = Array.from(container.querySelectorAll('.quiz-card'));
  if (!allCards.length) return;

  /* ── Card map ─────────────────────────────────────────────── */
  const cardMap = {};
  allCards.forEach(c => { cardMap[c.dataset.id] = c; });

  /* ── UI refs ─────────────────────────────────────────────── */
  const btnAnterior      = document.getElementById('btn-anterior');
  const btnNao           = document.getElementById('btn-nao');
  const btnSim           = document.getElementById('btn-sim');
  const inputRespondidas = document.getElementById('perguntas-respondidas');
  const barraProgresso   = document.getElementById('progresso-barra');
  const labelGrupo       = document.getElementById('progresso-grupo');
  const stepCounter      = document.getElementById('step-counter');

  const TOTAL     = 5;
  const THRESHOLD = 80; // px until commit

  let idAtual   = questaoInicial;
  let historico = [];
  let locked    = false; // block during animations

  /* ── Drag state ──────────────────────────────────────────── */
  let drag = null;

  /* ── Helpers ─────────────────────────────────────────────── */

  function card(id) { return cardMap[id]; }

  function setRadio(id, val) {
    const r = document.querySelector(`input[name="pergunta_${id}"][value="${val}"]`);
    if (r) r.checked = true;
  }

  function clearRadio(id) {
    document.querySelectorAll(`input[name="pergunta_${id}"]`)
            .forEach(r => r.checked = false);
  }

  function resetCard(c) {
    c.style.cssText = '';
    c.querySelectorAll('.swipe-indicator').forEach(o => o.style.opacity = '0');
  }

  function updateUI() {
    const done = historico.length;
    const pct  = Math.round((done / TOTAL) * 100);
    if (barraProgresso) barraProgresso.style.width = Math.min(pct, 95) + '%';
    if (stepCounter)    stepCounter.textContent = `${done + 1} / ${TOTAL}`;
    const c = card(idAtual);
    if (c && labelGrupo)
      labelGrupo.textContent = `// ${(c.dataset.grupo || '').toUpperCase()}`;
    if (btnAnterior) btnAnterior.disabled = historico.length === 0;
  }

  /* ── Show / hide ─────────────────────────────────────────── */

  function show(id, anim) {
    idAtual = id;
    const c = card(id);
    if (!c) return;

    c.style.cssText = '';
    c.querySelectorAll('.swipe-indicator').forEach(o => o.style.opacity = '0');
    c.classList.add('is-active');

    if (anim === 'enter') {
      c.style.transform = 'translateY(36px) scale(0.95)';
      c.style.opacity   = '0';
      /* double rAF guarantees the browser paints the initial state first */
      requestAnimationFrame(() => requestAnimationFrame(() => {
        c.style.transition = 'transform 0.38s cubic-bezier(0.34,1.4,0.64,1), opacity 0.28s ease-out';
        c.style.transform  = '';
        c.style.opacity    = '';
        setTimeout(() => { c.style.transition = ''; locked = false; }, 400);
      }));
    } else if (anim === 'back') {
      c.style.transform = 'translateY(-22px) scale(0.97)';
      c.style.opacity   = '0';
      requestAnimationFrame(() => requestAnimationFrame(() => {
        c.style.transition = 'transform 0.3s ease-out, opacity 0.24s ease-out';
        c.style.transform  = '';
        c.style.opacity    = '';
        setTimeout(() => { c.style.transition = ''; locked = false; }, 320);
      }));
    } else {
      locked = false;
    }

    updateUI();
  }

  function hide(c) {
    c.classList.remove('is-active');
    resetCard(c);
  }

  /* ── Animations ──────────────────────────────────────────── */

  function flyOut(c, dir) {
    return new Promise(resolve => {
      c.style.transition = 'transform 0.3s cubic-bezier(0.4,0,1,1), opacity 0.24s ease-in';
      c.style.transform  = `translateX(${dir * 120}%) rotate(${dir * 20}deg)`;
      c.style.opacity    = '0';
      setTimeout(() => { hide(c); resolve(); }, 320);
    });
  }

  function snapBack(c) {
    c.style.transition = 'transform 0.44s cubic-bezier(0.175,0.885,0.32,1.275), opacity 0.3s';
    c.style.transform  = '';
    c.style.opacity    = '';
    c.querySelectorAll('.swipe-indicator').forEach(o => o.style.opacity = '0');
    setTimeout(() => { c.style.transition = ''; }, 460);
  }

  /* ── Commit answer ───────────────────────────────────────── */

  async function commit(isSim) {
    if (locked) return;
    locked = true;

    const c = card(idAtual);
    if (!c) return;

    setRadio(idAtual, isSim ? 'sim' : 'nao');
    await flyOut(c, isSim ? 1 : -1);

    historico.push(idAtual);
    inputRespondidas.value = historico.join(',');

    const proximo = isSim ? c.dataset.proximaSim : c.dataset.proximaNao;

    if (!proximo) {
      /* Last question — include current in list and submit */
      document.getElementById('quiz-form').submit();
      return;
    }

    show(proximo, 'enter');
  }

  /* ── Go back ─────────────────────────────────────────────── */

  async function goBack() {
    if (locked || historico.length === 0) return;
    locked = true;

    const c = card(idAtual);
    c.style.transition = 'transform 0.22s ease-in, opacity 0.18s ease-in';
    c.style.transform  = 'translateY(26px) scale(0.95)';
    c.style.opacity    = '0';
    await new Promise(r => setTimeout(r, 240));
    hide(c);

    clearRadio(idAtual);
    const prev = historico.pop();
    inputRespondidas.value = historico.join(',');

    show(prev, 'back');
  }

  /* ── Pointer (touch + mouse) drag ───────────────────────── */

  container.addEventListener('pointerdown', e => {
    if (locked) return;
    const c = card(idAtual);
    if (!c) return;
    c.setPointerCapture(e.pointerId);
    c.style.transition = 'none';
    drag = { startX: e.clientX, startY: e.clientY, lastDx: 0, axis: null };
  });

  container.addEventListener('pointermove', e => {
    if (!drag) return;
    const dx = e.clientX - drag.startX;
    const dy = e.clientY - drag.startY;

    /* Lock axis on first significant movement */
    if (!drag.axis && (Math.abs(dx) > 8 || Math.abs(dy) > 8))
      drag.axis = Math.abs(dx) >= Math.abs(dy) ? 'h' : 'v';

    if (drag.axis !== 'h') return;
    e.preventDefault();

    drag.lastDx = dx;
    const c = card(idAtual);
    c.style.transform = `translateX(${dx}px) rotate(${dx * 0.045}deg)`;

    const intensity = Math.min(Math.abs(dx) / 100, 1);
    const simEl = c.querySelector('.swipe-sim');
    const naoEl = c.querySelector('.swipe-nao');

    if (dx > 8) {
      simEl.style.opacity = intensity;
      naoEl.style.opacity = '0';
    } else if (dx < -8) {
      naoEl.style.opacity = intensity;
      simEl.style.opacity = '0';
    } else {
      simEl.style.opacity = '0';
      naoEl.style.opacity = '0';
    }
  }, { passive: false });

  container.addEventListener('pointerup', e => {
    if (!drag) return;
    const { lastDx, axis } = drag;
    drag = null;

    const c = card(idAtual);
    if (axis !== 'h') return; /* vertical drag — browser handles scroll */

    if      (lastDx >  THRESHOLD) commit(true);
    else if (lastDx < -THRESHOLD) commit(false);
    else                           snapBack(c);
  });

  container.addEventListener('pointercancel', () => {
    if (!drag) return;
    drag = null;
    const c = card(idAtual);
    if (c) snapBack(c);
  });

  /* ── Tap buttons ─────────────────────────────────────────── */
  if (btnSim)      btnSim.addEventListener('click',      () => commit(true));
  if (btnNao)      btnNao.addEventListener('click',      () => commit(false));
  if (btnAnterior) btnAnterior.addEventListener('click', goBack);

  /* ── Boot ────────────────────────────────────────────────── */
  show(questaoInicial);
})();
