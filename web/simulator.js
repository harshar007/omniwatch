/**
 * Omnitrix Wearable Smartwatch Simulator - Web Edition
 * Zero-dependency Web Audio synthesizer, Canvas 2D engine, & State Machine.
 */

// --- 1. Sound Engine (Web Audio API Synthesizer) ---
class WebSoundEngine {
    constructor() {
        this.ctx = null;
        this.enabled = true;
        this.masterVolume = 0.5;
    }

    _initContext() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) {
                this.ctx = new AudioContext();
            }
        }
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    playClick() {
        if (!this.enabled) return;
        this._initContext();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(1400, now);
        osc.frequency.exponentialRampToValueAtTime(300, now + 0.04);
        gain.gain.setValueAtTime(0.3 * this.masterVolume, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.04);
    }

    playPopUp() {
        if (!this.enabled) return;
        this._initContext();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(400, now);
        osc.frequency.exponentialRampToValueAtTime(1100, now + 0.14);
        gain.gain.setValueAtTime(0.4 * this.masterVolume, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.15);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.15);
    }

    playTransform() {
        if (!this.enabled) return;
        this._initContext();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;

        // Sub bass slam
        const osc1 = this.ctx.createOscillator();
        const gain1 = this.ctx.createGain();
        osc1.type = 'sine';
        osc1.frequency.setValueAtTime(150, now);
        osc1.frequency.exponentialRampToValueAtTime(40, now + 0.5);
        gain1.gain.setValueAtTime(0.8 * this.masterVolume, now);
        gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.5);
        osc1.connect(gain1);
        gain1.connect(this.ctx.destination);
        osc1.start(now);
        osc1.stop(now + 0.5);

        // High frequency energy chord
        const osc2 = this.ctx.createOscillator();
        const gain2 = this.ctx.createGain();
        osc2.type = 'sawtooth';
        osc2.frequency.setValueAtTime(520, now);
        osc2.frequency.linearRampToValueAtTime(880, now + 0.25);
        gain2.gain.setValueAtTime(0.4 * this.masterVolume, now);
        gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.4);
        osc2.connect(gain2);
        gain2.connect(this.ctx.destination);
        osc2.start(now);
        osc2.stop(now + 0.4);
    }

    playAlarm() {
        if (!this.enabled) return;
        this._initContext();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(800, now);
        osc.frequency.setValueAtTime(600, now + 0.08);
        gain.gain.setValueAtTime(0.3 * this.masterVolume, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.16);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.16);
    }

    playRecharge() {
        if (!this.enabled) return;
        this._initContext();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(300, now);
        osc.frequency.exponentialRampToValueAtTime(950, now + 0.3);
        gain.gain.setValueAtTime(0.35 * this.masterVolume, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.3);
    }

    playRadarPing() {
        if (!this.enabled) return;
        this._initContext();
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(1800, now);
        osc.frequency.exponentialRampToValueAtTime(1200, now + 0.12);
        gain.gain.setValueAtTime(0.25 * this.masterVolume, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.12);
    }
}

