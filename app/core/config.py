class Settings():
    access_secret_key: str = "hongimee_access_token_secret_key"
    refresh_secret_key: str = "hongimee_refresh_token_secret_key"
    algorithm: str = "HS256"

def get_settings():
    return Settings()
