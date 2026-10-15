/* Local Three.js scenes: campus topology and a 3D embedding space. */
import * as THREE from "../../vendor/three.module.min.js";
import { OrbitControls } from "../../vendor/OrbitControls.js";

const TOPOLOGY = [
  { id: "learner", label: "Learner", pos: [-3.5, 0.45, 0.35], color: 0x818cf8 },
  { id: "prompt", label: "Prompt", pos: [-1.45, 1.85, 0.75], color: 0xfbbf24 },
  { id: "model", label: "Model", pos: [0.2, 0.25, 0], color: 0xa5b4fc },
  { id: "retriever", label: "Retriever", pos: [2.7, 1.7, -1.05], color: 0x2dd4bf },
  { id: "tools", label: "Tools", pos: [2.95, -1.35, 1.05], color: 0xf472b6 },
  { id: "eval", label: "Eval", pos: [0.15, -2.25, 0.55], color: 0x34d399 },
];

const TOPOLOGY_LINKS = [
  ["learner", "prompt"],
  ["prompt", "model"],
  ["retriever", "model", "retriever"],
  ["tools", "model", "tools"],
  ["model", "eval", "eval"],
];

const EMBED_POINTS = [
  { id: "refund", x: 0.78, y: 0.68, z: 0.62, color: 0x2dd4bf },
  { id: "shipping", x: 0.24, y: 0.74, z: 0.34, color: 0x818cf8 },
  { id: "hours", x: 0.62, y: 0.22, z: 0.74, color: 0xfbbf24 },
  { id: "invoice", x: 0.26, y: 0.28, z: 0.4, color: 0xf472b6 },
];

const scenes = { topology: null, embed: null };

function makeRenderer(host) {
  const canvas = document.createElement("canvas");
  canvas.className = "space-canvas";
  canvas.setAttribute("role", "img");
  host.appendChild(canvas);
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  } catch (err) {
    canvas.remove();
    return null;
  }
  if (!renderer.getContext()) {
    renderer.dispose();
    canvas.remove();
    return null;
  }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0x000000, 0);
  return renderer;
}

function fit(renderer, camera, host) {
  const width = host.clientWidth || 640;
  const height = host.clientHeight || 320;
  renderer.setSize(width, height, false);
  camera.aspect = width / Math.max(1, height);
  camera.updateProjectionMatrix();
}

function glowMaterial(color) {
  return new THREE.MeshStandardMaterial({
    color,
    emissive: color,
    emissiveIntensity: 0.85,
    roughness: 0.35,
    metalness: 0.1,
  });
}

function linkMesh(from, to, color) {
  const start = new THREE.Vector3(...from);
  const end = new THREE.Vector3(...to);
  const mid = start.clone().lerp(end, 0.5);
  const length = start.distanceTo(end);
  const geom = new THREE.CylinderGeometry(0.025, 0.025, Math.max(0.01, length), 8);
  const mesh = new THREE.Mesh(geom, glowMaterial(color));
  mesh.position.copy(mid);
  mesh.quaternion.setFromUnitVectors(
    new THREE.Vector3(0, 1, 0),
    end.clone().sub(start).normalize()
  );
  mesh.userData.base = color;
  return mesh;
}

function labelSprite(text, color) {
  const canvas = document.createElement("canvas");
  canvas.width = 256;
  canvas.height = 64;
  const ctx = canvas.getContext("2d");
  ctx.fillStyle = color;
  ctx.font = "600 28px system-ui, sans-serif";
  ctx.textAlign = "center";
  ctx.fillText(text, 128, 40);
  const texture = new THREE.CanvasTexture(canvas);
  const material = new THREE.SpriteMaterial({ map: texture, transparent: true, depthWrite: false });
  const sprite = new THREE.Sprite(material);
  sprite.scale.set(1.35, 0.34, 1);
  return sprite;
}

const PALETTES = {
  neon: { fog: 0x070018, grid: 0x22d3ee, ring: 0xe879f9, particles: 0x67e8f9, key: 0x22d3ee, fill: 0xe879f9 },
  holographic: { fog: 0x04141c, grid: 0x5eead4, ring: 0xc4b5fd, particles: 0xe0f2fe, key: 0x2dd4bf, fill: 0xa78bfa },
  cyberpunk: { fog: 0x140014, grid: 0xf472b6, ring: 0xfacc15, particles: 0xfb7185, key: 0xe879f9, fill: 0xfacc15 },
  sunset: { fog: 0x1a0b12, grid: 0xfb7185, ring: 0xfdba74, particles: 0xfbbf24, key: 0xf97316, fill: 0xfb7185 },
  light: { fog: 0xf8d0ff, grid: 0x0891b2, ring: 0xec4899, particles: 0x7c3aed, key: 0x22d3ee, fill: 0xf472b6 },
  futuristic: { fog: 0x070b16, grid: 0x22d3ee, ring: 0x67e8f9, particles: 0xa5f3fc, key: 0x22d3ee, fill: 0x818cf8 },
  gaming: { fog: 0x14081f, grid: 0xe879f9, ring: 0xa3e635, particles: 0xf0abfc, key: 0xe879f9, fill: 0xa3e635 },
  dark: { fog: 0x0b1020, grid: 0x818cf8, ring: 0x22d3ee, particles: 0xc7d2fe, key: 0x818cf8, fill: 0x2dd4bf },
  dusk: { fog: 0x1a120b, grid: 0xf6c177, ring: 0xe07a5f, particles: 0xf4a261, key: 0xf6c177, fill: 0xe9c46a },
  contrast: { fog: 0x000000, grid: 0xffe14a, ring: 0xffffff, particles: 0x9ff7ee, key: 0xffe14a, fill: 0xffffff },
};