// --- 2. Alien Database (18 Aliens) ---
const ALIEN_ROSTER = [
    {
        id: 1, codename: "ALIEN-01", name: "Heatblast", species: "Pyronite", homeworld: "Pyros",
        ability: "Pyrokinesis & Heat Generation", color: "#ff5500", quote: "Let's turn up the heat!",
        stats: { strength: 65, speed: 70, defense: 75, energy: 95, intellect: 60 }
    },
    {
        id: 2, codename: "ALIEN-02", name: "Diamondhead", species: "Petrosapien", homeworld: "Petropia",
        ability: "Crystalline Construct & Invulnerability", color: "#00ffff", quote: "Time to crystallize this situation!",
        stats: { strength: 80, speed: 50, defense: 95, energy: 70, intellect: 65 }
    },
    {
        id: 3, codename: "ALIEN-03", name: "XLR8", species: "Kineceleran", homeworld: "Kinet",
        ability: "Hypersonic Speed & Reflexes", color: "#00d4ff", quote: "Can't catch what you can't see!",
        stats: { strength: 45, speed: 100, defense: 55, energy: 60, intellect: 70 }
    },
    {
        id: 4, codename: "ALIEN-04", name: "Four Arms", species: "Tetramand", homeworld: "Khoros",
        ability: "Superhuman Strength & Sonic Shockwaves", color: "#ff2222", quote: "Four arms are better than two!",
        stats: { strength: 98, speed: 55, defense: 90, energy: 40, intellect: 50 }
    },
    {
        id: 5, codename: "ALIEN-05", name: "Grey Matter", species: "Galvan", homeworld: "Galvan Prime",
        ability: "Hyper-Evolutionary Intellect", color: "#a0a0a0", quote: "A battle of wits? You are utterly unarmed!",
        stats: { strength: 20, speed: 40, defense: 30, energy: 50, intellect: 100 }
    },
    {
        id: 6, codename: "ALIEN-06", name: "Upgrade", species: "Galvanic Mechamorph", homeworld: "Galvan B",
        ability: "Technological Merging & Enhancement", color: "#00ff55", quote: "Time for a technological upgrade!",
        stats: { strength: 60, speed: 65, defense: 85, energy: 90, intellect: 88 }
    },
    {
        id: 7, codename: "ALIEN-07", name: "Ripjaws", species: "Piscciss Volann", homeworld: "Piscciss",
        ability: "Underwater Mastery & Steel-Biting Jaws", color: "#20b2aa", quote: "Let's see how well you can swim!",
        stats: { strength: 75, speed: 80, defense: 65, energy: 50, intellect: 60 }
    },
    {
        id: 8, codename: "ALIEN-08", name: "Stinkfly", species: "Lepidopterran", homeworld: "Lepidopterra",
        ability: "Acrobatic Flight & Neurotoxin Muck", color: "#98fb98", quote: "Incoming aerial slime bombardment!",
        stats: { strength: 50, speed: 70, defense: 80, energy: 85, intellect: 75 }
    },
    {
        id: 9, codename: "ALIEN-09", name: "Ghostfreak", species: "Ectonurite", homeworld: "Anur Phaedos",
        ability: "Intangibility, Invisibility, & Fear Projection", color: "#e2e8f0", quote: "Boo! Did I frighten you?",
        stats: { strength: 55, speed: 85, defense: 50, energy: 75, intellect: 60 }
    },
    {
        id: 10, codename: "ALIEN-10", name: "Cannonbolt", species: "Arburian Pelarota", homeworld: "Arburia",
        ability: "Armored Sphere Kinetic Impact", color: "#ffd700", quote: "Let's roll!",
        stats: { strength: 85, speed: 80, defense: 100, energy: 45, intellect: 55 }
    },
    {
        id: 11, codename: "ALIEN-11", name: "Wildmutt", species: "Vulpimancer", homeworld: "Vulpin",
        ability: "Superhuman Senses & Thermographic Vision", color: "#ff8c00", quote: "*Feral Vulpimancer hunter roar!*",
        stats: { strength: 78, speed: 82, defense: 70, energy: 35, intellect: 45 }
    },
    {
        id: 12, codename: "ALIEN-12", name: "Swampfire", species: "Methanosian", homeworld: "Methanos",
        ability: "Methane Combustion & Plant Chlorokinesis", color: "#32cd32", quote: "Smells like victory!",
        stats: { strength: 82, speed: 65, defense: 85, energy: 90, intellect: 70 }
    },
    {
        id: 13, codename: "ALIEN-13", name: "Humungousaur", species: "Vaxasaurian", homeworld: "Terradino",
        ability: "Dinosaurian Might & Growth Amplification", color: "#8b4513", quote: "Humungousaur! Time to smash!",
        stats: { strength: 100, speed: 45, defense: 95, energy: 40, intellect: 50 }
    },
    {
        id: 14, codename: "ALIEN-14", name: "Big Chill", species: "Necrofriggian", homeworld: "Kylmyys",
        ability: "Cryokinesis & Ghostly Freezing Intangibility", color: "#00ced1", quote: "Chill out! Sub-zero freeze!",
        stats: { strength: 65, speed: 80, defense: 80, energy: 92, intellect: 75 }
    },
    {
        id: 15, codename: "ALIEN-15", name: "Echo Echo", species: "Sonorosian", homeworld: "Sonoros",
        ability: "Sonic Screams & Duplication", color: "#ffffff", quote: "Echo Echo! Hear the noise!",
        stats: { strength: 40, speed: 65, defense: 60, energy: 95, intellect: 70 }
    },
    {
        id: 16, codename: "ALIEN-16", name: "Chromastone", species: "Crystalsapien", homeworld: "Petropia",
        ability: "Ultraviolet Radiation & Energy Absorption", color: "#ba55d3", quote: "Energy absorbed and redirected!",
        stats: { strength: 85, speed: 65, defense: 90, energy: 100, intellect: 70 }
    },
    {
        id: 17, codename: "ALIEN-17", name: "Way Big", species: "To'kustar", homeworld: "Cosmic Storms",
        ability: "Cosmic Ray Projection & Colossal Mass", color: "#ff3344", quote: "Way Big! Stand down!",
        stats: { strength: 100, speed: 70, defense: 95, energy: 98, intellect: 65 }
    },
    {
        id: 18, codename: "ALIEN-18", name: "Alien X", species: "Celestialsapien", homeworld: "Forge of Creation",
        ability: "Omnipotent Reality Warping & Spacetime Control", color: "#a5b4fc", quote: "Motion carried! Reality altered.",
        stats: { strength: 100, speed: 100, defense: 100, energy: 100, intellect: 100 }
    }
];

