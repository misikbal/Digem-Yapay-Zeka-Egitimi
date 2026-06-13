import * as THREE from 'three';

// ─── Sabitler ───────────────────────────────────────────────
const WORLD_SIZE = 48;
const WORLD_HEIGHT = 32;
const BLOCK_SIZE = 1;
const GRAVITY = 25;
const JUMP_FORCE = 9;
const MOVE_SPEED = 6;
const SPRINT_MULT = 1.8;
const MOUSE_SENS = 0.002;
const REACH = 6;

const BLOCK = {
  AIR: 0,
  GRASS: 1,
  DIRT: 2,
  STONE: 3,
  WOOD: 4,
  SAND: 5,
  LEAVES: 6,
};

const BLOCK_NAMES = {
  [BLOCK.GRASS]: 'Çimen',
  [BLOCK.DIRT]: 'Toprak',
  [BLOCK.STONE]: 'Taş',
  [BLOCK.WOOD]: 'Odun',
  [BLOCK.SAND]: 'Kum',
  [BLOCK.LEAVES]: 'Yaprak',
};

const BLOCK_COLORS = {
  [BLOCK.GRASS]: { top: 0x5a9e3e, side: 0x8b6914, bottom: 0x8b6914 },
  [BLOCK.DIRT]: { top: 0x8b6914, side: 0x8b6914, bottom: 0x8b6914 },
  [BLOCK.STONE]: { top: 0x888888, side: 0x777777, bottom: 0x666666 },
  [BLOCK.WOOD]: { top: 0x8b5a2b, side: 0x6b4226, bottom: 0x8b5a2b },
  [BLOCK.SAND]: { top: 0xe6d5a8, side: 0xd4c494, bottom: 0xc4b484 },
  [BLOCK.LEAVES]: { top: 0x2d6a2d, side: 0x256025, bottom: 0x1e501e },
};

// Yüz yönleri: 0=+X, 1=-X, 2=+Y, 3=-Y, 4=+Z, 5=-Z
const FACE_NORMALS = [
  [1, 0, 0], [-1, 0, 0],
  [0, 1, 0], [0, -1, 0],
  [0, 0, 1], [0, 0, -1],
];

// ─── Gürültü (terrain) ──────────────────────────────────────
function noise2D(x, z) {
  const n = Math.sin(x * 0.08 + z * 0.06) * 0.5
    + Math.sin(x * 0.15 + 1.7) * 0.25
    + Math.cos(z * 0.12 + 2.3) * 0.25;
  return n;
}

function getHeight(x, z) {
  const base = Math.floor(noise2D(x, z) * 6 + 10);
  const hill = Math.floor(Math.abs(Math.sin(x * 0.05) * Math.cos(z * 0.05)) * 8);
  return Math.min(base + hill, WORLD_HEIGHT - 4);
}

// ─── Dünya ──────────────────────────────────────────────────
class World {
  constructor() {
    this.blocks = new Uint8Array(WORLD_SIZE * WORLD_HEIGHT * WORLD_SIZE);
    this.mesh = null;
    this.generate();
  }

  index(x, y, z) {
    return x + z * WORLD_SIZE + y * WORLD_SIZE * WORLD_SIZE;
  }

  getBlock(x, y, z) {
    if (x < 0 || x >= WORLD_SIZE || y < 0 || y >= WORLD_HEIGHT || z < 0 || z >= WORLD_SIZE) {
      return BLOCK.AIR;
    }
    return this.blocks[this.index(x, y, z)];
  }

  setBlock(x, y, z, type) {
    if (x < 0 || x >= WORLD_SIZE || y < 0 || y >= WORLD_HEIGHT || z < 0 || z >= WORLD_SIZE) {
      return;
    }
    this.blocks[this.index(x, y, z)] = type;
  }

  isSolid(x, y, z) {
    const b = this.getBlock(x, y, z);
    return b !== BLOCK.AIR;
  }

  generate() {
    for (let x = 0; x < WORLD_SIZE; x++) {
      for (let z = 0; z < WORLD_SIZE; z++) {
        const h = getHeight(x, z);
        for (let y = 0; y <= h; y++) {
          if (y === h) {
            this.setBlock(x, y, z, h < 8 ? BLOCK.SAND : BLOCK.GRASS);
          } else if (y > h - 3) {
            this.setBlock(x, y, z, BLOCK.DIRT);
          } else {
            this.setBlock(x, y, z, BLOCK.STONE);
          }
        }
      }
    }

    // Ağaçlar
    for (let i = 0; i < 30; i++) {
      const x = Math.floor(Math.random() * (WORLD_SIZE - 4)) + 2;
      const z = Math.floor(Math.random() * (WORLD_SIZE - 4)) + 2;
      const y = this.getTopBlock(x, z);
      if (y > 8 && this.getBlock(x, y, z) === BLOCK.GRASS) {
        this.plantTree(x, y + 1, z);
      }
    }
  }

  getTopBlock(x, z) {
    for (let y = WORLD_HEIGHT - 1; y >= 0; y--) {
      if (this.isSolid(x, y, z)) return y;
    }
    return -1;
  }

  plantTree(x, y, z) {
    const height = 4 + Math.floor(Math.random() * 2);
    for (let i = 0; i < height; i++) {
      this.setBlock(x, y + i, z, BLOCK.WOOD);
    }
    for (let dy = height - 2; dy <= height + 1; dy++) {
      for (let dx = -2; dx <= 2; dx++) {
        for (let dz = -2; dz <= 2; dz++) {
          if (Math.abs(dx) + Math.abs(dz) < 4 && Math.random() > 0.15) {
            if (this.getBlock(x + dx, y + dy, z + dz) === BLOCK.AIR) {
              this.setBlock(x + dx, y + dy, z + dz, BLOCK.LEAVES);
            }
          }
        }
      }
    }
  }

  buildMesh(scene) {
    if (this.mesh) {
      scene.remove(this.mesh);
      this.mesh.geometry.dispose();
      this.mesh.material.dispose();
    }

    const positions = [];
    const colors = [];
    const indices = [];
    let vertCount = 0;

    for (let x = 0; x < WORLD_SIZE; x++) {
      for (let y = 0; y < WORLD_HEIGHT; y++) {
        for (let z = 0; z < WORLD_SIZE; z++) {
          const type = this.getBlock(x, y, z);
          if (type === BLOCK.AIR) continue;

          const bc = BLOCK_COLORS[type];
          const faceColors = [bc.side, bc.side, bc.top, bc.bottom, bc.side, bc.side];

          for (let f = 0; f < 6; f++) {
            const [nx, ny, nz] = FACE_NORMALS[f];
            if (this.isSolid(x + nx, y + ny, z + nz)) continue;

            const verts = this.getFaceVertices(x, y, z, f);
            const col = new THREE.Color(faceColors[f]);

            for (const v of verts) {
              positions.push(v[0], v[1], v[2]);
              colors.push(col.r, col.g, col.b);
            }

            indices.push(
              vertCount, vertCount + 1, vertCount + 2,
              vertCount, vertCount + 2, vertCount + 3
            );
            vertCount += 4;
          }
        }
      }
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    geometry.setIndex(indices);
    geometry.computeVertexNormals();

    const material = new THREE.MeshLambertMaterial({ vertexColors: true });
    this.mesh = new THREE.Mesh(geometry, material);
    this.mesh.userData.isWorld = true;
    scene.add(this.mesh);
  }

  getFaceVertices(x, y, z, face) {
    const s = BLOCK_SIZE;
    const faces = [
      [[x+1,y,z],[x+1,y+1,z],[x+1,y+1,z+1],[x+1,y,z+1]],
      [[x,y,z+1],[x,y+1,z+1],[x,y+1,z],[x,y,z]],
      [[x,y+1,z+1],[x+1,y+1,z+1],[x+1,y+1,z],[x,y+1,z]],
      [[x,y,z],[x+1,y,z],[x+1,y,z+1],[x,y,z+1]],
      [[x,y,z+1],[x+1,y,z+1],[x+1,y+1,z+1],[x,y+1,z+1]],
      [[x+1,y,z],[x,y,z],[x,y+1,z],[x+1,y+1,z]],
    ];
    return faces[face];
  }
}

// ─── Oyuncu ─────────────────────────────────────────────────
class Player {
  constructor(camera) {
    this.camera = camera;
    this.position = new THREE.Vector3(WORLD_SIZE / 2, 20, WORLD_SIZE / 2);
    this.velocity = new THREE.Vector3();
    this.yaw = 0;
    this.pitch = 0;
    this.onGround = false;
    this.height = 1.7;
    this.radius = 0.3;
    this.selectedBlock = BLOCK.GRASS;

    this.keys = {};
    this.pointerLocked = false;

    window.addEventListener('keydown', (e) => {
      this.keys[e.code] = true;
      if (e.code.startsWith('Digit') && e.code !== 'Digit0') {
        const num = parseInt(e.code.replace('Digit', ''));
        if (num >= 1 && num <= 6) this.selectBlock(num);
      }
    });
    window.addEventListener('keyup', (e) => { this.keys[e.code] = false; });
  }

  selectBlock(num) {
    this.selectedBlock = num;
    document.querySelectorAll('.slot').forEach((s, i) => {
      s.classList.toggle('active', i === num - 1);
    });
    document.getElementById('info').textContent = `Blok: ${BLOCK_NAMES[num]}`;
  }

