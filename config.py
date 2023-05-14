import os
from environs import Env


class Config:
    SECRET_KEY = os.environ.get('SECRET KEY') or 'dhme;kghjanrkael/jgbuilarelkjmgbipuehjmghiotrkjhtoikle'
    DEBUG = True
    DATABASE = 'bd_vk_post.db'


def load_VK(path: str | None = None) -> Config:
    env = Env()
    env.read_env(os.path.join(path, '.env'))
    print('7777', os.path.join(path, '.env'))
    print('8888', env('VK_TOKEN'))

    return env('VK_TOKEN')


def load_BOT(path: str | None = None) -> Config:
    env = Env()
    env.read_env(os.path.join(path, '.env'))
    return env('BOT_TOKEN')
