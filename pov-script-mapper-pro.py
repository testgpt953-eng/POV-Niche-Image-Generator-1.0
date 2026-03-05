<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>POV Script → Image Mapper</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:ital,wght@0,300;0,400;0,500;1,300&family=Syne:wght@700;800&display=swap');

:root {
  --bg:      #080810;
  --surf:    #0e0e18;
  --card:    #13131e;
  --card2:   #181826;
  --border:  #252535;
  --border2: #323248;
  --red:     #e63946;
  --cyan:    #4cc9f0;
  --gold:    #f4a261;
  --green:   #2dc653;
  --purple:  #7b5ea7;
  --text:    #e6e6f0;
  --muted:   #686882;
  --dim:     #3a3a55;
}

*, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }

html { scroll-behavior: smooth; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: 'DM Mono', monospace;
  min-height: 100vh;
  overflow-x: hidden;
}

/* Grid bg */
body::before {
  content:'';
  position:fixed; inset:0;
  background-image:
    linear-gradient(rgba(76,201,240,.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(76,201,240,.025) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events:none; z-index:0;
}

/* Vignette */
body::after {
  content:'';
  position:fixed; inset:0;
  background: radial-gradient(ellipse at center, transparent 40%, rgba(8,8,16,.8) 100%);
  pointer-events:none; z-index:0;
}

.wrap { max-width:1080px; margin:0 auto; padding:48px 24px 100px; position:relative; z-index:1; }

/* ── HEADER ── */
header { text-align:center; margin-bottom:56px; }

.eyebrow {
  font-size:10px; letter-spacing:.35em; text-transform:uppercase;
  color:var(--cyan); margin-bottom:14px;
  opacity:0; animation: up .5s .1s forwards;
}

h1 {
  font-family:'Bebas Neue', sans-serif;
  font-size: clamp(48px,9vw,96px);
  letter-spacing:.04em; line-height:.9;
  opacity:0; animation: up .5s .2s forwards;
}
h1 em { color:var(--red); font-style:normal; }
h1 small { color:var(--cyan); font-size:.55em; display:block; letter-spacing:.12em; margin-top:6px; }

.tagline {
  font-size:11px; color:var(--muted); margin-top:18px; letter-spacing:.05em;
  opacity:0; animation: up .5s .3s forwards;
}

/* ── SECTION LABEL ── */
.slabel {
  font-size:9px; letter-spacing:.28em; text-transform:uppercase;
  color:var(--cyan); margin-bottom:14px;
  display:flex; align-items:center; gap:10px;
}
.slabel::before { content:''; width:24px; height:1px; background:var(--cyan); flex-shrink:0; }

/* ── CARD ── */
.card {
  background:var(--card); border:1px solid var(--border);
  border-radius:4px; padding:28px; margin-bottom:18px;
  opacity:0; animation: up .55s forwards;
}
.card:nth-child(1){animation-delay:.35s}
.card:nth-child(2){animation-delay:.42s}
.card:nth-child(3){animation-delay:.49s}
.card:nth-child(4){animation-delay:.56s}

/* ── API KEY ── */
.api-strip {
  background: linear-gradient(135deg, rgba(76,201,240,.07), rgba(76,201,240,.02));
  border:1px solid rgba(76,201,240,.2);
  border-radius:4px; padding:18px 22px;
  display:flex; align-items:center; gap:18px; flex-wrap:wrap;
  margin-bottom:18px;
  opacity:0; animation: up .5s .3s forwards;
}
.api-info { flex:1; min-width:200px; }
.api-info strong { display:block; font-size:10px; letter-spacing:.2em; text-transform:uppercase; color:var(--cyan); margin-bottom:4px; }
.api-info span { font-size:11px; color:var(--muted); }
.api-info a { color:var(--cyan); text-decoration:none; border-bottom:1px solid rgba(76,201,240,.3); }
.key-row { display:flex; gap:8px; flex:2; min-width:240px; }
.key-row input {
  flex:1; background:var(--surf); border:1px solid rgba(76,201,240,.25);
  border-radius:3px; color:var(--text); font-family:'DM Mono',monospace;
  font-size:12px; padding:9px 14px; outline:none; transition:border-color .2s;
}
.key-row input:focus { border-color:var(--cyan); }
.btn-key {
  padding:9px 16px; background:rgba(76,201,240,.12);
  border:1px solid rgba(76,201,240,.3); border-radius:3px;
  color:var(--cyan); font-family:'DM Mono',monospace;
  font-size:10px; letter-spacing:.12em; text-transform:uppercase;
  cursor:pointer; white-space:nowrap; transition:all .2s;
}
.btn-key:hover { background:var(--cyan); color:var(--bg); }
.key-status { font-size:10px; margin-top:5px; letter-spacing:.1em; }
.key-status.ok  { color:var(--green); }
.key-status.bad { color:var(--red); }

/* ── GRID 2 COL ── */
.g2 { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
.g3 { display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px; }
@media(max-width:640px){ .g2,.g3{grid-template-columns:1fr;} h1{font-size:42px;} }

/* ── FIELD ── */
.field { display:flex; flex-direction:column; gap:7px; }
.field label { font-size:10px; letter-spacing:.15em; text-transform:uppercase; color:var(--muted); }

input[type=text], input[type=password], select, textarea {
  background:var(--surf); border:1px solid var(--border2);
  border-radius:3px; color:var(--text);
  font-family:'DM Mono',monospace; font-size:12.5px;
  padding:10px 14px; outline:none; transition:border-color .2s; width:100%;
}
input:focus, select:focus, textarea:focus { border-color:var(--cyan); }
select option { background:var(--surf); }

textarea { min-height:220px; resize:vertical; line-height:1.75; }

/* ── CHARACTER TABS ── */
.char-tabs { display:flex; gap:0; margin-bottom:18px; border:1px solid var(--border2); border-radius:3px; overflow:hidden; }
.char-tab {
  flex:1; padding:10px 8px; font-family:'DM Mono',monospace;
  font-size:10px; letter-spacing:.12em; text-transform:uppercase;
  background:transparent; border:none; color:var(--muted);
  cursor:pointer; transition:all .2s; text-align:center;
}
.char-tab.active { background:var(--red); color:#fff; }
.char-tab:hover:not(.active) { background:var(--card2); color:var(--text); }

.tab-panel { display:none; }
.tab-panel.active { display:block; }

/* ── CUSTOM CHAR (reference images) ── */
.ref-upload-area {
  border:2px dashed var(--border2); border-radius:4px;
  padding:32px 20px; text-align:center;
  cursor:pointer; transition:border-color .2s, background .2s;
  position:relative;
}
.ref-upload-area:hover, .ref-upload-area.drag { border-color:var(--cyan); background:rgba(76,201,240,.04); }
.ref-upload-area input { position:absolute; inset:0; opacity:0; cursor:pointer; width:100%; }
.upload-icon { font-size:32px; margin-bottom:10px; }
.upload-text { font-size:11px; color:var(--muted); letter-spacing:.05em; line-height:1.6; }
.upload-text strong { color:var(--cyan); }

.ref-previews { display:flex; gap:10px; flex-wrap:wrap; margin-top:14px; }
.ref-preview {
  width:80px; height:80px; border-radius:3px; overflow:hidden;
  border:1px solid var(--border2); position:relative;
}
.ref-preview img { width:100%; height:100%; object-fit:cover; }
.ref-preview .rm {
  position:absolute; top:2px; right:2px;
  background:rgba(230,57,70,.85); border:none; border-radius:2px;
  color:#fff; font-size:9px; padding:1px 5px; cursor:pointer;
}

.analyze-refs-btn {
  margin-top:14px; width:100%; padding:11px;
  background:rgba(76,201,240,.1); border:1px solid rgba(76,201,240,.3);
  border-radius:3px; color:var(--cyan);
  font-family:'DM Mono',monospace; font-size:11px;
  letter-spacing:.15em; text-transform:uppercase; cursor:pointer;
  transition:all .2s;
}
.analyze-refs-btn:hover { background:var(--cyan); color:var(--bg); }
.analyze-refs-btn:disabled { opacity:.4; cursor:not-allowed; }

.char-analysis-result {
  margin-top:12px; background:var(--surf);
  border:1px solid var(--border); border-radius:3px;
  padding:14px 16px; font-size:11px; line-height:1.8; color:#b0b0cc;
  display:none;
}
.char-analysis-result.show { display:block; }

/* ── PRESET CHARS ── */
.preset-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(140px,1fr)); gap:10px; }
.preset-card {
  background:var(--surf); border:1px solid var(--border2);
  border-radius:3px; padding:14px 12px; cursor:pointer;
  transition:all .2s; text-align:center;
}
.preset-card:hover { border-color:var(--cyan); background:rgba(76,201,240,.05); }
.preset-card.selected { border-color:var(--red); background:rgba(230,57,70,.07); }
.preset-card .preset-icon { font-size:28px; margin-bottom:8px; }
.preset-card .preset-name { font-size:10px; letter-spacing:.1em; color:var(--text); text-transform:uppercase; }
.preset-card .preset-desc { font-size:9px; color:var(--muted); margin-top:4px; line-height:1.5; }

/* ── CUSTOM FIELDS ── */
.custom-char-fields { margin-top:16px; }

/* ── BIG ANALYZE BTN ── */
.btn-analyze {
  width:100%; padding:17px; background:var(--red);
  border:none; border-radius:3px; color:#fff;
  font-family:'Bebas Neue',sans-serif; font-size:24px;
  letter-spacing:.15em; cursor:pointer;
  transition:transform .15s, box-shadow .15s;
  margin-top:10px; position:relative; overflow:hidden;
}
.btn-analyze::after {
  content:''; position:absolute; inset:0;
  background:linear-gradient(135deg,rgba(255,255,255,.1),transparent 60%);
  pointer-events:none;
}
.btn-analyze:hover { transform:translateY(-2px); box-shadow:0 10px 36px rgba(230,57,70,.45); }
.btn-analyze:active { transform:translateY(0); }
.btn-analyze:disabled { opacity:.4; cursor:not-allowed; transform:none; box-shadow:none; }

/* ── LOADING ── */
.loading { display:none; text-align:center; padding:60px 0; }
.loading.on { display:block; }
.spin {
  width:40px; height:40px; margin:0 auto 20px;
  border:2px solid var(--border); border-top-color:var(--red);
  border-radius:50%; animation:spin .7s linear infinite;
}
.load-title { font-size:11px; letter-spacing:.22em; text-transform:uppercase; color:var(--muted); }
.load-step  { font-size:12px; color:var(--cyan); margin-top:9px; min-height:18px; }

/* ── ERROR ── */
.errbox {
  background:rgba(230,57,70,.07); border:1px solid rgba(230,57,70,.3);
  border-radius:3px; padding:16px 20px; font-size:12px;
  color:var(--red); display:none; margin-bottom:16px; line-height:1.7;
}
.errbox.on { display:block; }

/* ── OUTPUT ── */
#out { display:none; }
#out.on { display:block; }

.out-header {
  display:flex; align-items:center; justify-content:space-between;
  margin-bottom:24px; flex-wrap:wrap; gap:12px;
}
.out-title {
  font-family:'Bebas Neue',sans-serif; font-size:32px;
  letter-spacing:.1em; color:var(--gold);
}

.chips { display:flex; gap:8px; flex-wrap:wrap; }
.chip {
  background:var(--surf); border:1px solid var(--border);
  border-radius:2px; padding:5px 11px; font-size:10px;
  letter-spacing:.08em; color:var(--muted);
}
.chip b { color:var(--cyan); }

/* ── IMAGE CARDS ── */
.icard {
  background:var(--surf); border:1px solid var(--border);
  border-left:3px solid var(--red); border-radius:3px;
  padding:20px 22px; margin-bottom:14px;
  opacity:0; animation:up .35s forwards;
  transition:border-left-color .2s;
}
.icard:hover { border-left-color:var(--gold); }

.icard-top { display:flex; align-items:flex-start; gap:14px; margin-bottom:14px; }
.inum { font-family:'Bebas Neue',sans-serif; font-size:38px; color:var(--red); line-height:1; min-width:52px; }
.imeta { flex:1; }
.itrigger {
  font-size:10px; color:var(--muted); letter-spacing:.1em;
  text-transform:uppercase; margin-bottom:6px;
  display:flex; align-items:center; flex-wrap:wrap; gap:8px;
}
.iline {
  font-size:13px; color:var(--text); line-height:1.5;
  border-left:2px solid var(--cyan); padding-left:10px;
  font-style:italic;
}

.sec-lbl {
  font-size:9px; letter-spacing:.2em; text-transform:uppercase;
  color:var(--muted); margin:14px 0 8px;
}

.pbox {
  background:var(--bg); border:1px solid var(--border);
  border-radius:3px; padding:14px 16px; padding-right:84px;
  font-size:11.5px; line-height:1.9; color:#bebedd; position:relative;
}

.cpybtn {
  position:absolute; top:10px; right:10px;
  background:var(--dim); border:none; border-radius:2px;
  color:var(--muted); font-family:'DM Mono',monospace;
  font-size:9px; letter-spacing:.1em; padding:5px 12px;
  cursor:pointer; text-transform:uppercase; transition:all .2s;
}
.cpybtn:hover { background:var(--cyan); color:var(--bg); }
.cpybtn.ok    { background:var(--green); color:var(--bg); }

/* ── WHISK TIP BOX ── */
.whisk-tip {
  background:rgba(123,94,167,.08); border:1px solid rgba(123,94,167,.25);
  border-radius:3px; padding:14px 16px; margin-top:10px;
  font-size:11px; line-height:1.8; color:#b0a0cc; display:none;
}
.whisk-tip.show { display:block; }
.whisk-tip strong { color:#c4a8ff; font-size:10px; letter-spacing:.12em; text-transform:uppercase; }

/* ── BADGES ── */
.badge {
  display:inline-block; padding:2px 9px; border-radius:2px;
  font-size:9px; letter-spacing:.1em; text-transform:uppercase;
}
.b-ACTION     { background:rgba(230,57,70,.14);   color:var(--red);    border:1px solid rgba(230,57,70,.3); }
.b-EMOTION    { background:rgba(76,201,240,.1);   color:var(--cyan);   border:1px solid rgba(76,201,240,.25); }
.b-ESTABLISH  { background:rgba(244,162,97,.1);   color:var(--gold);   border:1px solid rgba(244,162,97,.25); }
.b-TRANSITION { background:rgba(100,100,130,.13); color:var(--muted);  border:1px solid var(--border); }

/* ── EXPORT ROW ── */
.exp-row { display:flex; gap:10px; margin-top:28px; flex-wrap:wrap; }
.btn-exp {
  flex:1; min-width:120px; padding:12px 16px;
  border:1px solid var(--border); border-radius:3px;
  background:transparent; color:var(--text);
  font-family:'DM Mono',monospace; font-size:10px;
  letter-spacing:.15em; text-transform:uppercase;
  cursor:pointer; transition:all .2s;
}
.btn-exp:hover          { background:var(--cyan);   color:var(--bg); border-color:var(--cyan); }
.btn-exp.gold           { border-color:var(--gold);  color:var(--gold); }
.btn-exp.gold:hover     { background:var(--gold);    color:var(--bg); border-color:var(--gold); }

/* ── DIVIDER ── */
.div { height:1px; background:linear-gradient(90deg,transparent,var(--border),transparent); margin:24px 0; }

/* ── ANIMS ── */
@keyframes up   { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
@keyframes spin { to{transform:rotate(360deg)} }

::-webkit-scrollbar      { width:5px; }
::-webkit-scrollbar-track{ background:var(--bg); }
::-webkit-scrollbar-thumb{ background:var(--border); border-radius:3px; }
</style>
</head>
<body>
<div class="wrap">

<!-- HEADER -->
<header>
  <div class="eyebrow">✦ POV Niche · Gemini 2.0 · Whisk Optimized</div>
  <h1>SCRIPT <em>IMAGE</em><small>MAPPER PRO</small></h1>
  <p class="tagline">Paste script → AI maps every visual moment → Get numbered prompts with full character consistency</p>
</header>

<!-- API KEY -->
<div class="api-strip">
  <div>🔑</div>
  <div class="api-info">
    <strong>Gemini API Key</strong>
    <span>Free key → <a href="https://aistudio.google.com/apikey" target="_blank">aistudio.google.com/apikey</a></span>
    <div class="key-status bad" id="keyStatus">⚠ No key saved</div>
  </div>
  <div class="key-row">
    <input type="password" id="apiKeyInput" placeholder="Paste Gemini API key (AIza...)">
    <button class="btn-key" onclick="saveKey()">Save</button>
  </div>
</div>

<!-- ① CHARACTER SETUP -->
<div class="card">
  <div class="slabel">① Character Setup</div>

  <div class="char-tabs">
    <button class="char-tab active" onclick="switchTab('preset')">🎭 Preset Characters</button>
    <button class="char-tab"        onclick="switchTab('custom')">🖼 Custom (Reference Images)</button>
    <button class="char-tab"        onclick="switchTab('manual')">✏️ Manual Description</button>
  </div>

  <!-- PRESET TAB -->
  <div class="tab-panel active" id="tab-preset">
    <div class="preset-grid" id="presetGrid"></div>
  </div>

  <!-- CUSTOM REFERENCE TAB -->
  <div class="tab-panel" id="tab-custom">
    <div class="ref-upload-area" id="uploadArea">
      <input type="file" id="refFiles" accept="image/*" multiple onchange="addRefImages(event)">
      <div class="upload-icon">📷</div>
      <div class="upload-text">
        <strong>Drop 2–4 reference images here</strong><br>
        AI will analyze them and extract your character's visual identity<br>
        <span style="font-size:10px;color:var(--dim)">Supports: JPG, PNG, WEBP</span>
      </div>
    </div>
    <div class="ref-previews" id="refPreviews"></div>
    <button class="analyze-refs-btn" id="analyzeRefsBtn" onclick="analyzeRefs()" disabled>
      🔍 Analyze References → Extract Character Identity
    </button>
    <div class="char-analysis-result" id="charAnalysisResult"></div>
  </div>

  <!-- MANUAL TAB -->
  <div class="tab-panel" id="tab-manual">
    <div class="g2" style="margin-bottom:12px">
      <div class="field">
        <label>Hair Style & Color</label>
        <input type="text" id="m_hair" placeholder="e.g. short brown hair, side-swept">
      </div>
      <div class="field">
        <label>Face Style</label>
        <select id="m_face">
          <option value="white blank oval face, dot eyes, simple line mouth (faceless POV style)">Faceless — White Oval (POV Default)</option>
          <option value="simple cartoon face, minimal features, dot eyes, small nose">Simple Cartoon Face</option>
          <option value="semi-detailed cartoon face, expressive eyes, defined jawline">Semi-Detailed Cartoon</option>
          <option value="realistic face, detailed features, photorealistic">Realistic</option>
        </select>
      </div>
      <div class="field">
        <label>Skin Tone</label>
        <select id="m_skin">
          <option value="white/pale skin">White / Pale</option>
          <option value="light tan skin">Light Tan</option>
          <option value="medium brown skin">Medium Brown</option>
          <option value="dark brown skin">Dark Brown</option>
          <option value="East Asian skin tone">East Asian</option>
          <option value="South Asian skin tone">South Asian</option>
        </select>
      </div>
      <div class="field">
        <label>Build / Height</label>
        <select id="m_build">
          <option value="average height, slim build">Average / Slim</option>
          <option value="tall, athletic build">Tall / Athletic</option>
          <option value="short, compact build">Short / Compact</option>
          <option value="muscular, broad-shouldered">Muscular</option>
        </select>
      </div>
    </div>
    <div class="field">
      <label>Default Outfit</label>
      <select id="m_outfit">
        <option value="light blue short-sleeve shirt, dark navy jeans, brown sneakers">Blue Shirt + Dark Jeans (Civilian)</option>
        <option value="navy blue tactical zip jacket, gray cargo pants, black combat boots">Navy Tactical Jacket + Cargo Pants (Agent)</option>
        <option value="olive green blazer, beige dress shirt, brown leather shoes">Olive Suit (Detective / Official)</option>
        <option value="all-black military tactical vest, black pants, black boots">All-Black Military Tactical</option>
        <option value="dark gray hoodie, black jeans, white sneakers">Dark Hoodie + Black Jeans</option>
        <option value="white lab coat over blue shirt, dark pants">Lab Coat (Scientist / Doctor)</option>
        <option value="black turtleneck, dark trousers, leather shoes">Black Turtleneck (Corporate / Spy)</option>
      </select>
    </div>
    <div class="field" style="margin-top:12px">
      <label>Extra Details (optional)</label>
      <input type="text" id="m_extra" placeholder="e.g. scar on left cheek, glasses, beard, tattoo on neck...">
    </div>
  </div>
</div>

<!-- ② SCENE & STYLE SETTINGS -->
<div class="card">
  <div class="slabel">② Scene & Style Settings</div>
  <div class="g3">
    <div class="field">
      <label>Art Style</label>
      <select id="artStyle">
        <option value="2D flat animation, clean bold black outlines, cel-shaded, muted desaturated palette, no texture on faces, cartoon illustration">Flat 2D Animation ✦ Recommended</option>
        <option value="2D animation, slightly detailed linework, cinematic lighting, muted color palette">Cinematic 2D Cartoon</option>
        <option value="simple clean cartoon, minimal shading, flat colors, clear outlines">Minimal Clean Cartoon</option>
        <option value="semi-realistic illustration, detailed shading, muted cinematic tones">Semi-Realistic Illustration</option>
        <option value="comic book style, high contrast, bold inks, halftone shadows">Comic Book Style</option>
      </select>
    </div>
    <div class="field">
      <label>Video Theme / Niche</label>
      <select id="theme">
        <option value="spy and espionage thriller">🕵️ Spy & Espionage</option>
        <option value="military and special forces">🪖 Military & Combat</option>
        <option value="crime and organized underworld">🔫 Crime & Underworld</option>
        <option value="government conspiracy and whistleblower">🏛️ Government Conspiracy</option>
        <option value="survival horror and psychological thriller">😨 Survival Thriller</option>
        <option value="corporate power and corruption">💼 Corporate Power</option>
        <option value="post-apocalyptic wasteland">☢️ Post-Apocalyptic</option>
        <option value="historical war and battlefield">⚔️ Historical War</option>
      </select>
    </div>
    <div class="field">
      <label>Target Platform</label>
      <select id="platform">
        <option value="whisk">🎨 Google Whisk</option>
        <option value="midjourney">Midjourney</option>
        <option value="leonardo">Leonardo AI</option>
        <option value="ideogram">Ideogram</option>
        <option value="dalle">DALL-E / ChatGPT</option>
        <option value="generic">Generic (All platforms)</option>
      </select>
    </div>
  </div>
</div>

<!-- ③ SCRIPT INPUT -->
<div class="card">
  <div class="slabel">③ Paste Your POV Script</div>
  <textarea id="scriptInput" placeholder="Paste your full POV script here...

Example:
You wake up in a cold, grey room. No windows. No door handles on the inside. You remember last night — the USB drive, the man in the black coat, the alley behind the embassy...

You check your pockets. Empty. But then you notice something scratched into the concrete floor beneath your feet. Coordinates. And a name you recognize.

Your handler's name."></textarea>
  <button class="btn-analyze" id="analyzeBtn" onclick="analyzeScript()">
    ▶ ANALYZE SCRIPT — GENERATE IMAGE MAP
  </button>
</div>

<!-- ERROR -->
<div class="errbox" id="errBox"></div>

<!-- LOADING -->
<div class="loading" id="loadBox">
  <div class="spin"></div>
  <div class="load-title">Gemini is analyzing your script</div>
  <div class="load-step" id="loadStep">Reading narrative structure...</div>
</div>

<!-- OUTPUT -->
<div id="out">
  <div class="out-header">
    <div class="out-title">📋 IMAGE MAPPING SHEET</div>
    <div class="chips" id="chips"></div>
  </div>
  <div id="icards"></div>
  <div class="exp-row">
    <button class="btn-exp gold" onclick="exportTxt()">⬇ Export .txt</button>
    <button class="btn-exp"      onclick="copyAll()">⎘ Copy All Prompts</button>
    <button class="btn-exp"      onclick="resetTool()">↺ New Script</button>
  </div>
</div>

</div><!-- /wrap -->

<script>
// ═══════════════════════════════════════════════════════════════
// PRESET CHARACTERS
// ═══════════════════════════════════════════════════════════════
const PRESETS = [
  {
    id:'default-agent',
    icon:'🕵️',
    name:'Default Agent',
    desc:'Brown hair, blue shirt, civilian look',
    anchor:'protagonist: white blank oval face, small dot eyes, simple line mouth, short brown hair, wearing light blue short-sleeve shirt and dark navy jeans, average height slim build, white hands, consistent character design throughout'
  },
  {
    id:'tactical-operator',
    icon:'🪖',
    name:'Tactical Operator',
    desc:'Black hair, navy tactical gear',
    anchor:'protagonist: white blank oval face, small dot eyes, simple line mouth, short black hair, wearing navy blue tactical zip jacket and gray cargo pants with black combat boots, athletic build, white hands, consistent character design throughout'
  },
  {
    id:'detective',
    icon:'🔍',
    name:'Detective',
    desc:'Dark slicked hair, olive suit',
    anchor:'protagonist: white blank oval face, small dot eyes, simple line mouth, dark slicked-back hair, wearing olive green blazer over beige dress shirt with brown leather shoes, medium build, white hands, consistent character design throughout'
  },
  {
    id:'rebel',
    icon:'🔥',
    name:'Street Rebel',
    desc:'Spiky dark hair, dark hoodie',
    anchor:'protagonist: white blank oval face, small dot eyes, simple line mouth, dark spiky hair, wearing dark gray hoodie and black jeans with white sneakers, slim build, white hands, consistent character design throughout'
  },
  {
    id:'soldier',
    icon:'⚔️',
    name:'Soldier',
    desc:'Buzz cut, all-black military',
    anchor:'protagonist: white blank oval face, small dot eyes, simple line mouth, military buzz cut brown hair, wearing all-black tactical military vest and pants with black combat boots, muscular broad build, white hands, consistent character design throughout'
  },
  {
    id:'executive',
    icon:'💼',
    name:'Corporate',
    desc:'Neat hair, black turtleneck',
    anchor:'protagonist: white blank oval face, small dot eyes, simple line mouth, neatly combed black hair, wearing black turtleneck and dark trousers with leather shoes, tall slim build, white hands, consistent character design throughout'
  },
];

let selectedPreset = PRESETS[0];
let refImages = [];         // base64 strings
let charAnalysisText = '';  // from Gemini vision
let allResults = [];
let activeTab = 'preset';

// ── render presets ──
function renderPresets() {
  const grid = document.getElementById('presetGrid');
  grid.innerHTML = PRESETS.map(p => `
    <div class="preset-card ${p.id===selectedPreset.id?'selected':''}" onclick="selectPreset('${p.id}')">
      <div class="preset-icon">${p.icon}</div>
      <div class="preset-name">${p.name}</div>
      <div class="preset-desc">${p.desc}</div>
    </div>
  `).join('');
}

function selectPreset(id) {
  selectedPreset = PRESETS.find(p=>p.id===id) || PRESETS[0];
  renderPresets();
}

renderPresets();

// ─── TABS ───────────────────────────────────────────────────────
function switchTab(name) {
  activeTab = name;
  document.querySelectorAll('.char-tab').forEach((t,i)=>{
    const tabs = ['preset','custom','manual'];
    t.classList.toggle('active', tabs[i]===name);
  });
  document.querySelectorAll('.tab-panel').forEach(p=>p.classList.remove('active'));
  document.getElementById('tab-'+name).classList.add('active');
}

// ─── REFERENCE IMAGES ───────────────────────────────────────────
function addRefImages(e) {
  const files = Array.from(e.target.files);
  files.forEach(file => {
    const reader = new FileReader();
    reader.onload = ev => {
      refImages.push(ev.target.result); // data URL
      renderRefPreviews();
    };
    reader.readAsDataURL(file);
  });
}

function renderRefPreviews() {
  const container = document.getElementById('refPreviews');
  container.innerHTML = refImages.map((src,i)=>`
    <div class="ref-preview">
      <img src="${src}" alt="ref ${i+1}">
      <button class="rm" onclick="removeRef(${i})">✕</button>
    </div>
  `).join('');
  document.getElementById('analyzeRefsBtn').disabled = refImages.length === 0;
}

function removeRef(i) {
  refImages.splice(i,1);
  renderRefPreviews();
}

// drag-drop
const ua = document.getElementById('uploadArea');
ua.addEventListener('dragover', e=>{ e.preventDefault(); ua.classList.add('drag'); });
ua.addEventListener('dragleave', ()=>ua.classList.remove('drag'));
ua.addEventListener('drop', e=>{
  e.preventDefault(); ua.classList.remove('drag');
  const files = Array.from(e.dataTransfer.files).filter(f=>f.type.startsWith('image/'));
  files.forEach(file => {
    const r = new FileReader();
    r.onload = ev => { refImages.push(ev.target.result); renderRefPreviews(); };
    r.readAsDataURL(file);
  });
});

// ── Analyze reference images with Gemini Vision ──
async function analyzeRefs() {
  const key = getKey();
  if (!key) { showErr('Save your Gemini API key first.'); return; }
  if (refImages.length === 0) return;

  const btn = document.getElementById('analyzeRefsBtn');
  btn.disabled = true; btn.textContent = '⏳ Analyzing...';

  const parts = [
    { text: `You are a character design analyst. Analyze these ${refImages.length} reference image(s) and extract a precise, detailed visual character description suitable for text-to-image AI prompts.

Focus on:
1. Face shape and features (be very specific)
2. Hair: color, length, style, texture
3. Skin tone
4. Body type and proportions
5. Any distinctive features (scars, glasses, beard, etc.)
6. Clothing style if visible

Output a single, dense paragraph (no headings) that acts as a character anchor for image generation. Start with "protagonist:" and write it as a prompt fragment. Be precise enough that every generated image will show the same character.` }
  ];

  refImages.forEach(src => {
    const [meta, data] = src.split(',');
    const mimeType = meta.match(/:(.*?);/)[1];
    parts.push({ inline_data: { mime_type: mimeType, data } });
  });

  try {
    const res = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${key}`,
      {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ contents:[{ role:'user', parts }] })
      }
    );
    const data = await res.json();
    charAnalysisText = data?.candidates?.[0]?.content?.parts?.map(p=>p.text||'').join('') || '';
    if (!charAnalysisText) throw new Error('Empty response from Gemini');

    const box = document.getElementById('charAnalysisResult');
    box.textContent = '✓ Character extracted:\n\n' + charAnalysisText;
    box.classList.add('show');
  } catch(err) {
    showErr('Reference analysis failed: ' + err.message);
  } finally {
    btn.disabled = false;
    btn.textContent = '🔍 Re-analyze References';
  }
}

// ─── BUILD CHARACTER ANCHOR ──────────────────────────────────────
function getCharAnchor() {
  if (activeTab === 'preset') return selectedPreset.anchor;
  if (activeTab === 'custom') {
    return charAnalysisText
      ? charAnalysisText
      : 'protagonist: white blank oval face, dot eyes, brown short hair, casual outfit, consistent character design';
  }
  // manual
  const hair   = document.getElementById('m_hair').value   || 'short brown hair';
  const face   = document.getElementById('m_face').value;
  const skin   = document.getElementById('m_skin').value;
  const build  = document.getElementById('m_build').value;
  const outfit = document.getElementById('m_outfit').value;
  const extra  = document.getElementById('m_extra').value;
  return `protagonist: ${face}, ${hair}, ${skin}, ${build}, wearing ${outfit}${extra ? ', '+extra : ''}, consistent character design throughout`;
}

// ─── PLATFORM-SPECIFIC SUFFIX ────────────────────────────────────
function getPlatformSuffix(platform) {
  const s = {
    whisk:      '--style flat 2D animation --consistency high --aspect 16:9',
    midjourney: '--style raw --ar 16:9 --v 6.1 --cref [your_character_ref] --cw 100',
    leonardo:   'Leonardo style: Illustration, consistent character, aspect ratio 16:9',
    ideogram:   'Style: Illustration. Aspect: 16:9.',
    dalle:      'digital illustration, consistent character style, 16:9 aspect ratio',
    generic:    '16:9 aspect ratio, consistent character, animation style'
  };
  return s[platform] || s.generic;
}

// ─── MASTER SYSTEM PROMPT ────────────────────────────────────────
function buildSystemPrompt(charAnchor, art, theme, platform) {
  const platNote = platform === 'whisk'
    ? `\n\n## WHISK-SPECIFIC RULES:\nWhisk is a Google image AI that takes style + subject + scene as separate inputs. Structure each prompt as ONE unified description but tag sections:\n[SUBJECT]: character description\n[SCENE]: environment and action\n[STYLE]: art style and mood\nMerge them naturally but keep this structure in mind for maximum Whisk compatibility.`
    : '';

  return `You are an expert visual director for POV-style animated YouTube videos in the "${theme}" niche. Your task: analyze a script and return a precise IMAGE MAPPING SHEET as a JSON array.

## PACING INTELLIGENCE (critical):
- Do NOT place an image on every sentence — avoid slideshoweffect
- Do NOT go more than 70 words without at least one image  
- MORE images at: action sequences, location reveals, dramatic discoveries, emotional peaks, confrontations, key dialogue moments
- FEWER images at: internal monologue passages, transition narration, explanatory sections
- Smart pacing: ~1 image per 40–65 words on average, varying with dramatic intensity
- Scale: 8–14 images for 300–500 word script; 14–20 for 500–900 words

## SCENE TYPES (use exactly):
ESTABLISH — New location or situation intro
ACTION    — Physical movement, confrontation, activity  
EMOTION   — Close-up emotional reaction, internal conflict, revelation
TRANSITION— Scene change, time skip, tone shift

## CHARACTER CONSISTENCY LAW (never break):
Character anchor to use in EVERY prompt that includes the protagonist:
${charAnchor}

This character description must appear verbatim in every prompt where the protagonist is visible. Never change hair, face, outfit, or build between images.${platNote}

## PROMPT FORMULA (apply to every single image):
[ART STYLE ANCHOR] + [CHARACTER ANCHOR if visible] + [ACTION/POSE] + [ENVIRONMENT] + [LIGHTING] + [MOOD] + [CAMERA ANGLE] + [CONSISTENCY TAGS]

### ART STYLE ANCHOR (begin every prompt with):
"${art}"

### LIGHTING by scene type:
ESTABLISH  → soft ambient light, even exposure, environmental glow, natural atmosphere
ACTION     → harsh directional side-light, strong cast shadows, high contrast, dynamic
EMOTION    → single dramatic overhead spotlight, pitch black surroundings, face illuminated
TRANSITION → dim atmospheric haze, desaturated mist, soft diffuse glow, liminal space

### ENVIRONMENT STYLE:
Cold, muted, institutional or oppressive. Examples: grey concrete corridors, dark brick alleys, dimly lit government buildings, cold urban streets at night, interrogation rooms, abandoned warehouses, surveillance offices, underground bunkers.

### MANDATORY END TAGS (on every prompt):
"character consistency, same protagonist throughout, ${theme} atmosphere, cinematic composition, 16:9 widescreen"

## OUTPUT:
Return ONLY a raw JSON array. No markdown fences. No explanation. Start with [ end with ].

Schema:
{
  "image_number": <int>,
  "scene_type": "<ESTABLISH|ACTION|EMOTION|TRANSITION>",
  "script_line": "<exact phrase from script>",
  "word_count_from_start": <int>,
  "image_prompt": "<complete ready-to-use prompt>"
}`;
}

// ─── API KEY ─────────────────────────────────────────────────────
function saveKey() {
  const k = document.getElementById('apiKeyInput').value.trim();
  if (!k) { alert('Enter a key first.'); return; }
  localStorage.setItem('gmk', k);
  updateKeyStatus();
  document.getElementById('apiKeyInput').value = '';
  document.getElementById('apiKeyInput').placeholder = '✓ Key saved';
}
function getKey() { return localStorage.getItem('gmk')||''; }
function updateKeyStatus() {
  const el = document.getElementById('keyStatus');
  const k = getKey();
  el.textContent = k ? `✓ Key saved (${k.slice(0,6)}••••)` : '⚠ No key saved';
  el.className = 'key-status ' + (k ? 'ok' : 'bad');
}
updateKeyStatus();

// ─── MAIN ANALYZE ────────────────────────────────────────────────
async function analyzeScript() {
  const key = getKey();
  if (!key) { showErr('Please save your Gemini API key first.'); return; }
  const script = document.getElementById('scriptInput').value.trim();
  if (script.length < 60) { showErr('Please paste a longer script (min 60 chars).'); return; }

  const charAnchor = getCharAnchor();
  const art        = document.getElementById('artStyle').value;
  const theme      = document.getElementById('theme').value;
  const platform   = document.getElementById('platform').value;

  document.getElementById('analyzeBtn').disabled = true;
  document.getElementById('errBox').classList.remove('on');
  document.getElementById('out').classList.remove('on');
  document.getElementById('loadBox').classList.add('on');

  const steps = [
    'Reading narrative structure...',
    'Identifying dramatic peaks & pacing...',
    'Building character consistency anchors...',
    'Mapping visual moments to script...',
    'Generating text-to-image prompts...',
    'Optimizing for ' + platform + '...',
    'Finalizing mapping sheet...'
  ];
  let si=0;
  const iv = setInterval(()=>{
    if(si<steps.length) document.getElementById('loadStep').textContent=steps[si++];
  }, 1800);

  const sysPrompt = buildSystemPrompt(charAnchor, art, theme, platform);
  const userMsg   = `Analyze this POV script. Return ONLY the raw JSON array:\n\n---\n${script}\n---`;

  try {
    const res = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${key}`,
      {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({
          system_instruction: { parts:[{ text: sysPrompt }] },
          contents:[{ role:'user', parts:[{ text: userMsg }] }],
          generationConfig:{
            temperature: 0.65,
            maxOutputTokens: 8192,
            responseMimeType: 'application/json'
          }
        })
      }
    );

    clearInterval(iv);
    if (!res.ok) {
      const e = await res.json();
      throw new Error(e?.error?.message || `HTTP ${res.status}`);
    }

    const data = await res.json();
    let raw = data?.candidates?.[0]?.content?.parts?.map(p=>p.text||'').join('')||'';
    if (!raw) throw new Error('Gemini returned empty response.');

    // clean JSON
    raw = raw.trim()
      .replace(/^```json\s*/i,'').replace(/^```\s*/i,'').replace(/\s*```$/,'').trim();

    const s=raw.indexOf('['), e2=raw.lastIndexOf(']');
    if(s===-1||e2===-1) throw new Error('No JSON array found in response. Try again.');

    allResults = JSON.parse(raw.substring(s,e2+1));
    if(!Array.isArray(allResults)||allResults.length===0)
      throw new Error('Gemini returned empty list. Try a longer script.');

    renderOutput(allResults, script, platform);

  } catch(err) {
    clearInterval(iv);
    showErr('Error: '+err.message);
    console.error(err);
  } finally {
    document.getElementById('loadBox').classList.remove('on');
    document.getElementById('analyzeBtn').disabled = false;
  }
}

// ─── RENDER OUTPUT ───────────────────────────────────────────────
function renderOutput(results, script, platform) {
  const wc = script.split(/\s+/).length;
  const sc = results.reduce((a,r)=>{ a[r.scene_type]=(a[r.scene_type]||0)+1; return a; },{});

  document.getElementById('chips').innerHTML = `
    <div class="chip">Images: <b>${results.length}</b></div>
    <div class="chip">Script words: <b>${wc}</b></div>
    <div class="chip">Avg interval: <b>~${Math.round(wc/results.length)} words</b></div>
    ${Object.entries(sc).map(([k,v])=>`<div class="chip">${k}: <b>${v}</b></div>`).join('')}
  `;

  const container = document.getElementById('icards');
  container.innerHTML = '';
  const platSuffix = getPlatformSuffix(platform);
  const isWhisk = platform === 'whisk';

  results.forEach((item,i)=>{
    const fullPrompt = item.image_prompt + '\n\n' + platSuffix;
    const card = document.createElement('div');
    card.className = 'icard';
    card.style.animationDelay = `${i*.04}s`;
    card.innerHTML = `
      <div class="icard-top">
        <div class="inum">${String(item.image_number).padStart(2,'0')}</div>
        <div class="imeta">
          <div class="itrigger">
            Word ~${item.word_count_from_start||'?'}
            <span class="badge b-${item.scene_type||'TRANSITION'}">${item.scene_type||'SCENE'}</span>
          </div>
          <div class="iline">"${esc(item.script_line)}"</div>
        </div>
      </div>
      <div class="sec-lbl">▸ Text-to-Image Prompt${isWhisk?' (Whisk Optimized)':''}</div>
      <div class="pbox">
        <button class="cpybtn" onclick="cpyOne(this,${i})">Copy</button>
        ${esc(fullPrompt)}
      </div>
      ${isWhisk?`<div class="whisk-tip show">
        <strong>💡 Whisk Usage</strong><br>
        In Whisk: paste the full prompt in the "Describe your image" field.
        For even better consistency, upload one reference image of your character in the "Subject" input.
      </div>`:''}
    `;
    container.appendChild(card);
  });

  const outEl = document.getElementById('out');
  outEl.classList.add('on');
  outEl.scrollIntoView({behavior:'smooth',block:'start'});
}

// ─── HELPERS ─────────────────────────────────────────────────────
function cpyOne(btn,idx) {
  const platform = document.getElementById('platform').value;
  const fullPrompt = allResults[idx].image_prompt + '\n\n' + getPlatformSuffix(platform);
  navigator.clipboard.writeText(fullPrompt).then(()=>{
    btn.textContent='Copied!'; btn.classList.add('ok');
    setTimeout(()=>{ btn.textContent='Copy'; btn.classList.remove('ok'); },2000);
  });
}

function copyAll() {
  const platform = document.getElementById('platform').value;
  const platSuffix = getPlatformSuffix(platform);
  const text = allResults.map(r=>
    `IMAGE ${String(r.image_number).padStart(2,'0')} [${r.scene_type}]\nTrigger: "${r.script_line}"\n\nPROMPT:\n${r.image_prompt}\n${platSuffix}`
  ).join('\n\n'+'─'.repeat(60)+'\n\n');
  navigator.clipboard.writeText(text).then(()=>alert('All prompts copied!'));
}

function exportTxt() {
  const platform = document.getElementById('platform').value;
  const platSuffix = getPlatformSuffix(platform);
  const lines = [
    'POV SCRIPT — IMAGE MAPPING SHEET',
    '='.repeat(60),'',
    `Generated: ${new Date().toLocaleString()}`,
    `Platform: ${platform}`,
    `Total Images: ${allResults.length}`,
    '','='.repeat(60),''
  ];
  allResults.forEach(r=>{
    lines.push(`IMAGE ${String(r.image_number).padStart(2,'0')} — [${r.scene_type}]`);
    lines.push(`Word position: ~${r.word_count_from_start}`);
    lines.push(`Script line: "${r.script_line}"`);
    lines.push('');
    lines.push('TEXT-TO-IMAGE PROMPT:');
    lines.push(r.image_prompt);
    lines.push(platSuffix);
    lines.push('','-'.repeat(60),'');
  });
  const blob = new Blob([lines.join('\n')],{type:'text/plain'});
  const a = Object.assign(document.createElement('a'),{
    href:URL.createObjectURL(blob), download:'pov-image-map.txt'
  });
  a.click();
}

function resetTool() {
  document.getElementById('out').classList.remove('on');
  document.getElementById('scriptInput').value='';
  document.getElementById('errBox').classList.remove('on');
  allResults=[];
  window.scrollTo({top:0,behavior:'smooth'});
}

function showErr(msg) {
  const b=document.getElementById('errBox');
  b.innerHTML=msg+'<br><small style="color:var(--muted);margin-top:6px;display:block">Check browser console (F12) for details.</small>';
  b.classList.add('on');
}

function esc(s){
  return (s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
</script>
</body>
</html>
