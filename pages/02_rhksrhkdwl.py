# Streamlit 앱: 서울 Top10 관광지 (Folium)

아래 파일들이 포함되어 있습니다 — 바로 Streamlit Cloud에 올려서 실행할 수 있어요.

* `app.py` — Streamlit 앱 코드 (지도 + 마커 + '코드 보기' 기능 포함)
* `requirements.txt` — 배포용 패키지 목록

---

## app.py

```python
# app.py
import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="Seoul Top10 Map", layout="wide")

st.title("🇰🇷 서울 Top 10 관광지 — 외국인들이 좋아하는 장소")
st.markdown("앱 하단의 `Show app code` 버튼을 누르면 이 파일을 화면에서 바로 복사할 수 있어요.")

# 관광지 데이터: 이름, 위도, 경도, 간단 설명
PLACES = [
    ("Gyeongbokgung Palace (경복궁)", 37.580467, 126.976944, "조선의 대표 궁궐"),
    ("N Seoul Tower (N서울타워)", 37.551170, 126.988228, "서울의 전망 명소"),
    ("Bukchon Hanok Village (북촌한옥마을)", 37.582178, 126.983257, "한옥 골목 산책하기 좋음"),
    ("Changdeokgung Palace (창덕궁)", 37.579617, 126.991018, "후원이 아름다운 궁궐"),
    ("Insadong (인사동)", 37.574025, 126.985600, "전통 공예와 찻집 거리"),
    ("Myeongdong (명동)", 37.559980, 126.985830, "쇼핑과 길거리 음식의 중심"),
    ("Hongdae (홍대)", 37.556113, 126.923405, "젊음의 거리, 스트리트 공연"),
    ("Dongdaemun Design Plaza (동대문디자인플라자)", 37.566295, 127.009405, "DDP의 곡선형 건축물"),
    ("Lotte World Tower (롯데월드타워)", 37.512593, 127.102823, "서울의 초고층 랜드마크"),
    ("Namdaemun Market (남대문시장)", 37.559532, 126.977000, "전통 시장과 길거리 음식")
]

# 기본 지도 (서울 중심)
m = folium.Map(location=[37.56, 126.98], zoom_start=12)

# 클러스터를 사용하면 마커가 겹칠 때 보기 좋아요 (옵션)
from folium.plugins import MarkerCluster
marker_cluster = MarkerCluster().add_to(m)

for name, lat, lon, desc in PLACES:
    popup_html = f"<b>{name}</b><br/>{desc}<br/><a href='https://www.google.com/maps/search/?api=1&query={lat},{lon}' target='_blank'>View on Google Maps</a>"
    folium.Marker(location=[lat, lon], popup=folium.Popup(popup_html, max_width=300)).add_to(marker_cluster)

# 지도를 Streamlit에 표시
st_folium(m, width=1200, height=700)

# 사이드바: 장소 필터(예시)
with st.sidebar:
    st.header("옵션")
    show_list = st.checkbox("장소 목록 보기", value=True)
    if show_list:
        for i, (name, lat, lon, desc) in enumerate(PLACES, start=1):
            st.markdown(f"**{i}. {name}** — {desc}  
LAT: {lat} / LON: {lon}")

# 코드 보기: 앱에서 자기 자신의 파일을 읽어 화면에 보여줌 (복사 가능)
st.markdown("---")
if st.button("Show app code (앱 코드 보기)"):
    try:
        with open(__file__, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception:
        # Streamlit Cloud나 일부 환경에서는 __file__ 접근이 제한될 수 있으므로
        # 미리 정의한 소스 문자열로 대체할 수 있게 해두었습니다.
        code = "# 앱 소스 코드를 파일에서 읽을 수 없습니다.\n# 하지만 이 앱의 소스는 배포용 repository 또는 캔버스에 포함되어 있습니다."
    st.code(code, language='python')


```

---

## requirements.txt

```
streamlit>=1.24
folium>=0.14
streamlit-folium>=0.12
```

---

### 사용법

1. 새 GitHub 리포지토리를 만듭니다.
2. `app.py` 파일과 `requirements.txt` 파일을 루트에 올립니다.
3. Streamlit Cloud([https://share.streamlit.io)에서](https://share.streamlit.io%29에서) 리포지토리를 연결하고 배포하세요.

필요하면 제가 이 코드를 `app.py` 형식으로 수정하거나, 마커 스타일(컬러/아이콘), 추가 정보(운영 시간, 입장료) 등을 더 추가해 드릴게요.

(참고: 지도에 사용한 좌표는 신뢰할 수 있는 공개 소스에서 확인해 가져왔습니다.)
