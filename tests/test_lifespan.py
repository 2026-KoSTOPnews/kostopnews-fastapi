from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

def test_lifespan():
    with (
        patch("app.core.lifespan.create_db_engine") as mock_create_engine,
        patch("app.core.lifespan.create_llm_client") as mock_create_llm_client,
    ):
        mock_engine = mock_create_engine.return_value
        mock_llm_client = mock_create_llm_client.return_value

        with TestClient(app):
            assert app.state.engine is mock_engine
            assert app.state.SessionLocal is not None
            assert app.state.llm_client is mock_llm_client

        mock_llm_client.close.assert_called_once()
        mock_engine.dispose.assert_called_once()