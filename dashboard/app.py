from datetime import date

import streamlit as st

from api import get_companies
from api import get_company_sentiment
from components.sentiment import render_sentiment_chart
from components.news import render_news

st.set_page_config(
    page_title="News Sentiment",
    page_icon="📰",
    layout="wide",
)

st.html(
    """
    <div style="
        font-size: 3rem;
        font-weight: 700;
        line-height: 1.5;
        margin-bottom: 1.5rem;
    ">
        📰 News Sentiment Dashboard
    </div>
    """
)

companies = get_companies()

if not companies:
    st.warning("등록된 기업이 없습니다.")
    st.stop()

company = st.selectbox(
    "기업을 선택하세요",
    companies,
    format_func=lambda company: company["name"],
)

# 감성 분석
selected_date = st.date_input(
    "조회 날짜",
    value=date.today(),
)

sentiment = get_company_sentiment(company["id"], selected_date)

st.html(
    """
    <div style="margin-bottom: 2rem;"></div>
    """
)

tab_daily, tab_weekly, tab_monthly = st.tabs(
    ["일간 분석", "주간 분석", "월간 분석"]
)

with tab_daily:
    render_sentiment_chart(
        "일간 분석",
        sentiment["daily"]
    )

with tab_weekly:
    render_sentiment_chart(
        "주간 분석",
        sentiment["weekly"]
    )

with tab_monthly:
    render_sentiment_chart(
        "월간 분석",
        sentiment["monthly"]
    )

# 뉴스
st.divider()
render_news(
    company["id"],
    selected_date,
)