// Generation Palettes
const GENERATIONS = {
    prototype: { name: "Prototype (Classic)", accent: "#00ff55", glow: "#70ff94", darkAccent: "#004d13", dialBg: "#050a06" },
    recalibrated: { name: "Recalibrated (AF)", accent: "#00ff88", glow: "#94ffd0", darkAccent: "#003b1e", dialBg: "#020704" },
    omniverse: { name: "Omniverse", accent: "#22ff66", glow: "#88ffaa", darkAccent: "#004415", dialBg: "#040c06" },
    albedo: { name: "Albedo (Crimson)", accent: "#ff2233", glow: "#ff7788", darkAccent: "#550009", dialBg: "#0d0204" }
};

// --- 3. Omnitrix Simulator Controller ---
class OmnitrixWebSimulator {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.sound = new WebSoundEngine();

        this.state = 'STANDBY'; // STANDBY, SELECTION, TRANSFORMING, TRANSFORMED, COOLDOWN, SDM, DNAScan
        this.currentGen = 'prototype';
        this.alienIndex = 0;
        this.popHeight = 0.0;
        this.targetPopHeight = 0.0;
        this.dialAngle = 0.0;
        this.targetDialAngle = 0.0;

        // Timers & States
        this.transformTimer = 0.0;
        this.maxTransformDuration = 15.0; // 15 seconds active
        this.rechargeTimer = 0.0;
        this.maxRechargeDuration = 8.0;
        this.sdmTimer = 10.0;
        this.isMasterControl = false;
        this.flashAlpha = 0.0;
        this.shockwaveRadius = 0.0;
        this.radarAngle = 0.0;
        this.pulsePhase = 0.0;

        // Interaction state
        this.isDragging = false;
        this.lastDragAngle = 0.0;
        this.lastClickTime = 0;

        this._setupListeners();
        this._buildRosterBar();
        this._updateUI();

