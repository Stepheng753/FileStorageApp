PASSWORD_IDX = 2
DB_PATH = './database/users.db'
from datetime import datetime


def index():
    return {}

def get_key():
    return {'key': datetime.now().strftime('%Y-%m-%d')}