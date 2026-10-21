// The dot field: 2,700 shape dots + 300 background stars on a fixed canvas.
//
// Scroll progress p runs from 0 to scenes.length - 1. Between scene i and i+1
// every dot moves from its point in shape A to its point in shape B, with its
// own start delay (stagger) and a swirl around the box centre. Dots follow
// their targets on springs, so motion stays smooth and the pointer can push
// them aside. WebGL draws the dots; Canvas 2D is the fallback.

import { buildShape, hexRgb, rng, SHAPE_DOTS } from './shapes.js';

const STARS = 300;
const TOTAL = SHAPE_DOTS + STARS;
const STRIDE = 7; // x, y, size, r, g, b, a
const TAU = Math.PI * 2;

const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);

// Where the shape box sits for each layout, in CSS pixels.
function layoutBox(kind, W, H) {
  const phone = W <= 760;
  const hdr = phone ? 56 : 64;
  if (kind === 'wide') {
    return phone
      ? { cx: W / 2, cy: H * 0.55, s: Math.min(W * 0.98, H * 0.62), a: 0.45 }
      : { cx: W / 2, cy: hdr / 2 + H * 0.56, s: Math.min(W * 0.62, (H - hdr) * 0.9), a: 0.45 };
  }
  if (kind === 'footer') {
    return phone
      ? { cx: W / 2, cy: hdr + (H * 0.5 - hdr) / 2, s: Math.min(W * 0.86, 520), a: 1 }
      : { cx: W / 2, cy: hdr / 2 + H * 0.33, s: Math.min(W * 0.6, 760), a: 1 };
  }
  if (phone) {
    const top = hdr + 8;
    const bot = H * 0.46;
    return { cx: W / 2, cy: (top + bot) / 2, s: Math.min(W * 0.84, (bot - top) * 0.98), a: 1 };
  }
  return { cx: W * 0.74, cy: hdr / 2 + H * 0.5, s: Math.min(W * 0.44, (H - hdr) * 0.8), a: 1 };
}

// ------------------------------------------------------------- renderers

const VERT = `
attribute vec2 a_pos;
attribute float a_size;
attribute vec4 a_col;
uniform vec2 u_res;
uniform float u_dpr;
varying vec4 v_col;
void main() {
  vec2 c = a_pos / u_res * 2.0 - 1.0;
  gl_Position = vec4(c.x, -c.y, 0.0, 1.0);
  gl_PointSize = a_size * u_dpr * 3.0;
  v_col = a_col;
}`;

const FRAG = `
precision mediump float;
varying vec4 v_col;
void main() {
  vec2 q = gl_PointCoord * 2.0 - 1.0;
  float d = dot(q, q);
  if (d > 1.0) discard;
  float core = smoothstep(0.13, 0.03, d);
  float h = 1.0 - d;
  float a = (core + h * h * h * 0.3) * v_col.a;
  gl_FragColor = vec4(v_col.rgb * a, a);
}`;

