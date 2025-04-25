from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.utils.config_loader import load_config

Base = declarative_base()

class TwitterUser(Base):
    __tablename__ = 'twitter_users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(255), nullable=False)

class TwitterData(Base):
    __tablename__ = 'twitter_data'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    user_name = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    create_time = Column(DateTime, default=func.now(), nullable=False)
    update_time = Column(DateTime, default=func.now(), nullable=False)

# 加载配置
config = load_config()
engine = create_engine(
    f"mysql+pymysql://{config['database']['username']}:{config['database']['password']}@"
    f"{config['database']['host']}:{config['database']['port']}/{config['database']['dbname']}"
)
Session = sessionmaker(bind=engine)
session = Session()