function scenePalette() {
  const name = document.documentElement.getAttribute("data-theme") || "neon";
  return PALETTES[name] || PALETTES.neon;
}

function motionReduced() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches
    || document.documentElement.getAttribute("data-motion") === "reduce";
}

function startLoop(state) {
  state.controls.autoRotate = false;
  state.controls.enableDamping = false;
  const render = () => {
    if (!state.alive) return;
    state.controls.update();
    state.renderer.render(state.scene, state.camera);
  };
  state.render = render;
  state.controls.addEventListener("change", render);
  render();
}

function bindResize(host, state) {
  const observer = new ResizeObserver(() => {
    fit(state.renderer, state.camera, host);
    state.renderer.render(state.scene, state.camera);
  });
  observer.observe(host);
  state.observer = observer;
}

function baseLights(scene) {
  scene.add(new THREE.AmbientLight(0xffffff, 0.55));
  const key = new THREE.PointLight(0x818cf8, 18, 12);
  key.position.set(2.5, 3, 2);
  scene.add(key);
  const fill = new THREE.PointLight(0x2dd4bf, 8, 10);
  fill.position.set(-3, -1, 2);
  scene.add(fill);
}

function clusterGroup(x, y, z, scale, color, count, drift) {
  const group = new THREE.Group();
  const nodes = [];
  for (let index = 0; index < count; index += 1) {
    const mesh = new THREE.Mesh(
      new THREE.SphereGeometry(0.16 * scale, 12, 12),
      new THREE.MeshBasicMaterial({
        color,
        transparent: true,
        opacity: 0.95,
        depthWrite: false,
        blending: THREE.AdditiveBlending,
      })
    );
    const angle = (index / count) * Math.PI * 2;
    mesh.position.set(Math.cos(angle) * 0.72 * scale, Math.sin(angle) * 0.72 * scale, Math.sin(angle * 2) * 0.28 * scale);
    group.add(mesh);
    nodes.push(mesh);
  }
  nodes.forEach((node, index) => {
    const next = nodes[(index + 1) % nodes.length];
    const geom = new THREE.BufferGeometry().setFromPoints([node.position, next.position]);
    group.add(new THREE.Line(geom, new THREE.LineBasicMaterial({ color, transparent: true, opacity: 0.4 })));
  });
  group.position.set(x, y, z);
  group.userData.drift = drift;
  return group;
}

function transformerStack(x, y, z, drift) {
  const group = new THREE.Group();
  const colors = [0x22d3ee, 0xe879f9, 0xfacc15, 0x67e8f9, 0xfb7185];
  colors.forEach((color, index) => {
    const mesh = new THREE.Mesh(
      new THREE.BoxGeometry(2.4, 0.22, 0.9),
      new THREE.MeshBasicMaterial({
        color,
        transparent: true,
        opacity: 0.72,
        depthWrite: false,
        blending: THREE.AdditiveBlending,
      })
    );
    mesh.position.y = (index - 2) * 0.38;
    group.add(mesh);
  });
  group.position.set(x, y, z);
  group.userData.drift = drift;
  return group;
}

function attentionArcs(x, y, z, drift) {
  const group = new THREE.Group();
  for (let row = 0; row < 6; row += 1) {
    for (let col = 0; col < 6; col += 1) {
      const heat = Math.exp(-((row - col) ** 2) / 5);
      const cell = new THREE.Mesh(
        new THREE.PlaneGeometry(0.22, 0.22),
        new THREE.MeshBasicMaterial({
          color: heat > 0.55 ? 0xfb7185 : 0x22d3ee,
          transparent: true,
          opacity: 0.2 + heat * 0.75,
          depthWrite: false,
          blending: THREE.AdditiveBlending,
          side: THREE.DoubleSide,
        })
      );
      cell.position.set((col - 2.5) * 0.26, (2.5 - row) * 0.26, -0.04);
      group.add(cell);
    }
  }
  for (let index = 0; index < 7; index += 1) {
    const curve = new THREE.QuadraticBezierCurve3(
      new THREE.Vector3(-1.15, (index - 3) * 0.28, 0.05),
      new THREE.Vector3(0, 0.55 + index * 0.05, 0.55),
      new THREE.Vector3(1.2, (3 - index) * 0.22, 0.05)
    );
    const geom = new THREE.BufferGeometry().setFromPoints(curve.getPoints(28));
    group.add(new THREE.Line(geom, new THREE.LineBasicMaterial({
      color: index % 2 ? 0xfb7185 : 0x67e8f9,
      transparent: true,
      opacity: 0.45 + index * 0.07,
    })));
  }
  group.position.set(x, y, z);
  group.userData.drift = drift;
  return group;
}

function embeddingGalaxy(x, y, z, count, drift) {
  const positions = new Float32Array(count * 3);
  for (let index = 0; index < count; index += 1) {
    const arm = index % 3;
    const t = index / count;
    const radius = 0.2 + t * 2.4;
    const angle = t * 8 + arm * ((Math.PI * 2) / 3);
    positions[index * 3] = Math.cos(angle) * radius;
    positions[index * 3 + 1] = (Math.random() - 0.5) * 0.22;
    positions[index * 3 + 2] = Math.sin(angle) * radius;
  }
  const geom = new THREE.BufferGeometry();
  geom.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  const points = new THREE.Points(geom, new THREE.PointsMaterial({
    color: 0xc4b5fd,
    size: 0.12,
    sizeAttenuation: true,
    transparent: true,
    opacity: 0.85,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
  }));
  const group = new THREE.Group();
  group.add(points);
  group.position.set(x, y, z);
  group.userData.drift = drift;
  return group;
}

function drift(x, y, z, speed, phase, amp, spin) {
  return { x, y, z, speed, phase, amp, spin };
}