  update(dt, world) {
    const speed = MOVE_SPEED * (this.keys['ShiftLeft'] ? SPRINT_MULT : 1);
    const forward = new THREE.Vector3(-Math.sin(this.yaw), 0, -Math.cos(this.yaw));
    const right = new THREE.Vector3(Math.cos(this.yaw), 0, -Math.sin(this.yaw));
    const move = new THREE.Vector3();

    if (this.keys['KeyW']) move.add(forward);
    if (this.keys['KeyS']) move.sub(forward);
    if (this.keys['KeyA']) move.sub(right);
    if (this.keys['KeyD']) move.add(right);

    if (move.length() > 0) {
      move.normalize().multiplyScalar(speed * dt);
    }

    this.velocity.x = move.x;
    this.velocity.z = move.z;

    if (this.keys['Space'] && this.onGround) {
      this.velocity.y = JUMP_FORCE;
      this.onGround = false;
    }

    this.velocity.y -= GRAVITY * dt;

    this.moveWithCollision(this.velocity.clone().multiplyScalar(dt), world);

    this.camera.position.copy(this.position);
    this.camera.position.y += this.height;
    this.camera.rotation.order = 'YXZ';
    this.camera.rotation.y = this.yaw;
    this.camera.rotation.x = this.pitch;
  }

  moveWithCollision(delta, world) {
    this.position.x += delta.x;
    this.collide(world, 'x');

    this.position.z += delta.z;
    this.collide(world, 'z');

    this.onGround = false;
    this.position.y += delta.y;
    if (this.collide(world, 'y')) {
      if (delta.y < 0) {
        this.onGround = true;
        this.velocity.y = 0;
      } else {
        this.velocity.y = 0;
      }
    }

    if (this.position.y < -10) {
      this.position.set(WORLD_SIZE / 2, 25, WORLD_SIZE / 2);
      this.velocity.set(0, 0, 0);
    }
  }

  collide(world, axis) {
    const px = this.position.x;
    const py = this.position.y;
    const pz = this.position.z;
    const r = this.radius;
    const h = this.height;

    const minX = Math.floor(px - r);
    const maxX = Math.floor(px + r);
    const minY = Math.floor(py);
    const maxY = Math.floor(py + h - 0.001);
    const minZ = Math.floor(pz - r);
    const maxZ = Math.floor(pz + r);

    let collided = false;

    for (let x = minX; x <= maxX; x++) {
      for (let y = minY; y <= maxY; y++) {
        for (let z = minZ; z <= maxZ; z++) {
          if (!world.isSolid(x, y, z)) continue;

          const overlapX = Math.min(px + r, x + 1) - Math.max(px - r, x);
          const overlapY = Math.min(py + h, y + 1) - Math.max(py, y);
          const overlapZ = Math.min(pz + r, z + 1) - Math.max(pz - r, z);

          if (overlapX <= 0 || overlapY <= 0 || overlapZ <= 0) continue;

          collided = true;

          if (axis === 'x') {
            this.position.x += px < x + 0.5 ? -overlapX : overlapX;
          } else if (axis === 'z') {
            this.position.z += pz < z + 0.5 ? -overlapZ : overlapZ;
          } else if (axis === 'y') {
            const pushUp = (y + 1) - py;
            const pushDown = (py + h) - y;
            if (pushUp <= pushDown) {
              this.position.y = Math.max(this.position.y, y + 1);
            } else {
              this.position.y = Math.min(this.position.y, y - h);
            }
          }
        }
      }
    }
    return collided;
  }

  raycast(world) {
    const origin = this.camera.position.clone();
    const direction = new THREE.Vector3(0, 0, -1);
    direction.applyQuaternion(this.camera.quaternion);

    let bx = Math.floor(origin.x);
    let by = Math.floor(origin.y);
    let bz = Math.floor(origin.z);

    const stepX = direction.x > 0 ? 1 : -1;
    const stepY = direction.y > 0 ? 1 : -1;
    const stepZ = direction.z > 0 ? 1 : -1;

    const tDeltaX = direction.x !== 0 ? Math.abs(1 / direction.x) : Infinity;
    const tDeltaY = direction.y !== 0 ? Math.abs(1 / direction.y) : Infinity;
    const tDeltaZ = direction.z !== 0 ? Math.abs(1 / direction.z) : Infinity;

    let tMaxX = direction.x !== 0
      ? ((stepX > 0 ? bx + 1 : bx) - origin.x) / direction.x : Infinity;
    let tMaxY = direction.y !== 0
      ? ((stepY > 0 ? by + 1 : by) - origin.y) / direction.y : Infinity;
    let tMaxZ = direction.z !== 0
      ? ((stepZ > 0 ? bz + 1 : bz) - origin.z) / direction.z : Infinity;

    let prevX = bx, prevY = by, prevZ = bz;

    for (let i = 0; i < REACH * 2; i++) {
      if (world.isSolid(bx, by, bz)) {
        return {
          block: { x: bx, y: by, z: bz },
          place: { x: prevX, y: prevY, z: prevZ },
        };
      }

      prevX = bx; prevY = by; prevZ = bz;

      if (tMaxX < tMaxY && tMaxX < tMaxZ) {
        bx += stepX; tMaxX += tDeltaX;
      } else if (tMaxY < tMaxZ) {
        by += stepY; tMaxY += tDeltaY;
      } else {
        bz += stepZ; tMaxZ += tDeltaZ;
      }
    }
    return null;
  }
}

// ─── Oyun ───────────────────────────────────────────────────
class Game {
  constructor() {
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x87ceeb);
    this.scene.fog = new THREE.Fog(0x87ceeb, 30, 80);

