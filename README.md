🗣️ AI Debate Bot

An interactive voice-enabled debate bot powered by OpenAI GPT-4, Whisper (Speech-to-Text), and TTS (Text-to-Speech). Users can debate any topic, choosing their stance (For/Against), and engage in a structured argument against AI. The bot provides voice and text responses, feedback, and scoring for relevance, logic, and persuasiveness.

![image](https://github.com/user-attachments/assets/d73d12a8-6162-4f58-9c54-3427de86e7f8)


🚀 Features

✅ Voice & Text Input: Speak or type your arguments.
✅ OpenAI Whisper: Converts speech to text.
✅ AI-Powered Rebuttals: GPT-4 generates structured counterarguments.
✅ OpenAI TTS: AI responses are read aloud.
✅ Real-Time Scoring: AI evaluates your arguments on relevance, logic, and persuasiveness.
✅ Debate Topic Selection: Users enter a custom debate topic.
✅ For/Against Dropdown: Choose your stance.
✅ Session History: Maintains conversation flow.
✅ Restart Debate Option: Easily start fresh.

🛠️ Setup Instructions

1️⃣ Clone the Repository

git clone https://github.com/Brownster/debate_bot.git
cd debate_bot

2️⃣ Set Up a Virtual Environment (Recommended)

python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate    # Windows

3️⃣ Install Dependencies

pip install -r requirements.txt

4️⃣ Set Up OpenAI API Key

Create a .env file and add your OpenAI API Key:

echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

Alternatively, set the API key as an environment variable:

export OPENAI_API_KEY=your_openai_api_key_here  # Mac/Linux
set OPENAI_API_KEY=your_openai_api_key_here     # Windows

5️⃣ Run the Streamlit App

streamlit run app.py

🎮 Usage

1️⃣ Open the App in your browser (http://localhost:8501).
2️⃣ Enter a Debate Topic (e.g., "AI will replace human jobs").
3️⃣ Select Stance (For/Against).
4️⃣ Press "Start Debate" to begin.
5️⃣ Respond via Text or Microphone.
6️⃣ AI Generates a Rebuttal & Reads It Aloud.
7️⃣ Continue the Debate for Multiple Rounds.
8️⃣ View Final Scores & Restart if Needed.

📝 To-Do / Known Issues

🔧 Speech not playing in first round (Workaround: Manually replay).

🎤 Improve microphone handling for better real-time interaction.

📊 Add visual feedback on scoring metrics.

🚀 Optimize debate history management.

🤝 Contributing

Pull requests are welcome! If you'd like to improve the bot or fix issues, feel free to contribute. Open an issue for discussions.

📜 License

MIT License. Feel free to use, modify, and distribute this project.

💡 Acknowledgments

OpenAI for GPT-4, Whisper, and TTS.

Streamlit for UI framework.

LangChain (if using PDF-based chatbot extension).

🚀 Enjoy debating with AI! 🗣️🤖

