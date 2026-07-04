from sqlmodel import SQLModel, Session, select

from backend.database import engine
from backend.models.page import Page

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
    
def init_db():
    create_db_and_tables()
    seed_pages()

if __name__ == "__main__":
    init_db()