const HALF_FOV = Math.tan((52 * Math.PI) / 360);

function frustumPoint(ndcX, ndcY, depth, aspect) {
  return {
    x: ndcX * depth * HALF_FOV * aspect,
    y: ndcY * depth * HALF_FOV,
    z: 6.45 - depth,
  };
}

function cornerBeacon(x, y, z, color, motion) {
  const group = new THREE.Group();
  const sphere = new THREE.Mesh(
    new THREE.SphereGeometry(0.42, 18, 18),
    new THREE.MeshBasicMaterial({
      color,
      transparent: true,
      opacity: 0.95,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    })
  );
  group.add(sphere);
  const halo = new THREE.Mesh(
    new THREE.SphereGeometry(0.9, 16, 16),
    new THREE.MeshBasicMaterial({
      color,
      transparent: true,
      opacity: 0.35,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    })
  );
  group.add(halo);
  group.position.set(x, y, z);
  group.userData.drift = motion;
  return group;
}

function buildDepthLayers() {
  const wide = 1.5;
  const tall = 0.48;
  const signs = [[-1, 1], [1, 1], [-1, -1], [1, -1]];
  const cornerColors = [0x22d3ee, 0xe879f9, 0xfacc15, 0x67e8f9];
  const groups = [];
  signs.forEach(([sx, sy], index) => {
    const color = cornerColors[index];
    const beacon = frustumPoint(sx * 0.9, sy * 0.9, 5.4, wide);
    groups.push(cornerBeacon(beacon.x, beacon.y, beacon.z, color, drift(beacon.x, beacon.y, beacon.z, 0.12, index, 0.06, 0.02)));
    const phone = frustumPoint(sx * 0.88, sy * 0.9, 5.6, tall);
    groups.push(cornerBeacon(phone.x, phone.y, phone.z, index % 2 ? 0xfb7185 : 0xa5f3fc, drift(phone.x, phone.y, phone.z, 0.11, index + 0.6, 0.05, -0.02)));
    const far = frustumPoint(sx * 0.82, sy * 0.8, 12.8, wide);
    groups.push(clusterGroup(far.x, far.y, far.z, 1.7, color, 7, drift(far.x, far.y, far.z, 0.15, index * 0.4, 0.16, 0.04)));
    const farPhone = frustumPoint(sx * 0.8, sy * 0.84, 11.2, tall);
    groups.push(clusterGroup(farPhone.x, farPhone.y, farPhone.z, 1.35, color, 6, drift(farPhone.x, farPhone.y, farPhone.z, 0.14, index + 1.1, 0.14, -0.03)));
    const near = frustumPoint(sx * 0.62, sy * 0.55, 3.7, wide);
    groups.push(clusterGroup(near.x, near.y, near.z, 0.7, color, 5, drift(near.x, near.y, near.z, 0.18, index + 0.3, 0.08, 0.03)));
  });
  [[-1, 0.02], [1, -0.02]].forEach(([sx, sy], index) => {
    const side = frustumPoint(sx * 0.94, sy, 4.6, wide);
    const color = index ? 0xe879f9 : 0x22d3ee;
    groups.push(cornerBeacon(side.x, side.y, side.z, color, drift(side.x, side.y, side.z, 0.13, index + 0.2, 0.05, 0.02)));
    groups.push(clusterGroup(side.x, side.y, side.z, 1.05, color, 6, drift(side.x, side.y, side.z, 0.16, index + 0.9, 0.1, 0.04)));
    const phoneSide = frustumPoint(sx * 0.9, sy, 4.8, tall);
    groups.push(clusterGroup(phoneSide.x, phoneSide.y, phoneSide.z, 0.9, color, 5, drift(phoneSide.x, phoneSide.y, phoneSide.z, 0.15, index + 1.4, 0.08, -0.03)));
  });
  [[-0.45, -1], [0.62, -1]].forEach(([sx, sy], index) => {
    const rim = frustumPoint(sx, sy * 0.97, 3.8, tall);
    const color = index ? 0x67e8f9 : 0xfacc15;
    groups.push(cornerBeacon(rim.x, rim.y, rim.z, color, drift(rim.x, rim.y, rim.z, 0.12, index + 0.4, 0.04, 0.02)));
  });
  [[-1, -1], [1, -1]].forEach(([sx, sy], index) => {
    const low = frustumPoint(sx * 0.93, sy * 0.93, 3.2, 1.67);
    const color = index ? 0x22d3ee : 0xfacc15;
    groups.push(cornerBeacon(low.x, low.y, low.z, color, drift(low.x, low.y, low.z, 0.1, index + 0.7, 0.04, 0.01)));
  });
  const stackL = frustumPoint(-0.55, 0.42, 9.4, wide);
  const stackR = frustumPoint(0.58, -0.38, 8.8, wide);
  const arcR = frustumPoint(0.7, 0.06, 7.6, wide);
  const arcL = frustumPoint(-0.68, -0.04, 7.2, wide);
  const galT = frustumPoint(0.04, 0.62, 14.2, wide);
  const galB = frustumPoint(-0.06, -0.6, 13.6, wide);
  const phoneArc = frustumPoint(0.12, 0.58, 8.4, tall);
  const phoneStack = frustumPoint(-0.1, -0.55, 8.8, tall);
  groups.push(transformerStack(stackL.x, stackL.y, stackL.z, drift(stackL.x, stackL.y, stackL.z, 0.1, 0.4, 0.12, 0.05)));
  groups.push(transformerStack(stackR.x, stackR.y, stackR.z, drift(stackR.x, stackR.y, stackR.z, 0.11, 1.5, 0.12, -0.04)));
  groups.push(attentionArcs(arcR.x, arcR.y, arcR.z, drift(arcR.x, arcR.y, arcR.z, 0.09, 2.2, 0.1, 0.03)));
  groups.push(attentionArcs(arcL.x, arcL.y, arcL.z, drift(arcL.x, arcL.y, arcL.z, 0.09, 0.8, 0.1, -0.03)));
  groups.push(embeddingGalaxy(galT.x, galT.y, galT.z, 280, drift(galT.x, galT.y, galT.z, 0.07, 0.3, 0.1, 0.1)));
  groups.push(embeddingGalaxy(galB.x, galB.y, galB.z, 240, drift(galB.x, galB.y, galB.z, 0.08, 1.2, 0.1, -0.08)));
  groups.push(attentionArcs(phoneArc.x, phoneArc.y, phoneArc.z, drift(phoneArc.x, phoneArc.y, phoneArc.z, 0.1, 1.8, 0.08, 0.04)));
  groups.push(transformerStack(phoneStack.x, phoneStack.y, phoneStack.z, drift(phoneStack.x, phoneStack.y, phoneStack.z, 0.1, 0.5, 0.08, -0.04)));
  return groups;
}

