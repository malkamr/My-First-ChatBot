🎓 StudyMate AI

A bilingual (Arabic & English) AI study assistant built with Streamlit and powered by OpenRouter. StudyMate helps students create study schedules, plan for exams, and organize their time — all through a friendly conversational interface.


🌍 Live Demo:


(https://my-interactive-chatbot.streamlit.app/)



✨ Features


💬 Conversational AI — Full multi-turn chat with memory across the session


🌍 Bilingual — Automatically replies in the same language the user writes in (Arabic or English)


📚 Study-focused — Specialized system prompt for study planning, scheduling, and exam prep


🌐 Powered by OpenRouter — Access to free AI models with a single API key


🔑 Secure API key handling — Loaded from an environment variable, not hardcoded


🔄 Reset button — Clear the conversation and start fresh at any time


⚠️ Error handling — Clear messages for invalid keys, rate limits, and timeouts


🧩 Easy to customize — Change the model or bot personality in just two lines




📁 Project Structure

project/


│


├── app.py          # Main application — UI + API logic


└── README.md       # This file


⚙️ Requirements


Python 3.8 or higher


Streamlit


A free OpenRouter API key

🌐 How to run


pip install -r requirements.txt


streamlit run app.py 
