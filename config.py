class Config(object):

    SECRET_KEY = '1652d576-484a-49fd-913a-6879acfa6ba4'

    SESSION_COOKIE_SECURE = True
    DEFAULT_THEME = None

class DevelopmentConfig(Config):
    DEBUG = True
