class Config(object):
    DATABASE_URI="some rando parameter"
    MERCHANT_ID="sample"
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://root@127.0.0.1/shopeasedb"#do not specify the port no
    SQLALCHEMY_TRACK_MODIFICATIONS ='true'
    MERCHANT_ID='T98765@0'
class TestConfig(Config):
    Database_url="Test Connection Parameters"