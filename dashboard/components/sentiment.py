import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def render_sentiment_chart(title: str, data: list[dict]):
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

    if not data:
        st.info("감성 분석 데이터가 없습니다.")
        return

    df = pd.DataFrame(data)

    df["period_start"] = pd.to_datetime(df["period_start"])
    df = df.sort_values("period_start").reset_index(drop=True)

    # 데이터가 있는 순서대로 X축을 균등하게 배치
    x = list(range(len(df)))

    date_labels = df["period_start"].dt.strftime("%Y-%m-%d").tolist()

    fig = go.Figure()

    # -------------------------
    # 보조 지표: 감성별 뉴스 개수
    # -------------------------
    fig.add_trace(
        go.Bar(
            x=x,
            y=df["positive_count"],
            name="긍정",
            marker=dict(
                color="rgba(99, 102, 241, 0.45)",
            ),
        )
    )

    fig.add_trace(
        go.Bar(
            x=x,
            y=df["negative_count"],
            name="부정",
            marker=dict(
                color="rgba(239, 68, 68, 0.45)",
            ),
        )
    )

    fig.add_trace(
        go.Bar(
            x=x,
            y=df["neutral_count"],
            name="중립",
            marker=dict(
                color="rgba(156, 163, 175, 0.45)",
            ),
        )
    )

    # -------------------------
    # 메인 지표: 감성 점수
    # -------------------------
    fig.add_trace(
        go.Scatter(
            x=x,
            y=df["sentiment_score"],
            name="감성 점수",
            mode="lines+markers",
            line=dict(
                color="#4B5563",
                width=4,
            ),
            marker=dict(
                color="#4B5563",
                size=9,
            ),
            yaxis="y2",
        )
    )

    fig.update_layout(
        barmode="stack",

        # 왼쪽 Y축
        yaxis=dict(
            title="뉴스 개수",
        ),

        # 오른쪽 Y축
        yaxis2=dict(
            title="감성 점수",
            overlaying="y",
            side="right",
            range=[0, 1],
            tickformat=".0%",
        ),

        # X축
        xaxis=dict(
            title="기간",
            tickmode="array",
            tickvals=x,
            ticktext=date_labels,
        ),

        hovermode="x unified",

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),

        margin=dict(
            l=60,
            r=80,
            t=80,
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