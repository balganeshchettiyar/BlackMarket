import os

with open("script.js", "r", encoding="utf-8-sig") as f:
    content = f.read()

split_marker = "// 11. MAIN ANIMATION LOOP"
parts = content.split(split_marker)
if len(parts) != 2:
    print("Failed to split!")
    exit(1)

new_tail = """
// 11. CINEMATIC FX & STATE MACHINE
// ============================================================================

const CinematicFX = {
  sleep: (ms) => new Promise(r => setTimeout(r, ms)),
  get layer() { return document.getElementById('cinematic-layer'); },
  get text() { return document.getElementById('cinematic-text'); },
  
  showBlack: () => {
    CinematicFX.layer.style.display = 'flex';
    CinematicFX.layer.style.backgroundColor = '#000000';
    CinematicFX.text.innerText = '';
    CinematicFX.text.style.opacity = '0';
    CinematicFX.text.className = 'cinematic-text';
  },

  hideLayer: () => {
    CinematicFX.layer.style.backgroundColor = 'transparent';
    CinematicFX.layer.style.pointerEvents = 'none';
    CinematicFX.text.style.opacity = '0';
    setTimeout(() => { CinematicFX.layer.style.display = 'none'; }, 500);
  },

  playIntro: async () => {
    CinematicFX.showBlack();
    await CinematicFX.sleep(2500);
    
    // BLACK MARKET reveal
    CinematicFX.text.innerText = 'BLACK MARKET';
    CinematicFX.text.classList.add('fragmented');
    CinematicFX.text.style.opacity = '0.3';
    
    await CinematicFX.sleep(800);
    CinematicFX.text.classList.remove('fragmented');
    CinematicFX.text.classList.add('glitch-medium');
    CinematicFX.text.style.opacity = '0.8';
    
    await CinematicFX.sleep(300);
    CinematicFX.text.classList.remove('glitch-medium');
    CinematicFX.text.style.opacity = '1';
    
    // Hold
    await CinematicFX.sleep(4000);
    
    // Blood effect / minor distortion
    CinematicFX.text.classList.add('blood-glow');
    
    await CinematicFX.sleep(1500);
    
    // Glitch Collapse
    CinematicFX.text.classList.add('glitch-major');
    await CinematicFX.sleep(400);
    CinematicFX.text.style.opacity = '0';
    CinematicFX.text.className = 'cinematic-text';
    
    // Silence before torch
    await CinematicFX.sleep(800);
    CinematicFX.hideLayer();
  },

  playDeath: async () => {
    CinematicFX.showBlack();
    CinematicFX.layer.style.backgroundColor = 'rgba(0,0,0,0.9)';
    await CinematicFX.sleep(1000);
    
    CinematicFX.layer.style.backgroundColor = '#000000';
    CinematicFX.text.innerText = "Death can be the greatest opportunity of your life.";
    CinematicFX.text.style.fontSize = '16px';
    CinematicFX.text.classList.add('fragmented');
    CinematicFX.text.style.opacity = '0.4';
    
    await CinematicFX.sleep(500);
    CinematicFX.text.classList.remove('fragmented');
    CinematicFX.text.classList.add('glitch-micro');
    CinematicFX.text.style.opacity = '1';
    
    await CinematicFX.sleep(200);
    CinematicFX.text.classList.remove('glitch-micro');
    
    await CinematicFX.sleep(2500);
    CinematicFX.text.classList.add('glitch-medium');
    await CinematicFX.sleep(300);
    CinematicFX.text.style.opacity = '0';
    await CinematicFX.sleep(500);
    
    CinematicFX.hideLayer();
  },

  playResurrection: async () => {
    CinematicFX.showBlack();
    await CinematicFX.sleep(500);
    
    CinematicFX.text.innerText = "I'm offering you resurrection, a second life.";
    CinematicFX.text.style.fontSize = '18px';
    CinematicFX.text.classList.add('fragmented');
    CinematicFX.text.style.opacity = '0.3';
    
    await CinematicFX.sleep(400);
    CinematicFX.text.classList.remove('fragmented');
    CinematicFX.text.style.opacity = '1';
    
    await CinematicFX.sleep(2000);
    CinematicFX.text.classList.add('glitch-major');
    
    await CinematicFX.sleep(400);
    CinematicFX.text.style.opacity = '0';
    await CinematicFX.sleep(800);
    
    CinematicFX.hideLayer();
  },

  playAccessGranted: async () => {
    CinematicFX.showBlack();
    CinematicFX.layer.style.backgroundColor = 'rgba(10,0,0,0.9)';
    CinematicFX.layer.classList.add('scan-sweep');
    
    CinematicFX.text.innerText = "ACCESS GRANTED";
    CinematicFX.text.style.color = "#00ffaa";
    CinematicFX.text.style.fontSize = '24px';
    CinematicFX.text.style.opacity = '1';
    
    await CinematicFX.sleep(2000);
    CinematicFX.hideLayer();
  }
};

const appState = {
  mode: 'init', // init, intro, puzzle, dying, dead, password, success
  fuel: 0,
  maxFuel: 0,
  targetRadius: 160
};

let lastFrameTime = performance.now();
let frameCount = 0;
let lastFpsUpdateTime = performance.now();

function animate(now) {
  requestAnimationFrame(animate);

  const deltaMs = now - lastFrameTime;
  lastFrameTime = now;
  const timeSec = now * 0.001;

  frameCount++;
  if (now - lastFpsUpdateTime > 500) {
    const fps = Math.round((frameCount * 1000) / (now - lastFpsUpdateTime));
    frameCount = 0;
    lastFpsUpdateTime = now;
    if (DEBUG_MODE) {
      const fpsEl = document.getElementById('debug-fps');
      if (fpsEl) fpsEl.textContent = `${fps} FPS`;
    }
  }

  if (DEBUG_MODE) {
    const dm = document.getElementById('debug-money');
    const df = document.getElementById('debug-fuel');
    const dd = document.getElementById('debug-duration');
    const dr = document.getElementById('debug-radius');
    
    if (dm) dm.textContent = `₹${playerMoney}`;
    if (df) df.textContent = `${appState.maxFuel > 0 ? ((appState.fuel / appState.maxFuel)*100).toFixed(1) : 0}%`;
    if (dd) dd.textContent = `${appState.fuel.toFixed(1)}s / ${appState.maxFuel.toFixed(1)}s`;
    if (dr) dr.textContent = `${torch.baseRadius.toFixed(1)}px (Max: ${appState.targetRadius.toFixed(1)}px)`;

    const dnums = document.getElementById('debug-numbers');
    const dsum = document.getElementById('debug-sum');
    const dbinary = document.getElementById('debug-binary');
    if (dnums) dnums.textContent = NUMBER_CLUES.map(c => c.value).join(', ');
    if (dsum) dsum.textContent = NUMBER_SUM.toString();
    if (dbinary) dbinary.textContent = FINAL_PASSWORD;
  }

  const dpr = transform.dpr || 1;
  const viewW = transform.viewportWidth;
  const viewH = transform.viewportHeight;

  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, viewW, viewH);

  if (!isLoaded || appState.mode === 'init' || appState.mode === 'intro' || appState.mode === 'dead' || appState.mode === 'success') {
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, viewW, viewH);
    return;
  }

  // PUZZLE MODE
  if (appState.mode === 'puzzle' || appState.mode === 'dying') {
    appState.fuel -= deltaMs / 1000;
    if (appState.fuel < 0) appState.fuel = 0;

    const ratio = appState.maxFuel > 0 ? (appState.fuel / appState.maxFuel) : 0;
    const smooth = ratio * ratio * (3 - 2 * ratio);
    const mult = 0.45 + 0.55 * smooth;
    
    let finalRadius = appState.targetRadius * mult;
    let alpha = 1.0;
    
    if (ratio < 0.7) {
      alpha = 0.4 + (ratio / 0.7) * 0.6;
    }
    
    // Death flicker sequence
    if (ratio < 0.15) {
      const flickerStr = (0.15 - ratio) / 0.15;
      if (Math.random() < 0.5 * flickerStr) {
        finalRadius *= (1.0 - Math.random() * 0.4 * flickerStr);
        alpha -= Math.random() * 0.6 * flickerStr;
      }
    }
    
    torch.baseRadius = finalRadius;
    torch.alpha = Math.max(0, alpha);

    // Check if dead
    if (appState.fuel <= 0 && appState.mode === 'puzzle') {
      appState.mode = 'dying';
      triggerDeathSequence();
    }
  }

  updateTorchGeometry(timeSec);

  // If fuel is 0 and dying, torch might just be black
  if (appState.fuel <= 0) {
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, viewW, viewH);
    if (DEBUG_MODE) drawDebugCalibration(ctx);
    return;
  }

  // Draw Full Color Scene
  ctx.drawImage(
    normalImage,
    transform.offsetX,
    transform.offsetY,
    transform.renderedWidth,
    transform.renderedHeight
  );

  // Draw Clues (masked by torch)
  NUMBER_CLUES.forEach((clue, index) => {
    drawDecimalClue(ctx, clue, numberStates[index]);
  });

  // Torch Mask
  ctx.globalCompositeOperation = 'destination-in';
  ctx.filter = 'blur(25px)';
  const tAlpha = torch.alpha !== undefined ? torch.alpha : 1.0;
  ctx.fillStyle = `rgba(255, 255, 255, ${tAlpha})`;
  
  traceTorchPath(ctx);
  ctx.fill();
  
  ctx.filter = 'none';

  // Fill background
  ctx.globalCompositeOperation = 'destination-over';
  ctx.fillStyle = '#000000'; 
  ctx.fillRect(0, 0, viewW, viewH);

  // Reset for next frame
  ctx.globalCompositeOperation = 'source-over';

  if (DEBUG_MODE) {
    drawDebugCalibration(ctx);
  }
}

requestAnimationFrame(animate);
handleResize();

// ============================================================================
// 12. DOM LISTENERS & GAME LOGIC
// ============================================================================

function updateFundsDisplay() {
  const hubFunds = document.getElementById('hub-funds');
  const resFunds = document.getElementById('resurrection-funds');
  const hudMoney = document.getElementById('hud-money-display');
  
  const text = `${BLACK_MARKET_CONFIG.currencySymbol}${playerMoney}`;
  if (hubFunds) hubFunds.innerText = text;
  if (resFunds) resFunds.innerText = text;
  if (hudMoney) hudMoney.innerText = text;
}

async function triggerDeathSequence() {
  const hud = document.getElementById('hud-container');
  const pwd = document.getElementById('password-trigger-new');
  const rid = document.getElementById('btn-riddle');
  if (hud) hud.style.display = 'none';
  if (pwd) pwd.style.display = 'none';
  if (rid) rid.style.display = 'none';
  
  await CinematicFX.playDeath();
  
  appState.mode = 'dead';
  const resScreen = document.getElementById('resurrection-screen');
  if (resScreen) resScreen.style.display = 'block';
}

let marketplace;

document.addEventListener('DOMContentLoaded', async () => {
  const currentTeam = TeamService.getCurrentTeam();
  const state = await TeamService.getTeamState(currentTeam);
  playerMoney = state.money;
  
  const hudTeam = document.getElementById('hud-team-display');
  if (hudTeam) hudTeam.innerText = currentTeam.replace('_', ' ');
  
  marketplace = new Marketplace();
  updateFundsDisplay();

  // If already unlocked, show hub directly
  if (state.blackMarketUnlocked) {
      document.getElementById('scene-container').style.display = 'none';
      const uiLayer = document.getElementById('ui-layer');
      if (uiLayer) uiLayer.style.display = 'none';
      const hub = document.getElementById('black-market-hub');
      if (hub) hub.style.display = 'flex';
      appState.mode = 'success';
      return;
  }

  // START INITIAL INTRO
  appState.mode = 'intro';
  await CinematicFX.playIntro();
  
  // Initial free fuel for first exploration
  const initialDuration = 60; // 60 seconds
  appState.fuel = initialDuration;
  appState.maxFuel = initialDuration;
  appState.targetRadius = TORCH_CONFIG.minRadius + 0.3 * (TORCH_CONFIG.maxRadius - TORCH_CONFIG.minRadius);
  torch.baseRadius = appState.targetRadius;
  
  const viewW = window.innerWidth;
  const viewH = window.innerHeight;
  torch.x = viewW / 2;
  torch.y = viewH / 2;
  torch.targetX = viewW / 2;
  torch.targetY = viewH / 2;
  hasUserMovedMouse = true;
  
  const hud = document.getElementById('hud-container');
  if (hud) hud.style.display = 'flex';
  
  if (BLACK_MARKET_CONFIG.finalCode.enabled) {
    const pwd = document.getElementById('password-trigger-new');
    if (pwd) pwd.style.display = 'block';
  }
  if (BLACK_MARKET_CONFIG.riddle.enabled) {
    const rid = document.getElementById('btn-riddle');
    if (rid) rid.style.display = 'block';
  }
  
  appState.mode = 'puzzle';

  // RESURRECTION LOGIC
  const btnResurrect = document.getElementById('btn-resurrect');
  if (btnResurrect) {
    btnResurrect.addEventListener('click', async () => {
      const amount = parseInt(document.getElementById('resurrection-input').value, 10);
      const errorEl = document.getElementById('resurrection-error');
      
      if (isNaN(amount) || amount < 0) {
        errorEl.innerText = "INVALID FUNDS.";
        return;
      }
      if (amount < TORCH_CONFIG.minInvestment) {
        errorEl.innerText = `MINIMUM ${BLACK_MARKET_CONFIG.currencySymbol}${TORCH_CONFIG.minInvestment} REQUIRED.`;
        return;
      }
      
      btnResurrect.innerText = "PROCESSING...";
      btnResurrect.classList.add('processing');
      
      try {
        playerMoney = await TeamService.deductFunds(TeamService.getCurrentTeam(), amount);
        updateFundsDisplay();
      } catch (err) {
        errorEl.innerText = err.message;
        btnResurrect.innerText = "[ RESURRECT ]";
        btnResurrect.classList.remove('processing');
        return;
      }
      
      let t = (amount - TORCH_CONFIG.minInvestment) / (TORCH_CONFIG.maxInvestment - TORCH_CONFIG.minInvestment);
      t = Math.max(0, Math.min(1, t));
      
      const radius = TORCH_CONFIG.minRadius + t * (TORCH_CONFIG.maxRadius - TORCH_CONFIG.minRadius);
      const duration = TORCH_CONFIG.minDuration + t * (TORCH_CONFIG.maxDuration - TORCH_CONFIG.minDuration);
      
      appState.fuel = duration;
      appState.maxFuel = duration;
      appState.targetRadius = radius;
      torch.baseRadius = 1; // start tiny for resurrection animation
      
      document.getElementById('resurrection-screen').style.display = 'none';
      btnResurrect.innerText = "[ RESURRECT ]";
      btnResurrect.classList.remove('processing');
      
      await CinematicFX.playResurrection();
      
      appState.mode = 'puzzle';
      const hud = document.getElementById('hud-container');
      if (hud) hud.style.display = 'flex';
      
      const pwd = document.getElementById('password-trigger-new');
      if (pwd) pwd.style.display = 'block';
      
      const rid = document.getElementById('btn-riddle');
      if (rid) rid.style.display = 'block';
    });
  }

  // Password Entry Logic
  const pwdTrigger = document.getElementById('password-trigger-new');
  if (pwdTrigger) {
    pwdTrigger.addEventListener('click', () => {
      document.getElementById('password-screen').style.display = 'block';
      const hud = document.getElementById('hud-container');
      if (hud) hud.style.display = 'none';
      pwdTrigger.style.display = 'none';
      const rid = document.getElementById('btn-riddle');
      if (rid) rid.style.display = 'none';
      appState.mode = 'password';
      
      const attemptsCount = document.getElementById('code-attempts-count');
      if (attemptsCount && marketplace.teamState) {
          attemptsCount.innerText = marketplace.teamState.codeAttempts.toString().padStart(2, '0');
      }
    });
  }

  const cancelPwd = document.getElementById('btn-cancel-password');
  if (cancelPwd) {
    cancelPwd.addEventListener('click', () => {
      document.getElementById('password-screen').style.display = 'none';
      const hud = document.getElementById('hud-container');
      if (hud) hud.style.display = 'flex';
      const pwd = document.getElementById('password-trigger-new');
      if (pwd) pwd.style.display = 'block';
      if (BLACK_MARKET_CONFIG.riddle.enabled) {
        const rid = document.getElementById('btn-riddle');
        if (rid) rid.style.display = 'block';
      }
      appState.mode = 'puzzle';
    });
  }

  let isSubmitting = false;

  const submitPwd = document.getElementById('btn-submit-password');
  if (submitPwd) {
    submitPwd.addEventListener('click', async () => {
      if (isSubmitting) return;
      
      const input = document.getElementById('password-input').value.trim();
      const msgEl = document.getElementById('password-msg');
      const panel = document.getElementById('password-screen');
      
      if (input === FINAL_PASSWORD) {
        isSubmitting = true;
        msgEl.innerText = "CODE ACCEPTED";
        msgEl.style.color = "#00ffaa";
        document.getElementById('password-input').disabled = true;
        submitPwd.disabled = true;
        document.getElementById('btn-cancel-password').style.display = 'none';
        
        appState.mode = 'success';
        
        const enterMarketplace = () => {
            document.getElementById('scene-container').style.display = 'none';
            document.getElementById('ui-layer').style.display = 'none';
            document.getElementById('password-screen').style.display = 'none';
            document.getElementById('black-market-hub').style.display = 'flex';
            isSubmitting = false;
        };
        
        try {
            const unlockTask = TeamService.unlockBlackMarket(TeamService.getCurrentTeam());
            await Promise.all([
                unlockTask,
                CinematicFX.playAccessGranted()
            ]);
            marketplace.teamState = await TeamService.getTeamState(TeamService.getCurrentTeam());
        } catch (error) {
            console.error("[BLACK MARKET] Unlock animation or save failed:", error);
        } finally {
            enterMarketplace();
        }

      } else {
        msgEl.innerText = "ACCESS DENIED";
        panel.classList.remove('glitch-error');
        void panel.offsetWidth;
        panel.classList.add('glitch-error');
        
        try {
            const newAttempts = await TeamService.recordCodeAttempt(TeamService.getCurrentTeam());
            document.getElementById('code-attempts-count').innerText = newAttempts.toString().padStart(2, '0');
        } catch (err) {
            console.error("[BLACK MARKET] Failed to record code attempt", err);
        }
      }
    });
  }

  // Riddle Logic
  if (BLACK_MARKET_CONFIG.riddle.enabled) {
    const riddleText = document.getElementById('riddle-content-text');
    if (riddleText) riddleText.innerHTML = BLACK_MARKET_CONFIG.riddle.text;
  }
  
  const btnRiddle = document.getElementById('btn-riddle');
  if (btnRiddle) {
    btnRiddle.addEventListener('click', () => {
      document.getElementById('riddle-screen').style.display = 'block';
      const hud = document.getElementById('hud-container');
      if (hud) hud.style.display = 'none';
      const pwd = document.getElementById('password-trigger-new');
      if (pwd) pwd.style.display = 'none';
      btnRiddle.style.display = 'none';
      appState.mode = 'riddle';
    });
  }
  
  const closeRiddle = document.getElementById('btn-close-riddle');
  if (closeRiddle) {
    closeRiddle.addEventListener('click', () => {
      document.getElementById('riddle-screen').style.display = 'none';
      const hud = document.getElementById('hud-container');
      if (hud) hud.style.display = 'flex';
      const pwd = document.getElementById('password-trigger-new');
      if (pwd) pwd.style.display = 'block';
      const rid = document.getElementById('btn-riddle');
      if (rid) rid.style.display = 'block';
      appState.mode = 'puzzle';
    });
  }

});
"""

with open("script.js", "w", encoding="utf-8-sig") as f:
    f.write(parts[0])
    f.write(new_tail)
