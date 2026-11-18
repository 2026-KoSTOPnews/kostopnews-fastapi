# 🚀 KoSTOPnews FastAPI

기업별 뉴스 및 AI 분석 결과를 제공하는 REST API 서버입니다.

FastAPI와 PostgreSQL을 기반으로 기업별 뉴스, 감성 분석, 키워드 분석 데이터를 조회하고, AI를 활용한 뉴스 분석 기능을 제공합니다.

---

## 🏗️ Architecture

- **FastAPI**: API 엔드포인트 및 비즈니스 로직 처리
- **PostgreSQL (Supabase)**: 뉴스 원본 및 AI 분석 결과 저장
- **Upstage Solar**: 뉴스 감성 및 키워드 분석
- **Streamlit**: API를 활용한 분석 결과 시각화

<br/>

#### 1차 Architecture - AWS 기반 서비스 구축
<div align="center">
  <img src="https://github.com/2026-KoSTOPnews/.github/blob/main/profile/assets/architecture.png" alt="KoSTOPnews Architecture" width="700">
</div>

<br/>

#### 2차 Architecture - 배포 환경 개선 및 비용 최적화
<div align="center">
  <img src="https://github.com/2026-KoSTOPnews/.github/blob/main/profile/assets/architecture2.png" alt="KoSTOPnews Architecture2" width="700">
</div>

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Backend | FastAPI, Uvicorn |
| ORM | SQLAlchemy |
| Database | PostgreSQL, psycopg2 |
| Validation & Settings | Pydantic, Pydantic Settings |
| LLM | Upstage Solar, OpenAI SDK |
| Cache | In-memory Cache |
| Scheduler | asyncio |
| Testing | pytest, pytest-asyncio, HTTPX |
| Containerization | Docker, Docker Compose |
| CI | GitHub Actions |
| Deployment | Render |

---

## ✨ Main Features

### 1. 🏢 Company Information
- PostgreSQL에 저장된 기업 목록 조회
- 기업별 데이터 조회를 위한 API 제공

### 2. 📰 News Data
- 기업별 날짜별 뉴스 조회
- 페이지네이션을 통한 뉴스 데이터 제공
- 원문 기사 링크 제공

### 3. 🤖 AI News Analysis
- Upstage Solar LLM 기반 뉴스 감성 분석
- 뉴스 기사별 주요 키워드 추출
- Batch API를 통한 다수 뉴스 데이터 일괄 분석
- 비동기 방식의 분석 요청 처리

### 4. 📊 Analysis Results
- 기업별 일간 감성 분석 결과 조회
- 기업별 주요 키워드 조회
- KST 기준 날짜 처리

### 5. ☁️ Word Cloud
- 기업별 주요 키워드 데이터 제공
- 일간·주간·월간 단위 키워드 집계
- 뉴스 제목 및 본문 기준 키워드 데이터 제공

### 6. ⚡ Performance Optimization
- TTL 기반 인메모리 캐싱
- 데이터 특성에 따른 캐시 유효시간 차등 적용
- KST 기준 예약 스케줄에 따른 캐시 자동 무효화
- 데이터 갱신 시점을 고려한 캐시 관리
- SQLAlchemy Connection Pool 설정
- FastAPI Lifespan을 통한 DB 및 LLM 클라이언트 관리
- 데이터베이스 Health Check 제공

---

## 📂 Project Structure

```text
kostopnews-fastapi/
├── .github/
│   └── workflows/             # GitHub Actions CI
├── app/
│   ├── main.py                # FastAPI 애플리케이션 진입점
│   ├── core/
│   │   ├── cache.py           # TTL 기반 캐시
│   │   ├── cache_scheduler.py # 예약 스케줄 기반 캐시 무효화
│   │   ├── config.py          # 환경 설정
│   │   ├── date.py            # KST 날짜 처리
│   │   └── lifespan.py        # 애플리케이션 생명주기 관리
│   ├── infrastructure/
│   │   ├── database.py        # DB 연결 및 세션 관리
│   │   ├── database_init.py   # 데이터베이스 초기화
│   │   ├── llm/               # LLM 클라이언트 및 프롬프트
│   │   └── models/            # SQLAlchemy ORM 모델
│   ├── router/                # API 라우터
│   ├── schema/                # Pydantic 요청 및 응답 스키마
│   └── service/               # 비즈니스 로직
├── sql/                       # SQL 스크립트
├── tests/                     # 테스트 코드
├── .env.example               # 환경변수 예시
├── Dockerfile
├── docker-compose.yml
├── docker-compose.local.yml
├── requirements.txt
├── pytest.ini
└── README.md
```

### Architecture Design