        // Animation loop
        this.lastFrameTime = performance.now();
        requestAnimationFrame((t) => this._loop(t));
    }

    _setupListeners() {
        this.canvas.addEventListener('mousedown', (e) => this._onPointerDown(e));
        window.addEventListener('mousemove', (e) => this._onPointerMove(e));
        window.addEventListener('mouseup', (e) => this._onPointerUp(e));

        this.canvas.addEventListener('touchstart', (e) => this._onTouchStart(e), { passive: false });
        window.addEventListener('touchmove', (e) => this._onTouchMove(e), { passive: false });
        window.addEventListener('touchend', (e) => this._onTouchEnd(e));

        this.canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            const dir = e.deltaY > 0 ? 1 : -1;
            this.rotateDial(dir);
        }, { passive: false });

        window.addEventListener('keydown', (e) => {
            if (e.code === 'Space') {
                e.preventDefault();
                this.slamOrPop();
            } else if (e.code === 'ArrowLeft' || e.key.toLowerCase() === 'a') {
                this.rotateDial(-1);
            } else if (e.code === 'ArrowRight' || e.key.toLowerCase() === 'd') {
                this.rotateDial(1);
            } else if (e.key.toLowerCase() === 'm') {
                this.toggleMasterControl();
            } else if (e.key.toLowerCase() === 's') {
                this.triggerSelfDestruct();
            } else if (e.key.toLowerCase() === 'r') {
                this.quickRecharge();
            } else if (e.code === 'Escape') {
                this.revertToHuman();
            }
        });
    }

    _getCanvasCoords(e) {
        const rect = this.canvas.getBoundingClientRect();
        const clientX = e.clientX !== undefined ? e.clientX : (e.touches && e.touches[0] ? e.touches[0].clientX : 0);
        const clientY = e.clientY !== undefined ? e.clientY : (e.touches && e.touches[0] ? e.touches[0].clientY : 0);
        const x = (clientX - rect.left) * (this.canvas.width / rect.width);
        const y = (clientY - rect.top) * (this.canvas.height / rect.height);
        return { x, y };
    }

    _onPointerDown(e) {
        const { x, y } = this._getCanvasCoords(e);
        const cx = this.canvas.width / 2;
        const cy = this.canvas.height / 2;
        const dist = Math.hypot(x - cx, y - cy);

        // Core tap
        if (dist <= 75) {
            const now = Date.now();
            if (now - this.lastClickTime < 320) {
                // Double tap
                this.quickRecharge();
            } else {
                this.slamOrPop();
            }
            this.lastClickTime = now;
            return;
        }

        // Bezel ring drag
        if (dist > 75 && dist < 170) {
            this.isDragging = true;
            this.lastDragAngle = Math.atan2(y - cy, x - cx);
        }
    }

    _onPointerMove(e) {
        if (!this.isDragging) return;
        const { x, y } = this._getCanvasCoords(e);
        const cx = this.canvas.width / 2;
        const cy = this.canvas.height / 2;
        const angle = Math.atan2(y - cy, x - cx);
        let diff = angle - this.lastDragAngle;
        if (diff > Math.PI) diff -= Math.PI * 2;
        if (diff < -Math.PI) diff += Math.PI * 2;

        if (Math.abs(diff) > 0.32) {
            const dir = diff > 0 ? 1 : -1;
            this.rotateDial(dir);
            this.lastDragAngle = angle;
        }
    }

    _onPointerUp() {
        this.isDragging = false;
    }

    _onTouchStart(e) {
        e.preventDefault();
        this._onPointerDown(e);
    }
    _onTouchMove(e) {
        e.preventDefault();
        this._onPointerMove(e);
    }
    _onTouchEnd(e) {
        this._onPointerUp();
    }

    // --- State Actions ---
    slamOrPop() {
        if (this.state === 'STANDBY') {
            this.popUpCore();
        } else if (this.state === 'SELECTION') {
            this.slamCore();
        } else if (this.state === 'TRANSFORMED') {
            if (this.isMasterControl) {
                this.rotateDial(1);
            } else {
                this.revertToHuman();
            }
        } else if (this.state === 'COOLDOWN') {
            this.quickRecharge();
        }
    }

    popUpCore() {
        if (this.state !== 'STANDBY') return;
        this.state = 'SELECTION';
        this.targetPopHeight = 1.0;
        this.sound.playPopUp();
        this._updateUI();
    }

    slamCore() {
        if (this.state !== 'SELECTION') return;
        this.state = 'TRANSFORMING';
        this.targetPopHeight = 0.0;
        this.popHeight = 0.0;
        this.flashAlpha = 1.0;
        this.shockwaveRadius = 20.0;
        this.sound.playTransform();
        this.transformTimer = this.maxTransformDuration;
        this._updateUI();
    }

    rotateDial(direction) {
        if (this.state === 'COOLDOWN' || this.state === 'SDM') return;
        const count = ALIEN_ROSTER.length;
        this.alienIndex = (this.alienIndex + direction + count) % count;
        this.targetDialAngle += direction * (Math.PI * 2 / count);
        this.sound.playClick();
        this._updateUI();
    }

    selectAlien(index) {
        if (index < 0 || index >= ALIEN_ROSTER.length) return;
        this.alienIndex = index;
        this.targetDialAngle = index * (Math.PI * 2 / ALIEN_ROSTER.length);
        this.sound.playClick();
        this._updateUI();
    }

    revertToHuman() {
        if (this.state !== 'TRANSFORMED') return;
        this.state = 'COOLDOWN';
        this.rechargeTimer = this.maxRechargeDuration;
        this.sound.playAlarm();
        this.flashAlpha = 0.7;
        this._updateUI();
    }

    quickRecharge() {
        this.state = 'STANDBY';
        this.rechargeTimer = 0.0;
        this.targetPopHeight = 0.0;
        this.sound.playRecharge();
        this._updateUI();
    }

    toggleMasterControl() {
        this.isMasterControl = !this.isMasterControl;
        if (this.isMasterControl) {
            this.sound.playTransform();
            this.quickRecharge();
        } else {
            this.sound.playClick();
        }
        this._updateUI();
    }

    triggerSelfDestruct() {
        if (this.state === 'SDM') {
            this.state = 'STANDBY';
            this._updateUI();
            return;
        }
        this.state = 'SDM';
        this.sdmTimer = 10.0;
        this.sound.playAlarm();
        this._updateUI();
    }

    triggerDNAScan() {
        if (this.state === 'DNAScan') {
            this.state = 'STANDBY';
        } else {
            this.state = 'DNAScan';
            this.sound.playRadarPing();
        }
        this._updateUI();
    }

    setGeneration(genKey) {
        if (!GENERATIONS[genKey]) return;
        this.currentGen = genKey;
        this.sound.playClick();
        this._updateUI();
    }

    // --- Update UI Dom elements ---
    _updateUI() {
        const alien = ALIEN_ROSTER[this.alienIndex];
        const gen = GENERATIONS[this.currentGen];

        // Status badge
        const badge = document.getElementById('stateBadge');
        if (badge) {
            badge.textContent = this.state;
            badge.style.color = (this.state === 'COOLDOWN' || this.state === 'SDM') ? '#ff4444' : gen.glow;
            badge.style.borderColor = (this.state === 'COOLDOWN' || this.state === 'SDM') ? '#ff4444' : gen.accent;
        }

        // Alien dossier
        const lblName = document.getElementById('alienName');
        const lblSpecies = document.getElementById('alienSpecies');
        const lblAbility = document.getElementById('alienAbility');
        const lblQuote = document.getElementById('alienQuote');

        if (lblName) {
            lblName.textContent = `[${alien.id.toString().padStart(2, '0')}] ${alien.name.toUpperCase()}`;
            lblName.style.color = alien.color;
        }
        if (lblSpecies) lblSpecies.textContent = `Species: ${alien.species} • Homeworld: ${alien.homeworld}`;
        if (lblAbility) lblAbility.textContent = `Ability: ${alien.ability}`;
        if (lblQuote) lblQuote.textContent = `"${alien.quote}"`;

        // Update stats
        for (const [stat, val] of Object.entries(alien.stats)) {
            const bar = document.getElementById(`stat_${stat}`);
            const valLbl = document.getElementById(`val_${stat}`);
            if (bar) bar.style.width = `${val}%`;
            if (valLbl) valLbl.textContent = `${val}%`;
        }

        // Master control button state
        const btnMaster = document.getElementById('btnMaster');
        if (btnMaster) {
            if (this.isMasterControl) {
                btnMaster.classList.add('active');
                btnMaster.textContent = '👑 MASTER CONTROL: ACTIVE';
            } else {
                btnMaster.classList.remove('active');
                btnMaster.textContent = '👑 MASTER CONTROL [M]';
            }
        }

        // Highlight selected alien in roster
        document.querySelectorAll('.roster-item').forEach((item, idx) => {
            if (idx === this.alienIndex) {
                item.classList.add('selected');
                item.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
            } else {
                item.classList.remove('selected');
            }
        });
    }

    _buildRosterBar() {
        const container = document.getElementById('rosterContainer');
        if (!container) return;
        container.innerHTML = '';

        ALIEN_ROSTER.forEach((alien, idx) => {
            const btn = document.createElement('button');
            btn.className = 'roster-item';
            btn.innerHTML = `<span class="id">#${alien.id.toString().padStart(2, '0')}</span><span class="name">${alien.name}</span>`;
            btn.style.setProperty('--alien-color', alien.color);
            btn.addEventListener('click', () => this.selectAlien(idx));
            container.appendChild(btn);
        });
    }

    // --- Main Loop & Canvas Rendering ---
    _loop(now) {
        const dt = Math.min((now - this.lastFrameTime) / 1000.0, 0.1);
        this.lastFrameTime = now;

        this._update(dt);
        this._render();

        requestAnimationFrame((t) => this._loop(t));
    }

    _update(dt) {
        // Physics & smooth rotation
        this.dialAngle += (this.targetDialAngle - this.dialAngle) * 0.18;
        this.popHeight += (this.targetPopHeight - this.popHeight) * 0.22;
        this.pulsePhase = (this.pulsePhase + dt * 3.0) % (Math.PI * 2);

        // Flash decay
        if (this.flashAlpha > 0) {
            this.flashAlpha = Math.max(0, this.flashAlpha - dt * 2.2);
            if (this.flashAlpha === 0 && this.state === 'TRANSFORMING') {
                this.state = 'TRANSFORMED';
                this._updateUI();
            }
        }

        // Shockwave expansion
        if (this.shockwaveRadius > 0) {
            this.shockwaveRadius += dt * 320;
            if (this.shockwaveRadius > 260) this.shockwaveRadius = 0;
        }

        // Active transformed countdown
        if (this.state === 'TRANSFORMED' && !this.isMasterControl) {
            this.transformTimer -= dt;
            if (this.transformTimer <= 3.0 && this.transformTimer > 0) {
                if (Math.floor(this.transformTimer * 4) % 2 === 0) {
                    this.sound.playAlarm();
                }
            }
            if (this.transformTimer <= 0) {
                this.revertToHuman();
            }
        }

        // Cooldown recharging
        if (this.state === 'COOLDOWN') {
            this.rechargeTimer -= dt;
            if (this.rechargeTimer <= 0) {
                this.quickRecharge();
            }
        }

        // Self-Destruct countdown
        if (this.state === 'SDM') {
            this.sdmTimer -= dt;
            if (this.sdmTimer <= 0) {
                this.state = 'STANDBY';
                this.sound.playTransform();
                this._updateUI();
            }
        }

        // DNA Scan radar rotation
        if (this.state === 'DNAScan') {
            this.radarAngle = (this.radarAngle + dt * 4.0) % (Math.PI * 2);
        }
    }

    _render() {
        const ctx = this.ctx;
        const w = this.canvas.width;
        const h = this.canvas.height;
        const cx = w / 2;
        const cy = h / 2;
        const gen = GENERATIONS[this.currentGen];
        const isRed = (this.state === 'COOLDOWN' || this.state === 'SDM' || this.currentGen === 'albedo');
        const accent = isRed ? '#ff2233' : gen.accent;
        const glow = isRed ? '#ff7788' : gen.glow;

        ctx.clearRect(0, 0, w, h);

        // 1. Wrist Straps (Top and Bottom)
        this._drawStraps(ctx, cx, cy);

        // 2. Watch Chassis (Brushed Gunmetal / Titanium Hexagonal Case)
        this._drawCase(ctx, cx, cy, gen, accent);

        // 3. Rotating Outer Bezel
        this._drawBezel(ctx, cx, cy, accent, glow);

        // 4. Elevated 3D Pop-Up Core (Depth rendering)
        this._drawPopCore(ctx, cx, cy, gen, accent, glow, isRed);

        // 5. Hero Badge / Center Display
        this._drawCenterDisplay(ctx, cx, cy, accent, glow, isRed);

        // 6. Mode Specific Overlays (DNA Radar, Transformation Flash, Shockwave)
        this._drawOverlays(ctx, cx, cy, accent, glow);
    }

    _drawStraps(ctx, cx, cy) {
        ctx.fillStyle = '#0a0d0b';
        ctx.strokeStyle = '#18241b';
        ctx.lineWidth = 2;

        // Top strap
        ctx.fillRect(cx - 72, 0, 144, cy - 140);
        ctx.strokeRect(cx - 72, 0, 144, cy - 140);

        // Bottom strap
        ctx.fillRect(cx - 72, cy + 140, 144, this.canvas.height - (cy + 140));
        ctx.strokeRect(cx - 72, cy + 140, 144, this.canvas.height - (cy + 140));

        // Silicone ribbing grooves
        ctx.fillStyle = '#050806';
        for (let y = 20; y < cy - 145; y += 22) {
            ctx.fillRect(cx - 60, y, 120, 6);
        }
        for (let y = cy + 155; y < this.canvas.height - 20; y += 22) {
            ctx.fillRect(cx - 60, y, 120, 6);
        }
    }

    _drawCase(ctx, cx, cy, gen, accent) {
        // Metallic case drop shadow
        ctx.save();
        ctx.shadowColor = 'rgba(0, 0, 0, 0.7)';
        ctx.shadowBlur = 24;
        ctx.shadowOffsetY = 10;

        // Main chassis circle / rounded octagon
        const grad = ctx.createLinearGradient(cx - 160, cy - 160, cx + 160, cy + 160);
        grad.addColorStop(0, '#242c26');
        grad.addColorStop(0.5, '#121814');
        grad.addColorStop(1, '#0c100d');

        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(cx, cy, 160, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        // Casing rim
        ctx.strokeStyle = '#2d3b31';
        ctx.lineWidth = 3;
        ctx.stroke();

        // 4 Corner Screws
        const screwDist = 142;
        const angles = [Math.PI * 0.25, Math.PI * 0.75, Math.PI * 1.25, Math.PI * 1.75];
        angles.forEach(a => {
            const sx = cx + screwDist * Math.cos(a);
            const sy = cy + screwDist * Math.sin(a);
            ctx.fillStyle = '#18221b';
            ctx.beginPath();
            ctx.arc(sx, sy, 7, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = '#384d3e';
            ctx.lineWidth = 1.5;
            ctx.stroke();
            // Screw slot
            ctx.beginPath();
            ctx.moveTo(sx - 4, sy);
            ctx.lineTo(sx + 4, sy);
            ctx.stroke();
        });

        // Lateral mechanical pushers / side buttons
        ctx.fillStyle = '#1a221c';
        ctx.fillRect(cx + 154, cy - 24, 14, 48);
        ctx.strokeRect(cx + 154, cy - 24, 14, 48);
    }

    _drawBezel(ctx, cx, cy, accent, glow) {
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(this.dialAngle);

        // Bezel groove track
        ctx.fillStyle = '#080c09';
        ctx.beginPath();
        ctx.arc(0, 0, 134, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = '#1d2c21';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Rotational Notches
        const notches = 24;
        for (let i = 0; i < notches; i++) {
            const a = (i * Math.PI * 2) / notches;
            const isMajor = (i % 6 === 0);
            const len = isMajor ? 12 : 7;
            const r1 = 132;
            const r2 = r1 - len;

            ctx.strokeStyle = isMajor ? accent : '#2a3e30';
            ctx.lineWidth = isMajor ? 3 : 1.5;
            ctx.beginPath();
            ctx.moveTo(r1 * Math.cos(a), r1 * Math.sin(a));
            ctx.lineTo(r2 * Math.cos(a), r2 * Math.sin(a));
            ctx.stroke();
        }

        ctx.restore();
    }

    _drawPopCore(ctx, cx, cy, gen, accent, glow, isRed) {
        const elevation = this.popHeight * 28;

        // Core shadow if popped up
        if (elevation > 0) {
            ctx.save();
            ctx.shadowColor = 'rgba(0, 0, 0, 0.85)';
            ctx.shadowBlur = elevation * 1.5;
            ctx.shadowOffsetY = elevation * 1.2;
            ctx.fillStyle = '#020403';
            ctx.beginPath();
            ctx.arc(cx, cy, 102, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();

            // Cylindrical elevation walls
            const wallGrad = ctx.createLinearGradient(cx - 100, cy, cx + 100, cy);
            wallGrad.addColorStop(0, '#101712');
            wallGrad.addColorStop(0.5, '#222f25');
            wallGrad.addColorStop(1, '#0e1510');
            ctx.fillStyle = wallGrad;
            ctx.beginPath();
            ctx.arc(cx, cy - elevation * 0.5, 100, 0, Math.PI * 2);
            ctx.fill();
        }

        // Inner core dial plate
        const plateY = cy - elevation;
        const plateGrad = ctx.createRadialGradient(cx, plateY, 10, cx, plateY, 96);
        plateGrad.addColorStop(0, isRed ? '#200508' : '#08170d');
        plateGrad.addColorStop(1, '#020503');

        ctx.fillStyle = plateGrad;
        ctx.beginPath();
        ctx.arc(cx, plateY, 96, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = (this.state === 'SELECTION') ? glow : accent;
        ctx.lineWidth = 3;
        ctx.stroke();
    }

    _drawCenterDisplay(ctx, cx, cy, accent, glow, isRed) {
        const plateY = cy - (this.popHeight * 28);
        const alien = ALIEN_ROSTER[this.alienIndex];

        if (this.state === 'STANDBY') {
            // Iconic classic Omnitrix Hourglass motif
            const pulse = 0.6 + 0.4 * Math.sin(this.pulsePhase);
            ctx.fillStyle = isRed ? `rgba(255, 34, 51, ${pulse})` : `rgba(0, 255, 85, ${pulse})`;
            ctx.strokeStyle = accent;
            ctx.lineWidth = 2;

            const triSize = 64;
            // Top triangle pointing down
            ctx.beginPath();
            ctx.moveTo(cx - triSize, plateY - triSize * 0.9);
            ctx.lineTo(cx + triSize, plateY - triSize * 0.9);
            ctx.lineTo(cx, plateY);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();

            // Bottom triangle pointing up
            ctx.beginPath();
            ctx.moveTo(cx - triSize, plateY + triSize * 0.9);
            ctx.lineTo(cx + triSize, plateY + triSize * 0.9);
            ctx.lineTo(cx, plateY);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();

            // Center black ring
            ctx.fillStyle = '#050a06';
            ctx.beginPath();
            ctx.arc(cx, plateY, 18, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = accent;
            ctx.lineWidth = 2;
            ctx.stroke();

        } else if (this.state === 'SELECTION') {
            // Popped Up Alien Silhouette Silhouette
            ctx.fillStyle = glow;
            ctx.shadowColor = glow;
            ctx.shadowBlur = 18;

            // Alien index & silhouette representation
            this._drawAlienSilhouette(ctx, cx, plateY, alien);

            ctx.shadowBlur = 0;
            ctx.fillStyle = accent;
            ctx.font = 'bold 11px Consolas, monospace';
            ctx.textAlign = 'center';
            ctx.fillText(alien.name.toUpperCase(), cx, plateY + 68);

        } else if (this.state === 'TRANSFORMED') {
            // Active Hero Transformed View with Depleting Ring
            const ringRadius = 78;
            const progress = this.isMasterControl ? 1.0 : (this.transformTimer / this.maxTransformDuration);

            // Depleting countdown arc
            ctx.strokeStyle = '#18261e';
            ctx.lineWidth = 6;
            ctx.beginPath();
            ctx.arc(cx, plateY, ringRadius, 0, Math.PI * 2);
            ctx.stroke();

            ctx.strokeStyle = (progress < 0.25) ? '#ff3344' : glow;
            ctx.lineWidth = 6;
            ctx.beginPath();
            ctx.arc(cx, plateY, ringRadius, -Math.PI / 2, -Math.PI / 2 + (Math.PI * 2 * progress));
            ctx.stroke();

            // Transformed hero silhouette & emblem
            this._drawAlienSilhouette(ctx, cx, plateY - 6, alien);

            // Seconds badge
            ctx.fillStyle = '#ffffff';
            ctx.font = 'bold 12px Consolas, monospace';
            ctx.textAlign = 'center';
            const timeTxt = this.isMasterControl ? "∞ ACTIVE" : `${Math.ceil(this.transformTimer)}s`;
            ctx.fillText(timeTxt, cx, plateY + 54);

        } else if (this.state === 'COOLDOWN') {
            // Crimson Recharge Mode
            const pulse = 0.5 + 0.5 * Math.sin(this.pulsePhase * 2);
            ctx.fillStyle = `rgba(255, 34, 51, ${pulse})`;
            ctx.font = 'bold 15px Consolas, monospace';
            ctx.textAlign = 'center';
            ctx.fillText("RECHARGING", cx, plateY - 10);

            const progress = 1.0 - (this.rechargeTimer / this.maxRechargeDuration);
            ctx.fillStyle = '#22080a';
            ctx.fillRect(cx - 50, plateY + 12, 100, 10);
            ctx.fillStyle = '#ff2233';
            ctx.fillRect(cx - 50, plateY + 12, 100 * progress, 10);
            ctx.strokeStyle = '#ff5566';
            ctx.strokeRect(cx - 50, plateY + 12, 100, 10);

            ctx.font = '9px Consolas, monospace';
            ctx.fillStyle = '#ff8899';
            ctx.fillText("[TAP TWICE TO BOOST]", cx, plateY + 40);

        } else if (this.state === 'SDM') {
            // Self-Destruct Mode
            const pulse = Math.floor(Date.now() / 150) % 2 === 0;
            ctx.fillStyle = pulse ? '#ff1122' : '#ffffff';
            ctx.font = 'bold 18px Consolas, monospace';
            ctx.textAlign = 'center';
            ctx.fillText("SELF-DESTRUCT", cx, plateY - 14);
            ctx.font = 'bold 24px Consolas, monospace';
            ctx.fillText(`00:0${Math.ceil(this.sdmTimer)}`, cx, plateY + 18);
            ctx.font = '8px Consolas, monospace';
            ctx.fillStyle = '#ff8899';
            ctx.fillText("PRESS [S] TO ABORT", cx, plateY + 44);
        }
    }

    _drawAlienSilhouette(ctx, cx, cy, alien) {
        ctx.save();
        ctx.fillStyle = alien.color;
        ctx.strokeStyle = '#ffffff';

        // Custom vector stylization for each alien based on id
        const id = alien.id;
        ctx.beginPath();

        if (id === 1) { // Heatblast (Flame Head)
            ctx.arc(cx, cy - 10, 18, 0, Math.PI * 2);
            ctx.moveTo(cx - 24, cy + 28);
            ctx.quadraticCurveTo(cx, cy - 2, cx + 24, cy + 28);
            ctx.lineTo(cx + 12, cy + 34);
            ctx.lineTo(cx - 12, cy + 34);
            ctx.closePath();
            ctx.fill();
        } else if (id === 2) { // Diamondhead (Crystal Shards)
            ctx.moveTo(cx, cy - 36);
            ctx.lineTo(cx + 20, cy - 10);
            ctx.lineTo(cx + 26, cy + 22);
            ctx.lineTo(cx, cy + 36);
            ctx.lineTo(cx - 26, cy + 22);
            ctx.lineTo(cx - 20, cy - 10);
            ctx.closePath();
            ctx.fill();
        } else if (id === 3) { // XLR8 (Aerodynamic Visor)
            ctx.moveTo(cx + 28, cy - 18);
            ctx.lineTo(cx - 22, cy - 4);
            ctx.lineTo(cx - 28, cy + 18);
            ctx.lineTo(cx + 14, cy + 28);
            ctx.closePath();
            ctx.fill();
        } else if (id === 4) { // Four Arms (Quad Muscular Spikes)
            ctx.arc(cx, cy - 6, 22, 0, Math.PI * 2);
            ctx.rect(cx - 32, cy - 18, 12, 34);
            ctx.rect(cx + 20, cy - 18, 12, 34);
            ctx.fill();
        } else if (id === 5) { // Grey Matter (Large Galvan Eyes)
            ctx.arc(cx, cy + 6, 16, 0, Math.PI * 2);
            ctx.arc(cx - 16, cy - 12, 12, 0, Math.PI * 2);
            ctx.arc(cx + 16, cy - 12, 12, 0, Math.PI * 2);
            ctx.fill();
        } else { // Generic Hero Silhouette with Alien Emblem
            ctx.arc(cx, cy - 8, 20, 0, Math.PI * 2);
            ctx.rect(cx - 18, cy + 14, 36, 18);
            ctx.fill();
        }

        // Alien badge center
        ctx.fillStyle = '#050a06';
        ctx.beginPath();
        ctx.arc(cx, cy, 9, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1.5;
        ctx.stroke();

        ctx.restore();
    }

    _drawOverlays(ctx, cx, cy, accent, glow) {
        // DNA Scan radar beam
        if (this.state === 'DNAScan') {
            ctx.save();
            ctx.strokeStyle = '#ffcc00';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.lineTo(cx + 96 * Math.cos(this.radarAngle), cy + 96 * Math.sin(this.radarAngle));
            ctx.stroke();

            // Radar trail
            ctx.fillStyle = 'rgba(255, 204, 0, 0.15)';
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.arc(cx, cy, 96, this.radarAngle - 0.4, this.radarAngle);
            ctx.closePath();
            ctx.fill();
            ctx.restore();
        }

        // Shockwave ripple
        if (this.shockwaveRadius > 0) {
            ctx.strokeStyle = glow;
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.arc(cx, cy, this.shockwaveRadius, 0, Math.PI * 2);
            ctx.stroke();
        }

        // Screen Flash Explosion
        if (this.flashAlpha > 0) {
            ctx.fillStyle = (this.state === 'COOLDOWN' || this.currentGen === 'albedo')
                ? `rgba(255, 34, 51, ${this.flashAlpha})`
                : `rgba(0, 255, 85, ${this.flashAlpha})`;
            ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        }
    }
}

// Global initialization
window.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('watchCanvas');
    if (canvas) {
        window.omnitrixSim = new OmnitrixWebSimulator(canvas);
    }
});
