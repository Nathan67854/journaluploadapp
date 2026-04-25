import streamlit as st
import base64
import os
import io
import requests
from PIL import Image
import pyperclip

st.set_page_config(page_title="Journal Intake", layout="centered")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">
<style>
    :root {
        --bg:           #F5ECD7;
        --surface:      #EFE0C4;
        --accent:       #A0522D;
        --accent-dark:  #7B3F22;
        --text:         #2C1810;
        --text-sub:     #7a5c3a;
        --text-muted:   #9e7e5e;
        --sage:         #4E7C59;
        --sage-bg:      #E4EDE6;
        --border:       #CEB896;
    }

    /* Paper background + subtle noise grain */
    .stApp {
        background-color: var(--bg);
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3CfeColorMatrix type='saturate' values='0'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
    }
    section.main > div {
        background-color: transparent;
        padding: 2rem 2rem 3rem !important;
    }

    /* Heading — Playfair Display */
    h1 {
        font-family: 'Playfair Display', Georgia, serif !important;
        color: var(--text) !important;
        font-weight: 600 !important;
        font-size: 2.1rem !important;
        letter-spacing: -0.01em !important;
        line-height: 1.2 !important;
    }

    /* Caption — italic watermark */
    .stCaption p {
        font-family: 'DM Sans', system-ui, sans-serif !important;
        font-style: italic !important;
        color: var(--text-muted) !important;
        font-size: 11.5px !important;
        letter-spacing: 0.04em !important;
    }

    /* Tabs — elegant bookmarks */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-radius: 0 !important;
        padding: 0 !important;
        gap: 3px !important;
        border-bottom: 2px solid var(--border) !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'DM Sans', system-ui, sans-serif !important;
        color: var(--text-sub) !important;
        font-weight: 400 !important;
        font-size: 14px !important;
        padding: 10px 28px !important;
        border-radius: 10px 10px 0 0 !important;
        background-color: transparent !important;
        border: 1.5px solid transparent !important;
        border-bottom: none !important;
        transition: all 0.18s ease !important;
        margin-bottom: -2px !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: var(--surface) !important;
        color: var(--accent) !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--surface) !important;
        border-color: var(--border) !important;
        border-bottom-color: var(--surface) !important;
        color: var(--accent) !important;
        font-weight: 600 !important;
    }

    /* Buttons — pill shape + lift on hover */
    .stButton > button {
        font-family: 'DM Sans', system-ui, sans-serif !important;
        background-color: var(--accent) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 999px !important;
        font-weight: 500 !important;
        font-size: 13.5px !important;
        padding: 0.45rem 1.6rem !important;
        letter-spacing: 0.03em !important;
        box-shadow: 0 2px 8px rgba(160, 82, 45, 0.28) !important;
        transition: background-color 0.18s ease, box-shadow 0.18s ease, transform 0.12s ease !important;
    }
    .stButton > button:hover {
        background-color: var(--accent-dark) !important;
        color: #fff !important;
        box-shadow: 0 5px 16px rgba(123, 63, 34, 0.38) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
        box-shadow: 0 1px 4px rgba(123, 63, 34, 0.2) !important;
    }
    .stButton > button:disabled {
        background-color: var(--border) !important;
        color: #a08060 !important;
        box-shadow: none !important;
        transform: none !important;
        opacity: 0.7 !important;
    }

    /* Text area — parchment card with inner shadow */
    .stTextArea textarea {
        background-color: var(--surface) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 14px !important;
        color: var(--text) !important;
        font-family: 'Playfair Display', Georgia, serif !important;
        font-size: 15px !important;
        line-height: 1.85 !important;
        padding: 1.2rem 1.4rem !important;
        box-shadow: inset 0 2px 8px rgba(100, 65, 30, 0.06) !important;
    }

    /* File uploader */
    .stFileUploader {
        background-color: var(--surface) !important;
        border-radius: 14px !important;
        border: 1.5px dashed var(--border) !important;
    }

    /* Radio labels */
    .stRadio label {
        font-family: 'DM Sans', system-ui, sans-serif !important;
        color: var(--text-sub) !important;
        font-size: 13.5px !important;
    }

    /* Info box */
    [data-testid="stAlert"] {
        border-radius: 12px !important;
        font-family: 'DM Sans', system-ui, sans-serif !important;
        font-size: 13.5px !important;
    }

    /* Divider */
    hr {
        border-color: var(--border) !important;
        opacity: 0.5 !important;
        margin: 2.5rem 0 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #E8D5B8 !important;
    }
    section[data-testid="stSidebar"] input {
        background-color: #F5E8D0 !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 8px !important;
        font-family: 'DM Sans', system-ui, sans-serif !important;
        color: var(--text) !important;
    }

    /* Audio input — warm gradient container */
    [data-testid="stAudioInput"] {
        background: linear-gradient(180deg, #fffaf3 0%, var(--surface) 100%) !important;
        border-radius: 14px !important;
        border: 1px solid var(--border) !important;
        padding: 4px !important;
    }
</style>
""", unsafe_allow_html=True)

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_AUDIO_URL = "https://api.groq.com/openai/v1/audio/transcriptions"
KEY_FILE = os.path.expanduser("~/.journal_intake_key")


def load_saved_key() -> str:
    try:
        with open(KEY_FILE) as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


def save_key(key: str):
    with open(KEY_FILE, "w") as f:
        f.write(key)


def to_jpeg_bytes(image_bytes: bytes) -> bytes:
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


def ocr_with_groq(image_bytes: bytes, api_key: str) -> str:
    b64 = base64.b64encode(to_jpeg_bytes(image_bytes)).decode()
    resp = requests.post(GROQ_URL, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }, json={
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [{
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
                },
                {
                    "type": "text",
                    "text": (
                        "You are an OCR tool. Copy every single word written on this paper exactly as it appears, "
                        "word for word, line by line. Do NOT summarize. Do NOT explain. Do NOT add anything. "
                        "Just copy the literal handwritten text from top to bottom. Begin copying now:"
                    )
                }
            ]
        }],
        "max_tokens": 1024,
    }, timeout=30)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def transcribe_with_groq(audio_file, api_key: str) -> str:
    resp = requests.post(
        GROQ_AUDIO_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        files={"file": (audio_file.name, audio_file.read(), audio_file.type or "audio/webm")},
        data={"model": "whisper-large-v3-turbo"},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["text"].strip()


# ── Sidebar ──────────────────────────────────────────────────────────────────

if "groq_key" not in st.session_state:
    st.session_state["groq_key"] = load_saved_key()

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    groq_key = st.text_input("Groq API key", type="password", key="groq_key",
                              help="Get a free key at console.groq.com")
    if groq_key:
        save_key(groq_key)
    st.caption("Free tier · no training on your data")

# ── Main UI ──────────────────────────────────────────────────────────────────

st.title("Journal Intake")
st.caption("Powered by Groq · no training on your data")

tab_photo, tab_voice = st.tabs(["📷 Photo", "🎙️ Voice"])

with tab_photo:
    photo_source = st.radio("Source", ["📷 Camera", "⬆️ Upload"], horizontal=True, key="photo_source")

    image_bytes = None
    if photo_source == "📷 Camera":
        camera_img = st.camera_input("Point camera at your journal entry")
        if camera_img:
            image_bytes = camera_img.getvalue()
    else:
        img_file = st.file_uploader(
            "Upload a photo of your handwritten notes",
            type=["jpg", "jpeg", "png", "webp"],
            key="img_uploader",
        )
        if img_file:
            image_bytes = img_file.getvalue()

    if image_bytes and st.button("Extract Text", key="ocr_btn"):
        api_key = st.session_state.get("groq_key", "")
        if not api_key:
            st.error("Enter your Groq API key in the sidebar first.")
        else:
            try:
                with st.spinner("Reading handwriting…"):
                    st.session_state["result"] = ocr_with_groq(image_bytes, api_key)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

with tab_voice:
    voice_source = st.radio("Source", ["🎙️ Record", "⬆️ Upload"], horizontal=True, key="voice_source")

    audio_bytes = None
    audio_name = None
    recorded = None

    if voice_source == "🎙️ Record":
        if "recording_queue" not in st.session_state:
            st.session_state["recording_queue"] = []

        recorded = st.audio_input("Click the mic to record, click again to stop")
        if recorded:
            current_bytes = recorded.getvalue()
            col_a, col_b = st.columns([2, 1])
            with col_a:
                st.markdown('<span style="background:#E4EDE6;color:#4E7C59;border-radius:999px;padding:5px 16px;font-size:13px;font-family:DM Sans,system-ui,sans-serif;display:inline-block;line-height:1.6;">✅ Recording captured</span>', unsafe_allow_html=True)
            with col_b:
                if st.button("➕ Add to queue", key="add_queue_btn"):
                    queue = st.session_state["recording_queue"]
                    if not queue or current_bytes != queue[-1]:
                        queue.append(current_bytes)
                    st.rerun()

        queue = st.session_state["recording_queue"]
        if queue:
            col_q, col_clear = st.columns([3, 1])
            with col_q:
                st.info(f"🎙️ {len(queue)} recording{'s' if len(queue) > 1 else ''} queued")
            with col_clear:
                if st.button("🗑️ Clear", key="clear_queue_btn"):
                    st.session_state["recording_queue"] = []
                    st.rerun()
    else:
        audio_file = st.file_uploader(
            "Upload your voice recording",
            type=["mp3", "wav", "m4a", "webm"],
            key="audio_uploader",
        )
        if audio_file:
            audio_bytes = audio_file.read()
            audio_name = audio_file.name

    transcribe_source = st.session_state.get("recording_queue") if voice_source == "🎙️ Record" else None
    can_transcribe = (transcribe_source or audio_bytes or recorded)

    if can_transcribe and st.button("Transcribe", key="audio_btn"):
        api_key = st.session_state.get("groq_key", "")
        if not api_key:
            st.error("Enter your Groq API key in the sidebar first.")
        else:
            try:
                queue = st.session_state.get("recording_queue", [])
                if queue:
                    items = [(b, f"recording_{i}.wav") for i, b in enumerate(queue)]
                elif recorded:
                    items = [(recorded.getvalue(), "recording_0.wav")]
                else:
                    items = [(audio_bytes, audio_name)]
                all_text = []
                for rec_bytes, rec_name in items:
                    with st.spinner(f"Transcribing{f' {items.index((rec_bytes, rec_name))+1} of {len(items)}' if len(items) > 1 else ''}…"):
                        resp = requests.post(
                            GROQ_AUDIO_URL,
                            headers={"Authorization": f"Bearer {api_key}"},
                            files={"file": (rec_name, rec_bytes, "audio/wav")},
                            data={"model": "whisper-large-v3-turbo"},
                            timeout=60,
                        )
                        resp.raise_for_status()
                        all_text.append(resp.json()["text"].strip())
                new_text = "\n".join(all_text)
                existing = st.session_state.get("result", "")
                st.session_state["result"] = (existing + "\n\n" + new_text).strip()
                st.session_state["recording_queue"] = []
                st.rerun()
            except Exception as e:
                st.error(f"Transcription failed: {e}")

# ── Result ───────────────────────────────────────────────────────────────────

if "result" in st.session_state:
    st.divider()
    result = st.session_state["result"]
    st.text_area("Result", value=result, height=300)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("📋 Copy to Clipboard"):
            pyperclip.copy(result)
            st.markdown('<span style="background:#E4EDE6;color:#4E7C59;border-radius:999px;padding:5px 16px;font-size:13px;font-family:DM Sans,system-ui,sans-serif;display:inline-block;line-height:1.6;">✅ Copied!</span>', unsafe_allow_html=True)

    with col2:
        st.button("🪨 Save to Obsidian", disabled=True, help="Coming soon")

    with col3:
        if st.button("🔄 Start Over"):
            del st.session_state["result"]
            st.rerun()
