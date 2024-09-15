from pydantic_settings import BaseSettings, SettingsConfigDict

from smm_vk.configs.vk_auth import VkAUthConfig


class ConfigMain(BaseSettings):
    vk_auth: VkAUthConfig = VkAUthConfig()

    model_config = SettingsConfigDict(env_file_encoding="utf-8", extra="ignore", env_file=".env")


config = ConfigMain()