from pydantic_settings import BaseSettings, SettingsConfigDict


class VkAUthConfig(BaseSettings):
    TOKEN: str

    model_config = SettingsConfigDict(extra="ignore", env_file=".env", env_prefix="VK_AUTH_")
