import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# --- 페이지 설정 ---
st.set_page_config(
    page_title="따릉이(공유 자전거) 상위 10개 대여소 분석",
    layout="wide",
)

DATA_FILE_PATH = "chicken.csv" 

# --- 1. 데이터 로드 함수 (Streamlit Caching 적용) ---
@st.cache_data
def load_data(file_path):
    """
    CSV 파일을 로드하고 필요한 전처리를 수행합니다.
    """
    if not os.path.exists(file_path):
        # 파일이 없을 경우 오류 메시지 출력 후 None 반환
        st.error(f"데이터 파일 '{file_path}'을(를) 찾을 수 없습니다. app.py와 함께 파일을 업로드했는지 확인해주세요.")
        return None
        
    try:
        df = pd.read_csv(file_path)
        df['전체_건수'] = pd.to_numeric(df['전체_건수'], errors='coerce').fillna(0).astype(int)
        return df
    except Exception as e:
        st.error(f"데이터 로드 및 처리 중 오류 발생: {e}")
        return None

# --- 2. 데이터 처리 및 분석 함수 ---
def analyze_top_stations(df):
    """
    승차/하차를 합산하여 상위 10개 대여소를 계산합니다.
    """
    ride_counts = df.groupby('시작_대여소명')['전체_건수'].sum().reset_index()
    ride_counts.columns = ['대여소명', '승차_건수']
    drop_counts = df.groupby('종료_대여소명')['전체_건수'].sum().reset_index()
    drop_counts.columns = ['대여소명', '하차_건수']
    
    station_analysis = pd.merge(ride_counts, drop_counts, on='대여소명', how='outer').fillna(0)
    station_analysis['총_승하차_건수'] = station_analysis['승차_건수'].astype(int) + station_analysis['하차_건수'].astype(int)
    
    # 상위 10개 추출
    top_10_stations = station_analysis.sort_values(
        by='총_승하차_건수', ascending=False
    ).head(10).reset_index(drop=True)
    
    return top_10_stations

# --- 3. Plotly 막대 그래프 생성 함수 (색상 요구사항 적용) ---
def create_plotly_bar_chart(df_top10):
    df_top10 = df_top10.copy()
    df_top10['순위'] = df_top10.index
    
    # 1등은 빨간색 (#FF0000)
    # 2등부터는 파란색 계열 그라데이션 (Plotly Blues_r 역순)
    blue_colors = px.colors.sequential.Blues_r[1:] 
    color_list = ['#FF0000'] + blue_colors[:9]
    df_top10['color'] = df_top10['순위'].apply(lambda x: color_list[x])

    fig = go.Figure(
        data=[
            go.Bar(
                x=df_top10['대여소명'], 
                y=df_top10['총_승하차_건수'],
                marker_color=df_top10['color'],
                hovertemplate="<b>%{x}</b><br>총 승하차: %{y:,}건<extra>순위 %{customdata[0]}</extra>",
                customdata=df_top10[['순위']].values + 1,
                name="총 승하차 건수",
                text=df_top10['총_승하차_건수'].apply(lambda x: f'{x:,}'),
                textposition='auto'
            )
        ]
    )
    
    fig.update_layout(
        title={'text': '🥇 총 승하차 건수 기준 상위 10개 따릉이 대여소', 'y':0.95, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top', 'font': {'size': 20}},
        xaxis_title="대여소명",
        yaxis_title="총 승하차 건수 (승차 + 하차)",
        template="plotly_white",
        yaxis=dict(tickformat=',d'),
    )
    fig.update_xaxes(tickangle=-45)

    return fig

# --- 4. Streamlit 메인 함수 ---
def main():
    st.title("🚲 따릉이 데이터 상위 대여소 분석 앱")
    st.markdown("---")

    df = load_data(DATA_FILE_PATH)

    if df is not None:
        
        st.subheader("📊 상위 10개 대여소 분석 결과")
        top_10_stations = analyze_top_stations(df)
        
        if top_10_stations.empty:
            st.warning("분석할 유효한 대여소 데이터가 없습니다.")
            return

        fig = create_plotly_bar_chart(top_10_stations)
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

if __name__ == "__main__":
    main()
