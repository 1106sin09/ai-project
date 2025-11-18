import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="따릉이(공유 자전거) 상위 10개 대여소 분석",
    layout="wide",
)

## 1. 데이터 로드 함수 (Streamlit Caching 적용)
# @st.cache_data를 사용하여 데이터를 한 번만 로드하고 캐싱합니다.
@st.cache_data
def load_data(file_path):
    """
    CSV 파일을 로드하고 필요한 전처리를 수행합니다.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return None

## 2. 데이터 처리 및 분석 함수
def analyze_top_stations(df):
    """
    승차/하차를 합산하여 상위 10개 대여소를 계산합니다.
    """
    
    # 1. 승차(출발) 대여소별 이용 건수 집계
    # 시작_대여소명으로 그룹화하고, 전체_건수를 합산합니다.
    ride_counts = df.groupby('시작_대여소명')['전체_건수'].sum().reset_index()
    ride_counts.columns = ['대여소명', '승차_건수']

    # 2. 하차(도착) 대여소별 이용 건수 집계
    # 종료_대여소명으로 그룹화하고, 전체_건수를 합산합니다.
    drop_counts = df.groupby('종료_대여소명')['전체_건수'].sum().reset_index()
    drop_counts.columns = ['대여소명', '하차_건수']
    
    # 3. 승차 및 하차 건수 병합 (outer join으로 모든 대여소를 포함)
    station_analysis = pd.merge(
        ride_counts, 
        drop_counts, 
        on='대여소명', 
        how='outer'
    ).fillna(0) # 승차 또는 하차만 있는 경우 0으로 채움
    
    # 4. 총 합산 건수 계산
    station_analysis['총_승하차_건수'] = (
        station_analysis['승차_건수'] + station_analysis['하차_건수']
    )
    
    # 5. 총 승하차 건수 기준 상위 10개 대여소 추출
    top_10_stations = station_analysis.sort_values(
        by='총_승하차_건수', 
        ascending=False
    ).head(10)
    
    return top_10_stations

## 3. Plotly 막대 그래프 생성 함수
def create_plotly_bar_chart(df_top10):
    """
    상위 10개 대여소의 총 승하차 건수를 Plotly 막대 그래프로 생성합니다.
    1등은 빨간색, 나머지는 파란색 그라데이션을 적용합니다.
    """
    
    # 순위 컬럼 추가
    df_top10 = df_top10.copy()
    df_top10['순위'] = np.arange(len(df_top10)) 
    
    # 색상 목록 생성
    # 1등은 빨간색 (#FF0000)
    # 2등부터는 파란색 계열 그라데이션 (2등부터 10등까지)
    
    # 파란색 그라데이션 (진한 파랑 -> 옅은 파랑)
    # Plotly의 colors.sequential.Blues에서 역순으로 9가지 색상 선택
    blue_colors = px.colors.sequential.Blues[::-1][1:] # 첫 번째(가장 밝은) 색 제외
    
    # 최종 색상 리스트: 1등 RED, 2등~10등 BLUE GRADIENT
    color_map = {0: '#FF0000'}  # 1등 (순위 0)
    
    for i, color in enumerate(blue_colors[:9]):
        color_map[i + 1] = color # 2등(순위 1)부터 10등(순위 9)까지 할당
    
    # df에 색상 컬럼 추가
    df_top10['color'] = df_top10['순위'].map(color_map)

    # Plotly Figure 생성
    fig = go.Figure(
        data=[
            go.Bar(
                x=df_top10['대여소명'], 
                y=df_top10['총_승하차_건수'],
                marker_color=df_top10['color'], # 계산된 색상 적용
                hovertemplate="<b>%{x}</b><br>총 승하차: %{y:,}건<extra></extra>",
                name="총 승하차 건수"
            )
        ]
    )
    
    # 레이아웃 설정
    fig.update_layout(
        title={
            'text': '🥇 총 승하차 건수 기준 상위 10개 따릉이 대여소',
            'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'
        },
        xaxis_title="대여소명",
        yaxis_title="총 승하차 건수 (승차 + 하차)",
        hoverlabel=dict(bgcolor="white", font_size=14),
        uniformtext_minsize=8, uniformtext_mode='hide',
        template="plotly_white"
    )

    # x축 레이블 회전
    fig.update_xaxes(tickangle=-45)

    return fig

## 4. Streamlit 메인 함수
def main():
    st.title("🚲 따릉이 데이터 상위 대여소 분석 앱")
    st.markdown("---")

    # 파일 경로 (Streamlit Cloud 환경에서 파일 접근 방식)
    # Streamlit Cloud에 배포할 때는 파일명을 직접 지정합니다.
    file_path = "chicken.csv" 
    
    df = load_data(file_path)

    if df is not None:
        
        # 1. 분석 수행
        st.subheader("📊 상위 10개 대여소 분석 결과")
        top_10_stations = analyze_top_stations(df)
        
        if top_10_stations.empty:
            st.warning("분석할 대여소 데이터가 없습니다.")
            return

        # 2. Plotly 그래프 생성
        fig = create_plotly_bar_chart(top_10_stations)
        
        # 3. Streamlit에 그래프 및 데이터 표시
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("💡 상세 데이터 테이블 (상위 10개)")
        st.dataframe(
            top_10_stations.rename(
                columns={
                    '대여소명': '대여소 이름', 
                    '승차_건수': '출발(승차) 건수', 
                    '하차_건수': '도착(하차) 건수', 
                    '총_승하차_건수': '총 합계'
                }
            ).drop(columns=['순위', 'color']),
            use_container_width=True
        )

# 앱 실행
if __name__ == "__main__":
    main()
