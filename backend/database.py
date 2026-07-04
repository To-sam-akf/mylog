from os import getenv
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import text
from sqlmodel import Session, create_engine

load_dotenv()

MYSQL_HOST = getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = getenv("MYSQL_PORT", "3306")
MYSQL_USER = getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = quote_plus(getenv("MYSQL_PASSWORD", "root"))
MYSQL_DATABASE = getenv("MYSQL_DATABASE", "mylog")
DATABASE_ECHO = getenv("DATABASE_ECHO", "false").lower() == "true"

DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}" # 协议+用户名+密码
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"  # 数据库地址+端口+数据库名
)

engine = create_engine(DATABASE_URL, echo=DATABASE_ECHO, pool_pre_ping=True)


def get_session():
    with Session(engine) as session:
        yield session


def ping_database() -> bool:
    with Session(engine) as session:
        session.execute(text("SELECT 1"))  # 执行 SELECT 1，测试连接是否正常
    return True