function makeGL(canvas) {
  let gl = null;
  try {
    gl = canvas.getContext('webgl', {
      alpha: true,
      premultipliedAlpha: true,
      antialias: false,
      depth: false,
      stencil: false,
    });
  } catch {
    gl = null;
  }
  if (!gl) return null;

  let prog;
  let buf;
  let loc;
  const init = () => {
    const sh = (type, src) => {
      const s = gl.createShader(type);
      gl.shaderSource(s, src);
      gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s) || 'shader');
      return s;
    };
    prog = gl.createProgram();
    gl.attachShader(prog, sh(gl.VERTEX_SHADER, VERT));
    gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, FRAG));
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) throw new Error('link');
    gl.useProgram(prog);
    buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, TOTAL * STRIDE * 4, gl.DYNAMIC_DRAW);
    loc = {
      pos: gl.getAttribLocation(prog, 'a_pos'),
      size: gl.getAttribLocation(prog, 'a_size'),
      col: gl.getAttribLocation(prog, 'a_col'),
      res: gl.getUniformLocation(prog, 'u_res'),
      dpr: gl.getUniformLocation(prog, 'u_dpr'),
    };
    const B = STRIDE * 4;
    gl.enableVertexAttribArray(loc.pos);
    gl.vertexAttribPointer(loc.pos, 2, gl.FLOAT, false, B, 0);
    gl.enableVertexAttribArray(loc.size);
    gl.vertexAttribPointer(loc.size, 1, gl.FLOAT, false, B, 8);
    gl.enableVertexAttribArray(loc.col);
    gl.vertexAttribPointer(loc.col, 4, gl.FLOAT, false, B, 12);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.ONE, gl.ONE);
    gl.disable(gl.DEPTH_TEST);
  };
  try {
    init();
  } catch {
    return null;
  }

  let lost = false;
  canvas.addEventListener('webglcontextlost', (e) => {
    e.preventDefault();
    lost = true;
  });
  canvas.addEventListener('webglcontextrestored', () => {
    try {
      init();
      lost = false;
    } catch {
      lost = true;
    }
  });

  return {
    kind: 'webgl',
    maxDpr: 2,
    draw(data, W, H, dpr) {
      if (lost) return;
      gl.viewport(0, 0, canvas.width, canvas.height);
      gl.clearColor(0, 0, 0, 0);
      gl.clear(gl.COLOR_BUFFER_BIT);
      gl.uniform2f(loc.res, W, H);
      gl.uniform1f(loc.dpr, dpr);
      gl.bufferSubData(gl.ARRAY_BUFFER, 0, data);
      gl.drawArrays(gl.POINTS, 0, TOTAL);
    },
  };
}

function make2D(canvas) {
  let ctx = null;
  try {
    ctx = canvas.getContext('2d');
  } catch {
    ctx = null;
  }
  if (!ctx) return null;

  // One small glow sprite per colour (4 bits per channel), drawn with drawImage.
  const sprites = new Map();
  const sprite = (r, g, b) => {
    const key = (r << 8) | (g << 4) | b;
    let c = sprites.get(key);
    if (!c) {
      if (sprites.size > 600) sprites.clear();
      c = document.createElement('canvas');
      c.width = c.height = 24;
      const x = c.getContext('2d');
      const col = `${r * 17},${g * 17},${b * 17}`;
      const grad = x.createRadialGradient(12, 12, 0, 12, 12, 12);
      grad.addColorStop(0, `rgba(${col},1)`);
      grad.addColorStop(0.26, `rgba(${col},0.95)`);
      grad.addColorStop(0.36, `rgba(${col},0.22)`);
      grad.addColorStop(1, `rgba(${col},0)`);
      x.fillStyle = grad;
      x.fillRect(0, 0, 24, 24);
      sprites.set(key, c);
    }
    return c;
  };

  return {
    kind: '2d',
    maxDpr: 1,
    draw(data, W, H, dpr) {
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.globalCompositeOperation = 'source-over';
      ctx.globalAlpha = 1;
      ctx.clearRect(0, 0, W, H);
      ctx.globalCompositeOperation = 'lighter';
      for (let i = 0, o = 0; i < TOTAL; i++, o += STRIDE) {
        const a = data[o + 6];
        if (a < 0.02) continue;
        const sz = data[o + 2] * 3;
        ctx.globalAlpha = a > 1 ? 1 : a;
        ctx.drawImage(
          sprite((data[o + 3] * 15 + 0.5) | 0, (data[o + 4] * 15 + 0.5) | 0, (data[o + 5] * 15 + 0.5) | 0),
          data[o] - sz / 2,
          data[o + 1] - sz / 2,
          sz,
          sz,
        );
      }
      ctx.globalAlpha = 1;
    },
  };
}

// ------------------------------------------------------------------ field

/**
 * @param {HTMLCanvasElement} canvas
 * @param {{scenes: {shape: string, tint: string, layout: string}[],
 *          getProgress: () => number, getDawn?: () => number, reduced?: boolean}} opts
 */
