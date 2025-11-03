import streamlit as st
st.title('나의 첫 웹 서비스 만들기!!')
name=st.text_input('이름을 압력하세요:')
t.selectbox('좋아하는 음식을 선택해 부세요:',['김치찌개','된장찌개'])
if st.button('인사말 생성'):
 st.info(name+'님! 안녕하세요')
 st.warning('반가워요')
 st. balloons()
