from app.core.config import Settings


def test_llm_settings_have_safe_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.gemini_api_key is None
    assert settings.llm_timeout_seconds > 0
