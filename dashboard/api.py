import os

import requests

API_URL = os.getenv("FASTAPI_URL")

def get_companies():
    response = requests.get(f"{API_URL}/api/companies")
    response.raise_for_status()
    return response.json()

def get_company_sentiment(company_id: int, target_date):
    response = requests.get(
        f"{API_URL}/api/companies/{company_id}/sentiment",
        params={
            "target_date": target_date.isoformat(),
        },
    )
    response.raise_for_status()
    return response.json()

def get_news_by_date(company_id: int, target_date, page: int = 1, size: int = 5):
    response = requests.get(
        f"{API_URL}/api/companies/{company_id}/news",
        params={
            "target_date": target_date.isoformat(),
            "page": page,
            "size": size,
        },
    )
    response.raise_for_status()
    return response.json()