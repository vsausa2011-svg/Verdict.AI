import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# Page Configuration
st.set_page_config(page_title="Verdict AI", page_icon="⚖️", layout="centered")

# Custom Styling
st.markdown("""
    <style>
    .main-title { text-align: center; font-size: 2.5rem; font-weight: bold; margin-bottom: 0px; }
    .sub-title { text-align: center; font-size: 1.1rem; color: #888; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>⚖️ Verdict AI</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Decode Subtext & Settle Text Debates Instantly</div>", unsafe_allow_html=True)

# Sidebar for API Key
st.sidebar.title("⚙️ Setup")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")
if not api_key:
    api_key = st.secrets.get("GEMINI_API_KEY", "") or st.secrets.get("OPENAI_API_KEY", "")

if not api_key:
    st.warning("👈 Please enter your Gemini API key in Streamlit Secrets!")
    st.stop()

genai.configure(api_key=api_key)

def generate_ai_response(contents):
    """Tries multiple model names until one succeeds."""
    candidate_models = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-2.5-flash', 'gemini-flash']
    last_error = None
    
    for model_name in candidate_models:
        try:
            m = genai.GenerativeModel(model_name)
            res = m.generate_content(
                contents,
                generation_config={"response_mime_type": "application/json"}
            )
            return res.text
        except Exception as e:
            last_error = e
            continue
            
    raise last_error

# App Tabs
tab1, tab2 = st.tabs(["🔍 Vibe & Mood Decoder", "⚖️ Screenshot Text Court"])

# -------------------------------------------------------------
# TAB 1: VIBE & MOOD DECODER
# -------------------------------------------------------------
with tab1:
    st.header("🔍 Decode Text & Mood")
    st.write("Upload a screenshot or paste text to see what they are *actually* feeling.")
    
    uploaded_vibe_img = st.file_uploader("Upload Chat Screenshot:", type=["png", "jpg", "jpeg"], key="vibe_img_direct")
    chat_text_fallback = st.text_area("Or Paste Text Here (Optional):", height=100, key="vibe_text")

    if st.button("🔮 Decode Vibe & Mood", use_container_width=True):
        if not uploaded_vibe_img and not chat_text_fallback:
            st.error("Please upload a screenshot or paste text!")
        else:
            with st.spinner("Verdict AI is reading the subtext..."):
                prompt = """Analyze this text message or chat screenshot.
Return ONLY a valid JSON object with these exact keys:
{
  "detected_mood": "Short summary of their current mood (e.g. Annoyed, Flirty, Disengaged)",
  "vibe_score": 75,
  "passive_aggression": "Low / Medium / High",
  "real_subtext": "What they are ACTUALLY thinking or feeling behind these texts",
  "power_dynamic": "Who holds the upper hand in this conversation and why",
  "response_witty": "A clever/witty response option",
  "response_cool": "A calm/unbothered response option",
  "response_direct": "A direct/firm response option"
}"""
                try:
                    contents = [prompt]
                    if uploaded_vibe_img:
                        img = Image.open(uploaded_vibe_img)
                        contents.append(img)
                    else:
                        contents.append(f"Chat Text:\n{chat_text_fallback}")

                    raw_json = generate_ai_response(contents)
                    data = json.loads(raw_json)

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Current Mood", data.get("detected_mood", "N/A"))
                    col2.metric("Vibe Score", f"{data.get('vibe_score', 0)}/100")
                    col3.metric("Passive Aggression", data.get("passive_aggression", "N/A"))

                    st.markdown("### 🧠 What They Are ACTUALLY Thinking:")
                    st.info(data.get("real_subtext", ""))

                    st.markdown("### ⚡ Power Dynamic:")
                    st.warning(data.get("power_dynamic", ""))

                    st.markdown("### 💬 Suggested Responses:")
                    st.write(f"**🔥 Witty:** {data.get('response_witty', '')}")
                    st.write(f"**🧊 Cool & Unbothered:** {data.get('response_cool', '')}")
                    st.write(f"**🎯 Direct:** {data.get('response_direct', '')}")

                except Exception as e:
                    st.error(f"Error analyzing vibe: {e}")

# -------------------------------------------------------------
# TAB 2: TEXT ARGUMENT SETTLER
# -------------------------------------------------------------
with tab2:
    st.header("⚖️ Instant Screenshot Court")
    st.write("Upload a screenshot of an argument—Verdict AI will auto-detect who is talking and declare a winner!")

    uploaded_arg_img = st.file_uploader("Upload Argument Screenshot:", type=["png", "jpg", "jpeg"], key="arg_img_direct")
    arg_text_fallback = st.text_area("Or Paste Argument Text Here (Optional):", height=100, key="arg_text")

    if st.button("🔨 Judge Argument Now", use_container_width=True):
        if not uploaded_arg_img and not arg_text_fallback:
            st.error("Please upload a screenshot or paste text!")
        else:
            with st.spinner("Verdict AI is reading the screenshot and judging..."):
                prompt = """Analyze this argument screenshot or text thread.
1. Automatically identify the two people in the argument (e.g. by contact name at top, or 'Blue Bubbles (You)' vs 'Grey Bubbles (Friend)').
2. Read all text spoken by both sides and evaluate logic, emotional control, and fairness.

Return ONLY a valid JSON object with these exact keys:
{
  "person_a": "Name/Label for Person 1",
  "person_b": "Name/Label for Person 2",
  "winner": "Name/Label of Winner (or Draw)",
  "headline": "A dramatic title for the verdict",
  "score_a": 80,
  "score_b": 40,
  "breakdown_a": "Summary of Person 1's argument strength",
  "breakdown_b": "Summary of Person 2's argument strength",
  "judge_ruling": "A hilarious yet logically sound final verdict explaining who won and why.",
  "penalty_for_loser": "A lighthearted/funny penalty for the loser."
}"""
                try:
                    contents = [prompt]
                    if uploaded_arg_img:
                        img = Image.open(uploaded_arg_img)
                        contents.append(img)
                    else:
                        contents.append(f"Argument Text:\n{arg_text_fallback}")

                    raw_json = generate_ai_response(contents)
                    data = json.loads(raw_json)

                    p_a = data.get('person_a', 'Person 1')
                    p_b = data.get('person_b', 'Person 2')

                    st.success(f"🏆 WINNER: {data.get('winner', 'Draw')}")
                    st.subheader(f"📜 {data.get('headline', 'Official Verdict')}")

                    col1, col2 = st.columns(2)
                    col1.metric(f"{p_a} Score", f"{data.get('score_a', 0)}/100")
                    col2.metric(f"{p_b} Score", f"{data.get('score_b', 0)}/100")

                    st.markdown(f"**{p_a} Breakdown:** {data.get('breakdown_a', '')}")
                    st.markdown(f"**{p_b} Breakdown:** {data.get('breakdown_b', '')}")

                    st.markdown("---")
                    st.markdown("### ⚖️ Final Judicial Verdict:")
                    st.write(data.get("judge_ruling", ""))

                    st.markdown("### 🚨 Mandatory Penalty for Loser:")
                    st.error(data.get("penalty_for_loser", ""))

                except Exception as e:
                    st.error(f"Error settling argument: {e}")
