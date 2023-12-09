from pydantic_settings import BaseSettings


class Config(BaseSettings):
    number_of_consumers: int = 1


config = Config()
