import streamlit as st
import openai
import base64
import json

# Page Configuration
st.set_page_config(page_title="Verdict AI", page_icon="⚖️", layout="centered")

# Custom Styling
st.markdown("""
    <style>
    .main-title { text-align: center; font-size: 2.5rem; font-weight: bold; margin-bottom: 0px; }
    .sub-title { text-align: center; font-size: 1.1rem; color: #888; margin-bottom: 25px; }
    .card { background-color: #1e1e2e; padding: 20px; border-radius: 12px; margin-bottom: 15px; border: 1px solid #313244; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>⚖️ Verdict AI</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Decode Subtext & Settle Text Debates with Friends</div>", unsafe_allow_html=True)

# Sidebar for API Key
st.sidebar.title("⚙️ Setup")
api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password")
if not api_key:
    api_key = st.secrets.get("OPENAI_API_KEY", "")

if not api_key:
    st.warning("👈 Please enter your OpenAI API key in the sidebar to start!")
    st.stop()

client = openai.OpenAI(api_key=api_key)

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# App Tabs
tab1, tab2 = st.tabs(["🔍 Vibe & Mood Decoder", "⚖️ Text Argument Settler"])

# TAB 1: VIBE & MOOD DECODER
with tab1:
    st.header("🔍 Decode Text & Mood")
    st.write("Find out what the other person is *actually* feeling behind their texts.")
    
    input_type = st.radio("Input method:", ["Type/Paste Text", "Upload Screenshot"], horizontal=True, key="vibe_input")
    
    chat_text = ""
    base64_img = None
    
    if input_type == "Type/Paste Text":
        chat_text = st.text_area("Paste the text conversation here:", height=150, placeholder="Person A: Hey are you coming tonight?\nPerson B: K. Guess so.")
    else:
        uploaded_img = st.file_uploader("Upload screenshot of chat:", type=["png", "jpg", "jpeg"], key="vibe_img")
        if uploaded_img:
            base64_img = encode_image(uploaded_img)
            st.image(uploaded_img, caption="Uploaded Chat", use_column_width=True)

    if st.button("🔮 Decode Vibe & Mood", use_container_width=True):
        if not chat_text and not base64_img:
            st.error("Please provide text or an image screenshot!")
        else:
            with st.spinner("Verdict AI is reading the subtext..."):
                prompt = """Analyze this text message or chat screenshot.
Return a valid JSON object with the following keys:
{
  "detected_mood": "Short summary of their current mood (e.g. Annoyed, Flirty, Disengaged)",
  "vibe_score": 75, (0-100 engagement/vibe score)
  "passive_aggression": "Low / Medium / High",
  "real_subtext": "What they are ACTUALLY thinking or feeling behind these texts",
  "power_dynamic": "Who holds the upper hand in this conversation and why",
  "response_witty": "A clever/witty response option",
  "response_cool": "A calm/unbothered response option",
  "response_direct": "A direct/firm response option"
}"""
                try:
                    messages = [{"role": "system", "content": "You are Verdict AI, an expert social dynamics psychologist and text analyzer. Always respond in JSON."}]
                    
                    if base64_img:
                        messages.append({
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                            ]
                        })
                    else:
                        messages.append({"role": "user", "content": f"{prompt}\n\nChat:\n{chat_text}"})

                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=messages,
                        response_format={"type": "json_object"}
                    )
                    
                    data = json.loads(response.choices[0].message.content)

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

# TAB 2: TEXT ARGUMENT SETTLER
with tab2:
    st.header("⚖️ Supreme Text Court")
    st.write("Settle arguments between you and a friend based on logic, fairness, and context.")

    arg_input_type = st.radio("Input method:", ["Type/Paste Text Argument", "Upload Screenshot"], horizontal=True, key="arg_input")
    
    arg_text = ""
    arg_base64_img = None
    
    person_a = st.text_input("Person A Name:", value="Friend A")
    person_b = st.text_input("Person B Name:", value="Friend B")

    if arg_input_type == "Type/Paste Text Argument":
        arg_text = st.text_area("Paste the argument thread here:", height=150, placeholder=f"{person_a}: You said you'd be here at 8!\n{person_b}: I said *around* 8, traffic exists!")
    else:
        uploaded_arg_img = st.file_uploader("Upload screenshot of argument:", type=["png", "jpg", "jpeg"], key="arg_img")
        if uploaded_arg_img:
            arg_base64_img = encode_image(uploaded_arg_img)
            st.image(uploaded_arg_img, caption="Argument Screenshot", use_column_width=True)

    if st.button("🔨 Issue Verdict", use_container_width=True):
        if not arg_text and not arg_base64_img:
            st.error("Please provide text or a screenshot of the argument!")
        else:
            with st.spinner("Verdict AI is reviewing court evidence..."):
                prompt = f"""Act as Verdict AI, a witty, fair, and authoritative Supreme Court Judge settling a debate between {person_a} and {person_b}.
Return a valid JSON object with:
{{
  "winner": "Name of Winner ({person_a}, {person_b}, or Draw)",
  "headline": "A dramatic title for the verdict",
  "score_a": 75, (0-100 logic score for {person_a})
  "score_b": 45, (0-100 logic score for {person_b})
  "breakdown_a": "Summary of {person_a}'s argument strength",
  "breakdown_b": "Summary of {person_b}'s argument strength",
  "judge_ruling": "A hilarious yet logically sound final verdict explaining who won and why.",
  "penalty_for_loser": "A lighthearted/funny penalty for the loser."
}}"""
                try:
                    messages = [{"role": "system", "content": "You are Verdict AI. Always respond in JSON."}]
                    
                    if arg_base64_img:
                        messages.append({
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{arg_base64_img}"}}
                            ]
                        })
                    else:
                        messages.append({"role": "user", "content": f"{prompt}\n\nArgument:\n{arg_text}"})

                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=messages,
                        response_format={"type": "json_object"}
                    )
                    
                    data = json.loads(response.choices[0].message.content)

                    st.success(f"🏆 WINNER: {data.get('winner', 'Draw')}")
                    st.subheader(f"📜 {data.get('headline', 'Official Verdict')}")

                    col1, col2 = st.columns(2)
                    col1.metric(f"{person_a} Score", f"{data.get('score_a', 0)}/100")
                    col2.metric(f"{person_b} Score", f"{data.get('score_b', 0)}/100")

                    st.markdown(f"**{person_a} Breakdown:** {data.get('breakdown_a', '')}")
                    st.markdown(f"**{person_b} Breakdown:** {data.get('breakdown_b', '')}")

                    st.markdown("---")
                    st.markdown("### ⚖️ Final Judicial Verdict:")
                    st.write(data.get("judge_ruling", ""))

                    st.markdown("### 🚨 Mandatory Penalty for Loser:")
                    st.error(data.get("penalty_for_loser", ""))

                except Exception as e:
                    st.error(f"Error settling argument: {e}")
