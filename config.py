import os

class Config(object):
    DEBUG = False
    MAX_DISTANCE_SEARCH_METERS = 10000
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SPATIAL_REFERENCE_SYSTEM_IDENTIFIER = os.environ.get('SPATIAL_REFERENCE_SYSTEM_IDENTIFIER')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/geo'
    SPATIAL_REFERENCE_SYSTEM_IDENTIFIER = 27700

class TestConfig(DevelopmentConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/geo'
    SPATIAL_REFERENCE_SYSTEM_IDENTIFIER = 27700

class DockerConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('GEODB_1_PORT_5432_TCP', '').replace('tcp://', 'http://')
    SPATIAL_REFERENCE_SYSTEM_IDENTIFIER = 27700

