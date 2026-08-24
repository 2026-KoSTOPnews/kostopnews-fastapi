import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def render_sentiment_chart(title: str, data: list[dict]):
    st.subheader(title)

    if not data:
        st.info("감성 분석 데이터가 없습니다.")
        return

    df = pd.DataFrame(data)

    df["period_start"] = pd.to_datetime(
        df["period_start"]
    )

    df = df.sort_values("period_start")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["period_start"],
            y=df["positive_count"],
            name="긍정",
            mode="lines+markers",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["period_start"],
            y=df["negative_count"],
            name="부정",
            mode="lines+markers",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["period_start"],
            y=df["neutral_count"],
            name="중립",
            mode="lines+markers",
        )
    )

    fig.update_layout(
        xaxis_title="기간",
        yaxis_title="뉴스 개수",
        hovermode="x unified",
        xaxis=dict(
            tickformat="%Y-%m-%d",
        ),
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )