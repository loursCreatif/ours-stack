#!/usr/bin/env python3
"""Compose self-contained memory-palace.html — oblique relief map."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
VENDOR = SKILL_ROOT / "references" / "vendor" / "three.min.js"

SCENE_JS = r"""
(function () {
  const data = PALACE_DATA;
  const conceptById = Object.fromEntries(data.concepts.map(c => [c.id, c]));
  const locusById = Object.fromEntries(data.loci.map(l => [l.id, l]));
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const TYPE_COLORS = {
    mechanism: '#3b82f6', finding: '#22c55e', belief: '#f59e0b',
    question: '#9ca3af', relationship: '#a855f7', source: '#64748b', date: '#06b6d4'
  };

  const THEME = {
    corridor: {
      ground: 0xe8e2d8, building: 0xf5f0e8, roof: 0xc9a87c, zone: 0xd4e4f7, pin: 0xf59e0b,
      sky: 0xf5f0ea, path: 0xe67e22, ribbon: 0x3b82f6, detail: 0xb8956a, edge: 0x8a7a68
    },
    museum: {
      ground: 0xe8e4dc, building: 0xf8f4ec, roof: 0xc9b896, zone: 0xe8e0d4, pin: 0xb8860b,
      sky: 0xf7f4ef, path: 0x8b6914, ribbon: 0x3b82f6, detail: 0xd4af37, edge: 0x9a8b78
    },
    construction: {
      ground: 0xe8dcc8, building: 0xf2e8d8, roof: 0xd4a574, zone: 0xf5e6c8, pin: 0xb45309,
      sky: 0xf0ead6, path: 0xc87941, ribbon: 0x2563eb, detail: 0x9a7b4f, edge: 0x8a7a60
    },
    library: {
      ground: 0xd8cfc0, building: 0xe8e0d0, roof: 0x5a6b4a, zone: 0xf0e8e4, pin: 0x8b2942,
      sky: 0xede8dc, path: 0x6b7c5e, ribbon: 0x3b82f6, detail: 0x4a5c3a, edge: 0x6a5a48
    },
    custom: {
      ground: 0xe8e2d8, building: 0xf5f0e8, roof: 0xc9a87c, zone: 0xd4e4f7, pin: 0xf59e0b,
      sky: 0xf5f0ea, path: 0xe67e22, ribbon: 0x3b82f6, detail: 0xb8956a, edge: 0x8a7a68
    }
  };
  const pal = THEME[data.theme] || THEME.corridor;

  function hexColor(n) {
    return '#' + (n >>> 0).toString(16).padStart(6, '0');
  }

  let navLevel = 'site';
  let activeBuildingId = null;
  let mapPan = { x: 0, z: 0 };
  let mapZoom = 1;
  let camTarget = { x: 0, y: 0, z: 0 };
  let camDist = 55;
  const ELEV = 52 * Math.PI / 180;
  const AZIM = 45 * Math.PI / 180;
  const EYE_HEIGHT = 1.7;

  let tourActive = false;
  let tourStopIdx = 0;
  let tourHighlightId = null;
  let reliefTourApi = null;
  let isoTourRebuild = null;

  const panel = document.getElementById('detail-panel');
  const crumbEl = document.getElementById('breadcrumb');
  const btnBack = document.getElementById('btn-back');
  const btnTour = document.getElementById('btn-tour');
  const btnMapView = document.getElementById('btn-map-view');
  const tourNav = document.getElementById('tour-nav');
  const tourPrev = document.getElementById('tour-prev');
  const tourNext = document.getElementById('tour-next');
  const tourCounter = document.getElementById('tour-counter');
  let goSite = () => {};

  function typeColor(t) { return TYPE_COLORS[t] || '#64748b'; }

  function showPanel(concepts, title, subtitle, scene) {
    panel.hidden = false;
    document.getElementById('panel-title').textContent = title || '';
    document.getElementById('panel-sub').textContent = subtitle || '';
    const body = document.getElementById('panel-body');
    body.replaceChildren();
    if (scene && scene.image) {
      const sceneBlock = document.createElement('div');
      sceneBlock.className = 'scene-block';
      const img = document.createElement('p');
      img.className = 'scene-image';
      img.textContent = scene.image;
      sceneBlock.appendChild(img);
      (scene.senses || []).forEach(s => {
        const sense = document.createElement('p');
        sense.className = 'scene-sense';
        sense.textContent = s;
        sceneBlock.appendChild(sense);
      });
      body.appendChild(sceneBlock);
    }
    concepts.forEach(c => {
      if (!c) return;
      const d = document.createElement('div');
      d.className = 'concept-card';
      const badge = document.createElement('span');
      badge.className = 'badge';
      badge.style.background = typeColor(c.type);
      badge.textContent = c.type;
      const h3 = document.createElement('h3');
      h3.textContent = c.label;
      const p = document.createElement('p');
      p.textContent = c.gloss;
      const small = document.createElement('small');
      small.textContent = c.source.file + ' · ' + c.source.section;
      d.append(badge, h3, p, small);
      body.appendChild(d);
    });
  }

  function closePanel() { panel.hidden = true; }

  function updateBreadcrumb() {
    const parts = [data.lang === 'fr' ? 'Carte du site' : 'Site map'];
    if (activeBuildingId) {
      const b = locusById[activeBuildingId];
      if (b) parts.push(b.label);
    }
    crumbEl.innerHTML = parts.map((p, i) => {
      const sep = i ? ' › ' : '';
      return sep + '<button type="button" class="crumb" data-i="' + i + '">' + p + '</button>';
    }).join('');
    crumbEl.querySelectorAll('.crumb').forEach(btn => {
      btn.onclick = () => {
        if (+btn.dataset.i === 0) goSite();
      };
    });
    btnBack.hidden = navLevel === 'site';
  }

  function conceptsForIds(ids) {
    return (ids || []).map(id => conceptById[id]).filter(Boolean);
  }

  function updateTourUI() {
    if (!btnTour) return;
    btnTour.hidden = tourActive;
    if (btnMapView) btnMapView.hidden = !tourActive;
    if (tourNav) tourNav.hidden = !tourActive;
    if (tourCounter && tourActive) {
      tourCounter.textContent = (tourStopIdx + 1) + ' / ' + data.path.length;
    }
    if (tourPrev) tourPrev.disabled = tourStopIdx <= 0;
    if (tourNext) tourNext.disabled = tourStopIdx >= data.path.length - 1;
  }

  function showTourStop(idx) {
    tourStopIdx = Math.max(0, Math.min(data.path.length - 1, idx));
    const bid = data.path[tourStopIdx];
    const loc = locusById[bid];
    if (!loc) return;
    tourHighlightId = bid;
    if (reliefTourApi) reliefTourApi.goToStop(tourStopIdx);
    if (isoTourRebuild) isoTourRebuild();
    const sub = data.lang === 'fr' ? 'Visite guidée' : 'Guided tour';
    showPanel(conceptsForIds(loc.concepts), loc.label, sub, loc.scene);
    updateTourUI();
  }

  function startTour() {
    tourActive = true;
    navLevel = 'tour';
    activeBuildingId = null;
    updateTourUI();
    if (reliefTourApi) reliefTourApi.enter();
    showTourStop(0);
  }

  function endTour() {
    tourActive = false;
    tourHighlightId = null;
    navLevel = 'site';
    updateTourUI();
    if (reliefTourApi) reliefTourApi.exit();
    if (isoTourRebuild) isoTourRebuild();
    closePanel();
    goSite();
  }

  function tourStep(delta) {
    if (!tourActive) return;
    showTourStop(tourStopIdx + delta);
  }

  if (btnTour) btnTour.onclick = startTour;
  if (btnMapView) btnMapView.onclick = endTour;
  if (tourPrev) tourPrev.onclick = () => tourStep(-1);
  if (tourNext) tourNext.onclick = () => tourStep(1);

  function roofVariant(stepIdx, loc) {
    if (loc.blocked) return 'scaffold';
    return ['flat', 'pitch', 'gable'][stepIdx % 3];
  }

  function buildingHeight(loc, stepIdx) {
    const base = loc.height || 3.5;
    const jitter = [0, 0.6, -0.3, 0.9, 0.2, -0.2, 0.5][stepIdx % 7];
    return Math.max(2.5, base + jitter);
  }

  const ISO_SCALE_X = 18;
  const ISO_SCALE_Y = 9;
  const FIT_MARGIN = 0.1;

  function isoProj(x, z) {
    return [(x - z) * ISO_SCALE_X + mapPan.x, (x + z) * ISO_SCALE_Y + mapPan.z];
  }

  function computeSiteBoundsRaw() {
    let minX = Infinity, maxX = -Infinity, minZ = Infinity, maxZ = -Infinity, maxY = 4;
    data.loci.forEach((loc, idx) => {
      if (loc.kind !== 'building') return;
      const [fx, fz, fw, fd] = loc.footprint;
      minX = Math.min(minX, fx);
      maxX = Math.max(maxX, fx + fw);
      minZ = Math.min(minZ, fz);
      maxZ = Math.max(maxZ, fz + fd);
      const pathIdx = data.path.indexOf(loc.id);
      const hi = buildingHeight(loc, pathIdx >= 0 ? pathIdx : idx);
      maxY = Math.max(maxY, hi + 2.2);
    });
    if (!isFinite(minX)) { minX = -10; maxX = 10; minZ = -10; maxZ = 10; }
    const spanX = maxX - minX || 10;
    const spanZ = maxZ - minZ || 10;
    return {
      minX, maxX, minZ, maxZ, spanX, spanZ,
      centerX: (minX + maxX) / 2, centerZ: (minZ + maxZ) / 2,
      maxY
    };
  }

  function computeSiteBounds() {
    const raw = computeSiteBoundsRaw();
    const padX = raw.spanX * FIT_MARGIN;
    const padZ = raw.spanZ * FIT_MARGIN;
    return {
      minX: raw.minX - padX, maxX: raw.maxX + padX,
      minZ: raw.minZ - padZ, maxZ: raw.maxZ + padZ,
      centerX: raw.centerX, centerZ: raw.centerZ,
      spanX: raw.spanX + padX * 2, spanZ: raw.spanZ + padZ * 2,
      maxY: raw.maxY + 1
    };
  }

  function pathSpriteWorldPos(loc, idx) {
    const [fx, fz, fw, fd] = loc.footprint;
    const h = buildingHeight(loc, idx);
    const cx = fx + fw / 2;
    const cz = fz + fd / 2;
    return new THREE.Vector3(cx, h + 1.8, cz + fd / 2 + 1.2);
  }

  let siteFitTarget = { x: 0, y: 0, z: 0 };
  let siteFitDist = 55;

  function enableIsoMode() {
    document.getElementById('relief-canvas')?.classList.add('hidden');
    document.getElementById('label-layer')?.classList.add('hidden');
    const isoMap = document.getElementById('iso-map');
    if (isoMap) {
      isoMap.classList.remove('hidden');
      isoMap.style.display = 'block';
    }
    goSite = goSiteIso;
    buildIsoSvg();
    updateBreadcrumb();
    btnBack.onclick = goSiteIso;
  }

  function goSiteIso() {
    navLevel = 'site';
    activeBuildingId = null;
    closePanel();
    buildIsoSvg();
    updateBreadcrumb();
  }

  // --- SVG isometric fallback ---
  function buildIsoSvg() {
    const wrap = document.getElementById('iso-map');
    const isoX = (x, z) => isoProj(x, z)[0];
    const isoY = (x, z) => isoProj(x, z)[1];
    const bounds = computeSiteBounds();
    const allPts = [];
    const centers = [];
    const sky = hexColor(pal.sky);
    const ground = hexColor(pal.ground);
    const ribbon = hexColor(pal.ribbon);

    function trackPt(x, y) { allPts.push([x, y]); }

    data.path.forEach((id, idx) => {
      const loc = locusById[id];
      if (!loc) return;
      const [fx, fz, fw, fd] = loc.footprint;
      const h = buildingHeight(loc, idx) * 6;
      const corners = [
        [fx, fz], [fx + fw, fz], [fx + fw, fz + fd], [fx, fz + fd]
      ];
      corners.forEach(([cx, cz]) => trackPt(isoX(cx, cz), isoY(cx, cz)));
      corners.forEach(([cx, cz]) => trackPt(isoX(cx, cz), isoY(cx, cz) - h));
      const lx = isoX(fx + fw / 2, fz + fd / 2);
      const ly = isoY(fx + fw / 2, fz + fd / 2) - h - 10;
      trackPt(lx, ly + 18);
      trackPt(lx, ly);
      centers.push([lx, isoY(fx + fw / 2, fz + fd / 2)]);
    });

    let vbX = 0, vbY = 0, vbW = 720, vbH = 480;
    if (allPts.length) {
      const xs = allPts.map(p => p[0]);
      const ys = allPts.map(p => p[1]);
      const minPx = Math.min(...xs), maxPx = Math.max(...xs);
      const minPy = Math.min(...ys), maxPy = Math.max(...ys);
      const padX = Math.max(24, (maxPx - minPx) * FIT_MARGIN);
      const padY = Math.max(24, (maxPy - minPy) * FIT_MARGIN);
      vbX = minPx - padX;
      vbY = minPy - padY;
      vbW = (maxPx - minPx) + padX * 2;
      vbH = (maxPy - minPy) + padY * 2;
    }

    const warmTop = '#f8e8c8';
    const warmBot = hexColor(pal.sky);
    let svg = '<svg viewBox="' + vbX + ' ' + vbY + ' ' + vbW + ' ' + vbH + '" xmlns="http://www.w3.org/2000/svg" role="img" preserveAspectRatio="xMidYMid meet">';
    svg += '<defs><linearGradient id="skyGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="' + warmTop + '"/><stop offset="100%" stop-color="' + warmBot + '"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>';
    svg += '<rect x="' + vbX + '" y="' + vbY + '" width="' + vbW + '" height="' + vbH + '" fill="url(#skyGrad)"/>';
    const gx = isoX(bounds.centerX - (bounds.maxX - bounds.minX) / 2, bounds.centerZ - (bounds.maxZ - bounds.minZ) / 2);
    const gy = isoY(bounds.centerX - (bounds.maxX - bounds.minX) / 2, bounds.centerZ - (bounds.maxZ - bounds.minZ) / 2);
    svg += '<rect x="' + gx + '" y="' + gy + '" width="' + vbW * 0.92 + '" height="' + vbH * 0.75 + '" rx="8" fill="' + ground + '" opacity="0.55"/>';

    data.path.forEach((id, idx) => {
      const loc = locusById[id];
      if (!loc) return;
      const [fx, fz, fw, fd] = loc.footprint;
      const tx = isoX(fx - 2 + (idx % 3) * 1.5, fz - 3);
      const ty = isoY(fx - 2 + (idx % 3) * 1.5, fz - 3);
      const trunkH = 14 + (idx % 3) * 4;
      svg += '<rect x="' + (tx - 2) + '" y="' + (ty - trunkH) + '" width="4" height="' + trunkH + '" fill="#6b5344" opacity="0.7" class="iso-tree"/>';
      svg += '<ellipse cx="' + tx + '" cy="' + (ty - trunkH - 8) + '" rx="10" ry="7" fill="#5a8a4a" opacity="0.75" class="iso-tree"/>';
      svg += '<ellipse cx="' + tx + '" cy="' + (ty - trunkH - 14) + '" rx="7" ry="5" fill="#6b9a5a" opacity="0.8" class="iso-tree"/>';
    });

    if (centers.length > 1) {
      const routePts = centers.map(p => p[0] + ',' + p[1]).join(' ');
      svg += '<polyline points="' + routePts + '" fill="none" stroke="' + ribbon + '" stroke-width="5" stroke-dasharray="10 6" opacity="0.75" stroke-linecap="round"/>';
      for (let i = 0; i < centers.length - 1; i++) {
        const a = centers[i], b = centers[i + 1];
        const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2;
        svg += '<ellipse cx="' + mx + '" cy="' + my + '" rx="6" ry="3" fill="' + ribbon + '" opacity="0.35"/>';
      }
    }

    data.path.forEach((id, idx) => {
      const loc = locusById[id];
      if (!loc) return;
      const [fx, fz, fw, fd] = loc.footprint;
      const pts = [
        [isoX(fx, fz), isoY(fx, fz)],
        [isoX(fx + fw, fz), isoY(fx + fw, fz)],
        [isoX(fx + fw, fz + fd), isoY(fx + fw, fz + fd)],
        [isoX(fx, fz + fd), isoY(fx, fz + fd)]
      ];
      const h = buildingHeight(loc, idx) * 6;
      const fill = loc.blocked ? '#9a9a9a' : hexColor(pal.building);
      const roofFill = loc.blocked ? '#7a7a7a' : hexColor(pal.roof);
      const dash = loc.blocked ? ' stroke-dasharray="6 4"' : '';
      const variant = roofVariant(idx, loc);
      const isTourHighlight = tourActive && tourHighlightId === id;
      const hlStroke = isTourHighlight ? ' stroke="#e67e22" stroke-width="3.5"' : ' stroke="' + hexColor(pal.edge) + '" stroke-width="1.2"';
      const hlFilter = isTourHighlight ? ' filter="url(#glow)"' : '';

      svg += '<polygon points="' + pts.map(p => p.join(',')).join(' ') + '" fill="' + fill + '"' + hlStroke + dash + ' data-bid="' + id + '" class="iso-bld' + (isTourHighlight ? ' iso-tour-active' : '') + '"' + hlFilter + '/>';

      if (variant === 'pitch') {
        const cx = isoX(fx + fw / 2, fz + fd / 2);
        const cy = isoY(fx + fw / 2, fz + fd / 2) - h;
        const rw = fw * 10;
        svg += '<polygon points="' + cx + ',' + (cy - h * 0.5) + ' ' + (cx - rw) + ',' + cy + ' ' + (cx + rw) + ',' + cy + '" fill="' + roofFill + '" data-bid="' + id + '" class="iso-bld"/>';
      } else if (variant === 'gable') {
        const left = [isoX(fx, fz + fd / 2), isoY(fx, fz + fd / 2) - h];
        const right = [isoX(fx + fw, fz + fd / 2), isoY(fx + fw, fz + fd / 2) - h];
        const peak = [isoX(fx + fw / 2, fz + fd / 2), isoY(fx + fw / 2, fz + fd / 2) - h - h * 0.45];
        svg += '<polygon points="' + [left, peak, right].map(p => p.join(',')).join(' ') + '" fill="' + roofFill + '" data-bid="' + id + '" class="iso-bld"/>';
      } else {
        const roof = pts.map(p => [p[0], p[1] - h]);
        const roofD = roof.map(p => p.join(',')).join(' ');
        svg += '<polygon points="' + roofD + '" fill="' + roofFill + '" opacity="0.95" data-bid="' + id + '" class="iso-bld"/>';
      }

      const lx = isoX(fx + fw / 2, fz + fd / 2);
      const ly = isoY(fx + fw / 2, fz + fd / 2) - h - 10;
      svg += '<circle cx="' + lx + '" cy="' + (ly + 18) + '" r="14" fill="' + ribbon + '" stroke="#fff" stroke-width="2"/>';
      svg += '<text x="' + lx + '" y="' + (ly + 23) + '" fill="#fff" font-size="14" font-weight="800" text-anchor="middle">' + (idx + 1) + '</text>';
      svg += '<text x="' + lx + '" y="' + ly + '" fill="#3a3a3a" font-size="11" font-weight="600" text-anchor="middle">' + loc.label + '</text>';
    });

    svg += '</svg>';
    wrap.innerHTML = svg;
    wrap.querySelectorAll('.iso-bld').forEach(el => {
      el.style.cursor = tourActive ? 'default' : 'pointer';
      el.onclick = () => { if (!tourActive) openBuildingIso(el.dataset.bid); };
    });
  }

  isoTourRebuild = () => { if (!document.getElementById('iso-map')?.classList.contains('hidden')) buildIsoSvg(); };

  function openBuildingIso(bid) {
    activeBuildingId = bid;
    navLevel = 'interior';
    const loc = locusById[bid];
    const wrap = document.getElementById('iso-map');
    wrap.innerHTML = '<button type="button" class="iso-back">← ' + (data.lang === 'fr' ? 'Retour' : 'Back') + '</button>';
    const grid = document.createElement('div');
    grid.className = 'iso-interior';
    (loc.interior?.zones || []).forEach(z => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'iso-zone';
      btn.textContent = z.label;
      btn.onclick = () => showPanel(conceptsForIds(z.concepts), z.label, loc.label);
      grid.appendChild(btn);
    });
    (loc.interior?.hotspots || []).forEach(h => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'iso-hotspot';
      btn.textContent = '● ' + h.label;
      btn.onclick = () => {
        const c = conceptById[h.concept];
        showPanel(c ? [c] : [], h.label, loc.label);
      };
      grid.appendChild(btn);
    });
    if (!loc.interior?.zones?.length) {
      showPanel(conceptsForIds(loc.concepts), loc.label, data.lang === 'fr' ? 'Bâtiment' : 'Building');
    }
    wrap.appendChild(grid);
    wrap.querySelector('.iso-back').onclick = goSiteIso;
    updateBreadcrumb();
  }

  function makeNumberSprite(n) {
    const canvas = document.createElement('canvas');
    canvas.width = 96;
    canvas.height = 96;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = hexColor(pal.ribbon);
    ctx.beginPath();
    ctx.arc(48, 48, 40, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 4;
    ctx.stroke();
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 44px system-ui, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(String(n), 48, 50);
    const tex = new THREE.CanvasTexture(canvas);
    const mat = new THREE.SpriteMaterial({ map: tex, depthTest: false });
    const sprite = new THREE.Sprite(mat);
    sprite.scale.set(3.2, 3.2, 1);
    sprite.renderOrder = 10;
    return sprite;
  }

  // --- Three.js relief ---
  function initRelief() {
    const canvas = document.getElementById('relief-canvas');
    const labelLayer = document.getElementById('label-layer');
    const scene = new THREE.Scene();
    function makeSkyTexture() {
      const c = document.createElement('canvas');
      c.width = 512; c.height = 512;
      const ctx = c.getContext('2d');
      const grad = ctx.createLinearGradient(0, 0, 0, 512);
      grad.addColorStop(0, '#f8e4c0');
      grad.addColorStop(1, hexColor(pal.sky));
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, 512, 512);
      return new THREE.CanvasTexture(c);
    }
    scene.background = makeSkyTexture();

    const camera = new THREE.PerspectiveCamera(42, 1, 0.5, 300);
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const siteBoundsRaw = computeSiteBoundsRaw();
    const tmpProj = new THREE.Vector3();

    function resizeCanvas() {
      const w = Math.max(1, canvas.clientWidth);
      const h = Math.max(1, canvas.clientHeight);
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h, false);
      if (navLevel === 'site' && !tourActive) fitSiteCamera();
    }

    function placeCameraAtDist(dist) {
      if (tourActive) return;
      const d = dist / mapZoom;
      camera.position.set(
        camTarget.x + d * Math.cos(ELEV) * Math.sin(AZIM) + mapPan.x,
        camTarget.y + d * Math.sin(ELEV),
        camTarget.z + d * Math.cos(ELEV) * Math.cos(AZIM) + mapPan.z
      );
      camera.lookAt(camTarget.x + mapPan.x, camTarget.y, camTarget.z + mapPan.z);
      camera.updateMatrixWorld();
    }

    function siteSamplePoints() {
      const b = computeSiteBoundsRaw();
      const pts = [];
      data.loci.forEach((loc, idx) => {
        if (loc.kind !== 'building') return;
        const [fx, fz, fw, fd] = loc.footprint;
        const pathIdx = data.path.indexOf(loc.id);
        const hi = buildingHeight(loc, pathIdx >= 0 ? pathIdx : idx);
        [[fx, fz], [fx + fw, fz], [fx + fw, fz + fd], [fx, fz + fd]].forEach(([x, z]) => {
          pts.push(new THREE.Vector3(x, 0, z));
          pts.push(new THREE.Vector3(x, hi, z));
        });
      });
      data.path.forEach((id, idx) => {
        const loc = locusById[id];
        if (!loc) return;
        pts.push(pathSpriteWorldPos(loc, idx));
      });
      return pts;
    }

    function projectSiteExtents(dist) {
      placeCameraAtDist(dist);
      let minNx = 1, maxNx = 0, minNy = 1, maxNy = 0;
      for (const p of siteSamplePoints()) {
        tmpProj.copy(p);
        tmpProj.project(camera);
        if (tmpProj.z > 1) return null;
        const nx = (tmpProj.x + 1) / 2;
        const ny = (-tmpProj.y + 1) / 2;
        minNx = Math.min(minNx, nx);
        maxNx = Math.max(maxNx, nx);
        minNy = Math.min(minNy, ny);
        maxNy = Math.max(maxNy, ny);
      }
      return { minNx, maxNx, minNy, maxNy, spanNx: maxNx - minNx, spanNy: maxNy - minNy };
    }

    function pointsInView(dist, margin) {
      const ext = projectSiteExtents(dist);
      if (!ext) return false;
      const m = margin ?? FIT_MARGIN;
      return ext.minNx >= m && ext.maxNx <= 1 - m
        && ext.minNy >= m && ext.maxNy <= 1 - m;
    }

    function fitsMargin(dist, margin) {
      const ext = projectSiteExtents(dist);
      if (!ext) return false;
      const m = margin ?? FIT_MARGIN;
      return ext.minNx >= m && ext.maxNx <= 1 - m
        && ext.minNy >= m && ext.maxNy <= 1 - m;
    }

    function fitSiteCamera() {
      if (tourActive) return;
      const b = computeSiteBoundsRaw();
      camTarget = { x: b.centerX, y: 0, z: b.centerZ };
      siteFitTarget = { x: b.centerX, y: 0, z: b.centerZ };
      let dist = 100;
      while (!fitsMargin(dist, FIT_MARGIN) && dist < 500) dist += 12;
      while (fitsMargin(dist * 0.965, FIT_MARGIN)) dist *= 0.965;
      camDist = dist;
      siteFitDist = dist;
      placeCameraAtDist(dist);
    }

    resizeCanvas();
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    scene.add(new THREE.AmbientLight(0xfff5e8, 0.5));
    const sun = new THREE.DirectionalLight(0xffd9a0, 1.05);
    sun.position.set(58, 9, 32);
    sun.castShadow = true;
    sun.shadow.mapSize.width = 2048;
    sun.shadow.mapSize.height = 2048;
    sun.shadow.camera.near = 1;
    sun.shadow.camera.far = 140;
    const sh = 65;
    sun.shadow.camera.left = -sh;
    sun.shadow.camera.right = sh;
    sun.shadow.camera.top = sh;
    sun.shadow.camera.bottom = -sh;
    sun.shadow.bias = -0.0008;
    scene.add(sun);

    function makeGroundTexture() {
      const c = document.createElement('canvas');
      c.width = 256; c.height = 256;
      const ctx = c.getContext('2d');
      ctx.fillStyle = hexColor(pal.ground);
      ctx.fillRect(0, 0, 256, 256);
      for (let i = 0; i < 600; i++) {
        ctx.fillStyle = 'rgba(60,40,20,' + (Math.random() * 0.06) + ')';
        ctx.fillRect(Math.random() * 256, Math.random() * 256, 1, 1);
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(6, 6);
      return tex;
    }
    function makeWallTexture() {
      const c = document.createElement('canvas');
      c.width = 128; c.height = 128;
      const ctx = c.getContext('2d');
      ctx.fillStyle = hexColor(pal.building);
      ctx.fillRect(0, 0, 128, 128);
      ctx.strokeStyle = 'rgba(80,60,40,0.12)';
      ctx.lineWidth = 1;
      for (let y = 0; y < 128; y += 12) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(128, y); ctx.stroke();
      }
      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(2, 2);
      return tex;
    }
    const groundW = siteBoundsRaw.spanX * 1.06;
    const groundD = siteBoundsRaw.spanZ * 1.06;
    const ground = new THREE.Mesh(
      new THREE.PlaneGeometry(groundW, groundD),
      new THREE.MeshLambertMaterial({ color: pal.ground, map: makeGroundTexture() })
    );
    ground.rotation.x = -Math.PI / 2;
    ground.position.set(siteBoundsRaw.centerX, 0, siteBoundsRaw.centerZ);
    ground.receiveShadow = true;
    ground.userData.pickable = false;
    scene.add(ground);

    const foliageAnim = [];
    const wallTex = makeWallTexture();
    data.path.forEach((id, idx) => {
      const loc = locusById[id];
      if (!loc) return;
      const [fx, fz, fw, fd] = loc.footprint;
      const cx = fx + fw / 2;
      const cz = fz + fd / 2;
      const ox = cx + (idx % 2 === 0 ? -3.5 : 3.5);
      const oz = cz - fd / 2 - 2.5 - (idx % 3) * 0.8;
      const trunk = new THREE.Mesh(
        new THREE.CylinderGeometry(0.15, 0.22, 1.8, 6),
        new THREE.MeshLambertMaterial({ color: 0x6b5344 })
      );
      trunk.castShadow = true;
      trunk.position.set(ox, 0.9, oz);
      const crown = new THREE.Mesh(
        new THREE.ConeGeometry(0.85, 1.5, 8),
        new THREE.MeshLambertMaterial({ color: 0x5a8a4a })
      );
      crown.castShadow = true;
      crown.position.set(ox, 2.4, oz);
      crown.userData.swayPhase = idx * 1.3;
      foliageAnim.push(crown);
      scene.add(trunk, crown);
      if (idx % 2 === 0) {
        const bush = new THREE.Mesh(
          new THREE.SphereGeometry(0.45, 8, 6),
          new THREE.MeshLambertMaterial({ color: 0x4a7a3a })
        );
        bush.castShadow = true;
        bush.position.set(ox + 1.1, 0.38, oz + 0.7);
        bush.userData.swayPhase = idx * 0.7 + 2;
        foliageAnim.push(bush);
        scene.add(bush);
      }
      if (idx % 3 === 1) {
        const pole = new THREE.Mesh(
          new THREE.CylinderGeometry(0.07, 0.09, 3, 6),
          new THREE.MeshLambertMaterial({ color: 0x888888 })
        );
        pole.position.set(cx + fw / 2 + 1.2, 1.5, cz + fd / 2 + 1.2);
        const lamp = new THREE.Mesh(
          new THREE.SphereGeometry(0.18, 8, 6),
          new THREE.MeshLambertMaterial({ color: 0xffe4a0, emissive: 0xffa040, emissiveIntensity: 0.25 })
        );
        lamp.position.set(cx + fw / 2 + 1.2, 3.1, cz + fd / 2 + 1.2);
        scene.add(pole, lamp);
      }
    });
    const dustCount = 36;
    const dustPos = new Float32Array(dustCount * 3);
    for (let i = 0; i < dustCount; i++) {
      dustPos[i * 3] = siteBoundsRaw.centerX + (Math.random() - 0.5) * siteBoundsRaw.spanX;
      dustPos[i * 3 + 1] = 0.5 + Math.random() * 2.5;
      dustPos[i * 3 + 2] = siteBoundsRaw.centerZ + (Math.random() - 0.5) * siteBoundsRaw.spanZ;
    }
    const dustGeo = new THREE.BufferGeometry();
    dustGeo.setAttribute('position', new THREE.BufferAttribute(dustPos, 3));
    const dust = new THREE.Points(dustGeo, new THREE.PointsMaterial({
      color: 0xffeedd, size: 0.14, transparent: true, opacity: 0.35, sizeAttenuation: true
    }));
    scene.add(dust);

    const edgeMat = new THREE.LineBasicMaterial({ color: pal.edge, linewidth: 1 });
    const buildingGroups = {};
    const interiorGroups = {};
    const buildingMeshes = {};
    const pickables = [];
    const labelEntries = [];
    let pathGroup = null;
    let hovered = null;

    function shadowMesh(mesh) {
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      return mesh;
    }

    function addEdges(mesh) {
      const edges = new THREE.LineSegments(new THREE.EdgesGeometry(mesh.geometry), edgeMat);
      edges.position.copy(mesh.position);
      edges.rotation.copy(mesh.rotation);
      edges.scale.copy(mesh.scale);
      mesh.parent.add(edges);
      return edges;
    }

    function addLabel(worldPos, text, kind, scope) {
      const el = document.createElement('div');
      el.className = 'map-label map-label-' + kind;
      el.textContent = text;
      labelLayer.appendChild(el);
      labelEntries.push({ el, pos: worldPos.clone(), kind, scope: scope || 'site' });
    }

    function updateLabelVisibility() {
      labelEntries.forEach(entry => {
        const show = navLevel === 'site'
          ? entry.scope === 'site'
          : entry.scope === 'interior' && entry.buildingId === activeBuildingId;
        entry.el.style.display = show ? 'block' : 'none';
      });
    }

    function updateLabels() {
      const w = canvas.clientWidth;
      const h = canvas.clientHeight;
      const tmp = new THREE.Vector3();
      labelEntries.forEach(entry => {
        if (entry.el.style.display === 'none') return;
        tmp.copy(entry.pos);
        tmp.project(camera);
        if (tmp.z > 1) { entry.el.style.opacity = '0'; return; }
        entry.el.style.opacity = '1';
        entry.el.style.left = ((tmp.x + 1) / 2 * w) + 'px';
        entry.el.style.top = ((-tmp.y + 1) / 2 * h) + 'px';
      });
    }

    function addRoof(g, fw, fd, h, variant, roofMat, loc) {
      if (variant === 'pitch') {
        const roof = shadowMesh(new THREE.Mesh(
          new THREE.ConeGeometry(Math.max(fw, fd) * 0.58, h * 0.42, 4),
          roofMat
        ));
        roof.position.y = h + h * 0.18;
        roof.rotation.y = Math.PI / 4;
        g.add(roof);
        addEdges(roof);
        return roof;
      }
      if (variant === 'gable') {
        const rw = fw + 0.25;
        const slopeH = h * 0.38;
        const s1 = shadowMesh(new THREE.Mesh(new THREE.BoxGeometry(rw, 0.18, fd * 0.55), roofMat));
        s1.position.set(0, h + slopeH * 0.35, -fd * 0.14);
        s1.rotation.x = Math.PI / 5;
        const s2 = shadowMesh(new THREE.Mesh(new THREE.BoxGeometry(rw, 0.18, fd * 0.55), roofMat));
        s2.position.set(0, h + slopeH * 0.35, fd * 0.14);
        s2.rotation.x = -Math.PI / 5;
        g.add(s1, s2);
        addEdges(s1);
        addEdges(s2);
        return s1;
      }
      if (variant === 'scaffold') {
        const frame = new THREE.Mesh(
          new THREE.BoxGeometry(fw, h, fd),
          new THREE.MeshLambertMaterial({ color: 0xaaaaaa, wireframe: true })
        );
        frame.position.y = h / 2;
        g.add(frame);
        return frame;
      }
      const roof = shadowMesh(new THREE.Mesh(
        new THREE.BoxGeometry(fw + 0.3, 0.35, fd + 0.3),
        roofMat
      ));
      roof.position.y = h + 0.15;
      g.add(roof);
      addEdges(roof);
      return roof;
    }

    function addArchetypeDetail(g, fw, fd, h, stepIdx) {
      const detailMat = new THREE.MeshLambertMaterial({ color: pal.detail });
      const theme = data.theme || 'corridor';
      if (theme === 'construction' && stepIdx % 2 === 0) {
        const pole = shadowMesh(new THREE.Mesh(new THREE.BoxGeometry(0.35, h * 1.4, 0.35), detailMat));
        pole.position.set(fw / 2 - 1.2, h * 0.7, -fd / 2 + 1);
        const arm = shadowMesh(new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.2, 0.2), detailMat));
        arm.position.set(fw / 2 - 2.4, h * 1.35, -fd / 2 + 1);
        g.add(pole, arm);
      } else if (theme === 'museum') {
        const ped = shadowMesh(new THREE.Mesh(new THREE.ConeGeometry(fw * 0.35, 1.1, 3), detailMat));
        ped.position.set(0, h + 0.65, fd / 2 + 0.05);
        ped.rotation.y = Math.PI;
        g.add(ped);
      } else if (theme === 'corridor') {
        const chim = shadowMesh(new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 1.1, 8), detailMat));
        chim.position.set(-fw / 2 + 1.2, h + 0.75, fd / 2 - 0.8);
        g.add(chim);
      } else if (theme === 'library') {
        for (let i = 0; i < 2; i++) {
          const stack = shadowMesh(new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.7 + i * 0.15, 0.35), detailMat));
          stack.position.set(fw / 2 - 1 - i * 0.6, h + 0.4, -fd / 2 + 0.8);
          g.add(stack);
        }
      }
    }

    function addBuilding(loc, stepIdx) {
      const [fx, fz, fw, fd] = loc.footprint;
      const h = buildingHeight(loc, stepIdx);
      const variant = roofVariant(stepIdx, loc);
      const g = new THREE.Group();
      g.position.set(fx + fw / 2, 0, fz + fd / 2);

      const bodyMat = new THREE.MeshLambertMaterial({
        color: loc.blocked ? 0x999999 : pal.building,
        map: loc.blocked ? null : wallTex,
        emissive: 0x000000
      });
      const body = shadowMesh(new THREE.Mesh(new THREE.BoxGeometry(fw, h, fd), bodyMat));
      body.position.y = h / 2;
      body.userData = { kind: 'building', id: loc.id };
      g.add(body);
      const bodyEdges = addEdges(body);

      const roofMat = new THREE.MeshLambertMaterial({ color: loc.blocked ? 0x888888 : pal.roof });
      const roof = addRoof(g, fw, fd, h, variant, roofMat, loc);
      roof.userData = { kind: 'building', id: loc.id };

      if (!loc.blocked) addArchetypeDetail(g, fw, fd, h, stepIdx);

      scene.add(g);
      buildingGroups[loc.id] = g;
      buildingMeshes[loc.id] = { body, bodyMat, roof, bodyEdges, h };
      pickables.push(body, roof);

      const cx = fx + fw / 2;
      const cz = fz + fd / 2;
      addLabel(new THREE.Vector3(cx, h + 2.4, cz), loc.label, 'building', 'site');

      const ig = new THREE.Group();
      ig.visible = false;
      ig.position.copy(g.position);
      (loc.interior?.zones || []).forEach(z => {
        const [zx, zz, zw, zd] = z.footprint;
        const zm = shadowMesh(new THREE.Mesh(
          new THREE.BoxGeometry(zw, 0.3, zd),
          new THREE.MeshLambertMaterial({ color: pal.zone })
        ));
        zm.position.set(zx + zw / 2 - fw / 2, 0.35, zz + zd / 2 - fd / 2);
        zm.userData = { kind: 'zone', id: z.id, buildingId: loc.id, concepts: z.concepts, label: z.label };
        ig.add(zm);
        addEdges(zm);
        pickables.push(zm);
        const zwx = cx + (zx + zw / 2 - fw / 2);
        const zwz = cz + (zz + zd / 2 - fd / 2);
        addLabel(new THREE.Vector3(zwx, 1.1, zwz), z.label, 'zone', 'interior');
        labelEntries[labelEntries.length - 1].buildingId = loc.id;
      });
      (loc.interior?.hotspots || []).forEach(hs => {
        const pin = shadowMesh(new THREE.Mesh(
          new THREE.CylinderGeometry(0.25, 0.25, 0.9, 8),
          new THREE.MeshLambertMaterial({ color: pal.pin })
        ));
        pin.position.set(hs.at[0] - fw / 2, 0.55, hs.at[2] - fd / 2);
        pin.userData = { kind: 'hotspot', id: hs.id, buildingId: loc.id, concept: hs.concept, label: hs.label };
        ig.add(pin);
        pickables.push(pin);
        const hwx = cx + (hs.at[0] - fw / 2);
        const hwz = cz + (hs.at[2] - fd / 2);
        addLabel(new THREE.Vector3(hwx, 1.4, hwz), '● ' + hs.label, 'hotspot', 'interior');
        labelEntries[labelEntries.length - 1].buildingId = loc.id;
      });
      scene.add(ig);
      interiorGroups[loc.id] = ig;
    }

    function buildPathRoute() {
      pathGroup = new THREE.Group();
      const pts = [];
      const ribbonMat = new THREE.MeshLambertMaterial({ color: pal.ribbon, transparent: true, opacity: 0.55 });

      data.path.forEach((id, idx) => {
        const loc = locusById[id];
        if (!loc) return;
        const [fx, fz, fw, fd] = loc.footprint;
        const cx = fx + fw / 2;
        const cz = fz + fd / 2;
        const h = buildingHeight(loc, idx);
        pts.push(new THREE.Vector3(cx, 0.12, cz));

        const pad = shadowMesh(new THREE.Mesh(
          new THREE.CylinderGeometry(0.9, 0.9, 0.05, 20),
          new THREE.MeshLambertMaterial({ color: pal.path, transparent: true, opacity: 0.35 })
        ));
        pad.position.set(cx, 0.04, cz);
        pathGroup.add(pad);

        const sprite = makeNumberSprite(idx + 1);
        sprite.position.copy(pathSpriteWorldPos(loc, idx));
        pathGroup.add(sprite);
      });

      if (pts.length > 1) {
        for (let i = 0; i < pts.length - 1; i++) {
          const a = pts[i];
          const b = pts[i + 1];
          const mid = new THREE.Vector3().addVectors(a, b).multiplyScalar(0.5);
          const len = a.distanceTo(b);
          const seg = shadowMesh(new THREE.Mesh(
            new THREE.BoxGeometry(len, 0.06, 0.55),
            ribbonMat
          ));
          seg.position.set(mid.x, 0.1, mid.z);
          seg.lookAt(b.x, b.y, b.z);
          seg.rotateY(Math.PI / 2);
          pathGroup.add(seg);
        }
        const geo = new THREE.BufferGeometry().setFromPoints(pts);
        const line = new THREE.Line(geo, new THREE.LineDashedMaterial({
          color: pal.ribbon, dashSize: 1.2, gapSize: 0.6, linewidth: 1
        }));
        line.computeLineDistances();
        pathGroup.add(line);
      }
      scene.add(pathGroup);
    }

    data.path.forEach((id, idx) => {
      const loc = locusById[id];
      if (loc && loc.kind === 'building') addBuilding(loc, idx);
    });
    buildPathRoute();

    let tourTween = null;
    let tourMode3d = false;

    function computeTourPose(stopIdx) {
      const id = data.path[stopIdx];
      const loc = locusById[id];
      if (!loc) return null;
      const [fx, fz, fw, fd] = loc.footprint;
      const h = buildingHeight(loc, stopIdx);
      const cx = fx + fw / 2;
      const cz = fz + fd / 2;
      const standoff = Math.max(fw, fd) * 0.9 + 2.5;
      return {
        pos: new THREE.Vector3(cx, EYE_HEIGHT, cz + fd / 2 + standoff),
        look: new THREE.Vector3(cx, h * 0.45, cz)
      };
    }

    function setTourHighlight(bid) {
      Object.entries(buildingMeshes).forEach(([id, bm]) => {
        const on = bid && id === bid;
        if (bm.bodyMat.emissive) {
          bm.bodyMat.emissive.setHex(on ? 0x553300 : 0x000000);
          bm.bodyMat.emissiveIntensity = on ? 0.35 : 0;
        }
      });
    }

    function animateTourCamera(pose, cb) {
      if (!pose) return;
      if (reducedMotion) {
        camera.position.copy(pose.pos);
        camera.lookAt(pose.look);
        if (cb) cb();
        return;
      }
      tourTween = {
        from: {
          px: camera.position.x, py: camera.position.y, pz: camera.position.z,
          lx: camTarget.x, ly: camTarget.y, lz: camTarget.z
        },
        to: {
          px: pose.pos.x, py: pose.pos.y, pz: pose.pos.z,
          lx: pose.look.x, ly: pose.look.y, lz: pose.look.z
        },
        start: performance.now(), dur: 1100, cb
      };
    }

    function enterTour3d() {
      tween = null;
      tourMode3d = true;
      navLevel = 'tour';
      restoreAllBuildings();
      Object.values(buildingGroups).forEach(g => { g.visible = true; });
      Object.values(interiorGroups).forEach(g => { g.visible = false; });
      if (pathGroup) pathGroup.visible = true;
      updateLabelVisibility();
      canvas.style.cursor = 'default';
    }

    function exitTour3d() {
      tourMode3d = false;
      tourTween = null;
      setTourHighlight(null);
      navLevel = 'site';
      fitSiteCamera();
      placeCamera();
    }

    reliefTourApi = {
      enter: enterTour3d,
      exit: exitTour3d,
      goToStop: (idx) => {
        const bid = data.path[idx];
        const pose = computeTourPose(idx);
        setTourHighlight(bid);
        tween = null;
        if (!pose) return;
        animateTourCamera(pose);
      },
      getCameraY: () => camera.position.y
    };

    function restoreAllBuildings() {
      Object.values(buildingMeshes).forEach(bm => {
        bm.roof.visible = true;
        bm.bodyMat.transparent = false;
        bm.bodyMat.opacity = 1;
        bm.bodyMat.depthWrite = true;
        bm.bodyEdges.visible = true;
      });
    }

    function applyCutaway(bid) {
      Object.entries(buildingMeshes).forEach(([id, bm]) => {
        if (id === bid) {
          bm.roof.visible = false;
          bm.bodyMat.transparent = true;
          bm.bodyMat.opacity = 0.14;
          bm.bodyMat.depthWrite = false;
          bm.bodyEdges.visible = true;
        }
      });
    }

    function getPickables() {
      return pickables.filter(m => {
        if (m.visible === false || m.parent?.visible === false) return false;
        if (navLevel === 'interior' && m.userData.kind === 'building') return false;
        return true;
      });
    }

    function clearHover() {
      if (!hovered) return;
      if (hovered.material?.emissive) hovered.material.emissive.setHex(0x000000);
      hovered = null;
    }

    function setHover(mesh) {
      if (hovered === mesh) return;
      clearHover();
      if (!mesh) {
        canvas.style.cursor = navLevel === 'site' ? 'grab' : 'default';
        return;
      }
      hovered = mesh;
      if (mesh.material?.emissive) mesh.material.emissive.setHex(0x222222);
      canvas.style.cursor = 'pointer';
    }

    function placeCamera() {
      placeCameraAtDist(camDist);
    }
    fitSiteCamera();
    canvas.style.cursor = 'grab';

    let tween = null;
    function animateCamera(toTarget, toDist, cb) {
      if (reducedMotion) {
        camTarget = toTarget;
        camDist = toDist;
        placeCamera();
        if (cb) cb();
        return;
      }
      const from = { tx: camTarget.x, ty: camTarget.y, tz: camTarget.z, d: camDist };
      const to = { tx: toTarget.x, ty: toTarget.y, tz: toTarget.z, d: toDist };
      tween = { from, to, start: performance.now(), dur: 400, cb };
    }

    function goSite3d() {
      navLevel = 'site';
      activeBuildingId = null;
      restoreAllBuildings();
      Object.values(buildingGroups).forEach(g => { g.visible = true; });
      Object.values(interiorGroups).forEach(g => { g.visible = false; });
      if (pathGroup) pathGroup.visible = true;
      updateLabelVisibility();
      mapPan = { x: 0, z: 0 };
      mapZoom = 1;
      closePanel();
      fitSiteCamera();
      animateCamera(
        { x: siteFitTarget.x, y: siteFitTarget.y, z: siteFitTarget.z },
        siteFitDist,
        () => updateBreadcrumb()
      );
    }
    goSite = goSite3d;

    function openBuilding3d(bid) {
      const loc = locusById[bid];
      if (!loc || loc.blocked) {
        showPanel(conceptsForIds(loc?.concepts), loc?.label, data.lang === 'fr' ? 'Question ouverte' : 'Open question');
        return;
      }
      activeBuildingId = bid;
      navLevel = 'interior';
      restoreAllBuildings();
      Object.entries(buildingGroups).forEach(([id, g]) => { g.visible = id === bid; });
      Object.entries(interiorGroups).forEach(([id, g]) => { g.visible = id === bid; });
      applyCutaway(bid);
      if (pathGroup) pathGroup.visible = false;
      updateLabelVisibility();
      const [fx, fz, fw, fd] = loc.footprint;
      animateCamera({ x: fx + fw / 2, y: 0, z: fz + fd / 2 }, 22, () => {
        updateBreadcrumb();
        if (!loc.interior?.zones?.length) {
          showPanel(conceptsForIds(loc.concepts), loc.label, data.lang === 'fr' ? 'Bâtiment' : 'Building');
        }
      });
    }

    btnBack.onclick = goSite3d;

    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    let pointerDown = false;
    let moved = false;
    let suppressClick = false;
    let downX = 0;
    let downY = 0;

    function setMouseFromEvent(e) {
      const rect = canvas.getBoundingClientRect();
      mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    }

    canvas.addEventListener('pointerdown', e => {
      if (e.button !== 0 || tourActive || tourMode3d) return;
      pointerDown = true;
      moved = false;
      suppressClick = false;
      downX = e.clientX;
      downY = e.clientY;
      canvas.setPointerCapture(e.pointerId);
      canvas.style.cursor = 'grabbing';
    });

    canvas.addEventListener('pointermove', e => {
      setMouseFromEvent(e);
      if (tourActive || tourMode3d) return;
      if (pointerDown && navLevel === 'site') {
        const dx = e.clientX - downX;
        const dy = e.clientY - downY;
        if (Math.abs(dx) > 5 || Math.abs(dy) > 5) {
          moved = true;
          mapPan.x -= dx * 0.04;
          mapPan.z -= dy * 0.04;
          downX = e.clientX;
          downY = e.clientY;
          placeCamera();
        }
        return;
      }
      if (!pointerDown) {
        raycaster.setFromCamera(mouse, camera);
        const hits = raycaster.intersectObjects(getPickables());
        setHover(hits.length ? hits[0].object : null);
      }
    });

    canvas.addEventListener('pointerup', e => {
      if (moved) suppressClick = true;
      pointerDown = false;
      try { canvas.releasePointerCapture(e.pointerId); } catch (_) {}
      canvas.style.cursor = hovered ? 'pointer' : (navLevel === 'site' ? 'grab' : 'default');
    });

    canvas.addEventListener('wheel', e => {
      if (tourActive || tourMode3d || navLevel !== 'site') return;
      e.preventDefault();
      mapZoom = Math.min(2.5, Math.max(0.6, mapZoom * (e.deltaY > 0 ? 0.92 : 1.08)));
      placeCamera();
    }, { passive: false });

    canvas.addEventListener('click', e => {
      if (suppressClick) { suppressClick = false; moved = false; return; }
      setMouseFromEvent(e);
      raycaster.setFromCamera(mouse, camera);
      const hits = raycaster.intersectObjects(getPickables());
      if (!hits.length) return;
      const ud = hits[0].object.userData;
      if (ud.kind === 'building' && navLevel === 'site') openBuilding3d(ud.id);
      else if (ud.kind === 'zone') showPanel(conceptsForIds(ud.concepts), ud.label, locusById[ud.buildingId]?.label);
      else if (ud.kind === 'hotspot') {
        const c = conceptById[ud.concept];
        showPanel(c ? [c] : [], ud.label, locusById[ud.buildingId]?.label);
      }
    });

    window.addEventListener('resize', resizeCanvas);
    if (typeof ResizeObserver !== 'undefined') {
      new ResizeObserver(resizeCanvas).observe(canvas);
    }

    window.__palaceMetrics = function () {
      const dpr = renderer.getPixelRatio();
      const cw = canvas.clientWidth;
      const ch = canvas.clientHeight;
      let sprites = 0;
      let ribbons = 0;
      const spriteViewport = [];
      if (pathGroup) {
        pathGroup.children.forEach(o => {
          if (o.isSprite) {
            sprites++;
            tmpProj.copy(o.position);
            tmpProj.project(camera);
            const nx = (tmpProj.x + 1) / 2;
            const ny = (-tmpProj.y + 1) / 2;
            const inView = tmpProj.z <= 1
              && nx >= FIT_MARGIN && nx <= 1 - FIT_MARGIN
              && ny >= FIT_MARGIN && ny <= 1 - FIT_MARGIN;
            spriteViewport.push({ inView, nx, ny, z: tmpProj.z });
          }
          if (o.geometry?.parameters?.height === 0.06) ribbons++;
        });
      }
      const siteExtents = projectSiteExtents(camDist);
      const spriteNx = spriteViewport.map(s => s.nx);
      const spriteNy = spriteViewport.map(s => s.ny);
      return {
        pathSteps: data.path.length,
        pathSprites: sprites,
        ribbonSegments: ribbons,
        spritesInView: spriteViewport.filter(s => s.inView).length,
        allSpritesInView: spriteViewport.length > 0 && spriteViewport.every(s => s.inView),
        spriteViewport,
        siteExtents,
        spriteSpreadNx: spriteNx.length ? Math.max(...spriteNx) - Math.min(...spriteNx) : 0,
        spriteSpreadNy: spriteNy.length ? Math.max(...spriteNy) - Math.min(...spriteNy) : 0,
        canvasW: canvas.width,
        canvasH: canvas.height,
        clientW: cw,
        clientH: ch,
        dpr,
        aspectCanvas: canvas.width / canvas.height,
        aspectClient: cw / ch,
        usesClientSizing: Math.abs(canvas.width - Math.round(cw * dpr)) <= 2,
        siteFitDist,
        siteFitTarget,
        hasFog: scene.fog !== null,
        skyHex: scene.background?.getHex?.() ?? 0,
        tourActive: tourActive,
        tourStop: tourStopIdx,
        cameraY: camera.position.y,
        tourMode3d: tourMode3d
      };
    };

    updateLabelVisibility();

    let tabVisible = true;
    document.addEventListener('visibilitychange', () => { tabVisible = !document.hidden; });

    function loop(now) {
      requestAnimationFrame(loop);
      if (tourTween) {
        const t = Math.min(1, (now - tourTween.start) / tourTween.dur);
        const ease = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
        const f = tourTween.from, to = tourTween.to;
        camera.position.set(
          f.px + (to.px - f.px) * ease,
          f.py + (to.py - f.py) * ease,
          f.pz + (to.pz - f.pz) * ease
        );
        const lx = f.lx + (to.lx - f.lx) * ease;
        const ly = f.ly + (to.ly - f.ly) * ease;
        const lz = f.lz + (to.lz - f.lz) * ease;
        camera.lookAt(lx, ly, lz);
        camTarget = { x: lx, y: ly, z: lz };
        if (t >= 1) { const cb = tourTween.cb; tourTween = null; if (cb) cb(); }
      } else if (tween && !tourActive) {
        const t = Math.min(1, (now - tween.start) / tween.dur);
        const ease = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
        camTarget.x = tween.from.tx + (tween.to.tx - tween.from.tx) * ease;
        camTarget.y = tween.from.ty + (tween.to.ty - tween.from.ty) * ease;
        camTarget.z = tween.from.tz + (tween.to.tz - tween.from.tz) * ease;
        camDist = tween.from.d + (tween.to.d - tween.from.d) * ease;
        placeCamera();
        if (t >= 1) { const cb = tween.cb; tween = null; if (cb) cb(); }
      }
      if (foliageAnim.length) {
        foliageAnim.forEach(m => {
          m.rotation.z = Math.sin(now * 0.0012 + (m.userData.swayPhase || 0)) * 0.035;
        });
      }
      if (dust) {
        const arr = dust.geometry.attributes.position.array;
        for (let i = 0; i < arr.length; i += 3) {
          arr[i + 1] += Math.sin(now * 0.0008 + i) * 0.0004;
        }
        dust.geometry.attributes.position.needsUpdate = true;
      }
      if (!tabVisible) return;
      updateLabels();
      renderer.render(scene, camera);
    }
    loop(0);
    updateBreadcrumb();
  }

  // --- Boot ---
  closePanel();
  document.getElementById('overlay-first')?.addEventListener('click', function () {
    this.classList.remove('visible');
    this.classList.add('hidden');
  });
  document.getElementById('panel-close')?.addEventListener('click', closePanel);
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      if (tourActive) endTour();
      else closePanel();
    }
    if (tourActive && e.key === 'ArrowLeft') tourStep(-1);
    if (tourActive && e.key === 'ArrowRight') tourStep(1);
  });

  const useIso = window.FORCE_2D
    || window.matchMedia('(max-width: 800px)').matches
    || window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (useIso) {
    enableIsoMode();
  } else if (typeof THREE !== 'undefined') {
    try {
      initRelief();
    } catch (err) {
      console.warn('WebGL relief failed, falling back to iso-SVG', err);
      enableIsoMode();
    }
  } else {
    enableIsoMode();
  }
})();
"""

CSS = """
:root {
  --bg: #1e2430; --surface: #2a3244; --text: #e8eaed; --muted: #9aa0a6; --accent: #5b8fd4;
  --map-sky: #f0ead6; --font: system-ui, -apple-system, sans-serif;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; overflow: hidden; font-family: var(--font); background: var(--bg); color: var(--text); }
body[data-theme="construction"] { --map-sky: #f0ead6; }
body[data-theme="museum"] { --map-sky: #f7f4ef; }
body[data-theme="corridor"] { --map-sky: #f5f0ea; }
body[data-theme="library"] { --map-sky: #ede8dc; }
#app { display: grid; grid-template-columns: 1fr auto; grid-template-rows: auto 1fr; height: 100vh; }
header.top { grid-column: 1 / -1; display: flex; align-items: center; gap: 1rem; padding: 0.5rem 1rem; background: var(--surface); border-bottom: 1px solid #3a4558; z-index: 10; }
header.top h1 { font-size: 0.95rem; font-weight: 600; }
#breadcrumb { font-size: 0.78rem; color: var(--muted); flex: 1; }
#breadcrumb .crumb { background: none; border: none; color: var(--accent); cursor: pointer; font-size: inherit; padding: 0; }
#btn-back, #btn-tour, #btn-map-view { background: var(--surface); color: var(--text); border: 1px solid #3a4558; padding: 0.35rem 0.75rem; border-radius: 4px; cursor: pointer; font-size: 0.78rem; }
#btn-tour { background: #c87941; color: #fff; border-color: #a06030; font-weight: 600; }
#btn-map-view { background: var(--accent); color: #fff; border-color: #4a7ab8; }
#btn-back[hidden], #btn-tour[hidden], #btn-map-view[hidden], #tour-nav[hidden] { display: none; }
#tour-nav { display: flex; align-items: center; gap: 0.5rem; }
#tour-nav button { background: var(--surface); color: var(--text); border: 1px solid #3a4558; padding: 0.3rem 0.6rem; border-radius: 4px; cursor: pointer; font-size: 0.75rem; }
#tour-nav button:disabled { opacity: 0.4; cursor: default; }
#tour-counter { font-size: 0.75rem; color: var(--muted); min-width: 3rem; text-align: center; }
.scene-block { margin-bottom: 1.25rem; padding: 1rem 1.1rem; border-radius: 10px; background: linear-gradient(135deg, rgba(200,121,65,0.18), rgba(255,230,180,0.12)); border: 1px solid rgba(200,121,65,0.35); }
.scene-image { font-size: 1.05rem; line-height: 1.55; font-weight: 500; color: #f5e6d0; margin-bottom: 0.65rem; }
.scene-sense { font-size: 0.82rem; line-height: 1.45; color: #c8b8a0; margin: 0.3rem 0; padding-left: 0.5rem; border-left: 2px solid rgba(200,121,65,0.5); }
.main-view { position: relative; min-height: 0; background: var(--map-sky); }
#relief-canvas { display: block; width: 100%; height: 100%; cursor: grab; touch-action: none; background: var(--map-sky); }
#relief-canvas.hidden, #iso-map.hidden, #label-layer.hidden { display: none !important; }
#label-layer { position: absolute; inset: 0; pointer-events: none; overflow: hidden; z-index: 4; }
.map-label { position: absolute; transform: translate(-50%, -100%); padding: 0.2rem 0.45rem; border-radius: 4px; font-size: 0.68rem; font-weight: 600; white-space: nowrap; background: rgba(255,255,255,0.92); color: #2a3040; border: 1px solid rgba(91,143,212,0.45); box-shadow: 0 2px 6px rgba(0,0,0,0.12); }
.map-label-building { color: #1a2030; border-color: #5b8fd4; }
.map-label-zone { font-size: 0.62rem; border-color: rgba(0,0,0,0.15); }
.map-label-hotspot { font-size: 0.6rem; color: #b45309; }
#iso-map { position: absolute; inset: 0; overflow: auto; padding: 3rem 1rem 1rem; background: var(--map-sky); display: block; }
.iso-interior { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 1rem; max-width: 640px; }
.iso-zone, .iso-hotspot, .iso-back { padding: 0.75rem 1rem; background: var(--surface); border: 2px solid var(--accent); border-radius: 8px; color: var(--text); cursor: pointer; font-size: 0.88rem; }
.iso-hotspot { border-style: dashed; }
#detail-panel { width: 300px; background: var(--surface); border-left: 1px solid #3a4558; padding: 1rem; overflow-y: auto; z-index: 10; }
#detail-panel[hidden] { display: none; }
#panel-close { float: right; background: none; border: none; color: var(--muted); font-size: 1.2rem; cursor: pointer; }
#panel-title { font-size: 1rem; color: var(--accent); margin-top: 0.25rem; }
#panel-sub { font-size: 0.75rem; color: var(--muted); margin-bottom: 0.75rem; }
.concept-card { margin-bottom: 1rem; padding: 0.75rem; background: var(--bg); border-radius: 8px; }
.concept-card h3 { font-size: 0.92rem; margin: 0.35rem 0; }
.concept-card p { font-size: 0.85rem; line-height: 1.45; color: var(--text); }
.concept-card small { color: var(--muted); font-size: 0.72rem; }
.badge { display: inline-block; padding: 0.12rem 0.45rem; border-radius: 4px; font-size: 0.65rem; color: #fff; text-transform: uppercase; }
.overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.8); z-index: 30; display: none; align-items: center; justify-content: center; padding: 2rem; }
.overlay.visible { display: flex; }
.overlay.hidden { display: none; }
.overlay .panel { background: var(--surface); padding: 1.5rem; border-radius: 10px; max-width: 420px; line-height: 1.55; text-align: center; }
footer.meta { position: fixed; bottom: 0; left: 0; font-size: 0.65rem; color: var(--muted); padding: 0.35rem 0.75rem; z-index: 5; pointer-events: none; }
@media (max-width: 800px) {
  #app { grid-template-columns: 1fr; grid-template-rows: auto 1fr auto; }
  #detail-panel { width: 100%; max-height: 40vh; border-left: none; border-top: 1px solid #3a4558; }
}
"""


def compose(json_path: Path, out_path: Path, force_2d: bool = False) -> None:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    lang = data.get("lang", "fr")
    title = data.get("title", data.get("slug", "Memory Palace"))
    created = data.get("created", "")
    sources = ", ".join(data.get("source_files", []))

    overlay_fr = "Clique un <strong>bâtiment</strong> pour entrer. À l'intérieur, clique une <strong>zone</strong> ou un <strong>repère</strong> pour voir le concept. Pas de déplacement — seulement la carte."
    overlay_en = "Click a <strong>building</strong> to enter. Inside, click a <strong>zone</strong> or <strong>pin</strong> for the concept. No walking — map and clicks only."

    three_js = ""
    if not force_2d and VENDOR.is_file():
        three_js = VENDOR.read_text(encoding="utf-8")
    elif not force_2d:
        print("warning: three.min.js missing — iso fallback", file=sys.stderr)
        force_2d = True

    palace_json = json.dumps(data, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Relief Map</title>
  <style>{CSS}</style>
</head>
<body data-theme="{data.get('theme', 'construction')}">
  <div id="app">
    <header class="top">
      <h1>{title}</h1>
      <nav id="breadcrumb" aria-label="breadcrumb"></nav>
      <button type="button" id="btn-tour">{'Visite guidée' if lang == 'fr' else 'Guided tour'}</button>
      <div id="tour-nav" hidden>
        <button type="button" id="tour-prev">{'← Précédent' if lang == 'fr' else '← Previous'}</button>
        <span id="tour-counter"></span>
        <button type="button" id="tour-next">{'Suivant →' if lang == 'fr' else 'Next →'}</button>
      </div>
      <button type="button" id="btn-map-view" hidden>{'Vue carte' if lang == 'fr' else 'Map view'}</button>
      <button type="button" id="btn-back" hidden>{'← Retour' if lang == 'fr' else '← Back'}</button>
    </header>
    <div class="main-view">
      <canvas id="relief-canvas" aria-label="Carte en relief"></canvas>
      <div id="label-layer" aria-hidden="true"></div>
      <div id="iso-map" class="hidden" aria-label="Carte isométrique"></div>
      <footer class="meta">{created} · {sources}</footer>
    </div>
    <aside id="detail-panel" hidden aria-live="polite">
      <button type="button" id="panel-close" aria-label="Fermer">×</button>
      <h2 id="panel-title"></h2>
      <p id="panel-sub"></p>
      <div id="panel-body"></div>
    </aside>
  </div>
  <div id="overlay-first" class="overlay visible">
    <div class="panel">{overlay_fr if lang == 'fr' else overlay_en}</div>
  </div>
  <script>{three_js}</script>
  <script>
    const PALACE_DATA = {palace_json};
    window.FORCE_2D = {'true' if force_2d else 'false'};
  </script>
  <script>{SCENE_JS}</script>
</body>
</html>
"""
    out_path.write_text(html, encoding="utf-8")
    print(f"Wrote {out_path} ({out_path.stat().st_size} bytes)")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("json", type=Path)
    p.add_argument("-o", "--output", type=Path)
    p.add_argument("--2d-only", action="store_true", dest="only_2d")
    args = p.parse_args()
    out = args.output or args.json.with_suffix(".html")
    compose(args.json, out, force_2d=args.only_2d)


if __name__ == "__main__":
    main()