export function mountTopology(host) {
  if (!host || scenes.topology) return scenes.topology;
  const renderer = makeRenderer(host);
  const note = host.querySelector(".space-fallback");
  if (!renderer) {
    if (note) note.hidden = false;
    return null;
  }
  if (note) note.hidden = true;
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(52, 1, 0.1, 80);
  camera.position.set(3.4, 2.1, 4.2);
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.target.set(0.1, 0, 0);
  baseLights(scene);
  const byId = {};
  const halos = [];
  TOPOLOGY.forEach((node) => {
    const mesh = new THREE.Mesh(new THREE.SphereGeometry(0.22, 24, 24), glowMaterial(node.color));
    mesh.material.emissiveIntensity = 1.35;
    mesh.position.set(node.pos[0], node.pos[1], node.pos[2]);
    scene.add(mesh);
    const halo = new THREE.Mesh(
      new THREE.SphereGeometry(0.55, 20, 20),
      new THREE.MeshBasicMaterial({
        color: node.color,
        transparent: true,
        opacity: 0.38,
        depthWrite: false,
        blending: THREE.AdditiveBlending,
      })
    );
    halo.position.copy(mesh.position);
    scene.add(halo);
    halos.push(halo);
    const sprite = labelSprite(node.label, "#E8EDF7");
    sprite.position.set(node.pos[0], node.pos[1] + 0.42, node.pos[2]);
    scene.add(sprite);
    byId[node.id] = { mesh, sprite, color: node.color, halo };
  });
  const links = TOPOLOGY_LINKS.map((entry) => {
    const from = TOPOLOGY.find((node) => node.id === entry[0]);
    const to = TOPOLOGY.find((node) => node.id === entry[1]);
    const mesh = linkMesh(from.pos, to.pos, 0x818cf8);
    mesh.userData.from = new THREE.Vector3(from.pos[0], from.pos[1], from.pos[2]);
    mesh.userData.to = new THREE.Vector3(to.pos[0], to.pos[1], to.pos[2]);
    mesh.userData.fail = entry[2] || "";
    scene.add(mesh);
    return mesh;
  });
  const pulses = [];
  links.forEach((link, index) => {
    [0, 0.48].forEach((shift) => {
      const mesh = new THREE.Mesh(
        new THREE.SphereGeometry(0.07, 12, 12),
        new THREE.MeshBasicMaterial({
          color: 0xf8fbff,
          transparent: true,
          opacity: 0.9,
          depthWrite: false,
          blending: THREE.AdditiveBlending,
        })
      );
      mesh.userData.link = link;
      mesh.userData.shift = shift + index * 0.08;
      mesh.position.lerpVectors(link.userData.from, link.userData.to, shift || 0.5);
      scene.add(mesh);
      pulses.push(mesh);
    });
  });
  const tokenPath = new THREE.CatmullRomCurve3(
    TOPOLOGY.map((node) => new THREE.Vector3(node.pos[0], node.pos[1], node.pos[2])),
    true
  );
  const tokenCount = (host.clientWidth || 800) < 700 ? 16 : 28;
  const tokens = [];
  for (let index = 0; index < tokenCount; index += 1) {
    const mesh = new THREE.Mesh(
      new THREE.BoxGeometry(0.11, 0.045, 0.16),
      new THREE.MeshBasicMaterial({ color: index % 2 ? 0xfacc15 : 0x67e8f9 })
    );
    mesh.userData.t = index / tokenCount;
    const start = tokenPath.getPointAt(mesh.userData.t);
    mesh.position.copy(start);
    scene.add(mesh);
    tokens.push(mesh);
  }
  const orbitNames = ["token", "layer", "logit", "sample"];
  const orbitLabels = orbitNames.map((name, index) => {
    const sprite = labelSprite(name, "#67E8F9");
    sprite.scale.set(1.15, 0.29, 1);
    sprite.userData.angle = index * (Math.PI / 2);
    sprite.userData.radius = 3.35 + (index % 2) * 0.45;
    scene.add(sprite);
    return sprite;
  });
  const neurons = [];
  for (let index = 0; index < 18; index += 1) {
    const mesh = new THREE.Mesh(
      new THREE.SphereGeometry(0.055, 10, 10),
      new THREE.MeshBasicMaterial({
        color: index % 3 === 0 ? 0xe879f9 : 0x22d3ee,
        transparent: true,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
      })
    );
    const angle = (index / 18) * Math.PI * 2;
    const radius = 1.6 + (index % 5) * 0.72;
    mesh.position.set(Math.cos(angle) * radius, Math.sin(angle * 1.7) * 0.55, Math.sin(angle) * radius);
    mesh.userData.home = mesh.position.clone();
    scene.add(mesh);
    neurons.push(mesh);
  }
  const pal = scenePalette();
  const grid = new THREE.GridHelper(46, 46, pal.grid, pal.grid);
  grid.position.y = -2.35;
  scene.add(grid);
  const ringMat = new THREE.MeshBasicMaterial({
    color: pal.ring,
    transparent: true,
    opacity: 0.9,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
  });
  const rings = [0, 1, 2].map((index) => {
    const mesh = new THREE.Mesh(new THREE.TorusGeometry(2.6 + index * 0.85, 0.02, 12, 96), ringMat.clone());
    mesh.rotation.x = Math.PI / 2.2;
    mesh.rotation.y = index * 0.4;
    scene.add(mesh);
    return mesh;
  });
  const narrow = (host.clientWidth || 800) < 700;
  const count = narrow ? 520 : 1100;
  const positions = new Float32Array(count * 3);
  for (let index = 0; index < count; index += 1) {
    const depth = 2.8 + Math.random() * 12;
    const aspect = Math.random() < 0.42 ? 0.5 : 1.55;
    const ndcX = (Math.random() * 2 - 1) * 0.96;
    const ndcY = (Math.random() * 2 - 1) * 0.96;
    positions[index * 3] = ndcX * depth * HALF_FOV * aspect;
    positions[index * 3 + 1] = ndcY * depth * HALF_FOV;
    positions[index * 3 + 2] = 6.45 - depth;
  }
  const pointGeom = new THREE.BufferGeometry();
  pointGeom.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  const points = new THREE.Points(
    pointGeom,
    new THREE.PointsMaterial({
      color: pal.particles,
      size: narrow ? 0.18 : 0.26,
      transparent: true,
      opacity: 0.92,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    })
  );
  scene.add(points);
  const sparkCount = narrow ? 70 : 140;
  const sparkPos = new Float32Array(sparkCount * 3);
  for (let index = 0; index < sparkCount; index += 1) {
    const depth = 3.2 + Math.random() * 10;
    const aspect = Math.random() < 0.42 ? 0.5 : 1.55;
    const ndcX = (Math.random() * 2 - 1) * 0.94;
    const ndcY = (Math.random() * 2 - 1) * 0.94;
    sparkPos[index * 3] = ndcX * depth * HALF_FOV * aspect;
    sparkPos[index * 3 + 1] = ndcY * depth * HALF_FOV;
    sparkPos[index * 3 + 2] = 6.45 - depth;
  }
  const sparkGeom = new THREE.BufferGeometry();
  sparkGeom.setAttribute("position", new THREE.BufferAttribute(sparkPos, 3));
  const sparks = new THREE.Points(
    sparkGeom,
    new THREE.PointsMaterial({
      color: pal.ring,
      size: 0.48,
      transparent: true,
      opacity: 0.55,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    })
  );
  scene.add(sparks);
  const depthCount = narrow ? 280 : 720;
  const depthPositions = new Float32Array(depthCount * 3);
  for (let index = 0; index < depthCount; index += 1) {
    const depth = 4 + Math.random() * 11;
    const aspect = Math.random() < 0.4 ? 0.52 : 1.6;
    const ndcX = (Math.random() * 2 - 1) * 0.98;
    const ndcY = (Math.random() * 2 - 1) * 0.98;
    depthPositions[index * 3] = ndcX * depth * HALF_FOV * aspect;
    depthPositions[index * 3 + 1] = ndcY * depth * HALF_FOV;
    depthPositions[index * 3 + 2] = 6.45 - depth;
  }
  const depthGeom = new THREE.BufferGeometry();
  depthGeom.setAttribute("position", new THREE.BufferAttribute(depthPositions, 3));
  const depth = new THREE.Points(
    depthGeom,
    new THREE.PointsMaterial({
      color: pal.particles,
      size: 0.16,
      sizeAttenuation: true,
      transparent: true,
      opacity: 0.75,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    })
  );
  scene.add(depth);
  scene.fog = new THREE.Fog(pal.fog, 16, 36);
  const layers = buildDepthLayers();
  layers.forEach((group) => scene.add(group));
  renderer.setClearColor(pal.fog, 1);
  const state = {
    alive: true,
    renderer,
    scene,
    camera,
    controls,
    links,
    byId,
    host,
    grid,
    rings,
    points,
    sparks,
    depth,
    halos,
    pulses,
    tokens,
    tokenPath,
    orbitLabels,
    neurons,
    layers,
    userMoved: false,
  };
  fit(renderer, camera, host);
  bindResize(host, state);
  controls.addEventListener("start", () => {
    state.userMoved = true;
  });
  let visible = true;
  const poke = () => {
    if (!state.alive || state.raf) return;
    if (document.hidden || !visible) return;
    state.raf = requestAnimationFrame(frame);
  };
  const watcher = new IntersectionObserver((entries) => {
    visible = entries.some((entry) => entry.isIntersecting);
    poke();
  });
  watcher.observe(host);
  document.addEventListener("visibilitychange", poke);
  state.watcher = watcher;
  const reduce = motionReduced();
  const pointer = { x: 0, y: 0 };
  window.addEventListener("pointermove", (event) => {
    pointer.x = event.clientX / Math.max(1, window.innerWidth) - 0.5;
    pointer.y = event.clientY / Math.max(1, window.innerHeight) - 0.5;
  });
  const paintPalette = () => {
    const next = scenePalette();
    const themeName = document.documentElement.getAttribute("data-theme") || "neon";
    scene.fog.color.set(next.fog);
    renderer.setClearColor(next.fog, 1);
    [].concat(grid.material).forEach((mat) => {
      if (mat && mat.color) mat.color.set(next.grid);
    });
    rings.forEach((ring) => ring.material.color.set(next.ring));
    points.material.color.set(next.particles);
    sparks.material.color.set(next.ring);
    depth.material.color.set(next.particles);
    const ink = themeName === "light" ? 0x3b0764 : 0xffffff;
    Object.values(byId).forEach((node) => {
      if (node.sprite && node.sprite.material) node.sprite.material.color.set(ink);
    });
    orbitLabels.forEach((sprite) => {
      if (sprite.material) sprite.material.color.set(ink);
    });
  };
  document.addEventListener("campus-theme", paintPalette);
  paintPalette();
  const poses = [
    new THREE.Vector3(0.1, 0.35, 6.5),
    new THREE.Vector3(-1.6, 0.9, 5.8),
    new THREE.Vector3(1.7, 0.15, 5.6),
    new THREE.Vector3(0.2, 1.35, 7.1),
    new THREE.Vector3(-0.3, -0.15, 5.4),
  ];
  camera.position.set(0.2, 2.4, 11);
  let fly = reduce ? null : { from: camera.position.clone(), to: poses[0].clone(), t: 0 };
  if (reduce) {
    camera.position.copy(poses[0]);
    camera.lookAt(0, 0, -1);
  }
  document.addEventListener("campus-show", () => {
    const hash = location.hash || "#home";
    let index = 0;
    for (let i = 0; i < hash.length; i += 1) index = (index + hash.charCodeAt(i)) % poses.length;
    fly = { from: camera.position.clone(), to: poses[index].clone(), t: 0 };
    state.userMoved = false;
  });
  const clock = new THREE.Clock();
  const frame = () => {
    state.raf = 0;
    if (!state.alive) return;
    if (document.hidden || !visible) return;
    state.raf = requestAnimationFrame(frame);
    const dt = Math.min(0.05, clock.getDelta());
    const elapsed = clock.elapsedTime;
    if (!motionReduced()) {
      rings.forEach((ring, index) => {
        ring.rotation.z = elapsed * (0.18 + index * 0.05);
        ring.position.x = pointer.x * (0.35 + index * 0.08);
      });
      points.rotation.y = elapsed * 0.05;
      sparks.rotation.y = -elapsed * 0.08;
      sparks.rotation.x = pointer.y * 0.4;
      halos.forEach((halo, index) => {
        const scale = 1 + Math.sin(elapsed * 1.6 + index) * 0.16;
        halo.scale.setScalar(scale);
      });
      pulses.forEach((pulse) => {
        const link = pulse.userData.link;
        if (!link.visible) {
          pulse.visible = false;
          return;
        }
        pulse.visible = true;
        const travel = (elapsed * 0.42 + pulse.userData.shift) % 1;
        pulse.position.lerpVectors(link.userData.from, link.userData.to, travel);
        const fire = Math.sin(travel * Math.PI) ** 2;
        pulse.scale.setScalar(0.55 + fire * 1.7);
        pulse.material.opacity = 0.3 + fire * 0.7;
      });
      tokens.forEach((token) => {
        token.userData.t = (token.userData.t + dt * 0.11) % 1;
        const point = tokenPath.getPointAt(token.userData.t);
        const tangent = tokenPath.getTangentAt(token.userData.t);
        token.position.copy(point);
        token.lookAt(point.x + tangent.x, point.y + tangent.y, point.z + tangent.z);
      });
      orbitLabels.forEach((sprite, index) => {
        const angle = elapsed * (0.2 + index * 0.03) + sprite.userData.angle;
        const radius = sprite.userData.radius;
        sprite.position.set(
          Math.cos(angle) * radius,
          0.2 + Math.sin(elapsed * 0.7 + index) * 0.28,
          Math.sin(angle) * radius * 0.7
        );
      });
      neurons.forEach((neuron, index) => {
        const beat = 0.45 + Math.max(0, Math.sin(elapsed * 2.4 + index * 0.7));
        neuron.scale.setScalar(beat);
        neuron.position.copy(neuron.userData.home);
        neuron.position.y += Math.sin(elapsed * 0.6 + index) * 0.08;
      });
      depth.rotation.y = elapsed * 0.03;
      layers.forEach((group) => {
        const drift = group.userData.drift;
        group.position.x = drift.x + Math.sin(elapsed * drift.speed + drift.phase) * drift.amp;
        group.position.y = drift.y + Math.cos(elapsed * drift.speed * 0.7 + drift.phase) * drift.amp * 0.45;
        group.position.z = drift.z + Math.sin(elapsed * drift.speed * 0.5) * 0.12;
        group.rotation.y = elapsed * drift.spin;
      });
      const scrollLean = Math.min(1.2, window.scrollY / 420);
      if (fly) {
        fly.t = Math.min(1, fly.t + dt / 1.35);
        const eased = fly.t * fly.t * (3 - 2 * fly.t);
        camera.position.lerpVectors(fly.from, fly.to, eased);
        camera.position.x += pointer.x * 0.55;
        camera.position.y += -pointer.y * 0.3 + scrollLean * 0.25;
        camera.lookAt(pointer.x * 0.35, 0, -1.2);
        if (fly.t >= 1) fly = null;
      } else if (!state.userMoved) {
        camera.position.x = Math.sin(elapsed * 0.1) * 0.4 + pointer.x * 0.55;
        camera.position.y = 0.32 + Math.cos(elapsed * 0.08) * 0.16 - pointer.y * 0.28 + scrollLean * 0.22;
        camera.position.z = 6.45 + Math.sin(elapsed * 0.07) * 0.18;
        camera.lookAt(pointer.x * 0.4, -pointer.y * 0.1, -1.2);
      } else {
        controls.update();
      }
    }
    renderer.render(scene, camera);
  };
  state.render = () => renderer.render(scene, camera);
  scenes.topology = state;
  frame();
  host.querySelectorAll("[data-fail]").forEach((button) => {
    button.addEventListener("click", () => {
      const on = button.getAttribute("aria-pressed") !== "true";
      button.setAttribute("aria-pressed", on ? "true" : "false");
      setTopologyFailure(button.getAttribute("data-fail"), on);
    });
  });
  const label = host.getAttribute("data-label");
  renderer.domElement.setAttribute(
    "aria-label",
    label || "3D campus. Orbit to inspect the learner, prompt, model, retriever, tools, and eval gate."
  );
  return state;
}

