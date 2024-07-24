import os
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass

load_dotenv(find_dotenv())


@dataclass
class VkSettings:
    api_token: str = os.getenv("VK_API_TOKEN")


vk_settings = VkSettings()