    this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 200);
    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.shadowMap.enabled = true;
    document.body.appendChild(this.renderer.domElement);

    const ambient = new THREE.AmbientLight(0xffffff, 0.6);
    this.scene.add(ambient);

    const sun = new THREE.DirectionalLight(0xffffff, 0.8);
    sun.position.set(50, 80, 30);
    sun.castShadow = true;
    this.scene.add(sun);

    this.world = new World();
    this.player = new Player(this.camera);

    this.highlightBox = new THREE.Mesh(
      new THREE.BoxGeometry(1.005, 1.005, 1.005),
      new THREE.MeshBasicMaterial({ color: 0x000000, wireframe: true, transparent: true, opacity: 0.5 })
    );
    this.highlightBox.visible = false;
    this.scene.add(this.highlightBox);

    this.running = false;
    this.lastTime = 0;
    this.raycastResult = null;

    this.setupUI();
    window.addEventListener('resize', () => this.onResize());
  }

  setupUI() {
    const overlay = document.getElementById('overlay');
    const hud = document.getElementById('hud');
    const startBtn = document.getElementById('start-btn');

    startBtn.addEventListener('click', () => {
      this.renderer.domElement.requestPointerLock();
    });

    document.addEventListener('pointerlockchange', () => {
      if (document.pointerLockElement === this.renderer.domElement) {
        overlay.classList.add('hidden');
        hud.classList.remove('hidden');
        this.running = true;
        this.lastTime = performance.now();

        this.world.buildMesh(this.scene);

        const spawnY = this.world.getTopBlock(
          Math.floor(WORLD_SIZE / 2),
          Math.floor(WORLD_SIZE / 2)
        ) + 2;
        this.player.position.set(WORLD_SIZE / 2, spawnY, WORLD_SIZE / 2);

        this.loop();
      } else {
        overlay.classList.remove('hidden');
        hud.classList.add('hidden');
        this.running = false;
      }
    });

    document.addEventListener('mousemove', (e) => {
      if (!this.running) return;
      this.player.yaw -= e.movementX * MOUSE_SENS;
      this.player.pitch -= e.movementY * MOUSE_SENS;
      this.player.pitch = Math.max(-Math.PI / 2 + 0.01, Math.min(Math.PI / 2 - 0.01, this.player.pitch));
    });

    this.renderer.domElement.addEventListener('mousedown', (e) => {
      if (!this.running || !this.raycastResult) return;
      e.preventDefault();

      if (e.button === 0) {
        const { x, y, z } = this.raycastResult.block;
        this.world.setBlock(x, y, z, BLOCK.AIR);
        this.world.buildMesh(this.scene);
      } else if (e.button === 2) {
        const { x, y, z } = this.raycastResult.place;
        const px = this.player.position.x;
        const py = this.player.position.y;
        const pz = this.player.position.z;
        const dist = Math.sqrt((x + 0.5 - px) ** 2 + (y + 0.5 - py) ** 2 + (z + 0.5 - pz) ** 2);
        if (dist > 1.5) {
          this.world.setBlock(x, y, z, this.player.selectedBlock);
          this.world.buildMesh(this.scene);
        }
      }
    });

    this.renderer.domElement.addEventListener('contextmenu', (e) => e.preventDefault());
  }

  onResize() {
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }

  loop() {
    if (!this.running) return;

    const now = performance.now();
    const dt = Math.min((now - this.lastTime) / 1000, 0.05);
    this.lastTime = now;

    this.player.update(dt, this.world);

    this.raycastResult = this.player.raycast(this.world);
    if (this.raycastResult) {
      const { x, y, z } = this.raycastResult.block;
      this.highlightBox.position.set(x + 0.5, y + 0.5, z + 0.5);
      this.highlightBox.visible = true;
    } else {
      this.highlightBox.visible = false;
    }

    this.renderer.render(this.scene, this.camera);
    requestAnimationFrame(() => this.loop());
  }
}

new Game();
