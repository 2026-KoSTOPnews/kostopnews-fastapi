import streamlit as st

from api import get_news_by_date

def render_news(company_id: int, selected_date, page_size: int = 5):
    st.html(
        """
        <div style="
            font-size: 1.7rem;
            font-weight: 700;
            line-height: 1.3;
            margin-bottom: 1rem;
        ">
            📰 뉴스
        </div>
        """
    )

    if (
        st.session_state.get("news_company_id") != company_id
        or st.session_state.get("news_date") != selected_date
    ):
        st.session_state.news_company_id = company_id
        st.session_state.news_date = selected_date
        st.session_state.news_page = 1
        st.session_state.news_list = []
        st.session_state.news_has_next = False

    if not st.session_state.news_list:
        result = get_news_by_date(
            company_id,
            selected_date,
            page=1,
            size=page_size,
        )

        st.session_state.news_list = result["items"]
        st.session_state.news_has_next = result["has_next"]

    news_list = st.session_state.news_list

    if not news_list:
        st.info("해당 날짜에 수집된 뉴스가 없습니다.")
        return

    for news in news_list:
        pub_date = news["pub_date"].replace("T", " ")

        sentiment = news["sentiment"]

        if sentiment == "positive":
            sentiment_color = "#E8F5E9"
            sentiment_text_color = "#2E7D32"
            sentiment_label = "긍정"
        elif sentiment == "negative":
            sentiment_color = "#FFEBEE"
            sentiment_text_color = "#C62828"
            sentiment_label = "부정"
        else:
            sentiment_color = "#F5F5F5"
            sentiment_text_color = "#616161"
            sentiment_label = "중립"

        st.html(
            f"""
            <style>
                .news-title {{
                    color: inherit;
                    text-decoration: none;
                }}

                .news-title:hover {{
                    color: #1976D2;
                }}
            </style>

            <div style="
                display: flex;
                align-items: center;
                gap: 14px;
                margin-bottom: 1rem;
            ">
                <span style="
                    background-color: {sentiment_color};
                    color: {sentiment_text_color};
                    padding: 5px 11px;
                    border-radius: 999px;
                    font-size: 0.9rem;
                    font-weight: 600;
                    white-space: nowrap;
                ">
                    {sentiment_label}
                </span>

                <a href="{news['link']}"
                   target="_blank"
                   title="원문 기사 보기"
                   class="news-title"
                   style="
                       font-size: 1.5rem;
                       font-weight: 700;
                       line-height: 1.3;
                   ">
                    {news['title']}
                </a>

                <div style="
                    align-self: flex-end;
                    color: #888;
                    font-size: 0.85rem;
                    white-space: nowrap;
                ">
                    {pub_date}
                </div>
            </div>
            """
        )

        # 키워드
        if news["keywords"]:
            st.write(
                " ".join(
                    f"`#{keyword}`"
                    for keyword in news["keywords"]
                )
            )

        # AI 요약
        if news["summary"]:
            st.markdown(
                """
                <div style="
                    font-size: 1.1rem;
                    font-weight: 600;
                    margin-top: 1rem;
                    margin-bottom: 0.5rem;
                ">
                    기사 핵심 내용
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write(news["summary"])

        st.divider()

    if st.session_state.news_has_next:
        if st.button("더 보기"):
            next_page = st.session_state.news_page + 1

            result = get_news_by_date(
                company_id,
                selected_date,
                page=next_page,
                size=page_size,
            )

            st.session_state.news_list.extend(
                result["items"]
            )

            st.session_state.news_page = next_page
            st.session_state.news_has_next = result["has_next"]

            st.rerun()