export function setTopologyFailure(name, on) {
  const state = scenes.topology;
  if (!state) return;
  state.links.forEach((mesh) => {
    if (mesh.userData.fail !== name) return;
    mesh.visible = !on;
  });
  const node = state.byId[name === "eval" ? "eval" : name];
  if (node) {
    node.mesh.material.emissiveIntensity = on ? 0.05 : 0.85;
    node.mesh.material.color.set(on ? 0xfb7185 : node.color);
    node.mesh.material.emissive.set(on ? 0xfb7185 : node.color);
  }
  if (state.render) state.render();
}

function toWorld(point) {
  return new THREE.Vector3((point.x - 0.5) * 4.2, (0.5 - point.y) * 3.2, ((point.z || 0.5) - 0.5) * 3.4);
}

export function mountEmbed(host) {
  if (!host) return null;
  if (scenes.embed && scenes.embed.host === host) return scenes.embed;
  if (scenes.embed) {
    scenes.embed.alive = false;
    if (scenes.embed.raf) cancelAnimationFrame(scenes.embed.raf);
    scenes.embed.observer.disconnect();
    scenes.embed.renderer.dispose();
    scenes.embed = null;
  }
  const renderer = makeRenderer(host);
  const note = host.querySelector(".space-fallback");
  if (!renderer) {
    if (note) note.hidden = false;
    return null;
  }
  if (note) note.hidden = true;
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(46, 1, 0.1, 40);
  camera.position.set(3.2, 2.4, 4.4);
  const controls = new OrbitControls(camera, renderer.domElement);
  baseLights(scene);
  const grid = new THREE.GridHelper(6, 8, 0x2a3650, 0x1b2740);
  grid.position.y = -1.7;
  scene.add(grid);
  const points = EMBED_POINTS.map((point) => {
    const mesh = new THREE.Mesh(new THREE.SphereGeometry(0.16, 20, 20), glowMaterial(point.color));
    mesh.position.copy(toWorld(point));
    mesh.userData.home = mesh.position.clone();
    mesh.userData.id = point.id;
    scene.add(mesh);
    const sprite = labelSprite(point.id, "#E8EDF7");
    sprite.position.copy(mesh.position).add(new THREE.Vector3(0, 0.36, 0));
    sprite.userData.follow = mesh;
    scene.add(sprite);
    return { point, mesh, sprite };
  });
  const query = new THREE.Mesh(new THREE.SphereGeometry(0.2, 24, 24), glowMaterial(0xfbbf24));
  scene.add(query);
  const rays = points.map(() => {
    const geom = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3(0, 1, 0)]);
    const mat = new THREE.LineBasicMaterial({ color: 0xfbbf24, transparent: true, opacity: 0.35 });
    const line = new THREE.Line(geom, mat);
    scene.add(line);
    return line;
  });
  const state = {
    alive: true,
    renderer,
    scene,
    camera,
    controls,
    host,
    points,
    query,
    rays,
    failures: { collapse: false, miss: false, flat: false },
  };
  fit(renderer, camera, host);
  bindResize(host, state);
  startLoop(state);
  scenes.embed = state;
  renderer.domElement.setAttribute(
    "aria-label",
    "3D embedding space. Drag to orbit. The amber query moves with the sliders, and rays show cosine similarity."
  );
  renderer.domElement.addEventListener("pointerdown", (event) => onEmbedPointer(state, event));
  return state;
}

