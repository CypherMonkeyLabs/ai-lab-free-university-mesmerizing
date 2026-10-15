/* Local Three.js scenes: campus topology and a 3D embedding space. */
import * as THREE from "../../vendor/three.module.min.js";
import { OrbitControls } from "../../vendor/OrbitControls.js";

const TOPOLOGY = [
  { id: "learner", label: "Learner", pos: [-2.4, 0.3, 0.2], color: 0x818cf8 },
  { id: "prompt", label: "Prompt", pos: [-1.0, 1.15, 0.5], color: 0xfbbf24 },
  { id: "model", label: "Model", pos: [0.15, 0.15, 0], color: 0xa5b4fc },
  { id: "retriever", label: "Retriever", pos: [1.7, 1.05, -0.7], color: 0x2dd4bf },
  { id: "tools", label: "Tools", pos: [1.85, -0.85, 0.65], color: 0xf472b6 },
  { id: "eval", label: "Eval", pos: [0.1, -1.45, 0.35], color: 0x34d399 },
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
  const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 40);
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
    mesh.userData.fail = entry[2] || "";
    scene.add(mesh);
    return mesh;
  });
  const pal = scenePalette();
  const grid = new THREE.GridHelper(16, 32, pal.grid, pal.grid);
  grid.position.y = -1.85;
  scene.add(grid);
  const ringMat = new THREE.MeshBasicMaterial({
    color: pal.ring,
    transparent: true,
    opacity: 0.9,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
  });
  const rings = [0, 1, 2].map((index) => {
    const mesh = new THREE.Mesh(new THREE.TorusGeometry(1.7 + index * 0.55, 0.018, 12, 96), ringMat.clone());
    mesh.rotation.x = Math.PI / 2.2;
    mesh.rotation.y = index * 0.4;
    scene.add(mesh);
    return mesh;
  });
  const narrow = (host.clientWidth || 800) < 700;
  const count = narrow ? 380 : 860;
  const positions = new Float32Array(count * 3);
  for (let index = 0; index < count; index += 1) {
    positions[index * 3] = (Math.random() - 0.5) * 14;
    positions[index * 3 + 1] = (Math.random() - 0.5) * 8;
    positions[index * 3 + 2] = (Math.random() - 0.5) * 12;
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
    sparkPos[index * 3] = (Math.random() - 0.5) * 10;
    sparkPos[index * 3 + 1] = (Math.random() - 0.5) * 6;
    sparkPos[index * 3 + 2] = (Math.random() - 0.5) * 8;
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
  scene.fog = new THREE.Fog(pal.fog, 7, 18);
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
    halos,
    userMoved: false,
  };
  fit(renderer, camera, host);
  bindResize(host, state);
  controls.addEventListener("start", () => {
    state.userMoved = true;
  });
  let visible = true;
  const watcher = new IntersectionObserver((entries) => {
    visible = entries.some((entry) => entry.isIntersecting);
  });
  watcher.observe(host);
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
    const ink = themeName === "light" ? 0x3b0764 : 0xffffff;
    Object.values(byId).forEach((node) => {
      if (node.sprite && node.sprite.material) node.sprite.material.color.set(ink);
    });
  };
  document.addEventListener("campus-theme", paintPalette);
  paintPalette();
  const poses = [
    new THREE.Vector3(3.4, 2.1, 4.2),
    new THREE.Vector3(-2.2, 1.35, 3.6),
    new THREE.Vector3(1.4, 2.7, 2.3),
    new THREE.Vector3(4.1, 0.7, 2.6),
    new THREE.Vector3(-0.4, 1.1, 5.4),
  ];
  camera.position.set(6.4, 3.6, 7.6);
  let fly = reduce ? null : { from: camera.position.clone(), to: poses[0].clone(), t: 0 };
  if (reduce) {
    camera.position.copy(poses[0]);
    camera.lookAt(0.1, 0.05, 0);
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
    if (!state.alive) return;
    state.raf = requestAnimationFrame(frame);
    if (!visible) return;
    const dt = clock.getDelta();
    const elapsed = clock.elapsedTime;
    if (!reduce) {
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
      const scrollLean = Math.min(1.8, window.scrollY / 360);
      if (fly) {
        fly.t = Math.min(1, fly.t + dt / 1.2);
        const eased = fly.t * fly.t * (3 - 2 * fly.t);
        camera.position.lerpVectors(fly.from, fly.to, eased);
        camera.position.x += pointer.x * 1.5;
        camera.position.y += -pointer.y * 0.9 + scrollLean * 0.85;
        camera.lookAt(0.1 + pointer.x * 0.4, 0.05, 0);
        if (fly.t >= 1) fly = null;
      } else if (!state.userMoved) {
        camera.position.x = 3.15 + Math.sin(elapsed * 0.16) * 0.85 + pointer.x * 1.7;
        camera.position.y = 1.7 + Math.cos(elapsed * 0.13) * 0.36 - pointer.y * 1.05 + scrollLean * 1.05;
        camera.position.z = 4.5 + Math.cos(elapsed * 0.11) * 0.45 - scrollLean * 0.4;
        camera.lookAt(0.1 + pointer.x * 0.45, 0.05 - pointer.y * 0.2, 0);
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
      if (!reduce) {
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
    if (!state.alive) return;
    state.raf = requestAnimationFrame(frame);
    const dt = clock.getDelta();
    draw(clock.elapsedTime || dt);
  };
  scenes.gems = state;
  draw(0);
  if (!reduce) frame();
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
