/* Grow Nest particle hero.
   A <canvas data-shapes="growth,phone,bag"> becomes a field of glowing dots that
   form each shape in turn. One shape = it holds and breathes. WebGL with a
   Canvas 2D fallback; pauses when off screen; static under reduced motion. */

const TAU = Math.PI * 2;
const rnd = (a, b) => a + Math.random() * (b - a);
const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
const smooth = (a, b, x) => { const t = clamp((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
const ease = t => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---------- sampling shapes from an offscreen canvas ---------- */
const S = 400, HS = 200;
let off = null, g = null;
function pen() {
  if (!g) { off = document.createElement('canvas'); off.width = off.height = S; g = off.getContext('2d', { willReadFrequently: true }); }
  return g;
}
function sample(draw, n) {
  const c = pen();
  c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, S, S);
  c.save(); c.fillStyle = '#fff'; c.strokeStyle = '#fff'; c.lineCap = 'round'; c.lineJoin = 'round'; c.lineWidth = 1;
  draw(c); c.restore();
  const d = c.getImageData(0, 0, S, S).data, pix = [];
  for (let i = 3, p = 0; i < d.length; i += 4, p++) if (d[i] > 127) pix.push(p);
  const out = new Float32Array(n * 2), m = pix.length;
  for (let i = 0; i < n; i++) {
    let p;
    if (!m) { out[i * 2] = rnd(-1, 1); out[i * 2 + 1] = rnd(-1, 1); continue; }
    if (m >= n) { const k = i + ((Math.random() * (m - i)) | 0); p = pix[k]; pix[k] = pix[i]; pix[i] = p; }
    else p = pix[(Math.random() * m) | 0];
    out[i * 2] = ((p % S) + Math.random() - HS) / HS;
    out[i * 2 + 1] = (((p / S) | 0) + Math.random() - HS) / HS;
  }
  return out;
}
const rr = (c, x, y, w, h, r) => {
  c.beginPath(); c.moveTo(x + r, y); c.lineTo(x + w - r, y); c.quadraticCurveTo(x + w, y, x + w, y + r);
  c.lineTo(x + w, y + h - r); c.quadraticCurveTo(x + w, y + h, x + w - r, y + h); c.lineTo(x + r, y + h);
  c.quadraticCurveTo(x, y + h, x, y + h - r); c.lineTo(x, y + r); c.quadraticCurveTo(x, y, x + r, y); c.closePath();
};
const line = (c, pts, w) => { c.lineWidth = w; c.beginPath(); c.moveTo(pts[0], pts[1]); for (let i = 2; i < pts.length; i += 2) c.lineTo(pts[i], pts[i + 1]); c.stroke(); };
const ring = (c, x, y, r, w) => { c.lineWidth = w; c.beginPath(); c.arc(x, y, r, 0, TAU); c.stroke(); };
const dot = (c, x, y, r) => { c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill(); };
function arrowHead(c, x1, y1, x2, y2, len, w) {
  const a = Math.atan2(y2 - y1, x2 - x1);
  line(c, [x2 - Math.cos(a - 0.55) * len, y2 - Math.sin(a - 0.55) * len, x2, y2, x2 - Math.cos(a + 0.55) * len, y2 - Math.sin(a + 0.55) * len], w);
}

/* tone: 0 = brand gradient, 1 = bright highlight, 2 = soft fill */
const SHAPES = {
  growth: () => [
    { f: 0.34, tone: 2, alpha: 0.55, draw: c => { [[95, 70], [160, 120], [225, 165], [290, 215]].forEach(([x, h]) => c.fillRect(x - 20, 318 - h, 40, h)); } },
    { f: 0.5, tone: 1, size: 1.08, draw: c => { line(c, [62, 300, 150, 205, 205, 252, 330, 92], 15); arrowHead(c, 205, 252, 330, 92, 46, 15); } },
    { f: 0.16, tone: 0, alpha: 0.75, draw: c => line(c, [52, 330, 348, 330], 5) }
  ],
  phone: () => [
    { f: 0.4, tone: 0, draw: c => { rr(c, 128, 38, 144, 324, 28); c.lineWidth = 10; c.stroke(); line(c, [182, 58, 218, 58], 6); } },
    { f: 0.3, tone: 2, alpha: 0.6, draw: c => c.fillRect(148, 108, 104, 104) },
    { f: 0.12, tone: 0, alpha: 0.8, draw: c => { line(c, [150, 86, 210, 86], 6); line(c, [150, 230, 248, 230], 6); line(c, [150, 248, 220, 248], 6); } },
    { f: 0.18, tone: 1, size: 1.08, draw: c => { rr(c, 148, 272, 104, 30, 15); c.fill(); dot(c, 250, 86, 9); } }
  ],
  bag: () => {
    const path = c => { c.beginPath(); c.moveTo(128, 150); c.lineTo(272, 150); c.lineTo(292, 316); c.quadraticCurveTo(294, 332, 278, 332); c.lineTo(122, 332); c.quadraticCurveTo(106, 332, 108, 316); c.closePath(); };
    return [
      { f: 0.6, tone: 0, draw: c => { path(c); c.lineWidth = 12; c.stroke(); } },
      { f: 0.2, tone: 1, size: 1.06, draw: c => { c.lineWidth = 11; c.beginPath(); c.arc(200, 172, 46, Math.PI * 1.02, Math.PI * 1.98); c.stroke(); dot(c, 154, 180, 6); dot(c, 246, 180, 6); } },
      { f: 0.2, tone: 2, alpha: 0.4, size: 0.85, draw: c => { path(c); c.fill(); } }
    ];
  },
  search: () => [
    { f: 0.5, tone: 0, draw: c => { ring(c, 178, 172, 100, 14); line(c, [252, 246, 326, 320], 24); } },
    { f: 0.32, tone: 1, size: 1.06, draw: c => { [[130, 40], [168, 70], [206, 100]].forEach(([x, h]) => c.fillRect(x - 13, 222 - h, 26, h)); } },
    { f: 0.18, tone: 2, alpha: 0.45, draw: c => { c.beginPath(); c.arc(178, 172, 88, 0, TAU); c.fill(); } }
  ],
  chat: () => [
    { f: 0.64, tone: 0, draw: c => {
      const x = 88, y = 104, w = 224, h = 162, r = 50;
      c.beginPath(); c.moveTo(x + r, y); c.lineTo(x + w - r, y); c.quadraticCurveTo(x + w, y, x + w, y + r);
      c.lineTo(x + w, y + h - r); c.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
      c.lineTo(x + 100, y + h); c.lineTo(x + 44, y + h + 46); c.lineTo(x + 60, y + h); c.lineTo(x + r, y + h);
      c.quadraticCurveTo(x, y + h, x, y + h - r); c.lineTo(x, y + r); c.quadraticCurveTo(x, y, x + r, y); c.closePath();
      c.lineWidth = 12; c.stroke();
    } },
    { f: 0.36, tone: 1, size: 1.06, draw: c => { line(c, [144, 188, 172, 214, 222, 160], 13); line(c, [196, 204, 206, 214, 256, 160], 13); } }
  ],
  mail: () => [
    { f: 0.55, tone: 0, draw: c => { rr(c, 84, 118, 232, 168, 14); c.lineWidth = 11; c.stroke(); } },
    { f: 0.33, tone: 1, size: 1.06, draw: c => line(c, [94, 128, 200, 214, 306, 128], 11) },
    { f: 0.12, tone: 2, alpha: 0.6, draw: c => { line(c, [94, 276, 166, 206], 6); line(c, [306, 276, 234, 206], 6); } }
  ],
  van: () => [
    { f: 0.52, tone: 0, draw: c => {
      c.lineWidth = 11; rr(c, 64, 140, 186, 128, 10); c.stroke();
      c.beginPath(); c.moveTo(250, 176); c.lineTo(300, 176); c.lineTo(338, 222); c.lineTo(338, 268); c.lineTo(250, 268); c.stroke();
      line(c, [262, 190, 296, 190, 318, 218, 262, 218, 262, 190], 7);
    } },
    { f: 0.3, tone: 1, size: 1.06, draw: c => { ring(c, 118, 284, 24, 11); ring(c, 290, 284, 24, 11); dot(c, 118, 284, 6); dot(c, 290, 284, 6); } },
    { f: 0.18, tone: 2, alpha: 0.7, draw: c => { line(c, [14, 170, 46, 170], 7); line(c, [4, 204, 46, 204], 7); line(c, [20, 238, 46, 238], 7); } }
  ],
  cart: () => [
    { f: 0.52, tone: 0, draw: c => {
      line(c, [38, 92, 84, 92], 11);
      c.lineWidth = 11; c.beginPath(); c.moveTo(84, 92); c.lineTo(334, 122); c.lineTo(308, 232); c.lineTo(112, 232); c.closePath(); c.stroke();
      line(c, [112, 232, 122, 272, 304, 272], 10);
    } },
    { f: 0.18, tone: 0, draw: c => { ring(c, 142, 302, 17, 10); ring(c, 280, 302, 17, 10); } },
    { f: 0.3, tone: 1, size: 1.06, draw: c => { c.lineWidth = 9; c.strokeRect(128, 144, 74, 62); c.strokeRect(216, 152, 72, 56); line(c, [165, 144, 165, 206], 5); line(c, [252, 152, 252, 208], 5); } }
  ],
  code: () => [
    { f: 0.48, tone: 0, draw: c => { rr(c, 56, 74, 288, 252, 20); c.lineWidth = 10; c.stroke(); line(c, [56, 118, 344, 118], 8); } },
    { f: 0.1, tone: 2, alpha: 0.8, draw: c => { dot(c, 84, 96, 7); dot(c, 106, 96, 7); dot(c, 128, 96, 7); } },
    { f: 0.42, tone: 1, size: 1.06, draw: c => { line(c, [150, 178, 112, 220, 150, 262], 15); line(c, [222, 168, 180, 274], 15); line(c, [252, 178, 290, 220, 252, 262], 15); } }
  ],
  nest: () => [
    { f: 0.8, tone: 0, draw: c => {
      const cx = 200, cy = 226;
      for (let i = 0; i < 48; i++) { const a0 = rnd(0, TAU); c.lineWidth = rnd(2.5, 5); c.beginPath(); c.ellipse(cx, cy, 148 * rnd(0.95, 1.05), 34 * rnd(0.85, 1.15), rnd(-0.06, 0.06), a0, a0 + rnd(0.5, 1.1)); c.stroke(); }
      for (let i = 0; i < 56; i++) { const ry = rnd(40, 92), rx = 148 - (ry - 40) * 0.6 * rnd(0.6, 1.1), a0 = rnd(0.05, Math.PI - 0.9); c.lineWidth = rnd(2.5, 5.5); c.beginPath(); c.ellipse(cx, cy, rx, ry, rnd(-0.08, 0.08), a0, Math.min(a0 + rnd(0.5, 1), Math.PI - 0.02)); c.stroke(); }
    } },
    { f: 0.2, tone: 1, size: 1.05, draw: c => { c.beginPath(); c.rect(0, 0, S, 236); c.clip(); c.beginPath(); c.ellipse(200, 200, 36, 52, 0, Math.PI, TAU); c.ellipse(200, 200, 36, 40, 0, 0, Math.PI); c.fill(); } }
  ],
  bird: () => [
    { f: 1, tone: 0, draw: c => {
      const wing = flip => {
        const X = x => (flip ? 400 - x : x);
        c.beginPath(); c.moveTo(X(192), 198); c.bezierCurveTo(X(165), 152, X(105), 118, X(26), 128);
        c.lineTo(X(70), 150); c.lineTo(X(62), 160); c.lineTo(X(104), 168); c.lineTo(X(98), 180);
        c.lineTo(X(140), 186); c.lineTo(X(136), 198); c.lineTo(X(190), 226); c.closePath(); c.fill();
      };
      wing(false); wing(true);
      c.beginPath(); c.ellipse(200, 222, 15, 40, 0, 0, TAU); c.fill();
      dot(c, 200, 178, 13);
      c.beginPath(); c.moveTo(188, 252); c.lineTo(190, 294); c.lineTo(200, 280); c.lineTo(210, 294); c.lineTo(212, 252); c.closePath(); c.fill();
    } }
  ],
  globe: () => null // built separately
};

/* ---------- globe ---------- */
const deg = Math.PI / 180;
const ll = (lat, lon) => [Math.cos(lat * deg) * Math.sin(lon * deg), -Math.sin(lat * deg), Math.cos(lat * deg) * Math.cos(lon * deg)];
const norm = v => { const l = Math.hypot(v[0], v[1], v[2]) || 1; return [v[0] / l, v[1] / l, v[2] / l]; };
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const MARKETS = [[40.2, -3.7], [53.5, -1.8], [51.1, 10.4], [46.6, 2.4], [52.2, 5.3], [39.8, -98.6], [24.0, 54.0], [-25.3, 133.8]].map(([a, b]) => ll(a, b));

function buildGlobe(N) {
  const nM = MARKETS.length, MK = 20, CORE = 12, ARC = 28;
  const nArc = (nM - 1) * ARC, nMk = nM * MK, nS = N - nArc - nMk;
  const type = new Uint8Array(N), A = new Float32Array(N), B = new Float32Array(N);
  const bx = new Float32Array(N), by = new Float32Array(N), bz = new Float32Array(N);
  const E = MARKETS.map(M => norm(cross([0, -1, 0], M))), Nn = MARKETS.map((M, i) => cross(M, E[i]));
  const arcs = MARKETS.slice(1).map(Bv => { const Av = MARKETS[0]; const om = Math.acos(clamp(Av[0] * Bv[0] + Av[1] * Bv[1] + Av[2] * Bv[2], -1, 1)); return { A: Av, B: Bv, om, so: Math.sin(om), h: 0.06 + om * 0.12 }; });
  let j = 0; const golden = Math.PI * (3 - Math.sqrt(5));
  for (let i = 0; i < nS; i++, j++) { const y = 1 - ((i + 0.5) / nS) * 2, r = Math.sqrt(1 - y * y), a = i * golden; bx[j] = Math.cos(a) * r; by[j] = y; bz[j] = Math.sin(a) * r; }
  for (let m = 0; m < nM; m++) for (let i = 0; i < MK; i++, j++) {
    A[j] = m;
    if (i < CORE) { type[j] = 1; const u = rnd(-0.02, 0.02), v = rnd(-0.02, 0.02), M = MARKETS[m]; const P = norm([M[0] + E[m][0] * u + Nn[m][0] * v, M[1] + E[m][1] * u + Nn[m][1] * v, M[2] + E[m][2] * u + Nn[m][2] * v]); bx[j] = P[0]; by[j] = P[1]; bz[j] = P[2]; }
    else { type[j] = 2; B[j] = ((i - CORE) / (MK - CORE)) * TAU; }
  }
  for (let k = 0; k < arcs.length; k++) for (let i = 0; i < ARC; i++, j++) { type[j] = 3; A[j] = k; B[j] = i / ARC; }
  const sh = blank(N);
  for (let i = 0; i < N; i++) {
    const t = type[i];
    const col = t === 0 ? [0.45, 0.7, 0.9] : t === 3 ? [0.55, 0.88, 0.66] : [0.75, 0.95, 0.8];
    const b = rnd(0.82, 1.1);
    sh.col[i * 3] = Math.min(1, col[0] * b); sh.col[i * 3 + 1] = Math.min(1, col[1] * b); sh.col[i * 3 + 2] = Math.min(1, col[2] * b);
  }
  sh.dyn = (s, t) => {
    const th = t * 0.22, al = -0.38, ct = Math.cos(th), st = Math.sin(th), ca = Math.cos(al), sa = Math.sin(al), R = 0.86;
    for (let i = 0; i < N; i++) {
      const ty = type[i]; let x, y, z, a = 1;
      if (ty <= 1) { x = bx[i]; y = by[i]; z = bz[i]; }
      else if (ty === 2) {
        const m = A[i] | 0, M = MARKETS[m], pp = (t * 0.45 + m * 0.13) % 1, r = 0.03 + 0.09 * pp, c = Math.cos(B[i]), sn = Math.sin(B[i]);
        x = M[0] + r * (c * E[m][0] + sn * Nn[m][0]); y = M[1] + r * (c * E[m][1] + sn * Nn[m][1]); z = M[2] + r * (c * E[m][2] + sn * Nn[m][2]);
        const l = Math.hypot(x, y, z); x /= l; y /= l; z /= l; a = 1 - pp;
      } else {
        const P = arcs[A[i] | 0], sp = (B[i] + t * 0.07) % 1, s0 = Math.sin((1 - sp) * P.om) / P.so, s1 = Math.sin(sp * P.om) / P.so, lift = 1 + P.h * Math.sin(Math.PI * sp);
        x = (P.A[0] * s0 + P.B[0] * s1) * lift; y = (P.A[1] * s0 + P.B[1] * s1) * lift; z = (P.A[2] * s0 + P.B[2] * s1) * lift;
        a = Math.pow(Math.sin(Math.PI * sp), 0.6);
      }
      const x1 = x * ct + z * st, z1 = -x * st + z * ct, y2 = y * ca - z1 * sa, z2 = y * sa + z1 * ca;
      s.nx[i] = x1 * R; s.ny[i] = y2 * R;
      const depth = smooth(-0.35, 1, z2);
      s.na[i] = a * (ty === 0 ? 0.12 + 0.88 * depth : 0.08 + 0.92 * depth);
      s.ns[i] = ty === 1 ? 1.4 : ty === 0 ? 0.7 + 0.45 * depth : 1;
    }
  };
  return sh;
}

function blank(N) {
  return { nx: new Float32Array(N), ny: new Float32Array(N), na: new Float32Array(N).fill(1), ns: new Float32Array(N).fill(1), col: new Float32Array(N * 3), dyn: null };
}
const BLUE = [0.42, 0.7, 0.92], GREEN = [0.42, 0.84, 0.6];
function makeShape(name, N, hot) {
  if (name === 'globe') return buildGlobe(N);
  const parts = (SHAPES[name] || SHAPES.growth)();
  const sh = blank(N);
  let j = 0;
  parts.forEach((p, k) => {
    const n = k === parts.length - 1 ? N - j : Math.round(p.f * N);
    const pts = sample(p.draw, n);
    for (let i = 0; i < n; i++, j++) {
      const x = pts[i * 2], y = pts[i * 2 + 1];
      sh.nx[j] = x; sh.ny[j] = y; sh.na[j] = p.alpha ?? 1; sh.ns[j] = p.size ?? 1;
      const m = clamp((x + 1) / 2 - y * 0.15, 0, 1), b = rnd(0.82, 1.1);
      for (let q = 0; q < 3; q++) {
        let v = (BLUE[q] + (GREEN[q] - BLUE[q]) * m) * b;
        if (p.tone === 1) v = v + (1 - v) * 0.5;
        if (p.tone === 2) v *= 0.85;
        if (hot[j]) v = v + (1 - v) * 0.45;
        sh.col[j * 3 + q] = Math.min(1, v);
      }
    }
  });
  if (name === 'bird') {
    const bx = sh.nx.slice(), by = sh.ny.slice();
    sh.dyn = (s, t) => {
      const fl = Math.sin(t * 3.4) * 0.36, bob = Math.sin(t * 1.7 + 1) * 0.03;
      for (let i = 0; i < N; i++) { const ax = Math.max(Math.abs(bx[i]) - 0.06, 0); s.nx[i] = bx[i] * (1 - 0.06 * Math.abs(fl) * ax); s.ny[i] = by[i] - fl * Math.pow(ax, 1.25) + bob; }
    };
  }
  return sh;
}

/* ---------- renderer ---------- */
const VS = 'attribute vec2 p;attribute vec4 c;attribute float s;uniform vec2 res;uniform float dpr;varying vec4 vc;void main(){vec2 q=p/res*2.0-1.0;gl_Position=vec4(q.x,-q.y,0.0,1.0);gl_PointSize=s*dpr;vc=c;}';
const FS = 'precision mediump float;varying vec4 vc;void main(){vec2 d=gl_PointCoord-0.5;float r=length(d)*2.0;if(r>1.0)discard;float h=1.0-r;float a=(h*h*0.7+smoothstep(0.45,0.0,r)*0.6)*vc.a;gl_FragColor=vec4(vc.rgb*a,a*0.75);}';

class Field {
  constructor(canvas) {
    this.canvas = canvas;
    const small = Math.min(window.innerWidth, window.innerHeight) < 700;
    this.N = parseInt(canvas.dataset.count || (small ? 1100 : 1800), 10);
    const N = this.N;
    this.hot = new Uint8Array(N); this.delay = new Float32Array(N); this.swirl = new Float32Array(N);
    this.scat = new Float32Array(N); this.sang = new Float32Array(N); this.ph = new Float32Array(N); this.sz = new Float32Array(N);
    for (let j = 0; j < N; j++) {
      this.hot[j] = Math.random() < 0.05 ? 1 : 0; this.delay[j] = Math.random(); this.swirl[j] = rnd(-0.45, 0.45);
      this.scat[j] = rnd(0.04, 0.3); this.sang[j] = rnd(0, TAU); this.ph[j] = rnd(0, TAU);
      this.sz[j] = rnd(2.4, 3.8) * (this.hot[j] ? 1.4 : 1);
    }
    this.names = (canvas.dataset.shapes || 'growth').split(',').map(s => s.trim());
    this.shapes = this.names.map(n => makeShape(n, N, this.hot));
    this.pos = new Float32Array(N * 2); this.vel = new Float32Array(N * 2);
    this.col = new Float32Array(N * 4); this.size = new Float32Array(N);
    this.pointer = { x: -1e5, y: -1e5 };
    this.t0 = performance.now(); this.last = this.t0; this.running = false; this.first = true;
    this.initGL();
    this.resize();
    for (let j = 0; j < N; j++) { this.pos[j * 2] = rnd(0, this.W); this.pos[j * 2 + 1] = rnd(0, this.H); }
    this.bind();
    if (reduce) { this.frame(this.t0, true); }
  }
  initGL() {
    let gl = null;
    try { gl = this.canvas.getContext('webgl', { alpha: true, antialias: false, premultipliedAlpha: true }); } catch (e) { gl = null; }
    if (gl) {
      try {
        const mk = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error('shader'); return s; };
        const prog = gl.createProgram();
        gl.attachShader(prog, mk(gl.VERTEX_SHADER, VS)); gl.attachShader(prog, mk(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(prog);
        if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error('link');
        gl.useProgram(prog);
        this.uRes = gl.getUniformLocation(prog, 'res'); this.uDpr = gl.getUniformLocation(prog, 'dpr');
        const buf = (name, data, n) => { const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, data.byteLength, gl.DYNAMIC_DRAW); const loc = gl.getAttribLocation(prog, name); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, n, gl.FLOAT, false, 0, 0); return b; };
        this.bPos = buf('p', this.pos, 2); this.bCol = buf('c', this.col, 4); this.bSize = buf('s', this.size, 1);
        gl.enable(gl.BLEND); gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA); gl.clearColor(0, 0, 0, 0);
        this.gl = gl; return;
      } catch (e) { const fresh = this.canvas.cloneNode(false); this.canvas.replaceWith(fresh); this.canvas = fresh; }
    }
    this.ctx = this.canvas.getContext('2d');
  }
  resize() {
    const r = this.canvas.getBoundingClientRect();
    this.dpr = Math.min(window.devicePixelRatio || 1, 2);
    this.W = Math.max(1, r.width); this.H = Math.max(1, r.height);
    this.canvas.width = Math.round(this.W * this.dpr); this.canvas.height = Math.round(this.H * this.dpr);
    if (this.gl) this.gl.viewport(0, 0, this.canvas.width, this.canvas.height);
    this.half = Math.min(this.W, this.H) * 0.47; this.cx = this.W / 2; this.cy = this.H / 2;
    this.scale = this.W < 420 ? 0.8 : 1;
    if (reduce) this.frame(performance.now(), true);
  }
  bind() {
    if ('ResizeObserver' in window) new ResizeObserver(() => this.resize()).observe(this.canvas);
    else addEventListener('resize', () => this.resize());
    const host = this.canvas.closest('[data-field-host]') || this.canvas.parentElement;
    const setP = (x, y) => { const r = this.canvas.getBoundingClientRect(); this.pointer.x = x - r.left; this.pointer.y = y - r.top; };
    host.addEventListener('pointermove', e => setP(e.clientX, e.clientY), { passive: true });
    host.addEventListener('pointerleave', () => { this.pointer.x = -1e5; });
    host.addEventListener('touchmove', e => { const t = e.touches[0]; if (t) setP(t.clientX, t.clientY); }, { passive: true });
    host.addEventListener('touchend', () => { this.pointer.x = -1e5; }, { passive: true });
    if (reduce) return;
    const loop = now => { if (!this.running) return; this.frame(now); requestAnimationFrame(loop); };
    const start = () => { if (this.running || document.hidden || !this.visible) return; this.running = true; this.last = performance.now(); requestAnimationFrame(loop); };
    const stop = () => { this.running = false; };
    this.visible = true;
    if ('IntersectionObserver' in window) new IntersectionObserver(es => { this.visible = es[0].isIntersecting; this.visible ? start() : stop(); }, { rootMargin: '80px' }).observe(this.canvas);
    document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));
    start();
  }
  frame(now, still) {
    const N = this.N, dt = Math.min(Math.max(now - this.last, 1), 50); this.last = now;
    const f = dt / 16.667, t = reduce ? 0 : (now - this.t0) / 1000, el = (now - this.t0) / 1000;
    const n = this.shapes.length, HOLD = 3.8, MORPH = 1.7, cyc = HOLD + MORPH;
    let iA = 0, iB = 0, tt = 0;
    if (n > 1 && !reduce) { const k = Math.floor(el / cyc); iA = k % n; iB = (k + 1) % n; const lt = el - k * cyc; tt = lt < HOLD ? 0 : (lt - HOLD) / MORPH; }
    const A = this.shapes[iA], B = this.shapes[iB];
    if (A.dyn) A.dyn(A, t); if (B !== A && B.dyn) B.dyn(B, t);
    const K = 0.06, df = Math.pow(0.8, f), PR = this.W < 500 ? 70 : 100, PR2 = PR * PR;
    const px = this.pointer.x, py = this.pointer.y, usePtr = !reduce && px > -1e4;
    const intro = !reduce && el < 2.4;
    const { pos, vel, col, size } = this;
    for (let j = 0; j < N; j++) {
      const e = reduce ? 0 : ease(clamp((tt - this.delay[j] * 0.4) / 0.6, 0, 1));
      const ax = A.nx[j], ay = A.ny[j], bx = B.nx[j], by = B.ny[j];
      let x = ax + (bx - ax) * e, y = ay + (by - ay) * e;
      if (e > 0 && e < 1) { const s = Math.sin(Math.PI * e), dx = bx - ax, dy = by - ay; x += (-dy * this.swirl[j] + Math.cos(this.sang[j]) * this.scat[j]) * s; y += (dx * this.swirl[j] + Math.sin(this.sang[j]) * this.scat[j]) * s; }
      if (!reduce) { x += Math.sin(t * 0.9 + this.ph[j]) * 0.006; y += Math.cos(t * 0.75 + this.ph[j] * 1.3) * 0.006; }
      const tx = this.cx + x * this.half, ty = this.cy + y * this.half, j2 = j * 2;
      if (still || reduce) { pos[j2] = tx; pos[j2 + 1] = ty; }
      else {
        const k = intro ? K * smooth(0, 0.5, el - this.delay[j] * 1.3) : K;
        let vx = vel[j2] + (tx - pos[j2]) * k * f, vy = vel[j2 + 1] + (ty - pos[j2 + 1]) * k * f;
        if (usePtr) { const dx = pos[j2] - px, dy = pos[j2 + 1] - py, d2 = dx * dx + dy * dy; if (d2 < PR2 && d2 > 0.01) { const d = Math.sqrt(d2), fo = 1 - d / PR, push = fo * fo * 4.2 * f; vx += (dx / d) * push; vy += (dy / d) * push; } }
        vx *= df; vy *= df; pos[j2] += vx * f; pos[j2 + 1] += vy * f; vel[j2] = vx; vel[j2 + 1] = vy;
      }
      const j3 = j * 3, j4 = j * 4;
      col[j4] = A.col[j3] + (B.col[j3] - A.col[j3]) * e;
      col[j4 + 1] = A.col[j3 + 1] + (B.col[j3 + 1] - A.col[j3 + 1]) * e;
      col[j4 + 2] = A.col[j3 + 2] + (B.col[j3 + 2] - A.col[j3 + 2]) * e;
      col[j4 + 3] = A.na[j] + (B.na[j] - A.na[j]) * e;
      size[j] = this.sz[j] * (A.ns[j] + (B.ns[j] - A.ns[j]) * e) * this.scale;
    }
    this.render();
  }
  render() {
    const gl = this.gl, N = this.N;
    if (gl) {
      gl.clear(gl.COLOR_BUFFER_BIT);
      gl.uniform2f(this.uRes, this.W, this.H); gl.uniform1f(this.uDpr, this.dpr);
      gl.bindBuffer(gl.ARRAY_BUFFER, this.bPos); gl.bufferSubData(gl.ARRAY_BUFFER, 0, this.pos);
      gl.bindBuffer(gl.ARRAY_BUFFER, this.bCol); gl.bufferSubData(gl.ARRAY_BUFFER, 0, this.col);
      gl.bindBuffer(gl.ARRAY_BUFFER, this.bSize); gl.bufferSubData(gl.ARRAY_BUFFER, 0, this.size);
      gl.drawArrays(gl.POINTS, 0, N);
    } else if (this.ctx) {
      const c = this.ctx; c.setTransform(this.dpr, 0, 0, this.dpr, 0, 0); c.clearRect(0, 0, this.W, this.H); c.globalCompositeOperation = 'lighter';
      for (let j = 0; j < N; j++) {
        const a = this.col[j * 4 + 3]; if (a < 0.03) continue;
        c.globalAlpha = Math.min(1, a * 0.85);
        c.fillStyle = 'rgb(' + ((this.col[j * 4] * 255) | 0) + ',' + ((this.col[j * 4 + 1] * 255) | 0) + ',' + ((this.col[j * 4 + 2] * 255) | 0) + ')';
        const s = this.size[j] * 0.55; c.fillRect(this.pos[j * 2] - s / 2, this.pos[j * 2 + 1] - s / 2, s, s);
      }
      c.globalAlpha = 1;
    }
  }
}

const start = () => document.querySelectorAll('canvas[data-shapes]').forEach(c => { try { new Field(c); } catch (e) { /* page works without the animation */ } });
if ('requestIdleCallback' in window) requestIdleCallback(start, { timeout: 600 }); else setTimeout(start, 120);