function onEmbedPointer(state, event) {
  if (!event.shiftKey && !event.altKey) return;
  const rect = state.renderer.domElement.getBoundingClientRect();
  const x = (event.clientX - rect.left) / rect.width;
  const y = (event.clientY - rect.top) / rect.height;
  const next = {
    x: Math.max(0.02, Math.min(0.98, x)),
    y: Math.max(0.02, Math.min(0.98, y)),
    z: state.query.userData.z == null ? 0.55 : state.query.userData.z,
  };
  if (typeof window.CampusEmbedDrag === "function") window.CampusEmbedDrag(next.x, next.y, next.z);
}

export function hasEmbed() {
  return Boolean(scenes.embed);
}

export function setEmbedFailure(name, on) {
  const state = scenes.embed;
  if (!state) return;
  state.failures[name] = on;
  setEmbedQuery(state.query.userData.x ?? 0.7, state.query.userData.y ?? 0.6, state.query.userData.z ?? 0.55);
}

export function setEmbedQuery(x, y, z) {
  const state = scenes.embed;
  if (!state) return;
  const query = { x, y, z: z == null ? 0.55 : z };
  state.query.userData.x = query.x;
  state.query.userData.y = query.y;
  state.query.userData.z = query.z;
  const visual = { ...query };
  if (state.failures.flat) visual.z = 0.5;
  state.query.position.copy(toWorld(visual));
  const qVec = [query.x - 0.5, query.y - 0.5, (state.failures.flat ? 0.5 : query.z) - 0.5];
  let best = -2;
  let bestId = "";
  state.points.forEach((entry, index) => {
    let pos = entry.mesh.userData.home.clone();
    if (state.failures.collapse) pos = pos.multiplyScalar(0.15);
    if (state.failures.flat) pos.z = 0;
    entry.mesh.position.copy(pos);
    entry.sprite.position.copy(pos).add(new THREE.Vector3(0, 0.36, 0));
    const point = entry.point;
    const pVec = [point.x - 0.5, point.y - 0.5, (state.failures.flat ? 0 : (point.z || 0.5) - 0.5)];
    const dot = qVec[0] * pVec[0] + qVec[1] * pVec[1] + qVec[2] * pVec[2];
    const na = Math.hypot(qVec[0], qVec[1], qVec[2]);
    const nb = Math.hypot(pVec[0], pVec[1], pVec[2]);
    const score = na < 0.04 || nb < 0.04 ? -2 : dot / (na * nb);
    if (score > best) {
      best = score;
      bestId = point.id;
    }
    const positions = state.rays[index].geometry.attributes.position;
    positions.setXYZ(0, state.query.position.x, state.query.position.y, state.query.position.z);
    positions.setXYZ(1, pos.x, pos.y, pos.z);
    positions.needsUpdate = true;
    const hot = score >= 0.75;
    state.rays[index].material.color.set(hot ? 0x34d399 : 0xfbbf24);
    state.rays[index].material.opacity = state.failures.miss && hot ? 0.05 : 0.2 + Math.max(0, score) * 0.7;
    state.rays[index].visible = !(state.failures.miss && point.id === bestId && score === best);
  });
  if (state.failures.miss) {
    state.points.forEach((entry, index) => {
      if (entry.point.id === bestId) state.rays[index].visible = false;
    });
  }
  if (state.render) state.render();
}

