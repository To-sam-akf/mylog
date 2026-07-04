from sqlmodel import SQLModel, Session, select
from backend.database import engine
from backend.models.page import Page
from backend.models.user import User
from backend.models.page_version import PageVersion
from backend.models.asset import Asset
from passlib.context import CryptContext

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def seed_pages():
    with Session(engine) as session:
        existing = session.exec(select(Page).where(Page.slug == "life-notes")).first()
        if not existing:
            session.add(Page(
                slug="life-notes",
                title="Life Notes",
                content="<h1>Life Notes</h1><p>这里记录生活、想法和日常片段。</p>",
                content_markdown="# Life Notes\n\n这里记录生活、想法和日常片段。",
            ))
        existing = session.exec(select(Page).where(Page.slug == "works")).first()
        if not existing:
            session.add(Page(
                slug="works",
                title="Works",
                content="<h1>Works</h1><p>这里记录我的作品和项目。</p>",
                content_markdown="# Works\n\n这里记录我的作品和项目。",
            ))
        session.commit()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_admin_user():
    with Session(engine) as session:
        existing=session.exec(select(User).where(User.username=="admin")).first()
        if not existing:
            # 添加管理者
            session.add(User(
                username="admin",
                password_hash=pwd_context.hash("admin123"),
                role="admin"
            ))
        session.commit()

def init_db():
    create_db_and_tables()
    seed_pages()
    seed_admin_user()

if __name__ == "__main__":
    init_db()