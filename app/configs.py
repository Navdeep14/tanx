class Config:
    DEBUG = False
    # Other common configurations

class DevelopmentConfig(Config):
    DEBUG = True
    

class ProductionConfig(Config):
    DEBUG=False
    # Production configurations