- **Router**: HTTP 요청 수신 및 API 엔드포인트 정의
- **Service**: 데이터 조회 및 분석 관련 비즈니스 로직 처리
- **Schema**: Pydantic 기반 요청 및 응답 데이터 검증
- **Infrastructure**: PostgreSQL 연결, ORM 모델 및 LLM 연동
- **Core**: 환경 설정, 캐싱, 날짜 처리 및 애플리케이션 생명주기 관리

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/companies` | 기업 목록 조회 |
| GET | `/api/companies/{company_id}/sentiment` | 기업별 감성 분석 결과 조회 |
| GET | `/api/companies/{company_id}/keywords` | 기업별 주요 키워드 조회 |
| GET | `/api/companies/{company_id}/news` | 기업별 날짜별 뉴스 조회 |
| GET | `/api/companies/{company_id}/word-cloud` | 워드 클라우드 데이터 조회 |
| POST | `/sentiment/batch` | 뉴스 감성 분석 일괄 처리 |
| POST | `/keywords/batch` | 뉴스 키워드 추출 일괄 처리 |
| GET | `/health/db` | 데이터베이스 연결 상태 확인 |

### News API Parameters

`GET /api/companies/{company_id}/news`

| Parameter | Default | Description |
|---|---|---|
| target_date | Today (KST) | 조회 날짜 |
| page | 1 | 페이지 번호 |
| size | 5 | 페이지당 뉴스 개수 (1~20) |

### Word Cloud API Parameters

`GET /api/companies/{company_id}/word-cloud`

| Parameter | Default | Description |
|---|---|---|
| target_date | Today (KST) | 조회 기준 날짜 |
| period_type | daily | 집계 기간 (daily / weekly / monthly) |
| text_type | title | 분석 대상 (title / content) |
| limit | 100 | 반환할 키워드 개수 (1~500) |

---

## ⚡ Cache Strategy

TTL 기반 인메모리 캐싱을 적용하여 반복적인 데이터베이스 조회를 줄이고 API 응답 성능을 개선합니다.

### Cache Policy

| Data | Cache Condition | TTL |
|---|---|---|
| Companies | 전체 기업 목록 | 24시간 |
| Sentiment | 어제 날짜 데이터 | 1시간 |
| Keywords | 어제 날짜 데이터 | 1시간 |
| News | 오늘 및 어제 데이터 | 10분 |
| Word Cloud | 어제 날짜 데이터 | 1시간 |

### Cache Invalidation Scheduler

KST 기준 예약된 시간에 캐시를 무효화하여 데이터 갱신 시점에 맞춰 최신 조회 결과를 반영합니다.

| Cache Type | Invalidation Schedule (KST) |
|---|---|
| News | 매시 15분, 25분, 35분 |
| Word Cloud | 매일 01:50 |
| Sentiment | 매일 03:50 |
| Keywords | 매일 04:50 |

- 데이터 유형별 캐시 독립 관리
- 예약된 시간에 따른 자동 캐시 무효화
- 데이터 갱신 시점을 고려한 캐시 갱신 일정 관리

---

## 🔐 Environment Variables

프로젝트 실행을 위해 루트 디렉터리에 `.env` 파일을 생성하고 환경변수를 설정합니다.

| Variable | Description |
|---|---|
| `POSTGRES_HOST` | PostgreSQL 호스트 |
| `POSTGRES_PORT` | PostgreSQL 포트 |
| `POSTGRES_DB` | 데이터베이스 이름 |
| `POSTGRES_USER` | 데이터베이스 사용자 |
| `POSTGRES_PASSWORD` | 데이터베이스 비밀번호 |
| `UPSTAGE_API_KEY` | Upstage Solar API 인증 키 |

실제 운영 환경에서는 Render의 환경변수 설정을 사용합니다.

---

## 🚀 Getting Started

### Requirements

- Python 3.10+
- PostgreSQL

### Installation

1. 저장소 클론

```bash
git clone https://github.com/2026-KoSTOPnews/kostopnews-fastapi.git
cd kostopnews-fastapi
```

2. 가상환경 생성 및 활성화

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

3. 의존성 설치

```bash
pip install -r requirements.txt
```

4. 환경변수 설정

```bash
# Windows PowerShell
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

`.env` 파일에 데이터베이스 연결 정보와 필요한 API Key를 설정합니다.

### Run Server

```bash
uvicorn app.main:app --reload
```

서버 실행 후 다음 주소에서 API 문서를 확인할 수 있습니다.

- API Server: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## 🧪 Testing

pytest를 활용하여 애플리케이션의 주요 기능을 테스트합니다.

- **Service Tests**: 서비스 로직 테스트
- **Cache Tests**: 캐시 동작 테스트
- **Lifespan Tests**: 애플리케이션 시작 및 종료 시 리소스 관리 테스트
- **Router Tests**: API 엔드포인트 테스트

### Run Tests

```bash
pytest
```

### Run Integration Tests

실제 외부 API를 호출하는 테스트는 `integration` 마커로 구분합니다.

```bash
pytest -m integration
```

---

## 🔄 CI

GitHub Actions를 활용하여 코드 변경 시 자동으로 테스트 및 애플리케이션 실행 검증을 수행합니다.

### CI Workflow

- `main` 브랜치 Push 및 Pull Request 시 CI 실행
- PostgreSQL 17 기반 테스트 환경 구성
- 테스트 데이터베이스 스키마 초기화
- FastAPI Lifespan 테스트
- Integration 테스트를 제외한 테스트 실행
- Uvicorn 서버 실행 및 DB Health Check
- OpenAPI 문서 엔드포인트 확인

---

## ☁️ Deployment

FastAPI 서버는 Render Web Service를 통해 배포 및 운영합니다.

- **Hosting**: Render Web Service
- **Database**: Supabase PostgreSQL
- **Deployment**: GitHub Repository 연동
- **Configuration**: Render 환경변수 관리

### Start Command

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
