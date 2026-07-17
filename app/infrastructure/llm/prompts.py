def sentiment_prompt(company, title, content):
    return f"""
당신은 금융 뉴스를 분석하는 AI입니다.

목표:
아래 기사를 읽고 기업 "{company}"에 미치는 영향을 분석하세요.

분석 기준:
- 반드시 기업 "{company}" 관점에서 판단하세요.
- 기사 전체 분위기가 아닌 기업 가치에 미치는 영향을 평가하세요.

감성 기준:
- positive: 기업 가치에 긍정적인 영향
- neutral: 영향이 거의 없거나 판단이 어려움
- negative: 기업 가치에 부정적인 영향

기사 제목:
{title}

기사 본문:
{content}

다음 JSON 형식으로만 응답하세요.

{{
  "summary": "기사 핵심 사실을 2~3문장으로 요약",
  "sentiment": "positive | neutral | negative",
  "score": 0.0,
  "reason": "감성 판단 핵심 이유 (20자 이내)"
}}

score 기준:
- 1.0: 매우 긍정적
- 0.75: 긍정적
- 0.5: 중립
- 0.25: 부정적
- 0.0: 매우 부정적

주의:
- summary는 객관적인 사실 중심으로 작성하세요.
- reason은 기업 영향 판단의 핵심 근거만 작성하세요.
"""