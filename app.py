import streamlit as st

st.title("🎓 StudyMate AI")

if "step" not in st.session_state:
    st.session_state.step = 0

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("اكتب سؤالك")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    if st.session_state.step == 0:
        if "جدول" in user_input or "اذاكر" in user_input:
            reply = "تمام 👍 قولّي عندك كام مادة؟"
            st.session_state.step = 1
        elif "امتحان" in user_input:
            reply = "امتحانك كمان كام يوم؟"
            st.session_state.step = 2
        else:
            reply = "ممكن أساعدك تعمل جدول أو خطة مذاكرة 📚"

    elif st.session_state.step == 1:
        try:
            subjects = int(user_input)
            reply = f"تمام 👌 ذاكر {subjects} مواد، كل مادة ساعتين يوميًا"
        except:
            reply = "قولّي رقم بس (عدد المواد)"

    elif st.session_state.step == 2:
        try:
            days = int(user_input)
            if days <= 3:
                reply = "ركز على المراجعة السريعة"
            else:
                reply = f"عندك {days} أيام 👍 ذاكر كل يوم جزء"
        except:
            reply = "قولّي عدد الأيام بالأرقام"

    # عرض رد البوت
    with st.chat_message("assistant"):
        st.write(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

if st.button("🔄 إعادة المحادثة"):
    st.session_state.step = 0
    st.session_state.messages = []

   