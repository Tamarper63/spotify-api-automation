# import os
#
#
# class ConfigManager:
#
#     @staticmethod
#     def get_client_id():
#         return os.getenv("SPOTIFY_CLIENT_ID")
#
#     @staticmethod
#     def get_client_secret():
#         return os.getenv("SPOTIFY_CLIENT_SECRET")
#
#     @staticmethod
#     def get_base_url() -> str:
#         return os.getenv("SPOTIFY_BASE_URL", "https://api.spotify.com/v1")
#
#     @staticmethod
#     def get_timeout() -> int:
#         return int(os.getenv("TIMEOUT", "10"))
#
#     @staticmethod
#     def get_env() -> str:
#         return os.getenv("ENV_NAME", "local")
