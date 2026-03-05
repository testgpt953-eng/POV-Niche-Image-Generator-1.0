# ================================================================
# POV Script → Image Mapper Pro  |  Streamlit + Gemini REST API
# GitHub: create new repo → paste this as app.py
# requirements.txt needs ONLY:  streamlit>=1.32.0
# (requests is built-in to Streamlit Cloud — no extra install)
# ================================================================

import streamlit as st
import json
import re
from datetime import datetime
import requests as _requests

# ── Page Config ──────────────────────────────────────────────────
st.set_page_config(
    page_title="POV Script → Image Mapper Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================================================
# CUSTOM CSS  —  Dark Cyberpunk Theme
# ================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:ital,wght@0,400;0,500;1,400&display=swap');

/* ── Base ── */
.stApp                    { background-color: #080810 !important; }
.stApp > header           { background-color: #080810 !important; }
.block-container          { padding-top: 1.5rem !important; max-width: 1060px !important; padding-bottom: 4rem !important; }

/* Grid background */
.stApp::before {
  content:''; position:fixed; inset:0;
  background-image: linear-gradient(rgba(76,201,240,.015) 1px,transparent 1px),
                    linear-gradient(90deg,rgba(76,201,240,.015) 1px,transparent 1px);
  background-size: 48px 48px; pointer-events:none; z-index:0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"]              { background-color: #0e0e18 !important; border-right: 1px solid #252535 !important; }
[data-testid="stSidebar"] .stMarkdown p { color: #686882 !important; font-size: 11px !important; }

/* ── Typography ── */
body, p, div, span  { font-family: 'DM Mono', monospace !important; }
h1                  { font-family: 'Bebas Neue', sans-serif !important; }
h2, h3              { font-family: 'DM Mono', monospace !important; font-size: 9px !important; letter-spacing: .28em !important; text-transform: uppercase !important; color: #4cc9f0 !important; }
label               { font-family: 'DM Mono', monospace !important; font-size: 10px !important; letter-spacing: .12em !important; text-transform: uppercase !important; color: #686882 !important; }

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea  > div > div > textarea {
  background-color: #0e0e18 !important; border: 1px solid #323248 !important;
  border-radius: 3px !important; color: #e6e6f0 !important;
  font-family: 'DM Mono', monospace !important; font-size: 12.5px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea  > div > div > textarea:focus { border-color: #4cc9f0 !important; box-shadow: 0 0 0 1px #4cc9f0 !important; }
.stTextArea  > div > div > textarea        { min-height: 180px !important; line-height: 1.75 !important; }

/* ── Selectbox ── */
.stSelectbox > div > div { background-color: #0e0e18 !important; border: 1px solid #323248 !important; border-radius: 3px !important; color: #e6e6f0 !important; font-family: 'DM Mono', monospace !important; font-size: 12px !important; }
.stSelectbox svg { fill: #686882 !important; }
[data-baseweb="select"] div  { background-color: #0e0e18 !important; color: #e6e6f0 !important; }
[data-baseweb="popover"]     { background-color: #0e0e18 !important; border: 1px solid #323248 !important; }
[data-baseweb="option"]      { background-color: #0e0e18 !important; color: #e6e6f0 !important; font-family: 'DM Mono', monospace !important; font-size: 12px !important; }
[data-baseweb="option"]:hover { background-color: #13131e !important; }

/* ── Buttons ── */
.stButton > button {
  font-family: 'DM Mono', monospace !important; border-radius: 3px !important;
  transition: all 0.2s !important; background-color: transparent !important;
  border: 1px solid #323248 !important; color: #e6e6f0 !important;
  font-size: 10px !important; letter-spacing: .14em !important; text-transform: uppercase !important;
}
.stButton > button:hover { background-color: #4cc9f0 !important; color: #080810 !important; border-color: #4cc9f0 !important; }

/* Primary (Analyze) button */
.stButton > button[kind="primary"] {
  background-color: #e63946 !important; border: none !important; color: #fff !important;
  font-family: 'Bebas Neue', sans-serif !important; font-size: 22px !important;
  letter-spacing: .15em !important; padding: 14px !important;
}
.stButton > button[kind="primary"]:hover { background-color: #ff4d5a !important; transform: translateY(-1px); box-shadow: 0 8px 24px rgba(230,57,70,.4) !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]  { background-color: #13131e !important; border: 1px solid #323248 !important; border-radius: 3px !important; gap: 0 !important; overflow: hidden !important; }
.stTabs [data-baseweb="tab"]       { background-color: transparent !important; color: #686882 !important; font-family: 'DM Mono', monospace !important; font-size: 10px !important; letter-spacing: .1em !important; text-transform: uppercase !important; border: none !important; border-radius: 0 !important; padding: 10px 18px !important; }
.stTabs [aria-selected="true"]     { background-color: #e63946 !important; color: #fff !important; }
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── Alerts ── */
.stAlert   { background-color: rgba(230,57,70,.07) !important; border: 1px solid rgba(230,57,70,.3) !important; border-radius: 3px !important; font-family: 'DM Mono', monospace !important; font-size: 12px !important; }
div[data-baseweb="notification"][kind="positive"] { background-color: rgba(45,198,83,.07) !important; border: 1px solid rgba(45,198,83,.3) !important; }
div[data-baseweb="notification"][kind="info"]     { background-color: rgba(76,201,240,.07) !important; border: 1px solid rgba(76,201,240,.25) !important; }

/* ── Code blocks (prompts go here — has built-in copy icon) ── */
.stCode, code, pre { background-color: #080810 !important; border: 1px solid #252535 !important; border-radius: 3px !important; font-family: 'DM Mono', monospace !important; font-size: 11.5px !important; color: #bebedd !important; line-height: 1.9 !important; }

/* ── Metrics ── */
[data-testid="metric-container"]                          { background-color: #0e0e18 !important; border: 1px solid #252535 !important; border-radius: 3px !important; padding: 12px 16px !important; }
[data-testid="metric-container"] label                    { color: #686882 !important; font-size: 9px !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #4cc9f0 !important; font-family: 'Bebas Neue', sans-serif !important; font-size: 28px !important; }

/* ── Download button ── */
.stDownloadButton > button { background-color: transparent !important; border: 1px solid #f4a261 !important; color: #f4a261 !important; font-family: 'DM Mono', monospace !important; font-size: 10px !important; letter-spacing: .14em !important; text-transform: uppercase !important; border-radius: 3px !important; }
.stDownloadButton > button:hover { background-color: #f4a261 !important; color: #080810 !important; }

/* ── Divider / Scrollbar ── */
hr { border-color: #252535 !important; margin: 8px 0 !important; }
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:#080810; }
::-webkit-scrollbar-thumb { background:#252535; border-radius:3px; }
</style>
""", unsafe_allow_html=True)


# ================================================================
# DATA
# ================================================================
PRESETS = [
    {"id": "agent",     "icon": "🕵️", "name": "Default Agent",      "desc": "Brown hair, blue shirt",
     "anchor": "protagonist: white blank oval face, small dot eyes, simple line mouth, short brown hair, wearing light blue short-sleeve shirt and dark navy jeans, average height slim build, white hands, consistent character design throughout"},
    {"id": "tactical",  "icon": "🪖", "name": "Tactical Operator",   "desc": "Black hair, navy jacket",
     "anchor": "protagonist: white blank oval face, small dot eyes, simple line mouth, short black hair, wearing navy blue tactical zip jacket and gray cargo pants with black combat boots, athletic build, white hands, consistent character design throughout"},
    {"id": "detective", "icon": "🔍", "name": "Detective",            "desc": "Slicked hair, olive suit",
     "anchor": "protagonist: white blank oval face, small dot eyes, simple line mouth, dark slicked-back hair, wearing olive green blazer over beige dress shirt with brown leather shoes, medium build, white hands, consistent character design throughout"},
    {"id": "rebel",     "icon": "🔥", "name": "Street Rebel",         "desc": "Spiky hair, dark hoodie",
     "anchor": "protagonist: white blank oval face, small dot eyes, simple line mouth, dark spiky hair, wearing dark gray hoodie and black jeans with white sneakers, slim build, white hands, consistent character design throughout"},
    {"id": "soldier",   "icon": "⚔️", "name": "Soldier",              "desc": "Buzz cut, all-black gear",
     "anchor": "protagonist: white blank oval face, small dot eyes, simple line mouth, military buzz cut brown hair, wearing all-black tactical military vest and pants with black combat boots, muscular broad build, white hands, consistent character design throughout"},
    {"id": "corporate", "icon": "💼", "name": "Corporate",            "desc": "Neat hair, turtleneck",
     "anchor": "protagonist: white blank oval face, small dot eyes, simple line mouth, neatly combed black hair, wearing black turtleneck and dark trousers with leather shoes, tall slim build, white hands, consistent character design throughout"},
    {"id": "scientist", "icon": "🔬", "name": "Scientist",            "desc": "Brown hair, lab coat",
     "anchor": "protagonist: white blank oval face, small dot eyes, simple line mouth, short brown hair, wearing white lab coat over blue shirt with dark pants, average build, white hands, consistent character design throughout"},
    {"id": "criminal",  "icon": "🎭", "name": "Criminal",             "desc": "Dark hair, black jacket",
     "anchor": "protagonist: white blank oval face, small dot eyes, simple line mouth, dark messy hair, wearing black leather jacket and dark jeans with black boots, lean build, white hands, consistent character design throughout"},
]

PLATFORM_SUFFIXES = {
    "🎨 Google Whisk":  "--style flat 2D animation --consistency high --aspect 16:9",
    "Midjourney":       "--style raw --ar 16:9 --v 6.1 --cw 100",
    "Leonardo AI":      "Style: Illustration, consistent character, aspect ratio 16:9",
    "Ideogram":         "Style: Illustration. Aspect: 16:9.",
    "DALL-E / ChatGPT": "digital illustration, consistent character style, 16:9 aspect ratio",
    "Generic":          "16:9 aspect ratio, consistent character, animation style",
}

ART_STYLES = {
    "Flat 2D Animation ✦":  "2D flat animation, clean bold black outlines, cel-shaded, muted desaturated palette, no texture on faces",
    "Cinematic 2D Cartoon": "2D animation, detailed linework, cinematic lighting, muted color palette",
    "Minimal Cartoon":      "simple clean cartoon, minimal shading, flat colors, clear outlines",
    "Semi-Realistic":       "semi-realistic illustration, detailed shading, muted cinematic tones",
    "Comic Book":           "comic book style, high contrast, bold inks, halftone shadows",
}

VIDEO_THEMES = {
    "🕵️ Spy & Espionage":  "spy and espionage thriller",
    "🪖 Military & Combat": "military and special forces",
    "🔫 Crime & Underworld":"crime and organized underworld",
    "🏛️ Gov Conspiracy":    "government conspiracy",
    "😨 Survival Thriller": "survival horror and psychological thriller",
    "💼 Corporate Power":   "corporate power and corruption",
    "☢️ Post-Apocalyptic":  "post-apocalyptic wasteland",
    "⚔️ Historical War":    "historical war and battlefield",
}

BADGE_STYLES = {
    "ESTABLISH":  ("background:rgba(244,162,97,.12);color:#f4a261;border:1px solid rgba(244,162,97,.3)", "🌅"),
    "ACTION":     ("background:rgba(230,57,70,.14);color:#e63946;border:1px solid rgba(230,57,70,.35)",  "⚡"),
    "EMOTION":    ("background:rgba(76,201,240,.1);color:#4cc9f0;border:1px solid rgba(76,201,240,.3)",  "💠"),
    "TRANSITION": ("background:rgba(100,100,130,.13);color:#686882;border:1px solid #323248",            "🔄"),
}


# ================================================================
# SESSION STATE INIT
# ================================================================
defaults = {
    "api_key":         "",      # stored Gemini API key
    "api_key_saved":   False,   # whether key is saved this session
    "selected_model":  "gemini-2.5-flash",  # chosen Gemini model
    "selected_preset": "agent",
    "results":         [],
    "analyzed_script": "",
    "platform_used":   "🎨 Google Whisk",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ================================================================
# HELPER FUNCTIONS
# ================================================================
def get_char_anchor(tab: str, preset_id: str, manual: dict) -> str:
    if tab == "preset":
        p = next((x for x in PRESETS if x["id"] == preset_id), PRESETS[0])
        return p["anchor"]
    hair   = manual.get("hair", "short brown hair") or "short brown hair"
    face   = manual.get("face", "white blank oval face, dot eyes, simple line mouth, faceless POV style")
    skin   = manual.get("skin", "white pale skin")
    build  = manual.get("build", "average height slim build")
    outfit = manual.get("outfit", "light blue short-sleeve shirt, dark navy jeans, brown sneakers")
    extra  = manual.get("extra", "").strip()
    return f"protagonist: {face}, {hair}, {skin}, {build}, wearing {outfit}{', ' + extra if extra else ''}, consistent character design throughout"


def build_system_prompt(char_anchor: str, art: str, theme: str, platform: str) -> str:
    whisk_note = ""
    if "whisk" in platform.lower():
        whisk_note = "\n\n## WHISK OPTIMIZATION:\nWhisk uses subject + style + scene. Write each prompt as a unified description covering all three. Keep it natural and flowing."
    return f"""You are an expert visual director for POV-style animated YouTube videos in the "{theme}" niche.

TASK: Analyze the given script and create a precise IMAGE MAPPING SHEET as a JSON array.

## PACING RULES (strictly follow):
- NEVER place an image on every sentence — this creates a slideshow effect, avoid it
- NEVER go more than 70 words without at least one image
- Place MORE images during: action sequences, new location reveals, dramatic discoveries, emotional peaks, confrontations
- Place FEWER images during: internal monologue, explanatory narration, dialogue-heavy sections
- Average: 1 image per 40-65 words, but vary based on dramatic need
- Total count: 8-14 images for 300-500 word script, 14-20 for 500-900 words

## SCENE TYPES (use exactly as written):
- ESTABLISH — New location or situation introduction
- ACTION — Physical movement, confrontation, activity
- EMOTION — Close-up emotional reaction, revelation, internal conflict
- TRANSITION — Scene change, time skip, tone shift

## CHARACTER CONSISTENCY (CRITICAL):
Use this character anchor VERBATIM in every prompt where the protagonist appears:
"{char_anchor}"
Never change hair, face, outfit, or build between images.{whisk_note}

## PROMPT FORMULA:
[ART STYLE] + [CHARACTER ANCHOR] + [POSE/ACTION] + [ENVIRONMENT] + [LIGHTING] + [MOOD] + [CAMERA ANGLE] + [END TAGS]

ART STYLE to start every prompt: "{art}"

LIGHTING by scene type:
- ESTABLISH: soft ambient light, even exposure, natural environmental glow
- ACTION: harsh directional side-lighting, strong cast shadows, high contrast
- EMOTION: single dramatic overhead spotlight, pitch black background
- TRANSITION: dim atmospheric haze, desaturated mist, soft diffuse glow

ENVIRONMENT (always cold/oppressive):
grey concrete corridors, dark brick alleys, dimly lit government buildings, cold urban streets at night, interrogation rooms, abandoned warehouses, underground bunkers

END EVERY PROMPT WITH:
"character consistency, same protagonist throughout, {theme} atmosphere, cinematic composition, 16:9 widescreen"

## OUTPUT RULE:
Return ONLY a raw JSON array. No markdown fences. No backticks. No explanation.
Start directly with [ and end with ]

## JSON SCHEMA:
{{
  "image_number": <integer starting at 1>,
  "scene_type": "<ESTABLISH|ACTION|EMOTION|TRANSITION>",
  "script_line": "<exact phrase from script where image appears>",
  "word_count_from_start": <approximate word position>,
  "image_prompt": "<complete ready-to-use prompt>"
}}"""


# ── Model options (only CONFIRMED working model IDs) ─────────────
# Source: ai.google.dev/gemini-api/docs/models  (verified March 2025)
MODEL_OPTIONS = {
    "gemini-2.5-flash":      "Gemini 2.5 Flash      ★ Recommended",
    "gemini-2.0-flash":      "Gemini 2.0 Flash      (stable)",
    "gemini-2.0-flash-lite": "Gemini 2.0 Flash-Lite (fast/cheap)",
    "gemini-1.5-flash":      "Gemini 1.5 Flash      (fallback)",
}

GEMINI_REST_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "{model}:generateContent?key={key}"
)


def _try_one_model(api_key: str, model_name: str, user_msg: str, sys_prompt: str) -> str:
    """Direct REST call to Gemini — no SDK needed."""
    url = GEMINI_REST_URL.format(model=model_name, key=api_key)
    payload = {
        "system_instruction": {"parts": [{"text": sys_prompt}]},
        "contents": [{"role": "user", "parts": [{"text": user_msg}]}],
        "generationConfig": {
            "temperature": 0.65,
            "maxOutputTokens": 8192,
            "responseMimeType": "application/json",
        },
    }
    resp = _requests.post(url, json=payload, timeout=120)
    if resp.status_code == 429:
        raise RuntimeError(f"429 RESOURCE_EXHAUSTED {resp.text[:200]}")
    if not resp.ok:
        data = resp.json()
        msg = data.get('error', {}).get('message', resp.text[:300])
        raise RuntimeError(f"API Error {resp.status_code}: {msg}")
    data = resp.json()
    parts = data.get('candidates', [{}])[0].get('content', {}).get('parts', [])
    raw = ''.join(p.get('text', '') for p in parts)
    if not raw:
        raise RuntimeError("Empty response from Gemini. Try again.")
    return raw.strip()


def call_gemini(api_key: str, script_text: str, system_prompt: str,
                primary_model: str = "gemini-2.0-flash") -> list:
    user_msg = (
        "Analyze this POV script and return ONLY the raw JSON array:\n\n"
        "---SCRIPT START---\n" + script_text + "\n---SCRIPT END---"
    )
    # Auto-fallback chain — only confirmed working model IDs
    _all_models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-1.5-flash"]
    fallback_chain = [primary_model] + [m for m in _all_models if m != primary_model]
    last_err = None
    used_model = primary_model
    raw = ""
    for attempt_model in fallback_chain:
        try:
            used_model = attempt_model
            raw = _try_one_model(api_key, attempt_model, user_msg, system_prompt)
            break   # success
        except Exception as ex:
            last_err = ex
            err_str = str(ex)
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "quota" in err_str.lower():
                continue    # try next model
            raise           # non-quota error — raise immediately
    else:
        raise RuntimeError(
            "429 QUOTA EXHAUSTED — saare free models pe limit aa gayi.\n\n"
            "Solutions:\n"
            "1. Sidebar mein doosra model try karo\n"
            "2. 1-2 min ruko (per-minute limit reset hoti hai)\n"
            "3. Naya API key banao: aistudio.google.com/apikey\n"
            "4. Google AI Studio mein billing enable karo (paid tier mein zyada quota)\n\n"
            f"Last error: {last_err}"
        )
    # Parse JSON
    raw = re.sub(r"^```json\s*", "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"^```\s*",     "", raw, flags=re.IGNORECASE)
    raw = re.sub(r"\s*```$",     "", raw).strip()
    s, e = raw.find("["), raw.rfind("]")
    if s == -1 or e == -1:
        raise ValueError("JSON array response mein nahi mila. Script thoda lamba rakho.")
    results = json.loads(raw[s : e + 1])
    if not isinstance(results, list) or len(results) == 0:
        raise ValueError("Gemini ne empty list di. Script mein aur detail add karo.")
    for r in results:
        r["_model_used"] = used_model
    return results


def build_export_text(results: list, platform: str) -> str:
    suffix = PLATFORM_SUFFIXES.get(platform, PLATFORM_SUFFIXES["Generic"])
    lines = [
        "POV SCRIPT — IMAGE MAPPING SHEET",
        "=" * 60, "",
        f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"Platform  : {platform}",
        f"Total imgs: {len(results)}",
        "", "=" * 60, "",
    ]
    for r in results:
        num    = str(r.get("image_number", "?")).zfill(2)
        stype  = r.get("scene_type", "SCENE")
        line   = r.get("script_line", "")
        wpos   = r.get("word_count_from_start", "?")
        prompt = r.get("image_prompt", "")
        lines += [
            f"IMAGE {num} — [{stype}]",
            f"Word position : ~{wpos}",
            f'Script line   : "{line}"', "",
            "TEXT-TO-IMAGE PROMPT:",
            prompt, suffix, "",
            "-" * 60, "",
        ]
    return "\n".join(lines)


# ================================================================
# SIDEBAR  —  API KEY MANAGEMENT
# ================================================================
with st.sidebar:

    # ── Logo / Title ─────────────────────────────────────────────
    st.markdown("""
<div style="text-align:center;padding:12px 0 18px;">
  <div style="font-size:9px;letter-spacing:.3em;text-transform:uppercase;color:#4cc9f0;margin-bottom:6px;">✦ POV NICHE · GEMINI 2.0</div>
  <div style="font-family:'Bebas Neue',sans-serif;font-size:26px;letter-spacing:.08em;color:#e6e6f0;line-height:1.1;">
    SCRIPT<span style="color:#e63946;">IMAGE</span><br>
    <span style="font-size:.55em;letter-spacing:.2em;color:#4cc9f0;">MAPPER PRO</span>
  </div>
</div>
<hr style="border-color:#252535;margin:0 0 18px;">
""", unsafe_allow_html=True)

    # ── API Key Section ──────────────────────────────────────────
    st.markdown('<div style="font-size:9px;letter-spacing:.28em;text-transform:uppercase;color:#4cc9f0;margin-bottom:10px;">🔑 GEMINI API KEY</div>', unsafe_allow_html=True)

    if not st.session_state.api_key_saved:
        # ── Show input + Save button ─────────────────────────────
        new_key = st.text_input(
            "API Key",
            type="password",
            placeholder="AIzaSy...",
            label_visibility="collapsed",
            key="api_key_input_field",
        )
        save_col, _ = st.columns([1, 0.01])
        with save_col:
            if st.button("💾  SAVE API KEY", use_container_width=True):
                if new_key.strip():
                    st.session_state.api_key       = new_key.strip()
                    st.session_state.api_key_saved = True
                    st.rerun()
                else:
                    st.error("Key khali hai — paste karo!")

        st.markdown("""
<div style="margin-top:8px;font-size:10px;color:#686882;line-height:1.8;">
  Free key yahan se lo:<br>
  <a href="https://aistudio.google.com/apikey" target="_blank"
     style="color:#4cc9f0;">aistudio.google.com/apikey</a>
</div>
""", unsafe_allow_html=True)

    else:
        # ── Show saved status + Change button ────────────────────
        masked = st.session_state.api_key[:8] + "••••••••••••" if len(st.session_state.api_key) > 8 else "••••••••"
        st.markdown(f"""
<div style="background:rgba(45,198,83,.08);border:1px solid rgba(45,198,83,.3);border-radius:3px;padding:10px 14px;margin-bottom:10px;">
  <div style="font-size:9px;letter-spacing:.1em;color:#2dc653;margin-bottom:4px;">✅ API KEY SAVED</div>
  <div style="font-size:11px;color:#686882;font-family:'DM Mono',monospace;">{masked}</div>
</div>
""", unsafe_allow_html=True)
        if st.button("🔄  CHANGE KEY", use_container_width=True):
            st.session_state.api_key       = ""
            st.session_state.api_key_saved = False
            st.rerun()

    st.markdown('<hr style="border-color:#252535;margin:18px 0;">', unsafe_allow_html=True)

    # ── Model Selector
    st.markdown('<div style="font-size:9px;letter-spacing:.28em;text-transform:uppercase;color:#4cc9f0;margin-bottom:8px;">🤖 GEMINI MODEL</div>', unsafe_allow_html=True)
    chosen_model = st.selectbox(
        "Model",
        options=list(MODEL_OPTIONS.keys()),
        format_func=lambda m: MODEL_OPTIONS[m],
        index=list(MODEL_OPTIONS.keys()).index(st.session_state.selected_model),
        label_visibility="collapsed",
        key="model_selector",
    )
    if chosen_model != st.session_state.selected_model:
        st.session_state.selected_model = chosen_model
    st.markdown('<div style="font-size:9px;color:#686882;margin-top:4px;line-height:1.7;">💡 429 error aaye → model badlo<br>Auto-fallback bhi enabled hai</div>', unsafe_allow_html=True)
    st.markdown('<hr style="border-color:#252535;margin:14px 0;">', unsafe_allow_html=True)

    # ── How to use ───────────────────────────────────────────────
    st.markdown("""
<div style="font-size:9px;letter-spacing:.28em;text-transform:uppercase;color:#4cc9f0;margin-bottom:10px;">📖 HOW TO USE</div>
<div style="font-size:11px;color:#686882;line-height:2.1;">
① API key paste → 💾 Save<br>
② Character preset choose karo<br>
③ Art style + theme + platform<br>
④ Script paste karo (60+ words)<br>
⑤ Analyze button click karo<br>
⑥ Prompts copy → Whisk / MJ
</div>
<hr style="border-color:#252535;margin:16px 0;">
<div style="font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:#4cc9f0;margin-bottom:8px;">⚙️ MODEL</div>
<div style="font-size:10px;color:#686882;line-height:1.9;">
Gemini 2.0 Flash<br>
Pacing: 40-65 words/img<br>
Types: ESTABLISH · ACTION<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;EMOTION · TRANSITION
</div>
""", unsafe_allow_html=True)


# ================================================================
# MAIN — HEADER
# ================================================================
st.markdown("""
<div style="text-align:center;margin-bottom:36px;position:relative;z-index:1;">
  <div style="font-size:10px;letter-spacing:.35em;text-transform:uppercase;color:#4cc9f0;margin-bottom:10px;">
    ✦ POV Niche · Gemini 2.0 Flash · Whisk Optimized
  </div>
  <div style="font-family:'Bebas Neue',sans-serif;font-size:clamp(42px,7vw,80px);letter-spacing:.04em;line-height:.92;color:#e6e6f0;">
    SCRIPT <span style="color:#e63946;">IMAGE</span>
    <span style="font-size:.48em;color:#4cc9f0;letter-spacing:.16em;display:block;margin-top:6px;">MAPPER PRO</span>
  </div>
  <p style="font-size:11px;color:#686882;margin-top:14px;font-family:'DM Mono',monospace;">
    Script paste karo → AI har visual moment map kare → Numbered prompts with full character consistency
  </p>
</div>
""", unsafe_allow_html=True)

# ── API key banner if not saved ───────────────────────────────────
if not st.session_state.api_key_saved:
    st.markdown("""
<div style="background:rgba(230,57,70,.07);border:1px solid rgba(230,57,70,.3);border-radius:3px;
            padding:12px 18px;margin-bottom:18px;font-size:12px;color:#e63946;text-align:center;">
  ⚠️ Sidebar mein Gemini API key paste karo aur 💾 Save karo — tab analyze hoga
</div>
""", unsafe_allow_html=True)


# ================================================================
# STEP 1 — CHARACTER SETUP
# ================================================================
st.markdown("""
<div style="background:#13131e;border:1px solid #252535;border-radius:4px;padding:20px 24px 14px;margin-bottom:14px;">
  <div style="font-size:9px;letter-spacing:.28em;text-transform:uppercase;color:#4cc9f0;margin-bottom:16px;display:flex;align-items:center;gap:10px;">
    <span style="width:22px;height:1px;background:#4cc9f0;flex-shrink:0;display:inline-block;"></span>
    ① CHARACTER SETUP
  </div>
""", unsafe_allow_html=True)

tab_preset, tab_manual = st.tabs(["🎭  Preset Characters", "✏️  Manual Builder"])

with tab_preset:
    st.markdown('<p style="font-size:10px;color:#686882;margin-bottom:12px;">Character card pe click karo to select:</p>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, preset in enumerate(PRESETS):
        with cols[i % 4]:
            is_sel   = st.session_state.selected_preset == preset["id"]
            brd      = "#e63946" if is_sel else "#323248"
            bg       = "rgba(230,57,70,.07)" if is_sel else "#0e0e18"
            txt_clr  = "#e63946" if is_sel else "#e6e6f0"
            st.markdown(f"""
<div style="background:{bg};border:1px solid {brd};border-radius:3px;
            padding:13px 8px;text-align:center;margin-bottom:6px;">
  <div style="font-size:22px;margin-bottom:5px;">{preset['icon']}</div>
  <div style="font-size:10px;letter-spacing:.09em;text-transform:uppercase;color:{txt_clr};">{preset['name']}</div>
  <div style="font-size:9px;color:#686882;margin-top:2px;">{preset['desc']}</div>
</div>
""", unsafe_allow_html=True)
            label = "✔ Selected" if is_sel else "Select"
            if st.button(label, key=f"p_{preset['id']}", use_container_width=True):
                st.session_state.selected_preset = preset["id"]
                st.rerun()

with tab_manual:
    mc1, mc2 = st.columns(2)
    with mc1:
        m_hair  = st.text_input("Hair Style & Color", placeholder="e.g. short brown hair, side-swept", key="m_hair")
        m_skin  = st.selectbox("Skin Tone", ["white pale skin","light tan skin","medium brown skin","dark brown skin","East Asian skin tone","South Asian skin tone"], key="m_skin")
    with mc2:
        m_face  = st.selectbox("Face Style", ["white blank oval face, dot eyes, simple line mouth, faceless POV style","simple cartoon face, minimal features, dot eyes","semi-detailed cartoon face, expressive eyes, defined jawline","realistic face, detailed features"], key="m_face")
        m_build = st.selectbox("Build", ["average height slim build","tall athletic build","short compact build","muscular broad-shouldered build"], key="m_build")
    m_outfit = st.selectbox("Outfit", ["light blue short-sleeve shirt, dark navy jeans, brown sneakers","navy blue tactical zip jacket, gray cargo pants, black combat boots","olive green blazer, beige dress shirt, brown leather shoes","all-black military tactical vest, black pants, black boots","dark gray hoodie, black jeans, white sneakers","white lab coat over blue shirt, dark pants","black turtleneck, dark trousers, leather shoes"], key="m_outfit")
    m_extra  = st.text_input("Extra Details (optional)", placeholder="e.g. scar on left cheek, glasses, beard...", key="m_extra")

st.markdown("</div>", unsafe_allow_html=True)

# resolve active tab & char anchor
_manual = {"hair": st.session_state.get("m_hair",""), "face": st.session_state.get("m_face","white blank oval face, dot eyes, simple line mouth, faceless POV style"), "skin": st.session_state.get("m_skin","white pale skin"), "build": st.session_state.get("m_build","average height slim build"), "outfit": st.session_state.get("m_outfit","light blue short-sleeve shirt, dark navy jeans, brown sneakers"), "extra": st.session_state.get("m_extra","")}
_tab    = "manual" if _manual["hair"] else "preset"


# ================================================================
# STEP 2 — STYLE SETTINGS
# ================================================================
st.markdown("""
<div style="background:#13131e;border:1px solid #252535;border-radius:4px;padding:20px 24px;margin-bottom:14px;">
  <div style="font-size:9px;letter-spacing:.28em;text-transform:uppercase;color:#4cc9f0;margin-bottom:16px;display:flex;align-items:center;gap:10px;">
    <span style="width:22px;height:1px;background:#4cc9f0;flex-shrink:0;display:inline-block;"></span>
    ② STYLE SETTINGS
  </div>
""", unsafe_allow_html=True)

sc1, sc2, sc3 = st.columns(3)
with sc1: art_label      = st.selectbox("Art Style",      list(ART_STYLES.keys()),      key="art_sel")
with sc2: theme_label    = st.selectbox("Video Theme",    list(VIDEO_THEMES.keys()),     key="theme_sel")
with sc3: platform_label = st.selectbox("Image Platform", list(PLATFORM_SUFFIXES.keys()),key="platform_sel")
st.markdown("</div>", unsafe_allow_html=True)


# ================================================================
# STEP 3 — SCRIPT INPUT
# ================================================================
st.markdown("""
<div style="background:#13131e;border:1px solid #252535;border-radius:4px;padding:20px 24px;margin-bottom:14px;">
  <div style="font-size:9px;letter-spacing:.28em;text-transform:uppercase;color:#4cc9f0;margin-bottom:16px;display:flex;align-items:center;gap:10px;">
    <span style="width:22px;height:1px;background:#4cc9f0;flex-shrink:0;display:inline-block;"></span>
    ③ PASTE YOUR POV SCRIPT
  </div>
""", unsafe_allow_html=True)

script_input = st.text_area(
    "Script",
    height=220,
    label_visibility="collapsed",
    placeholder="""Apna full POV script yahan paste karo...

Misal:
You wake up in a cold grey room. No windows. No door handles on the inside. You remember last night — the USB drive, the man in the black coat, the alley behind the embassy...

You check your pockets. Empty. But then you notice something scratched into the concrete floor beneath your feet. Coordinates. And a name you recognize. Your handler's name.""",
    key="script_input",
)

wc = len(script_input.split()) if script_input.strip() else 0
st.markdown(f'<p style="font-size:10px;color:#686882;text-align:right;margin:-6px 0 10px;">Words: <span style="color:#4cc9f0;">{wc}</span></p>', unsafe_allow_html=True)

analyze_clicked = st.button(
    "▶  ANALYZE SCRIPT — GENERATE IMAGE MAP",
    use_container_width=True,
    type="primary",
    key="analyze_btn",
    disabled=not st.session_state.api_key_saved,
)
if not st.session_state.api_key_saved:
    st.caption("💡 Analyze button tab active hoga jab API key save hogi")

st.markdown("</div>", unsafe_allow_html=True)


# ================================================================
# ANALYZE
# ================================================================
if analyze_clicked:
    if wc < 30:
        st.error("❌ Script bahut chota hai — kam az kam 60 words chahiye.")
    else:
        char_anchor = get_char_anchor(_tab, st.session_state.selected_preset, _manual)
        sys_prompt  = build_system_prompt(char_anchor, ART_STYLES[art_label], VIDEO_THEMES[theme_label], platform_label)

        primary = st.session_state.selected_model
        with st.spinner(f"🔄 {primary} analyze kar raha hai... auto-fallback on (15-30 sec)"):
            try:
                results = call_gemini(
                    st.session_state.api_key, script_input, sys_prompt,
                    primary_model=primary,
                )
                model_used = results[0].get("_model_used", primary) if results else primary
                st.session_state.results          = results
                st.session_state.analyzed_script  = script_input
                st.session_state.platform_used    = platform_label
                st.session_state.model_used_last  = model_used
                if model_used != primary:
                    st.warning(f"⚠️ {primary} quota tha — auto-switched to **{model_used}** ✅ All prompts generated!")
                else:
                    st.success(f"✅ Done! {len(results)} prompts generated! (Model: {model_used})")
            except RuntimeError as e:
                st.error(str(e))
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    st.error(
                        "❌ 429 — Quota Exhausted!\n\n"
                        "**Quick Fixes:**\n"
                        "1. Sidebar mein doosra model select karo\n"
                        "2. 1-2 min ruko phir try karo\n"
                        "3. Naya API key banao: aistudio.google.com/apikey\n"
                        "4. Billing enable karo AI Studio mein (zyada quota)"
                    )
                else:
                    st.error(f"❌ Error: {e}")


# ================================================================
# RESULTS
# ================================================================
if st.session_state.results:
    results  = st.session_state.results
    platform = st.session_state.platform_used
    suffix   = PLATFORM_SUFFIXES.get(platform, PLATFORM_SUFFIXES["Generic"])
    is_whisk = "whisk" in platform.lower()
    script_wc = len(st.session_state.analyzed_script.split())
    avg_w     = round(script_wc / len(results)) if results else 0

    st.markdown('<hr style="border-color:#252535;margin:22px 0 18px;">', unsafe_allow_html=True)

    # Header
    st.markdown("""
<div style="font-family:'Bebas Neue',sans-serif;font-size:26px;letter-spacing:.1em;color:#f4a261;margin-bottom:16px;">
  📋 IMAGE MAPPING SHEET
</div>
""", unsafe_allow_html=True)

    # Metrics
    sc_cnt = {}
    for r in results:
        t = r.get("scene_type", "SCENE"); sc_cnt[t] = sc_cnt.get(t, 0) + 1

    m1, m2, m3, m4, m5 = st.columns(5)
    with m1: st.metric("Total Images",     len(results))
    with m2: st.metric("Script Words",     script_wc)
    with m3: st.metric("Avg Words/Image",  f"~{avg_w}")
    with m4: st.metric("Platform",         platform.replace("🎨 ",""))
    with m5: st.metric("Action Scenes",    sc_cnt.get("ACTION", 0))

    # Scene type chips
    chips = ""
    for stype, cnt in sc_cnt.items():
        sty, ico = BADGE_STYLES.get(stype, ("background:#1a1a2e;color:#686882;border:1px solid #323248","▸"))
        chips += f'<span style="{sty};padding:3px 11px;border-radius:2px;font-size:9px;letter-spacing:.1em;margin-right:6px;">{ico} {stype}: <b>{cnt}</b></span>'
    st.markdown(f'<div style="margin:14px 0 20px;">{chips}</div>', unsafe_allow_html=True)

    # Image Cards
    for item in results:
        num        = str(item.get("image_number","?")).zfill(2)
        stype      = item.get("scene_type","SCENE")
        sline      = item.get("script_line","")
        wpos       = item.get("word_count_from_start","?")
        prompt     = item.get("image_prompt","")
        full_p     = prompt + "\n\n" + suffix
        bstyle, bico = BADGE_STYLES.get(stype, BADGE_STYLES["TRANSITION"])

        st.markdown(f"""
<div style="background:#0e0e18;border:1px solid #252535;border-left:3px solid #e63946;
            border-radius:3px;padding:16px 20px 10px;margin-bottom:4px;">
  <div style="display:flex;align-items:flex-start;gap:12px;margin-bottom:10px;">
    <div style="font-family:'Bebas Neue',sans-serif;font-size:38px;color:#e63946;line-height:1;min-width:50px;">{num}</div>
    <div style="flex:1;">
      <div style="font-size:10px;color:#686882;letter-spacing:.1em;text-transform:uppercase;margin-bottom:5px;display:flex;align-items:center;flex-wrap:wrap;gap:8px;">
        Word ~{wpos}
        <span style="{bstyle};padding:2px 9px;border-radius:2px;font-size:9px;letter-spacing:.12em;">{bico} {stype}</span>
      </div>
      <div style="font-size:13px;color:#e6e6f0;line-height:1.5;border-left:2px solid #4cc9f0;padding-left:9px;font-style:italic;">"{sline}"</div>
    </div>
  </div>
  <div style="font-size:9px;letter-spacing:.18em;text-transform:uppercase;color:#686882;margin-bottom:6px;">
    ▸ Text-to-Image Prompt{'&nbsp;&nbsp;<span style="color:#7b5ea7;">(Whisk Optimized)</span>' if is_whisk else ''}
  </div>
</div>
""", unsafe_allow_html=True)

        # Code block = built-in copy button (clipboard icon top-right)
        st.code(full_p, language=None)

        if is_whisk:
            st.markdown("""
<div style="background:rgba(123,94,167,.08);border:1px solid rgba(123,94,167,.25);border-radius:3px;
            padding:10px 14px;font-size:11px;line-height:1.8;color:#b0a0cc;margin-top:-8px;margin-bottom:6px;">
  <strong style="color:#c4a8ff;font-size:9px;letter-spacing:.12em;text-transform:uppercase;">💡 Whisk Tip</strong><br>
  Prompt ko "Describe your image" mein paste karo. Character reference image "Subject" mein daalo.
</div>
""", unsafe_allow_html=True)

        st.markdown('<div style="height:6px;"></div>', unsafe_allow_html=True)

    # Export row
    st.markdown('<hr style="border-color:#252535;margin:20px 0 14px;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:9px;letter-spacing:.28em;text-transform:uppercase;color:#4cc9f0;margin-bottom:10px;">⬇ EXPORT</div>', unsafe_allow_html=True)

    exp1, exp2, exp3 = st.columns(3)
    with exp1:
        st.download_button(
            "⬇  Export as .txt",
            data=build_export_text(results, platform),
            file_name=f"pov-image-map-{datetime.now().strftime('%Y%m%d-%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with exp2:
        st.markdown('<p style="font-size:10px;color:#686882;text-align:center;padding:9px 0;">Each prompt box mein 📋 icon hai → click = copy</p>', unsafe_allow_html=True)
    with exp3:
        if st.button("↺  New Script", use_container_width=True):
            st.session_state.results         = []
            st.session_state.analyzed_script = ""
            st.rerun()

# Footer
st.markdown("""
<div style="text-align:center;padding:40px 0 10px;font-size:10px;color:#2a2a42;letter-spacing:.1em;">
  POV SCRIPT → IMAGE MAPPER PRO · Gemini 2.0 Flash · Streamlit
</div>
""", unsafe_allow_html=True)
