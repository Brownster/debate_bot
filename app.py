import streamlit as st
import os
import json
import tempfile
import openai
from openai import OpenAI, APIError
from audio_recorder_streamlit import audio_recorder
from helpers import text_to_speech, autoplay_audio

# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
    st.stop()

client = OpenAI(api_key=api_key)

class DebateBot:
    def __init__(self, topic, stance, rounds=3):
        self.client = client
        self.topic = topic
        self.stance = stance
        self.rounds = rounds
        self.history = []
        self.feedback_list = []
        self.total_scores = {"relevance": 0, "logic": 0, "persuasiveness": 0}

    def call_openai(self, user_input=None, first_round=False):
        system_prompt = f"""
        You are an AI debate opponent. The topic is: "{self.topic}".
        The user is arguing "{self.stance}". You will argue the opposite stance.
        
        Respond ONLY with a JSON object containing:
        - ai_argument: Your main argument in 3-4 sentences
        - ai_counterargument: A rebuttal to the user's response
        - feedback: Constructive feedback on the user's argument
        - relevance_score: Integer (1-5)
        - logic_score: Integer (1-5)
        - persuasiveness_score: Integer (1-5)
        """

        messages = [{"role": "system", "content": system_prompt}]
        if not first_round and user_input:
            messages.append({"role": "user", "content": user_input})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                response_format={"type": "json_object"},
                messages=messages,
                max_tokens=500
            )

            if not response.choices or not response.choices[0].message:
                return None

            message_content = response.choices[0].message.content
            return json.loads(message_content) if message_content else None

        except (APIError, json.JSONDecodeError, Exception) as e:
            st.error(f"Error: {e}")
            return None

# Streamlit UI
st.title("🎤 AI Debate Bot 🗣️")

# Session state initialization
if "debate_started" not in st.session_state:
    st.session_state.debate_started = False
if "history" not in st.session_state:
    st.session_state.history = []
if "bot" not in st.session_state:
    st.session_state.bot = None
if "round" not in st.session_state:
    st.session_state.round = 1
if "total_scores" not in st.session_state:
    st.session_state.total_scores = {"relevance": 0, "logic": 0, "persuasiveness": 0}

# Debate setup section
st.markdown("### Enter Debate Topic & Choose Your Stance")
col1, col2 = st.columns([3, 1])

with col1:
    debate_topic = st.text_input("Debate Topic", placeholder="E.g., 'Volunteers are worth the money'")

with col2:
    stance = st.selectbox("Your Stance", ["For", "Against"])

# Start Debate button
if st.button("Start Debate") and debate_topic.strip():
    st.session_state.bot = DebateBot(debate_topic, stance)
    st.session_state.debate_started = True
    st.session_state.history = []
    st.session_state.round = 1
    st.session_state.total_scores = {"relevance": 0, "logic": 0, "persuasiveness": 0}

# Start debate if initialized
if st.session_state.debate_started:
    bot = st.session_state.bot
    round_num = st.session_state.round

    if round_num == 1 and not st.session_state.history:
        ai_response = bot.call_openai(first_round=True)
        if ai_response:
            st.session_state.history.append(("AI", ai_response["ai_argument"]))
            st.session_state.round += 1

    for speaker, text in st.session_state.history:
        with st.chat_message("assistant" if speaker == "AI" else "user"):
            st.markdown(text)

    # Microphone Integration
    audio_bytes = audio_recorder()
    if audio_bytes:
        st.spinner("Transcribing...")
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_audio.write(audio_bytes)
        temp_audio.close()

        # Whisper Speech-to-Text
        with open(temp_audio.name, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                response_format="text",
                file=audio_file
            )

        if transcript:
            user_input = transcript
            os.remove(temp_audio.name)

            with st.chat_message("user"):
                st.markdown(user_input)

            ai_response = bot.call_openai(user_input=user_input)
            if ai_response:
                with st.chat_message("assistant"):
                    st.markdown(ai_response["ai_counterargument"])

                # Save interaction history
                st.session_state.history.append(("User", user_input))
                st.session_state.history.append(("AI", ai_response["ai_counterargument"]))

                # Store scores
                st.session_state.total_scores["relevance"] += ai_response["relevance_score"]
                st.session_state.total_scores["logic"] += ai_response["logic_score"]
                st.session_state.total_scores["persuasiveness"] += ai_response["persuasiveness_score"]

                # Generate AI Voice Response
                st.spinner("Generating AI audio response...")
                audio_response = text_to_speech(ai_response["ai_counterargument"])
                autoplay_audio(audio_response)
                os.remove(audio_response)

                st.session_state.round += 1

    # Display results at the end
    if st.session_state.round > bot.rounds:
        st.markdown("## Debate Completed!")
        st.markdown("### Final Scores")
        st.markdown(f"**Relevance:** {st.session_state.total_scores['relevance']} / {bot.rounds * 5}")
        st.markdown(f"**Logic:** {st.session_state.total_scores['logic']} / {bot.rounds * 5}")
        st.markdown(f"**Persuasiveness:** {st.session_state.total_scores['persuasiveness']} / {bot.rounds * 5}")

        # Reset button
        if st.button("Restart Debate"):
            st.session_state.debate_started = False
            st.session_state.history = []
            st.session_state.round = 1
            st.session_state.total_scores = {"relevance": 0, "logic": 0, "persuasiveness": 0}
