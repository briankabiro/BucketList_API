import os

class Config(object):
	DEBUG = False
	SECRET_KEY = os.getenv('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
	# config for app when in development mode
	DEBUG = True

class TestingConfig(Config):
	# config for the app when running tests
	TESTING = True
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')

class ProductionConfig(Config):
	# config for app when in production
	DEBUG = False
	TESTING = False

app_config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig
}
