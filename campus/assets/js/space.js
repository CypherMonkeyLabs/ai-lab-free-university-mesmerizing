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
  TOPOLOGY.forEach((node) => {
    const mesh = new THREE.Mesh(new THREE.SphereGeometry(0.22, 24, 24), glowMaterial(node.color));
    mesh.position.set(node.pos[0], node.pos[1], node.pos[2]);
    scene.add(mesh);
    const sprite = labelSprite(node.label, "#E8EDF7");
    sprite.position.set(node.pos[0], node.pos[1] + 0.42, node.pos[2]);
    scene.add(sprite);
    byId[node.id] = { mesh, sprite, color: node.color };
  });
  const links = TOPOLOGY_LINKS.map((entry) => {
    const from = TOPOLOGY.find((node) => node.id === entry[0]);
    const to = TOPOLOGY.find((node) => node.id === entry[1]);
    const mesh = linkMesh(from.pos, to.pos, 0x818cf8);
    mesh.userData.fail = entry[2] || "";
    scene.add(mesh);
    return mesh;
  });
  const state = { alive: true, renderer, scene, camera, controls, links, byId, host };
  fit(renderer, camera, host);
  bindResize(host, state);
  startLoop(state);
  scenes.topology = state;
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

window.CampusSpace = {
  mountTopology,
  mountEmbed,
  hasEmbed,
  setEmbedQuery,
  setEmbedFailure,
  setTopologyFailure,
};
