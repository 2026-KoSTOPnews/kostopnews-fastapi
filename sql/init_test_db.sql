-- 기업 정보
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    name_kr TEXT,
    ticker TEXT,
    sector TEXT,
    aliases TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

-- 뉴스 기사
CREATE TABLE news_articles (
    id SERIAL PRIMARY KEY,
    title TEXT,
    link TEXT UNIQUE,
    pub_date TIMESTAMP,
    source TEXT,
    content TEXT,
    company_extraction_processed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 기사와 기업 간 멘션 관계
CREATE TABLE news_mentions (
    id SERIAL PRIMARY KEY,
    article_id INT REFERENCES news_articles(id) ON DELETE CASCADE,
    company_id INT REFERENCES companies(id) ON DELETE CASCADE,
    confidence FLOAT DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (article_id, company_id)
);

-- 뉴스 감성 분석 결과
CREATE TABLE news_analysis (
    id SERIAL PRIMARY KEY,
    article_id INT NOT NULL REFERENCES news_articles(id) ON DELETE CASCADE,
    company_id INT NOT NULL REFERENCES companies(id),
    summary TEXT,
    sentiment TEXT,
    sentiment_score FLOAT,
    model_version TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT news_analysis_article_company_unique
        UNIQUE (article_id, company_id)
);

-- 기사별 키워드
CREATE TABLE news_keywords (
    id SERIAL PRIMARY KEY,
    article_id INT REFERENCES news_articles(id) ON DELETE CASCADE,
    keyword TEXT,
    model_version TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE (article_id, keyword)
);

-- 기간별 감성 분석 집계
CREATE TABLE news_sentiment_aggregate (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES companies(id) ON DELETE CASCADE,
    period_type TEXT,
    period_start TIMESTAMP,
    positive_count INT,
    negative_count INT,
    neutral_count INT,
    sentiment_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT news_sentiment_aggregate_unique
        UNIQUE (company_id, period_type, period_start)
);

-- 기간별 키워드 집계
CREATE TABLE news_keyword_aggregate (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES companies(id) ON DELETE CASCADE,
    period_type TEXT,
    period_start TIMESTAMP,
    keyword TEXT,
    count INT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT news_keyword_aggregate_unique
        UNIQUE (company_id, period_type, period_start, keyword)
);