import streamlit as st

st.set_page_config(page_title="MBTI 진로 추천 💫", page_icon="🎯")

# 제목
st.title("💡 MBTI 기반 진로 추천기 🔍")
st.write("안녕! 👋 네 MBTI를 골라주면, 너한테 어울리는 진로를 추천해줄게! 😎")

# MBTI 리스트
mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# 사용자 입력
selected_mbti = st.selectbox("👉 네 MBTI를 골라줘!", mbti_types)

# MBTI별 진로 추천 사전
career_dict = {
    "INTJ": ["데이터 분석가 📊", "전략 컨설턴트 💼"],
    "INTP": ["연구원 🔬", "소프트웨어 개발자 💻"],
    "ENTJ": ["기업가 🚀", "경영 컨설턴트 📈"],
    "ENTP": ["마케팅 기획자 📣", "창업가 💡"],
    "INFJ": ["심리상담사 💬", "작가 ✍️"],
    "INFP": ["디자이너 🎨", "시인 또는 작가 📖"],
    "ENFJ": ["교사 👩‍🏫", "HR 매니저 🧑‍💼"],
    "ENFP": ["크리에이터 🎥", "이벤트 플래너 🎉"],
    "ISTJ": ["공무원 🏛️", "회계사 📘"],
    "ISFJ": ["간호사 🩺", "교직원 🏫"],
    "ESTJ": ["프로젝트 매니저 📋", "관리자 🧱"],
    "ESFJ": ["사회복지사 🤝", "고객 서비스 전문가 ☎️"],
    "ISTP": ["엔지니어 🔧", "파일럿 ✈️"],
    "ISFP": ["사진작가 📷", "플로리스트 🌸"],
    "ESTP": ["세일즈 전문가 💬", "스포츠 코치 🏀"],
    "ESFP": ["연예인 🎤", "이벤트 진행자 🎈"]
}

# 결과 출력
if selected_mbti:
    careers = career_dict[selected_mbti]
    st.subheader(f"🌟 {selected_mbti} 유형에게 어울리는 진로는?")
    st.write(f"✅ {careers[0]}")
    st.write(f"✅ {careers[1]}")
    st.success("네 성향에 딱 맞는 길을 찾아보는 것도 멋지다구! 🌈")

st.markdown("---")
st.caption("Made with ❤️ by ChatGPT")
