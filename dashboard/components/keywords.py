import streamlit as st
import plotly.graph_objects as go

def render_keywords_chart(title: str, keywords: list[dict]):
    st.html(
        f"""
        <div style="
            font-size: 1.7rem;
            font-weight: 700;
            line-height: 1.3;
            margin-top: 0.5rem;
        ">
            {title}
        </div>
        """
    )

    if not keywords:
        st.info("키워드 데이터가 없습니다.")
        return

    changes = [keyword["change"] for keyword in keywords]
    counts = [keyword["count"] for keyword in keywords]

    change_colors = [
        "#2E7D32" if change > 0
        else "#C62828" if change < 0
        else "#9CA3AF"
        for change in changes
    ]

    # 전체 막대에서 증가분을 제외한 부분
    neutral_counts = [
        max(count - max(change, 0), 0)
        for count, change in zip(counts, changes)
    ]

    # 증가한 부분
    positive_counts = [
        min(max(change, 0), count)
        for count, change in zip(counts, changes)
    ]

    fig = go.Figure()

    # 1. 전체 막대의 회색 부분
    fig.add_trace(
        go.Bar(
            x=neutral_counts,
            y=[keyword["keyword"] for keyword in keywords],
            orientation="h",
            marker=dict(
                color="#F5F5F5",
            ),
            hoverinfo="skip",
        )
    )

    # 2. 증가분의 초록색 부분
    fig.add_trace(
        go.Bar(
            x=positive_counts,
            y=[keyword["keyword"] for keyword in keywords],
            orientation="h",
            marker=dict(
                color="#E8F5E9",
            ),
            hoverinfo="skip",
        )
    )

    # 3. 증감 표시
    fig.add_trace(
        go.Scatter(
            x=counts,
            y=[keyword["keyword"] for keyword in keywords],
            mode="text",
            text=[
                f"▲ {change}" if change > 0
                else f"▼ {abs(change)}" if change < 0
                else "−"
                for change in changes
            ],
            textposition="middle right",
            textfont=dict(
                size=16,
                color=change_colors,
            ),
            hoverinfo="skip",
        )
    )

    fig.update_layout(
        barmode="stack",

        xaxis=dict(
            title="횟수",
            dtick=1,
        ),

        yaxis=dict(
            title="키워드",
            autorange="reversed",
            tickfont=dict(
                size=16,
                color="#374151",
            ),
        ),

        margin=dict(
            l=60,
            r=60,
            t=20,
            b=50,
        ),
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={
            "displayModeBar": False,
        },
    )