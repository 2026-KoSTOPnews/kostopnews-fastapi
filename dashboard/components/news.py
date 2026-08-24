import streamlit as st

from api import get_news_by_date

def render_news(company_id: int, selected_date, page_size: int = 5):
    st.subheader("📰 뉴스")

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
        st.markdown(f"### {news['title']}")

        st.caption(news["pub_date"])

        if news["summary"]:
            st.write(news["summary"])

        st.write(
            f"**감성:** {news['sentiment']}  "
            f"**점수:** {news['sentiment_score']:.2f}"
        )

        if news["keywords"]:
            st.write(
                " ".join(
                    f"`#{keyword}`"
                    for keyword in news["keywords"]
                )
            )

        with st.expander("기사 내용 보기"):
            st.write(news["content"])

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