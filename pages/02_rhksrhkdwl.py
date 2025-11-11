# Streamlit 앱: 서울 Top10 관광지 (Folium)

서울의 외국인 인기 관광지 10곳을 지도에 표시하고, 아래에는 각 명소와 인근 전철역 정보를 함께 소개합니다.

---

## 📁 app.py

```python
# app.py
import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import MarkerCluster

st.set_page_config(page_title="Seoul Top10 Map", layout="wide")

st.title("🇰🇷 서울 Top 10 관광지 — 외국인들이 사랑하는 명소")
st.markdown("지도는 전체 화면의 약 80% 크기로 표시됩니다. 아래에는 각 명소와 주변 전철역 정보가 함께 나와요.")

# 관광지 데이터 (명소명, 위도, 경도, 설명, 가까운 전철역)
PLACES = [
    ("Gyeongbokgung Palace (경복궁)", 37.580467, 126.976944, "조선의 대표 궁궐", "경복궁역 5호선"),
    ("N Seoul Tower (N서울타워)", 37.551170, 126.988228, "서울 전경을 한눈에 볼 수 있는 전망대", "명동역 4호선"),
    ("Bukchon Hanok Village (북촌한옥마을)", 37.582178, 126.983257, "한옥 골목길을 따라 전통미를 느낄 수 있는 마을", "안국역 3호선"),
    ("Changdeokgung Palace (창덕궁)", 37.579617, 126.991018, "유네스코 세계문화유산에 등재된 궁궐", "안국역 3호선"),
    ("Insadong (인사동)", 37.574025, 126.985600, "전통 공예품과 찻집 거리", "종로3가역 1·3·5호선"),
    ("Myeongdong (명동)", 37.559980, 126.985830, "서울의 대표 쇼핑 거리", "명동역 4호선"),
    ("Hongdae (홍대)", 37.556113, 126.923405, "젊음의 거리, 음악과 예술의 중심", "홍대입구역 2호선·공항철도"),
    ("Dongdaemun Design Plaza (DDP)", 37.566295, 127.009405, "미래적 건축미를 자랑하는 디자인 명소", "동대문역사문화공원역 2·4·5호선"),
    ("Lotte World Tower (롯데월드타워)", 37.512593, 127.102823, "123층 초고층 전망대와 쇼핑 복합단지", "잠실역 2·8호선"),
    ("Namdaemun Market (남대문시장)", 37.559532, 126.977000, "서울의 전통 시장과 길거리 음식", "회현역 4호선")
]

# 기본 지도 생성 (컬러맵 스타일 적용)
m = folium.Map(location=[37.56, 126.98], zoom_start=12, tiles='CartoDB positron')

# 마커 클러스터 추가
marker_cluster = MarkerCluster().add_to(m)

# 관광지 및 전철역 마커 표시
for name, lat, lon, desc, station in PLACES:
    popup_html = f"""
    <b>{name}</b><br/>{desc}<br/>🚇 가까운 전철역: {station}<br/>
    <a href='https://www.google.com/maps/search/?api=1&query={lat},{lon}' target='_blank'>📍 Google Maps에서 보기</a>
    """
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.Icon(color='black', icon='info-sign')
    ).add_to(marker_cluster)

# 지도 표시 (80% 크기로 조정)
st.markdown("---")
st_folium(m, width=960, height=560)

# 사이드바: 옵션
with st.sidebar:
    st.header("옵션")
    if st.checkbox("장소 목록 보기", value=True):
        for i, (name, lat, lon, desc, station) in enumerate(PLACES, start=1):
            st.markdown(f"**{i}. {name}** — {desc}  
🚇 {station}  
LAT: {lat} / LON: {lon}")

# 지도 아래 관광지 소개
st.markdown("---")
st.subheader("📖 관광지 간단 소개")

for i, (name, _, _, desc, station) in enumerate(PLACES, start=1):
    st.markdown(f"**{i}. {name}** — {desc}  
👉 가까운 전철역: {station}")

# 코드 보기 버튼
st.markdown("---")
if st.button("Show app code (앱 코드 보기)"):
    try:
        with open(__file__, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception:
        code = "# 앱 소스 코드를 파일에서 읽을 수 없습니다.\n# Streamlit Cloud에서는 이 기능이 제한될 수 있습니다."
    st.code(code, language='python')
```

---

## 📄 requirements.txt

```
streamlit>=1.24
folium>=0.14
streamlit-folium>=0.12
```

---

### 🚀 사용법

1. 새 GitHub 리포지토리를 만듭니다.
2. `app.py`와 `requirements.txt` 두 파일을 루트에 업로드합니다.
3. [Streamlit Cloud](https://share.streamlit.io)에서 리포지토리를 연결하고 배포하면 완성!

📍 지도 크기는 80%로 줄였으며, 마커 색상은 검정색(`black`)으로 통일했고, 각 관광지의 가까운 전철역 정보도 함께 표시됩니다.
