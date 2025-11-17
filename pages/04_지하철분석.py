import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 데이터 로드 함수 수정 및 캐싱
@st.cache_data
def load_data(file_path):
    # 파일 경로를 변경하지 않고, 파일이 현재 실행 디렉토리에 있다고 가정합니다.
    # 만약 파일이 상위 디렉토리에 있다면 '../subway.1csv.csv'로 변경해야 합니다.
    # Streamlit Cloud 배포 시에는 'subway.1csv.csv'로 배포되는 것이 일반적입니다.
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"오류: 데이터 파일 '{file_path}'를 찾을 수 없습니다. 파일이 Streamlit 프로젝트 폴더에 정확히 업로드되었는지 확인해주세요.")
        st.stop()
        
    # '사용일자'를 datetime 객체로 변환합니다.
    df['사용일자'] = pd.to_datetime(df['사용일자'], format='%Y%m%d')
    # 총 승객수(승차 + 하차) 컬럼을 계산합니다.
    df['총승객수'] = df['승차총승객수'] + df['하차총승객수']
    return df

# Streamlit 앱 시작
def main():
    st.set_page_config(
        page_title="지하철 역별 승하차 분석 (2025년 10월)",
        layout="wide"
    )

    st.title("🚇 2025년 10월 지하철 역별 이용객 Top 10 분석")
    st.markdown("특정 날짜와 노선을 선택하여 해당 조건에서 이용객(승차 + 하차)이 가장 많은 상위 10개 역을 시각화합니다.")

    # 파일 경로: 사용자가 업로드한 정확한 파일명으로 지정
    file_path = "subway.1csv.csv"
    data = load_data(file_path) # 데이터 로드

    # 2. 사용자 입력 위젯 설정
    
    # 2-1. 날짜 선택
    min_date = data['사용일자'].min().date()
    max_date = data['사용일자'].max().date()
    
    # 데이터가 10월 데이터이므로, 기본값을 최신 날짜로 설정하여 사용 편의성을 높입니다.
    selected_date = st.sidebar.date_input(
        "📅 분석할 날짜를 선택하세요 (2025년 10월)",
        value=max_date, 
        min_value=min_date,
        max_value=max_date
    )

    # 2-2. 노선 선택
    all_lines = data['노선명'].unique().tolist()
    line_options = ["전체 노선"] + sorted(all_lines)
    
    selected_line = st.sidebar.selectbox(
        "🚊 노선을 선택하세요",
        options=line_options
    )

    st.sidebar.markdown(f"**선택된 조건:**")
    st.sidebar.markdown(f"- 날짜: **{selected_date}**")
    st.sidebar.markdown(f"- 노선: **{selected_line}**")

    # 3. 데이터 필터링 및 계산
    
    # 3-1. 날짜 필터링
    filtered_data = data[data['사용일자'].dt.date == selected_date]

    if filtered_data.empty:
        st.warning("선택하신 날짜에는 데이터가 없습니다.")
        return

    # 3-2. 노선 필터링
    if selected_line != "전체 노선":
        filtered_data = filtered_data[filtered_data['노선명'] == selected_line]

    if filtered_data.empty:
        st.warning(f"선택하신 날짜({selected_date})에 **{selected_line}** 데이터는 없습니다.")
        return

    # 3-3. 역별 총승객수 집계 및 Top 10 추출
    top_10_stations = filtered_data.groupby('역명')['총승객수'].sum().nlargest(10).reset_index()
    top_10_stations = top_10_stations.sort_values(by='총승객수', ascending=False)
    
    if top_10_stations.empty:
        st.info("선택된 조건에 해당하는 이용객 데이터가 충분하지 않아 Top 10을 표시할 수 없습니다.")
        return

    # Top 10 역의 노선 정보 추출 (툴팁에 표시하기 위해)
    top_10_stations['노선명'] = top_10_stations['역명'].apply(
        lambda x: ', '.join(filtered_data[filtered_data['역명'] == x]['노선명'].unique())
    )
    
    # 4. Plotly 시각화 (요청 사항 반영: 1등 빨간색, 나머지 파란색 그라데이션)
    
    # 4-1. 색상 설정 (1등 빨간색, 나머지 파란색 그라데이션)
    blue_colors = px.colors.sequential.Blues_r[1:][:9]
    custom_colors = ['#FF0000'] + blue_colors

    # 4-2. 막대그래프 생성
    fig = px.bar(
        top_10_stations,
        x='총승객수',
        y='역명',
        orientation='h',
        title=f"**{selected_date}** ({selected_line} 노선) 이용객 Top {len(top_10_stations)} 역",
        labels={
            '총승객수': '승하차 총 승객수 (명)',
            '역명': '지하철 역명'
        },
        height=600
    )
    
    # 4-3. 색상 매핑을 수동으로 적용 (순위별 색상 지정)
    fig.update_traces(
        marker_color=custom_colors[:len(top_10_stations)],
        hovertemplate=(
            "<b>역명</b>: %{y}<br>"
            "<b>총 승객수</b>: %{x:,}명<br>"
            "<b>노선</b>: %{customdata}<extra></extra>"
        ),
        customdata=top_10_stations['노선명']
    )

    # 4-4. 레이아웃 업데이트
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='lightgrey'),
        title_font_size=20
    )
    
    # 5. Streamlit에 그래프 및 데이터 표시
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📊 상위 10개 역 원본 데이터 보기"):
        st.dataframe(top_10_stations, use_container_width=True)

if __name__ == "__main__":
    main()
