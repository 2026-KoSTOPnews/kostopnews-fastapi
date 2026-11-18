
from sqlalchemy import text
from sqlalchemy.engine import Engine


def initialize_companies(engine: Engine):
    query = text("""
        INSERT INTO companies (name, name_kr, ticker, sector, aliases)
        VALUES
        (:name, :name_kr, :ticker, :sector, :aliases)
        ON CONFLICT (name) DO NOTHING
    """)

    companies = [
        {
            "name": "삼성전자",
            "name_kr": "삼성전자",
            "ticker": "005930.KS",
            "sector": "반도체",
            "aliases": [
                "삼성전자", "Samsung Electronics", "삼성", "Samsung",
                "삼성전자(005930)", "Samsung Elec", "SSNLF",
            ],
        },
        {
            "name": "SK하이닉스",
            "name_kr": "SK하이닉스",
            "ticker": "000660.KS",
            "sector": "반도체",
            "aliases": [
                "SK하이닉스", "하이닉스", "SK Hynix", "SK hynix",
                "SK하이닉스(000660)", "Hynix",
            ],
        },
        {
            "name": "현대차",
            "name_kr": "현대자동차",
            "ticker": "005380.KS",
            "sector": "자동차",
            "aliases": [
                "현대차", "현대자동차", "Hyundai Motor", "Hyundai",
                "Hyundai Motor Company", "현대차(005380)",
            ],
        },
        {
            "name": "기아",
            "name_kr": "기아",
            "ticker": "000270.KS",
            "sector": "자동차",
            "aliases": [
                "기아", "기아자동차", "Kia", "Kia Motors",
                "KIA", "기아(000270)",
            ],
        },
        {
            "name": "LG에너지솔루션",
            "name_kr": "LG에너지솔루션",
            "ticker": "373220.KS",
            "sector": "배터리",
            "aliases": [
                "LG에너지솔루션", "LG Energy Solution", "LGES",
                "LG엔솔", "LG Energy", "LG에너지솔루션(373220)",
            ],
        },
        {
            "name": "삼성SDI",
            "name_kr": "삼성SDI",
            "ticker": "006400.KS",
            "sector": "배터리",
            "aliases": [
                "삼성SDI", "Samsung SDI",
                "삼성 SDI", "SDI", "삼성SDI(006400)",
            ],
        },
        {
            "name": "삼성전기",
            "name_kr": "삼성전기",
            "ticker": "009150.KS",
            "sector": "전자부품",
            "aliases": [
                "삼성전기", "Samsung Electro-Mechanics",
                "SEMCO", "삼성전기(009150)",
            ],
        },
        {
            "name": "LG이노텍",
            "name_kr": "LG이노텍",
            "ticker": "011070.KS",
            "sector": "전자부품",
            "aliases": [
                "LG이노텍", "LG Innotek",
                "LG이노텍(011070)",
            ],
        },
        {
            "name": "한화에어로스페이스",
            "name_kr": "한화에어로스페이스",
            "ticker": "012450.KS",
            "sector": "방산",
            "aliases": [
                "한화에어로스페이스", "Hanwha Aerospace",
                "한화에어로", "한화에어로스페이스(012450)",
            ],
        },
        {
            "name": "SK텔레콤",
            "name_kr": "SK텔레콤",
            "ticker": "017670.KS",
            "sector": "통신",
            "aliases": [
                "SK텔레콤", "SK Telecom", "SKT",
                "SK텔레콤(017670)",
            ],
        },
    ]

    with engine.begin() as connection:
        connection.execute(query, companies)