const GEM_COLORS = [0x22d3ee, 0xe879f9, 0xfacc15, 0xfb7185, 0x34d399, 0x818cf8];

function gemGeometry(index) {
  const kind = index % 6;
  if (kind === 0) return new THREE.TorusKnotGeometry(0.42, 0.14, 80, 12);
  if (kind === 1) return new THREE.IcosahedronGeometry(0.58, 0);
  if (kind === 2) return new THREE.OctahedronGeometry(0.62, 0);
  if (kind === 3) return new THREE.BoxGeometry(0.72, 0.72, 0.72);
  if (kind === 4) return new THREE.ConeGeometry(0.48, 0.9, 5);
  return new THREE.DodecahedronGeometry(0.55, 0);
}

export function mountCardIcons() {
  if (scenes.gems) return scenes.gems;
  const hosts = Array.from(document.querySelectorAll("[data-gem]"));
  if (!hosts.length) return null;
  const canvas = document.createElement("canvas");
  canvas.width = 160;
  canvas.height = 160;
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
  } catch (err) {
    return null;
  }
  if (!renderer.getContext()) {
    renderer.dispose();
    return null;
  }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setSize(160, 160, false);
  renderer.setClearColor(0x000000, 0);
  const items = hosts.map((host, index) => {
    const color = GEM_COLORS[index % GEM_COLORS.length];
    const local = document.createElement("canvas");
    local.className = "gem-canvas";
    local.width = 160;
    local.height = 160;
    local.setAttribute("aria-hidden", "true");
    host.appendChild(local);
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 20);
    camera.position.set(0.85, 0.7, 2.35);
    camera.lookAt(0, 0, 0);
    const mesh = new THREE.Mesh(
      gemGeometry(index),
      new THREE.MeshBasicMaterial({ color })
    );
    scene.add(mesh);
    const halo = new THREE.Mesh(
      new THREE.SphereGeometry(1.05, 20, 20),
      new THREE.MeshBasicMaterial({
        color,
        transparent: true,
        opacity: 0.28,
        depthWrite: false,
        blending: THREE.AdditiveBlending,
      })
    );
    scene.add(halo);
    const hex = `#${color.toString(16).padStart(6, "0")}`;
    return { host, scene, camera, mesh, halo, ctx: local.getContext("2d"), hex };
  });
  const state = { alive: true, renderer, items, canvas };
  const reduce = motionReduced();
  const draw = (elapsed) => {
    let painted = 0;
    items.forEach((item, index) => {
      if (!motionReduced()) {
        item.mesh.rotation.y = elapsed * 0.7 + index;
        item.mesh.rotation.x = 0.4 + Math.sin(elapsed * 0.5 + index) * 0.25;
        item.halo.scale.setScalar(1 + Math.sin(elapsed * 1.8 + index) * 0.06);
      }
      renderer.clear();
      renderer.render(item.scene, item.camera);
      const ctx = item.ctx;
      ctx.clearRect(0, 0, 160, 160);
      const glow = ctx.createRadialGradient(80, 84, 8, 80, 84, 78);
      glow.addColorStop(0, item.hex);
      glow.addColorStop(1, "transparent");
      ctx.globalAlpha = 0.55;
      ctx.fillStyle = glow;
      ctx.fillRect(0, 0, 160, 160);
      ctx.globalAlpha = 1;
      ctx.drawImage(canvas, 0, 0);
      painted += 1;
    });
    if (painted) document.documentElement.classList.add("gems-on");
  };
  const clock = new THREE.Clock();
  const frame = () => {
    state.raf = 0;
    if (!state.alive || document.hidden || motionReduced()) return;
    state.raf = requestAnimationFrame(frame);
    draw(clock.elapsedTime);
  };
  document.addEventListener("visibilitychange", () => {
    if (document.hidden || !state.alive || state.raf || motionReduced()) return;
    state.raf = requestAnimationFrame(frame);
  });
  scenes.gems = state;
  draw(0);
  if (!motionReduced()) state.raf = requestAnimationFrame(frame);
  return state;
}

window.CampusSpace = {
  mountTopology,
  mountEmbed,
  mountCardIcons,
  hasEmbed,
  setEmbedQuery,
  setEmbedFailure,
  setTopologyFailure,
};
