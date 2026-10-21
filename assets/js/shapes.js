// Shape definitions for the dot field.
//
// Every shape is 2,700 points in box units: x and y run from -1 to 1 across a
// square box that the engine places on screen. Static shapes are drawn on an
// offscreen 400x400 canvas as parts (each with a point count) and sampled from
// the lit pixels. Dynamic shapes also get an update(time, still) function that
// rewrites their points every frame.
//
// Shape fields:
//   x, y   positions in box units
//   b      brightness (1 = normal, >1 glows whiter)
//   s      size multiplier
//   rgb    own colour per point (0..1), used where own[i] is 1; else the scene tint
//   alpha  overall alpha for the shape
//   update optional (time, still) => void
//   exit   optional (t) => {dx, dy}, offset applied while leaving this shape

export const SHAPE_DOTS = 2700;

const C = 400;
const H = C / 2;
const TAU = Math.PI * 2;

export function hexRgb(hex) {
  const h = hex.replace('#', '').trim();
  const v = h.length === 3 ? h.split('').map((c) => c + c).join('') : h;
  const n = parseInt(v, 16);
  return [((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255];
}

export function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function blank() {
  const n = SHAPE_DOTS;
  return {
    x: new Float32Array(n),
    y: new Float32Array(n),
    b: new Float32Array(n).fill(1),
    s: new Float32Array(n).fill(1),
    rgb: new Float32Array(n * 3),
    own: new Uint8Array(n),
    alpha: 1,
    ranges: {},
    update: null,
    exit: null,
  };
}

function setOwn(sh, i, rgb) {
  sh.own[i] = 1;
  sh.rgb[i * 3] = rgb[0];
  sh.rgb[i * 3 + 1] = rgb[1];
  sh.rgb[i * 3 + 2] = rgb[2];
}

// ---------------------------------------------------------------- sampling

let surf = null;
let hits = null;

function surface() {
  if (!surf) {
    const cv =
      typeof OffscreenCanvas !== 'undefined'
        ? new OffscreenCanvas(C, C)
        : Object.assign(document.createElement('canvas'), { width: C, height: C });
    surf = cv.getContext('2d', { willReadFrequently: true });
    hits = new Int32Array(C * C);
  }
  return surf;
}

// parts: [{ n, draw(g), b?, s?, rgb?, id? }]
function fromParts(parts, seed) {
  const sh = blank();
  const r = rng(seed);
  const g = surface();
  let k = 0;
  for (const part of parts) {
    g.setTransform(1, 0, 0, 1, 0, 0);
    g.globalCompositeOperation = 'source-over';
    g.clearRect(0, 0, C, C);
    g.fillStyle = g.strokeStyle = '#fff';
    g.lineCap = 'round';
    g.lineJoin = 'round';
    g.lineWidth = 11;
    g.save();
    part.draw(g, r);
    g.restore();
    const data = g.getImageData(0, 0, C, C).data;
    let m = 0;
    for (let p = 0, i = 3; p < C * C; p++, i += 4) if (data[i] > 127) hits[m++] = p;
    const start = k;
    for (let j = 0; j < part.n && k < SHAPE_DOTS; j++, k++) {
      const p = m ? hits[(r() * m) | 0] : H * C + H;
      sh.x[k] = ((p % C) + r() - H) / H;
      sh.y[k] = (((p / C) | 0) + r() - H) / H;
      sh.b[k] = (part.b ?? 1) * (0.82 + 0.36 * r());
      sh.s[k] = part.s ?? 1;
      if (part.rgb) setOwn(sh, k, part.rgb);
    }
    if (part.id) sh.ranges[part.id] = [start, k];
  }
  // Counts should add up to SHAPE_DOTS; if not, repeat earlier points.
  for (; k < SHAPE_DOTS; k++) {
    const j = (r() * k) | 0;
    sh.x[k] = sh.x[j];
    sh.y[k] = sh.y[j];
    sh.b[k] = sh.b[j];
    sh.s[k] = sh.s[j];
    if (sh.own[j]) setOwn(sh, k, sh.rgb.subarray(j * 3, j * 3 + 3));
  }
  return sh;
}

// ------------------------------------------------------------ draw helpers

function rrect(g, x, y, w, h, r) {
  g.moveTo(x + r, y);
  g.arcTo(x + w, y, x + w, y + h, r);
  g.arcTo(x + w, y + h, x, y + h, r);
  g.arcTo(x, y + h, x, y, r);
  g.arcTo(x, y, x + w, y, r);
  g.closePath();
}

function poly(g, pts, close = false) {
  g.moveTo(pts[0], pts[1]);
  for (let i = 2; i < pts.length; i += 2) g.lineTo(pts[i], pts[i + 1]);
  if (close) g.closePath();
}

const stroke = (lw, path) => (g, r) => {
  g.lineWidth = lw;
  g.beginPath();
  path(g, r);
  g.stroke();
};

const fill = (path) => (g, r) => {
  g.beginPath();
  path(g, r);
  g.fill();
};

const circle = (g, x, y, rad) => {
  g.moveTo(x + rad, y);
  g.arc(x, y, rad, 0, TAU);
};

// Egg outline, wider at the bottom. t = 0 is the right side, t = PI/2 the bottom.
function eggPt(cx, cy, rx, ry, t) {
  return [cx + rx * Math.cos(t) * (1 + 0.1 * Math.sin(t)), cy + ry * Math.sin(t)];
}

function eggPath(g, cx, cy, rx, ry, a0 = 0, a1 = TAU, move = true) {
  const steps = 96;
  for (let i = 0; i <= steps; i++) {
    const [x, y] = eggPt(cx, cy, rx, ry, a0 + ((a1 - a0) * i) / steps);
    if (i === 0 && move) g.moveTo(x, y);
    else g.lineTo(x, y);
  }
}

// Store the sampled points as the base pose for dynamic shapes.
function withBase(sh) {
  sh.bx = Float32Array.from(sh.x);
  sh.by = Float32Array.from(sh.y);
  sh.bb = Float32Array.from(sh.b);
  return sh;
}

// ------------------------------------------------------------------ shapes

// 1. Nest with an egg
function nest() {
  const straw = hexRgb('#EBC98A');
  const cream = hexRgb('#FFF1DA');
  const rimY = 212;
  const rimRx = 130;
  const rimRy = 26;
  const egg = [200, 174, 56, 74];

  const aboveRim = (g) => {
    g.beginPath();
    g.moveTo(0, 0);
    g.lineTo(C, 0);
    g.lineTo(C, rimY);
    for (let i = 0; i <= 48; i++) {
      const t = (i / 48) * Math.PI;
      g.lineTo(200 + rimRx * Math.cos(t), rimY + rimRy * Math.sin(t));
    }
    g.lineTo(0, rimY);
    g.closePath();
    g.clip();
  };
  const bowl = (g) => {
    g.beginPath();
    g.ellipse(200, rimY, rimRx + 6, 98, 0, 0, Math.PI);
    g.ellipse(200, rimY, rimRx + 6, rimRy + 6, 0, Math.PI, TAU);
    g.clip();
  };

  const sh = fromParts(
    [
      {
        n: 1350,
        b: 0.8,
        rgb: straw,
        draw: (g, r) => {
          bowl(g);
          for (let k = 0; k < 40; k++) {
            g.lineWidth = 4 + r() * 3.5;
            g.beginPath();
            g.ellipse(
              200 + (r() - 0.5) * 24,
              rimY - 2 + r() * 12,
              rimRx * (0.5 + 0.52 * r()),
              16 + r() * 80,
              (r() - 0.5) * 0.3,
              r() * 0.5,
              Math.PI - r() * 0.5,
            );
            g.stroke();
          }
          for (let k = 0; k < 16; k++) {
            const x = 110 + r() * 180;
            const y = rimY + 14 + r() * 60;
            const a = (r() - 0.5) * 1.4;
            const l = 26 + r() * 30;
            g.lineWidth = 4;
            g.beginPath();
            g.moveTo(x - Math.cos(a) * l, y - Math.sin(a) * l);
            g.lineTo(x + Math.cos(a) * l, y + Math.sin(a) * l);
            g.stroke();
          }
        },
      },
      {
        n: 520,
        b: 1.05,
        rgb: straw,
        draw: (g) => {
          g.lineWidth = 12;
          g.beginPath();
          g.ellipse(200, rimY, rimRx, rimRy, 0, 0, Math.PI);
          g.stroke();
          g.lineWidth = 8;
          g.beginPath();
          g.ellipse(200, rimY, rimRx, rimRy, 0, Math.PI, TAU);
          g.stroke();
          // the egg hides the back of the rim
          g.globalCompositeOperation = 'destination-out';
          g.beginPath();
          eggPath(g, ...egg);
          g.fill();
        },
      },
      {
        n: 180,
        b: 0.7,
        rgb: straw,
        draw: (g, r) => {
          g.lineWidth = 4;
          for (let k = 0; k < 14; k++) {
            const t = r() * Math.PI;
            const x = 200 + (rimRx + 2) * Math.cos(t);
            const y = rimY + rimRy * Math.sin(t) + r() * 30;
            const a = Math.PI + t + (r() - 0.5) * 1.6;
            const l = 16 + r() * 22;
            g.beginPath();
            g.moveTo(x, y);
            g.lineTo(x - Math.cos(a) * l, y - Math.sin(a) * l * 0.6);
            g.stroke();
          }
        },
      },
      {
        n: 450,
        b: 1.35,
        rgb: cream,
        id: 'egg',
        draw: (g) => {
          aboveRim(g);
          g.lineWidth = 11;
          g.beginPath();
          eggPath(g, ...egg);
          g.stroke();
        },
      },
      {
        n: 200,
        b: 0.5,
        rgb: cream,
        id: 'eggFill',
        draw: (g) => {
          aboveRim(g);
          g.beginPath();
          eggPath(g, ...egg);
          g.fill();
        },
      },
    ],
    1,
  );
  withBase(sh);
  const pivotY = (egg[1] + egg[3] - H) / H;
  const eggs = [sh.ranges.egg, sh.ranges.eggFill];
  sh.update = (t, still) => {
    const k = still ? 1 : 1 + 0.012 * Math.sin(t * 1.25);
    for (let i = 0; i < SHAPE_DOTS; i++) {
      sh.x[i] = sh.bx[i] * k;
      sh.y[i] = (sh.by[i] - 0.05) * k + 0.05;
    }
    if (still) return;
    const a = 0.035 * Math.sin(t * 0.9);
    const ca = Math.cos(a);
    const sa = Math.sin(a);
    for (const [s0, s1] of eggs) {
      for (let i = s0; i < s1; i++) {
        const dx = sh.x[i];
        const dy = sh.y[i] - pivotY;
        sh.x[i] = dx * ca - dy * sa;
        sh.y[i] = pivotY + dx * sa + dy * ca;
      }
    }
  };
  return sh;
}

// 2. Shopping bag
function bag() {
  const body = (g) => poly(g, [104, 142, 296, 142, 314, 322, 86, 322], true);
  return fromParts(
    [
      { n: 1250, draw: stroke(12, body) },
      {
        n: 500,
        b: 1.15,
        draw: stroke(12, (g) => {
          g.moveTo(152, 148);
          g.lineTo(152, 116);
          g.arc(200, 116, 48, Math.PI, 0);
          g.lineTo(248, 148);
        }),
      },
      { n: 220, b: 0.75, draw: stroke(6, (g) => poly(g, [112, 168, 288, 168])) },
      { n: 330, b: 1.35, draw: stroke(9, (g) => circle(g, 200, 246, 30)) },
      { n: 400, b: 0.3, draw: fill(body) },
    ],
    2,
  );
}

// 3. Three stacked cartons on a pallet
function cartons() {
  const boxes = [
    [72, 180, 122, 112],
    [206, 180, 122, 112],
    [139, 62, 122, 112],
  ];
  return fromParts(
    [
      {
        n: 1700,
        draw: stroke(11, (g) => {
          for (const [x, y, w, h] of boxes) rrect(g, x, y, w, h, 6);
        }),
      },
      {
        n: 300,
        b: 0.85,
        draw: stroke(7, (g) => {
          for (const [x, y, w] of boxes) poly(g, [x + 8, y + 24, x + w - 8, y + 24]);
        }),
      },
      {
        n: 400,
        b: 0.8,
        draw: (g) => {
          g.beginPath();
          rrect(g, 56, 302, 288, 14, 3);
          rrect(g, 56, 340, 288, 12, 3);
          for (const x of [68, 184, 300]) g.rect(x, 316, 32, 24);
          g.fill();
        },
      },
      {
        n: 300,
        b: 1.55,
        draw: stroke(12, (g) => {
          for (const [x, y, w, h] of boxes) poly(g, [x + w / 2, y + 2, x + w / 2, y + h * 0.48]);
        }),
      },
    ],
    3,
  );
}

// 4. Rising bars with a trend arrow
function bars() {
  const xs = [78, 146, 214, 282];
  const hs = [74, 118, 162, 214];
  const base = 322;
  const rects = (g) => xs.forEach((x, i) => rrect(g, x, base - hs[i], 46, hs[i], 5));
  // arrow head along the last segment
  const tip = [304, 113];
  const d = [104, -118];
  const dl = Math.hypot(...d);
  const u = [d[0] / dl, d[1] / dl];
  const back = [tip[0] - u[0] * 42, tip[1] - u[1] * 42];
  const p = [-u[1], u[0]];
  return fromParts(
    [
      { n: 250, b: 0.7, draw: stroke(8, (g) => poly(g, [56, base + 8, 348, base + 8])) },
      { n: 1150, draw: stroke(10, rects) },
      { n: 450, b: 0.32, draw: fill(rects) },
      { n: 620, b: 1.4, draw: stroke(11, (g) => poly(g, [70, 262, 140, 214, 196, 236, back[0] + u[0] * 10, back[1] + u[1] * 10])) },
      {
        n: 230,
        b: 1.55,
        draw: fill((g) =>
          poly(g, [tip[0], tip[1], back[0] + p[0] * 22, back[1] + p[1] * 22, back[0] - p[0] * 22, back[1] - p[1] * 22], true),
        ),
      },
    ],
    4,
  );
}

// 5. Chat bubble with a double tick
function chat() {
  const bubble = (g) => {
    g.ellipse(200, 178, 136, 104, 0, 2.62, 1.92 + TAU);
    g.lineTo(80, 318);
    g.closePath();
  };
  return fromParts(
    [
      { n: 1400, draw: stroke(12, bubble) },
      { n: 400, b: 0.28, draw: fill(bubble) },
      { n: 450, b: 1.5, draw: stroke(13, (g) => poly(g, [128, 182, 164, 218, 236, 146])) },
      { n: 450, b: 1.5, draw: stroke(13, (g) => poly(g, [180, 202, 194, 216, 266, 144])) },
    ],
    5,
  );
}

// 6. Envelope
function envelope() {
  const body = (g) => rrect(g, 62, 108, 276, 184, 14);
  return fromParts(
    [
      { n: 1250, draw: stroke(12, body) },
      { n: 650, b: 1.2, draw: stroke(11, (g) => poly(g, [70, 118, 200, 212, 330, 118])) },
      {
        n: 350,
        b: 0.75,
        draw: stroke(8, (g) => {
          poly(g, [72, 282, 164, 202]);
          poly(g, [328, 282, 236, 202]);
        }),
      },
      { n: 150, b: 1.5, draw: fill((g) => circle(g, 200, 212, 14)) },
      { n: 300, b: 0.28, draw: fill(body) },
    ],
    6,
  );
}

// 7. Delivery van with spinning wheels and speed lines
function van() {
  const ox = 18;
  const oy = -10;
  const W1 = [140 + ox, 268 + oy];
  const W2 = [300 + ox, 268 + oy];
  const arch = 36;
  const wheel = ([cx, cy]) => (g) => {
    circle(g, cx, cy, 25);
  };
  const spokes = ([cx, cy]) => (g) => {
    for (let k = 0; k < 4; k++) {
      const a = (k / 4) * TAU + 0.4;
      g.moveTo(cx + Math.cos(a) * 8, cy + Math.sin(a) * 8);
      g.lineTo(cx + Math.cos(a) * 21, cy + Math.sin(a) * 21);
    }
  };
  const sh = fromParts(
    [
      {
        n: 1300,
        draw: stroke(11, (g) => {
          const y0 = 120 + oy;
          const yb = 262 + oy;
          g.moveTo(95 + ox, y0);
          g.lineTo(255 + ox, y0);
          g.lineTo(255 + ox, 150 + oy);
          g.lineTo(305 + ox, 150 + oy);
          g.lineTo(343 + ox, 208 + oy);
          g.lineTo(343 + ox, yb);
          g.arc(W2[0], W2[1], arch, -0.17, Math.PI + 0.17, true);
          g.lineTo(W1[0] + arch, yb);
          g.arc(W1[0], W1[1], arch, -0.17, Math.PI + 0.17, true);
          g.lineTo(95 + ox, yb);
          g.closePath();
        }),
      },
      {
        n: 300,
        b: 0.95,
        draw: stroke(8, (g) => poly(g, [268 + ox, 162 + oy, 300 + ox, 162 + oy, 326 + ox, 204 + oy, 268 + ox, 204 + oy], true)),
      },
      { n: 150, b: 0.6, draw: stroke(6, (g) => poly(g, [108 + ox, 206 + oy, 242 + ox, 206 + oy])) },
      { n: 220, b: 1.1, id: 'w1', draw: stroke(10, wheel(W1)) },
      { n: 220, b: 1.1, id: 'w2', draw: stroke(10, wheel(W2)) },
      { n: 80, b: 0.9, id: 's1', draw: stroke(5, spokes(W1)) },
      { n: 80, b: 0.9, id: 's2', draw: stroke(5, spokes(W2)) },
      { n: 50, b: 1.45, id: 'h1', draw: fill((g) => circle(g, W1[0], W1[1], 7)) },
      { n: 50, b: 1.45, id: 'h2', draw: fill((g) => circle(g, W2[0], W2[1], 7)) },
      {
        n: 250,
        b: 0.8,
        id: 'speed',
        draw: stroke(9, (g) => {
          poly(g, [24, 152 + oy, 74, 152 + oy]);
          poly(g, [12, 192 + oy, 80, 192 + oy]);
          poly(g, [28, 232 + oy, 74, 232 + oy]);
        }),
      },
    ],
    7,
  );
  withBase(sh);
  const hubs = [
    [(W1[0] - H) / H, (W1[1] - H) / H, ['w1', 's1', 'h1']],
    [(W2[0] - H) / H, (W2[1] - H) / H, ['w2', 's2', 'h2']],
  ];
  const [sp0, sp1] = sh.ranges.speed;
  const speedMin = (12 - H) / H;
  const speedLen = (80 - 12) / H;
  sh.update = (t, still) => {
    if (still) return;
    const a = t * 2.4;
    const ca = Math.cos(a);
    const sa = Math.sin(a);
    for (const [hx, hy, ids] of hubs) {
      for (const id of ids) {
        const [s0, s1] = sh.ranges[id];
        for (let i = s0; i < s1; i++) {
          const dx = sh.bx[i] - hx;
          const dy = sh.by[i] - hy;
          sh.x[i] = hx + dx * ca - dy * sa;
          sh.y[i] = hy + dx * sa + dy * ca;
        }
      }
    }
    // speed lines stream backwards
    for (let i = sp0; i < sp1; i++) {
      const f = (((sh.bx[i] - speedMin) / speedLen - t * 0.9) % 1 + 1) % 1;
      sh.b[i] = sh.bb[i] * (0.35 + 0.9 * Math.sin(f * Math.PI));
    }
  };
  return sh;
}

// 8. Shopping cart holding two parcels
function cart() {
  const basket = (g) => poly(g, [104, 132, 346, 132, 318, 242, 128, 242], true);
  const parcels = [
    [134, 58, 88, 74],
    [232, 84, 74, 48],
  ];
  const aboveRim = (g) => {
    g.beginPath();
    g.rect(0, 0, C, 126);
    g.clip();
  };
  return fromParts(
    [
      { n: 950, draw: stroke(11, basket) },
      {
        n: 200,
        b: 0.5,
        draw: stroke(5, (g) => {
          poly(g, [120, 188, 332, 188]);
          poly(g, [190, 138, 186, 236]);
          poly(g, [262, 138, 258, 236]);
        }),
      },
      { n: 450, draw: stroke(11, (g) => poly(g, [44, 92, 84, 92, 128, 242, 138, 272, 322, 272])) },
      {
        n: 300,
        b: 1.15,
        draw: stroke(9, (g) => {
          circle(g, 160, 298, 17);
          circle(g, 298, 298, 17);
        }),
      },
      {
        n: 600,
        b: 1.3,
        draw: (g) => {
          aboveRim(g);
          g.lineWidth = 10;
          g.beginPath();
          for (const [x, y, w, h] of parcels) rrect(g, x, y, w, h + 20, 5);
          g.stroke();
        },
      },
      {
        n: 200,
        b: 1.6,
        draw: (g) => {
          aboveRim(g);
          g.lineWidth = 10;
          g.beginPath();
          for (const [x, y, w, h] of parcels) poly(g, [x + w / 2, y + 2, x + w / 2, y + h]);
          g.stroke();
        },
      },
    ],
    8,
  );
}

// 9. Browser window with </>
function browser() {
  const win = (g) => rrect(g, 55, 76, 290, 250, 18);
  return fromParts(
    [
      { n: 1050, draw: stroke(11, win) },
      { n: 250, b: 0.9, draw: stroke(8, (g) => poly(g, [58, 120, 342, 120])) },
      {
        n: 150,
        b: 1.3,
        draw: fill((g) => {
          circle(g, 86, 98, 7);
          circle(g, 110, 98, 7);
          circle(g, 134, 98, 7);
        }),
      },
      { n: 150, b: 0.5, draw: stroke(5, (g) => rrect(g, 160, 89, 158, 18, 9)) },
      {
        n: 850,
        b: 1.5,
        draw: stroke(13, (g) => {
          poly(g, [150, 172, 112, 222, 150, 272]);
          poly(g, [218, 162, 182, 282]);
          poly(g, [250, 172, 288, 222, 250, 272]);
        }),
      },
      { n: 250, b: 0.25, draw: fill(win) },
    ],
    9,
  );
}

// 10. Video frame with a play triangle
function video() {
  return fromParts(
    [
      { n: 1300, draw: stroke(11, (g) => rrect(g, 40, 110, 320, 180, 16)) },
      { n: 900, b: 1.5, draw: fill((g) => poly(g, [176, 148, 176, 230, 244, 189], true)) },
      { n: 250, b: 0.6, draw: stroke(5, (g) => poly(g, [68, 264, 332, 264])) },
      { n: 200, b: 1.3, draw: stroke(6, (g) => poly(g, [68, 264, 168, 264])) },
      { n: 50, b: 1.6, draw: fill((g) => circle(g, 170, 264, 8)) },
    ],
    10,
  );
}

// 11. Four glowing clusters joined by dotted lines (Selected work)
function clusters() {
  const sh = blank();
  const r = rng(11);
  const centres = [
    [0.04, -0.5],
    [0.74, -0.02],
    [-0.04, 0.52],
    [-0.72, 0.04],
  ];
  const per = 550;
  const sigma = 0.1;
  const ox = new Float32Array(SHAPE_DOTS);
  const oy = new Float32Array(SHAPE_DOTS);
  const owner = new Int8Array(SHAPE_DOTS).fill(-1);
  let k = 0;
  centres.forEach((c, ci) => {
    for (let j = 0; j < per; j++, k++) {
      const rad = Math.min(2.6, Math.sqrt(-2 * Math.log(1 - r() * 0.999))) * sigma;
      const a = r() * TAU;
      ox[k] = Math.cos(a) * rad;
      oy[k] = Math.sin(a) * rad;
      owner[k] = ci;
      sh.b[k] = 1.45 - 0.6 * (rad / (2.6 * sigma)) + 0.15 * r();
      sh.s[k] = 1.15 - 0.4 * (rad / (2.6 * sigma));
    }
  });
  // dotted lines around the diamond
  const lines = SHAPE_DOTS - k;
  for (let j = 0; j < lines; j++, k++) {
    const e = j % 4;
    const a = centres[e];
    const b = centres[(e + 1) % 4];
    const len = Math.hypot(b[0] - a[0], b[1] - a[1]);
    const gap = 0.2 / len;
    // dashes: keep points in "on" stretches only
    let f;
    do f = gap + r() * (1 - 2 * gap);
    while ((f * len * 22) % 1 > 0.55);
    const jit = (r() - 0.5) * 0.012;
    sh.x[k] = a[0] + (b[0] - a[0]) * f - (b[1] - a[1]) / len * jit;
    sh.y[k] = a[1] + (b[1] - a[1]) * f + (b[0] - a[0]) / len * jit;
    sh.b[k] = 0.62;
    sh.s[k] = 0.8;
  }
  sh.update = (t, still) => {
    for (let i = 0; i < per * 4; i++) {
      const ci = owner[i];
      const ph = still ? 0 : Math.sin(t * 1.4 + ci * (Math.PI / 2));
      const sc = 1 + 0.15 * ph;
      sh.x[i] = centres[ci][0] + ox[i] * sc;
      sh.y[i] = centres[ci][1] + oy[i] * sc;
    }
  };
  sh.update(0, true);
  return sh;
}

// 12. Winding path with four nodes, dots flowing along it (How we work)
function path() {
  const sh = blank();
  const r = rng(12);
  // Resample an S curve to equal arc-length steps.
  const raw = [];
  for (let i = 0; i <= 600; i++) {
    const u = i / 600;
    raw.push([-0.8 + 1.6 * u, -0.46 * Math.sin(TAU * u) + 0.06 * Math.sin(Math.PI * u)]);
  }
  const acc = [0];
  for (let i = 1; i < raw.length; i++) acc.push(acc[i - 1] + Math.hypot(raw[i][0] - raw[i - 1][0], raw[i][1] - raw[i - 1][1]));
  const total = acc[acc.length - 1];
  const N = 1024;
  const px = new Float32Array(N);
  const py = new Float32Array(N);
  for (let i = 0, j = 0; i < N; i++) {
    const want = (i / (N - 1)) * total;
    while (j < acc.length - 2 && acc[j + 1] < want) j++;
    const f = (want - acc[j]) / (acc[j + 1] - acc[j] || 1);
    px[i] = raw[j][0] + (raw[j + 1][0] - raw[j][0]) * f;
    py[i] = raw[j][1] + (raw[j + 1][1] - raw[j][1]) * f;
  }
  const at = (f) => {
    const q = Math.min(N - 1.001, Math.max(0, f * (N - 1)));
    const i = q | 0;
    const g = q - i;
    return [px[i] + (px[i + 1] - px[i]) * g, py[i] + (py[i + 1] - py[i]) * g, px[i + 1] - px[i], py[i + 1] - py[i]];
  };
  const nodes = [0.08, 0.36, 0.64, 0.92].map((f) => at(f));
  const nearNode = (x, y) => nodes.some(([nx, ny]) => Math.hypot(x - nx, y - ny) < 0.1);

  let k = 0;
  // path line
  while (k < 1300) {
    const [x, y, dx, dy] = at(r());
    const l = Math.hypot(dx, dy) || 1;
    const o = (r() - 0.5) * 0.03;
    const X = x - (dy / l) * o;
    const Y = y + (dx / l) * o;
    if (nearNode(X, Y)) continue;
    sh.x[k] = X;
    sh.y[k] = Y;
    sh.b[k] = 0.55;
    sh.s[k] = 0.85;
    k++;
  }
  // nodes: ring + core
  for (const [nx, ny] of nodes) {
    for (let j = 0; j < 200; j++, k++) {
      const a = r() * TAU;
      const ring = j < 130;
      const rad = ring ? 0.078 + (r() - 0.5) * 0.022 : Math.sqrt(r()) * 0.036;
      sh.x[k] = nx + Math.cos(a) * rad;
      sh.y[k] = ny + Math.sin(a) * rad;
      sh.b[k] = ring ? 1.25 : 1.6;
      sh.s[k] = ring ? 1 : 1.15;
    }
  }
  // flow
  const f0 = k;
  const flow = SHAPE_DOTS - f0;
  const seed = new Float32Array(flow);
  const off = new Float32Array(flow);
  for (let j = 0; j < flow; j++) {
    seed[j] = j / flow + (r() - 0.5) * 0.004;
    off[j] = (r() - 0.5) * 0.045;
  }
  sh.update = (t, still) => {
    const shift = still ? 0 : t * 0.045;
    for (let j = 0; j < flow; j++) {
      const f = (seed[j] + shift) % 1;
      const [x, y, dx, dy] = at(f);
      const l = Math.hypot(dx, dy) || 1;
      const i = f0 + j;
      sh.x[i] = x - (dy / l) * off[j];
      sh.y[i] = y + (dx / l) * off[j];
      sh.b[i] = 1.55 * Math.pow(Math.sin(Math.PI * f), 0.6);
      sh.s[i] = 1.05;
    }
  };
  sh.update(0, true);
  return sh;
}

// 13. Egg cracking open, light spilling out (About)
function hatch() {
  const cx = 200;
  const cy = 214;
  const rx = 90;
  const ry = 116;
  const crackY = 196;
  const glow = hexRgb('#FFF4DC');
  // where the crack meets the egg outline on each side
  const solve = (side) => {
    // find t with y = crackY on the right (side 1) or left (side -1)
    let best = 0;
    let bestD = 1e9;
    for (let i = 0; i <= 2000; i++) {
      const t = -Math.PI / 2 + (i / 2000) * Math.PI * (side > 0 ? 1 : -1);
      const [, y] = eggPt(cx, cy, rx, ry, side > 0 ? t : Math.PI - (t + Math.PI / 2) - Math.PI / 2);
      const d = Math.abs(y - crackY);
      if (d < bestD) {
        bestD = d;
        best = t;
      }
    }
    return best;
  };
  const tR = solve(1);
  const tL = Math.PI - tR;
  const [xR] = eggPt(cx, cy, rx, ry, tR);
  const [xL] = eggPt(cx, cy, rx, ry, tL);
  const teeth = 7;
  const zig = [];
  for (let i = 0; i <= teeth * 2; i++) {
    const f = i / (teeth * 2);
    zig.push(xR + (xL - xR) * f, crackY + (i % 2 ? -15 : 9) * (i === 0 || i === teeth * 2 ? 0 : 1));
  }
  const bottom = (g) => {
    eggPath(g, cx, cy, rx, ry, tR, tL);
    for (let i = 0; i < zig.length; i += 2) g.lineTo(zig[zig.length - 2 - i], zig[zig.length - 1 - i]);
    g.closePath();
  };
  const lift = [44, -62];
  const tilt = 0.38;
  const capCx = (xR + xL) / 2;
  const cap = (g) => {
    g.translate(capCx + lift[0], crackY + lift[1]);
    g.rotate(tilt);
    g.translate(-capCx, -crackY);
    eggPath(g, cx, cy, rx, ry, tL, tR + TAU);
    for (let i = 0; i < zig.length; i += 2) g.lineTo(zig[i], zig[i + 1]);
    g.closePath();
  };
  const sh = fromParts(
    [
      { n: 1100, draw: stroke(11, bottom) },
      { n: 300, b: 0.3, draw: fill(bottom) },
      { n: 800, draw: stroke(11, cap) },
      { n: 100, b: 1.7, rgb: glow, id: 'edge', draw: stroke(6, (g) => poly(g, zig)) },
      { n: 400, b: 1.6, rgb: glow, id: 'rise', draw: stroke(6, (g) => poly(g, zig)) },
    ],
    13,
  );
  // rising light between the shells
  const [r0, r1] = sh.ranges.rise;
  const r = rng(131);
  const n = r1 - r0;
  const x0 = new Float32Array(n);
  const ph = new Float32Array(n);
  const sp = new Float32Array(n);
  const openY = (crackY - H) / H;
  const half = (xL - xR) / 2 / H;
  for (let j = 0; j < n; j++) {
    x0[j] = (r() * 2 - 1) * Math.abs(half) * 0.8 + (capCx - H) / H;
    ph[j] = r();
    sp[j] = 0.12 + r() * 0.1;
  }
  sh.update = (t, still) => {
    for (let j = 0; j < n; j++) {
      const life = (ph[j] + (still ? 0 : t * sp[j])) % 1;
      const i = r0 + j;
      const cxn = (capCx - H) / H;
      sh.x[i] = cxn + (x0[j] - cxn) * (1 + life * 0.7) + (still ? 0 : 0.02 * Math.sin(t * 1.7 + j));
      sh.y[i] = openY - 0.02 - life * 0.62;
      sh.b[i] = 1.7 * (1 - life) * Math.min(1, life * 8);
      sh.s[i] = 0.75 + (1 - life) * 0.5;
    }
  };
  sh.update(0, true);
  return sh;
}

// 14. Globe with PK, ES, UK markers and flowing arcs (Markets)
function globe() {
  const sh = blank();
  const r = rng(14);
  const R = 0.74;
  const D = Math.PI / 180;
  const N = SHAPE_DOTS;
  const lat = new Float32Array(N);
  const lon = new Float32Array(N);
  const kind = new Uint8Array(N); // 0 grid, 1 surface, 2 marker ring, 3 marker core, 4 arc
  const aux = new Float32Array(N);
  const which = new Uint8Array(N);
  let k = 0;
  // graticule: parallels and meridians, weighted by length
  const pars = [-60, -30, 0, 30, 60];
  const lines = [...pars.map((p) => ({ p, w: Math.cos(p * D) })), ...[0, 30, 60, 90, 120, 150].map((m) => ({ m, w: 2 }))];
  const wsum = lines.reduce((s, l) => s + l.w, 0);
  for (; k < 1400; k++) {
    let q = r() * wsum;
    let l = lines[0];
    for (const c of lines) {
      q -= c.w;
      if (q <= 0) {
        l = c;
        break;
      }
    }
    if (l.p !== undefined) {
      lat[k] = l.p * D;
      lon[k] = (r() * 360 - 180) * D;
    } else {
      const a = r() * TAU;
      lat[k] = Math.asin(Math.sin(a));
      lon[k] = (l.m + (Math.cos(a) < 0 ? 180 : 0)) * D;
    }
    kind[k] = 0;
  }
  // faint surface dots (Fibonacci sphere)
  const surf = 400;
  for (let j = 0; j < surf; j++, k++) {
    const y = 1 - (2 * (j + 0.5)) / surf;
    lat[k] = Math.asin(y);
    lon[k] = (j * 2.39996) % TAU;
    kind[k] = 1;
  }
  const markers = [
    [30.4, 69.3],
    [40.4, -3.7],
    [54.0, -2.0],
  ].map(([a, b]) => [a * D, b * D]);
  for (let m = 0; m < 3; m++) {
    for (let j = 0; j < 100; j++, k++) {
      kind[k] = j < 70 ? 2 : 3;
      which[k] = m;
      aux[k] = j < 70 ? (j / 70) * TAU : r();
      lat[k] = r() * TAU;
    }
  }
  const arcs = [
    [0, 1, 260],
    [0, 2, 260],
    [1, 2, 80],
  ];
  const vec = ([la, lo]) => [Math.cos(la) * Math.sin(lo), -Math.sin(la), Math.cos(la) * Math.cos(lo)];
  const mv = markers.map(vec);
  for (let a = 0; a < arcs.length; a++) {
    const cnt = arcs[a][2];
    for (let j = 0; j < cnt && k < N; j++, k++) {
      kind[k] = 4;
      which[k] = a;
      aux[k] = j / cnt + (r() - 0.5) * 0.004;
      lat[k] = (r() - 0.5) * 0.02;
    }
  }
  for (; k < N; k++) kind[k] = 1;

  const markerRgb = hexRgb('#FFF2D8');
  for (let i = 0; i < N; i++) if (kind[i] === 2 || kind[i] === 3) setOwn(sh, i, markerRgb);

  let ry = 0;
  let cy = 1;
  let sy = 0;
  let ct = 1;
  let st = 0;
  const proj = (x, y, z) => {
    // rotate around the vertical axis, then tilt toward the viewer
    const x1 = x * cy - z * sy;
    const z1 = x * sy + z * cy;
    const y2 = y * ct - z1 * st;
    const z2 = y * st + z1 * ct;
    return [x1 * R, y2 * R, z2];
  };
  sh.update = (t, still) => {
    const time = still ? 0 : t;
    ry = (32 + 16 * Math.sin(time * 0.13)) * D;
    cy = Math.cos(ry);
    sy = Math.sin(ry);
    const tilt = -0.42;
    ct = Math.cos(tilt);
    st = Math.sin(tilt);
    const pm = mv.map((v) => proj(...v));
    for (let i = 0; i < N; i++) {
      let X;
      let Y;
      let Z;
      let b = 1;
      let s = 1;
      switch (kind[i]) {
        case 0:
        case 1: {
          const v = vec([lat[i], lon[i]]);
          [X, Y, Z] = proj(...v);
          b = kind[i] === 0 ? 0.75 : 0.35;
          s = kind[i] === 0 ? 0.9 : 0.75;
          break;
        }
        case 2:
        case 3: {
          const [mx, my, mz] = pm[which[i]];
          const pulse = 1 + (still ? 0 : 0.28 * Math.sin(time * 2.2 + which[i] * 2));
          const rad = kind[i] === 2 ? 0.052 * pulse : Math.sqrt(aux[i]) * 0.018;
          const a = kind[i] === 2 ? aux[i] : lat[i];
          X = mx + Math.cos(a) * rad;
          Y = my + Math.sin(a) * rad;
          Z = mz;
          b = kind[i] === 2 ? 1.35 : 1.8;
          s = 1.1;
          break;
        }
        default: {
          const [ia, ib] = arcs[which[i]];
          const A = mv[ia];
          const B = mv[ib];
          const f = (aux[i] + (still ? 0 : time * 0.11)) % 1;
          const dot = A[0] * B[0] + A[1] * B[1] + A[2] * B[2];
          const om = Math.acos(Math.min(1, Math.max(-1, dot)));
          const so = Math.sin(om) || 1;
          const wa = Math.sin((1 - f) * om) / so;
          const wb = Math.sin(f * om) / so;
          const h = 1 + (0.06 + 0.42 * (om / Math.PI)) * Math.sin(Math.PI * f) + lat[i];
          [X, Y, Z] = proj((A[0] * wa + B[0] * wb) * h, (A[1] * wa + B[1] * wb) * h, (A[2] * wa + B[2] * wb) * h);
          b = 1.5 * Math.pow(Math.sin(Math.PI * f), 0.5);
          s = 1;
        }
      }
      if (Z < 0) {
        b *= 0.22;
        s *= 0.75;
      }
      sh.x[i] = X;
      sh.y[i] = Y;
      sh.b[i] = b;
      sh.s[i] = s;
    }
  };
  sh.update(0, true);
  return sh;
}

// 15. Slow spiral galaxy (FAQ)
function galaxy() {
  const sh = blank();
  const r = rng(15);
  const N = SHAPE_DOTS;
  const rad = new Float32Array(N);
  const ang = new Float32Array(N);
  const gauss = () => Math.sqrt(-2 * Math.log(1 - r() * 0.999)) * Math.cos(r() * TAU);
  let k = 0;
  for (; k < 450; k++) {
    rad[k] = Math.min(0.22, Math.abs(gauss()) * 0.06);
    ang[k] = r() * TAU;
    sh.b[k] = 1.35 - rad[k] * 3;
    sh.s[k] = 1;
  }
  const arms = 2;
  const perArm = 1000;
  for (let a = 0; a < arms; a++) {
    for (let j = 0; j < perArm; j++, k++) {
      const th = 3 * Math.PI * Math.pow(r(), 0.7);
      const base = 0.05 * Math.exp(0.3 * th);
      const spread = 0.012 + 0.05 * base;
      rad[k] = base + gauss() * spread;
      ang[k] = th + (a / arms) * TAU + gauss() * 0.05;
      sh.b[k] = 1.15 - 0.5 * Math.min(1, base);
      sh.s[k] = 0.95;
    }
  }
  for (; k < N; k++) {
    rad[k] = Math.sqrt(r()) * 0.92;
    ang[k] = r() * TAU;
    sh.b[k] = 0.3;
    sh.s[k] = 0.7;
  }
  sh.alpha = 0.6;
  const tilt = -0.35;
  const ct = Math.cos(tilt);
  const st = Math.sin(tilt);
  sh.update = (t, still) => {
    const rot = still ? 0 : t * 0.07;
    for (let i = 0; i < N; i++) {
      const a = ang[i] + rot;
      const x = rad[i] * Math.cos(a);
      const y = rad[i] * Math.sin(a) * 0.62;
      sh.x[i] = x * ct - y * st;
      sh.y[i] = x * st + y * ct;
    }
  };
  sh.update(0, true);
  return sh;
}

// 16. Flying bird (Contact)
function bird() {
  const sh = blank();
  const r = rng(16);
  const N = SHAPE_DOTS;
  const mx = new Float32Array(N);
  const my = new Float32Array(N);
  const mz = new Float32Array(N);
  const span = new Float32Array(N);
  const side = new Int8Array(N);
  let k = 0;
  // body: ellipsoid along x, thinner toward the tail
  for (; k < 450; k++) {
    const u = r() * 2 - 1;
    const th = r() * TAU;
    const s = Math.sqrt(1 - u * u) * (1 - Math.max(0, -u) * 0.45);
    const q = 0.82 + 0.18 * r();
    mx[k] = u * 0.34 * q;
    my[k] = s * Math.cos(th) * 0.1 * q;
    mz[k] = s * Math.sin(th) * 0.1 * q;
    sh.b[k] = 1.1;
  }
  // head
  for (let j = 0; j < 150; j++, k++) {
    const u = r() * 2 - 1;
    const th = r() * TAU;
    const s = Math.sqrt(1 - u * u);
    mx[k] = 0.36 + u * 0.085;
    my[k] = -0.07 + s * Math.cos(th) * 0.085;
    mz[k] = s * Math.sin(th) * 0.085;
    sh.b[k] = 1.2;
  }
  // beak
  for (let j = 0; j < 50; j++, k++) {
    const f = r();
    const w = 0.024 * (1 - f);
    const a = r() * TAU;
    mx[k] = 0.43 + f * 0.12;
    my[k] = -0.066 + f * 0.012 + Math.cos(a) * w;
    mz[k] = Math.sin(a) * w;
    sh.b[k] = 1.6;
  }
  // tail fan
  for (let j = 0; j < 250; j++, k++) {
    const f = Math.sqrt(r());
    mx[k] = -0.3 - f * 0.3;
    my[k] = 0.02 - f * 0.05;
    mz[k] = (r() * 2 - 1) * (0.03 + f * 0.16);
    sh.b[k] = 0.95;
  }
  // wings: near (+1) and far (-1)
  const wing0 = k;
  for (const sd of [1, -1]) {
    for (let j = 0; j < 900; j++, k++) {
      const s = r();
      const c = Math.pow(r(), 1.5);
      const lead = 0.13 - 0.24 * s * s;
      const chord = 0.32 * (1 - 0.78 * Math.pow(s, 1.4)) + 0.03;
      mx[k] = lead - c * chord;
      span[k] = s;
      mz[k] = 0.07 + s * 0.8; // distance from the body axis
      side[k] = sd;
      sh.b[k] = (sd > 0 ? 1.05 : 0.8) * (1.25 - c * 0.45);
    }
  }
  const bb = Float32Array.from(sh.b);

  const yaw = 0.55;
  const pitch = -0.38;
  const roll = -0.38;
  const cyw = Math.cos(yaw);
  const syw = Math.sin(yaw);
  const cp = Math.cos(pitch);
  const sp = Math.sin(pitch);
  const cr = Math.cos(roll);
  const sr = Math.sin(roll);
  const scale = 1.05;

  sh.update = (t, still) => {
    const ph = still ? 1.9 : t * 4.6;
    const bob = still ? 0 : -0.035 * Math.sin(ph - 0.6);
    for (let i = 0; i < N; i++) {
      let x = mx[i];
      let y = my[i];
      let z = mz[i];
      if (i >= wing0) {
        const s = span[i];
        const th = 0.95 * Math.sin(ph - 0.75 * s) * (0.55 + 0.45 * s) + 0.12;
        const d = z;
        y = -d * Math.sin(th);
        z = side[i] * d * Math.cos(th);
      }
      // yaw (vertical axis), pitch (tilt toward viewer), then roll in the screen plane
      const x1 = x * cyw + z * syw;
      const z1 = -x * syw + z * cyw;
      const y2 = y * cp - z1 * sp;
      const z2 = y * sp + z1 * cp;
      const xs = x1 * cr - y2 * sr;
      const ys = x1 * sr + y2 * cr;
      sh.x[i] = xs * scale - 0.04;
      sh.y[i] = ys * scale + bob + 0.08;
      const depth = Math.max(-1, Math.min(1, z2 * 1.4));
      sh.b[i] = bb[i] * (0.8 + 0.25 * depth);
      sh.s[i] = 0.95 + 0.15 * depth;
    }
  };
  // fly up and away when the page moves on to the logo
  sh.exit = (t) => {
    const e = t * t;
    return { dx: 0.9 * e, dy: -2.2 * e };
  };
  sh.update(0, true);
  return sh;
}

// 17. The Grow Nest logo, sampled from the logo image (wordmark only)
function logo() {
  const sh = bird();
  const fallbackUpdate = sh.update;
  const url = new URL('../img/grownest-logo.png', import.meta.url).href;
  const img = new Image();
  img.decoding = 'async';
  img.onload = () => {
    try {
      sampleLogo(sh, img);
    } catch {
      // keep the bird
    }
  };
  img.src = url;
  sh.update = (t, still) => {
    if (!sh.isLogo) fallbackUpdate(t, still);
  };
  sh.exit = null;
  return sh;
}

function sampleLogo(sh, img) {
  const w = img.naturalWidth;
  const h = img.naturalHeight;
  const cv = Object.assign(document.createElement('canvas'), { width: w, height: h });
  const g = cv.getContext('2d', { willReadFrequently: true });
  g.drawImage(img, 0, 0);
  const d = g.getImageData(0, 0, w, h).data;
  const inkAt = (i) => 255 - Math.min(d[i], d[i + 1], d[i + 2]);
  // Find the ink bands (GROW, NEST, tagline) and keep the first two.
  const bands = [];
  let start = -1;
  for (let y = 0; y < h; y++) {
    let any = false;
    for (let x = 0; x < w; x += 2) {
      if (inkAt((y * w + x) * 4) > 90) {
        any = true;
        break;
      }
    }
    if (any && start < 0) start = y;
    if (!any && start >= 0) {
      if (y - start > 8) bands.push([start, y]);
      start = -1;
    }
  }
  if (bands.length < 2) throw new Error('logo bands');
  const y0 = bands[0][0];
  const y1 = bands[1][1];
  const idx = [];
  let xMin = w;
  let xMax = 0;
  for (let y = y0; y < y1; y++) {
    for (let x = 0; x < w; x++) {
      if (inkAt((y * w + x) * 4) > 110) {
        idx.push(y * w + x);
        if (x < xMin) xMin = x;
        if (x > xMax) xMax = x;
      }
    }
  }
  if (idx.length < 100) throw new Error('logo ink');
  const r = rng(17);
  const cx = (xMin + xMax) / 2;
  const cy = (y0 + y1) / 2;
  const sc = 2 / (xMax - xMin);
  for (let k = 0; k < SHAPE_DOTS; k++) {
    const p = idx[(r() * idx.length) | 0];
    const x = p % w;
    const y = (p / w) | 0;
    sh.x[k] = (x + r() - cx) * sc;
    sh.y[k] = (y + r() - cy) * sc;
    sh.b[k] = 0.95 + 0.25 * r();
    sh.s[k] = 1;
    const i = p * 4;
    setOwn(sh, k, lightenRgb(d[i] / 255, d[i + 1] / 255, d[i + 2] / 255));
  }
  sh.isLogo = true;
}

// Keep the hue, lift the lightness so blue and grey read on the night sky.
function lightenRgb(r, g, b) {
  const mx = Math.max(r, g, b);
  const mn = Math.min(r, g, b);
  let h = 0;
  let s = 0;
  const l0 = (mx + mn) / 2;
  const dd = mx - mn;
  if (dd > 1e-6) {
    s = dd / (1 - Math.abs(2 * l0 - 1));
    if (mx === r) h = ((g - b) / dd) % 6;
    else if (mx === g) h = (b - r) / dd + 2;
    else h = (r - g) / dd + 4;
    h /= 6;
    if (h < 0) h += 1;
  }
  const l = Math.max(l0, 0.7);
  s = Math.min(s, 0.68);
  const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
  const p = 2 * l - q;
  const ch = (t) => {
    t = (t + 1) % 1;
    if (t < 1 / 6) return p + (q - p) * 6 * t;
    if (t < 1 / 2) return q;
    if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
    return p;
  };
  return [ch(h + 1 / 3), ch(h), ch(h - 1 / 3)];
}

const builders = {
  nest,
  bag,
  cartons,
  bars,
  chat,
  envelope,
  van,
  cart,
  browser,
  video,
  clusters,
  path,
  hatch,
  globe,
  galaxy,
  bird,
  logo,
};

export function buildShape(name) {
  const make = builders[name] || bird;
  const sh = make();
  sh.name = name;
  return sh;
}
