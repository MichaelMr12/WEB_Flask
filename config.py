import os
import sys
from pprint import pprint

class Config:
    SECRET_KEY =  os.environ.get('SECRET KEY') or'dhme;kghjanrkael/jgbuilarelkjmgbipuehjmghiotrkjhtoikle'
    DEBUG = True
    DATABASE = 'bd_vk_post.db'