export function createField(canvas, opts) {
  const renderer = makeGL(canvas) || make2D(canvas);
  if (!renderer) return null;

  const scenes = opts.scenes.map((s, i) => ({
    ...s,
    rgb: hexRgb(s.tint || '#EEF0F7'),
    seed: 101 + i,
    shape: null,
    perm: null,
    name: s.shape,
  }));
  const n = scenes.length;
  let reduced = !!opts.reduced;

  const data = new Float32Array(TOTAL * STRIDE);
  const r = rng(7);

  // per-dot state
  const px = new Float32Array(SHAPE_DOTS);
  const py = new Float32Array(SHAPE_DOTS);
  const vx = new Float32Array(SHAPE_DOTS);
  const vy = new Float32Array(SHAPE_DOTS);
  const stag = new Float32Array(SHAPE_DOTS);
  const swirl = new Float32Array(SHAPE_DOTS);
  const base = new Float32Array(SHAPE_DOTS);
  const wf = new Float32Array(SHAPE_DOTS);
  const wp = new Float32Array(SHAPE_DOTS);
  const release = new Float32Array(SHAPE_DOTS);
  for (let i = 0; i < SHAPE_DOTS; i++) {
    stag[i] = r();
    swirl[i] = (r() < 0.5 ? -1 : 1) * (0.5 + r() * 0.7);
    base[i] = 0.7 + r() * 0.6;
    wf[i] = 0.6 + r() * 1.2;
    wp[i] = r() * TAU;
    release[i] = 0.25 + r() * 1.5;
  }
  // stars
  const sx = new Float32Array(STARS);
  const sy = new Float32Array(STARS);
  const sd = new Float32Array(STARS);
  const ss = new Float32Array(STARS);
  const sa = new Float32Array(STARS);
  const tf = new Float32Array(STARS);
  const tp = new Float32Array(STARS);
  for (let i = 0; i < STARS; i++) {
    sx[i] = r();
    sy[i] = r();
    sd[i] = 0.2 + r() * 0.8;
    ss[i] = 0.6 + r() * r() * 1.4;
    sa[i] = 0.25 + r() * 0.55;
    tf[i] = 0.5 + r() * 2;
    tp[i] = r() * TAU;
  }

  let W = 0;
  let H = 0;
  let dpr = 1;
  const resize = () => {
    W = window.innerWidth;
    H = window.innerHeight;
    dpr = Math.min(renderer.maxDpr, window.devicePixelRatio || 1);
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    canvas.style.width = `${W}px`;
    canvas.style.height = `${H}px`;
  };
  resize();

  // Dots start scattered like stars and gather into the first shape.
  for (let i = 0; i < SHAPE_DOTS; i++) {
    px[i] = r() * W;
    py[i] = r() * H;
  }

  const permFor = (seed) => {
    const p = new Uint16Array(SHAPE_DOTS);
    for (let i = 0; i < SHAPE_DOTS; i++) p[i] = i;
    const q = rng(seed);
    for (let i = SHAPE_DOTS - 1; i > 0; i--) {
      const j = (q() * (i + 1)) | 0;
      const t = p[i];
      p[i] = p[j];
      p[j] = t;
    }
    return p;
  };
  const ensure = (i) => {
    const sc = scenes[i];
    if (!sc.shape) {
      sc.shape = buildShape(sc.name);
      sc.perm = permFor(sc.seed);
    }
    return sc;
  };

  // Build the rest of the shapes a few at a time while the browser is idle.
  let pending = scenes.map((_, i) => i);
  const idle = window.requestIdleCallback || ((fn) => setTimeout(() => fn({ timeRemaining: () => 8 }), 60));
  const buildSome = (deadline) => {
    while (pending.length && deadline.timeRemaining() > 4) ensure(pending.shift());
    if (pending.length) idle(buildSome);
  };

  // pointer
  const ptr = { x: 0, y: 0, on: false, until: 0 };
  const onMove = (e) => {
    ptr.x = e.clientX;
    ptr.y = e.clientY;
    ptr.on = true;
  };
  const onTouch = (e) => {
    const t = e.touches[0];
    if (!t) return;
    ptr.x = t.clientX;
    ptr.y = t.clientY;
    ptr.on = true;
    ptr.until = performance.now() + 400;
  };
  window.addEventListener('pointermove', onMove, { passive: true });
  window.addEventListener('touchstart', onTouch, { passive: true });
  window.addEventListener('touchmove', onTouch, { passive: true });
  window.addEventListener('touchend', () => (ptr.until = performance.now() + 250), { passive: true });
  document.documentElement.addEventListener('mouseleave', () => (ptr.on = false));

  let raf = 0;
  let last = 0;
  let time = 0;
  let running = false;
  let gathered = reduced;

  const frame = (now) => {
    raf = requestAnimationFrame(frame);
    const dt = last ? Math.min(0.05, (now - last) / 1000) : 1 / 60;
    last = now;
    time += dt;
    if (ptr.until && now > ptr.until) {
      ptr.on = false;
      ptr.until = 0;
    }
    step(dt);
    renderer.draw(data, W, H, dpr);
  };

  const step = (dt) => {
    let p = clamp(opts.getProgress(), 0, n - 1);
    let i = Math.min(Math.floor(p), Math.max(0, n - 2));
    let t = n > 1 ? p - i : 0;
    if (reduced) {
      if (t >= 0.5) i = Math.min(i + 1, n - 1);
      t = 0;
    }
    const A = ensure(i);
    const B = ensure(Math.min(i + 1, n - 1));
    const SA = A.shape;
    const SB = B.shape;
    const st = reduced ? 0 : time;
    SA.update?.(st, reduced);
    if (t > 0 && SB !== SA) SB.update?.(st, reduced);

    const bA = layoutBox(A.layout, W, H);
    const bB = layoutBox(B.layout, W, H);
    const hA = bA.s / 2;
    const hB = bB.s / 2;
    const ex = t > 0 && SA.exit ? SA.exit(t) : null;
    const exX = ex ? ex.dx * hA : 0;
    const exY = ex ? ex.dy * hA : 0;
    const aA = bA.a * SA.alpha;
    const aB = bB.a * SB.alpha;
    const pxA = clamp((bA.s / 400) * 2.7, 1.6, 3.4);
    const pxB = clamp((bB.s / 400) * 2.7, 1.6, 3.4);
    const PA = A.perm;
    const PB = B.perm;
    const tA = A.rgb;
    const tB = B.rgb;
    const wob = reduced ? 0 : 0.7;
    const K = 70;
    const D = 13;
    const R = 100;
    const R2 = R * R;
    const usePtr = ptr.on && !reduced;
    let allIn = true;

    for (let d = 0, o = 0; d < SHAPE_DOTS; d++, o += STRIDE) {
      const ia = PA[d];
      const ib = PB[d];
      const e = t <= 0 ? 0 : ease(clamp((t - stag[d] * 0.4) / 0.6, 0, 1));
      const ax = bA.cx + SA.x[ia] * hA + exX;
      const ay = bA.cy + SA.y[ia] * hA + exY;
      const bx = bB.cx + SB.x[ib] * hB;
      const by = bB.cy + SB.y[ib] * hB;
      let tx = ax + (bx - ax) * e;
      let ty = ay + (by - ay) * e;
      if (e > 0 && e < 1 && !reduced) {
        const w = Math.sin(Math.PI * e);
        const cx = bA.cx + (bB.cx - bA.cx) * e;
        const cy = bA.cy + (bB.cy - bA.cy) * e;
        const ang = w * swirl[d];
        const k = 1 + 0.16 * w;
        const ca = Math.cos(ang) * k;
        const sa2 = Math.sin(ang) * k;
        const dx = tx - cx;
        const dy = ty - cy;
        tx = cx + dx * ca - dy * sa2;
        ty = cy + dx * sa2 + dy * ca;
      }
      if (wob) {
        tx += wob * Math.sin(time * wf[d] + wp[d]);
        ty += wob * Math.cos(time * wf[d] * 0.8 + wp[d]);
      }

      let g = 1;
      if (reduced) {
        px[d] = tx;
        py[d] = ty;
        vx[d] = vy[d] = 0;
      } else {
        if (!gathered) {
          g = clamp((time - release[d]) / 0.9, 0, 1);
          if (g < 1) allIn = false;
        }
        if (g > 0) {
          let fx = (tx - px[d]) * K - vx[d] * D;
          let fy = (ty - py[d]) * K - vy[d] * D;
          if (usePtr) {
            const dx = px[d] - ptr.x;
            const dy = py[d] - ptr.y;
            const d2 = dx * dx + dy * dy;
            if (d2 < R2 && d2 > 0.01) {
              const dist = Math.sqrt(d2);
              const f = 1 - dist / R;
              const push = f * f * 5200;
              fx += (dx / dist) * push;
              fy += (dy / dist) * push;
            }
          }
          vx[d] += fx * dt;
          vy[d] += fy * dt;
          px[d] += vx[d] * dt;
          py[d] += vy[d] * dt;
        }
      }

      // colour, brightness, size
      let cr;
      let cg;
      let cb;
      if (SA.own[ia]) {
        cr = SA.rgb[ia * 3];
        cg = SA.rgb[ia * 3 + 1];
        cb = SA.rgb[ia * 3 + 2];
      } else {
        cr = tA[0];
        cg = tA[1];
        cb = tA[2];
      }
      if (e > 0) {
        let r2;
        let g2;
        let b2;
        if (SB.own[ib]) {
          r2 = SB.rgb[ib * 3];
          g2 = SB.rgb[ib * 3 + 1];
          b2 = SB.rgb[ib * 3 + 2];
        } else {
          r2 = tB[0];
          g2 = tB[1];
          b2 = tB[2];
        }
        cr += (r2 - cr) * e;
        cg += (g2 - cg) * e;
        cb += (b2 - cb) * e;
      }
      const br = SA.b[ia] + (SB.b[ib] - SA.b[ia]) * e;
      const hot = br > 1 ? Math.min(1, (br - 1) * 0.7) : 0;
      cr += (1 - cr) * hot;
      cg += (1 - cg) * hot;
      cb += (1 - cb) * hot;
      const lay = aA + (aB - aA) * e;
      const gatherA = g < 1 ? 0.3 + 0.7 * g : 1;
      const sz = (SA.s[ia] + (SB.s[ib] - SA.s[ia]) * e) * (pxA + (pxB - pxA) * e) * base[d] * (1 + hot * 0.25);

      data[o] = px[d];
      data[o + 1] = py[d];
      data[o + 2] = g < 1 ? sz * (0.6 + 0.4 * g) : sz;
      data[o + 3] = cr;
      data[o + 4] = cg;
      data[o + 5] = cb;
      data[o + 6] = clamp(br * 0.85, 0, 1.25) * lay * gatherA;
    }
    if (!gathered && allIn) gathered = true;

    // background stars with a little parallax
    const dawn = opts.getDawn ? opts.getDawn() : 0;
    const scrollY = window.scrollY || 0;
    const span = H + 40;
    for (let s = 0, o = SHAPE_DOTS * STRIDE; s < STARS; s++, o += STRIDE) {
      let y = (sy[s] * span - scrollY * sd[s] * 0.12) % span;
      if (y < 0) y += span;
      data[o] = sx[s] * W;
      data[o + 1] = y - 20;
      data[o + 2] = ss[s];
      data[o + 3] = 0.86;
      data[o + 4] = 0.9;
      data[o + 5] = 1;
      const tw = reduced ? 1 : 0.65 + 0.35 * Math.sin(time * tf[s] + tp[s]);
      data[o + 6] = sa[s] * tw * (1 - 0.6 * dawn);
    }
  };

  const api = {
    kind: renderer.kind,
    resize() {
      resize();
    },
    setReduced(v) {
      reduced = !!v;
      if (reduced) gathered = true;
    },
    pause() {
      running = false;
      cancelAnimationFrame(raf);
    },
    resume() {
      if (running) return;
      running = true;
      last = 0;
      raf = requestAnimationFrame(frame);
    },
  };

  ensure(0);
  if (n > 1) ensure(1);
  idle(buildSome);
  api.resume();
  return api;
}
