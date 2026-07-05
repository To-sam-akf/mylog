from sqlmodel import SQLModel, Session, select
from backend.database import engine
from backend.models.user import User
from backend.models.asset import Asset
from backend.models.life_note import LifeNote
from backend.models.work import Work, WorkPageSetting
from passlib.context import CryptContext

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def seed_life_notes():
    with Session(engine) as session:
        existing = session.exec(select(LifeNote)).first()
        if not existing:
            session.add(LifeNote(
                title="Life Notes",
                content="这里记录生活、想法和日常片段。",
                content_markdown="# Life Notes\n\n这里记录生活、想法和日常片段。",
            ))
        session.commit()

def seed_works():
    with Session(engine) as session:
        existing_setting = session.exec(select(WorkPageSetting)).first()
        if not existing_setting:
            session.add(WorkPageSetting(
                title="WORKS!",
                subtitle="CREATE · BUILD · SHOW",
                description="展示项目、作品、练习和创造过程。",
            ))

        existing_work = session.exec(select(Work)).first()
        if not existing_work:
            session.add_all([
                Work(
                    name="MYLOG!",
                    tech="Vue · FastAPI · MySQL",
                    desc="个人生活记录与作品展示网站",
                    status="BUILDING",
                    github="https://github.com/xxx/mylog",
                    color="yellow",
                    sort_order=1,
                ),
                Work(
                    name="MARKET ANA!",
                    tech="FastAPI · MySQL · LLM",
                    desc="期货文章观点提取与趋势分析平台",
                    status="IN PROGRESS",
                    github="https://github.com/xxx/marketAna",
                    color="blue",
                    sort_order=2,
                ),
                Work(
                    name="AI RESEARCH!",
                    tech="Multi-modal · LLM",
                    desc="多模态研究与 AI 应用实验",
                    status="RESEARCH",
                    github="https://github.com/xxx/ai-research",
                    color="pink",
                    sort_order=3,
                ),
                Work(
                    name="VUE DEMOS!",
                    tech="Vue · TypeScript",
                    desc="前端交互与界面练习合集",
                    status="DEMO",
                    github="https://github.com/xxx/vue-demos",
                    color="green",
                    sort_order=4,
                ),
            ])
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
    seed_life_notes()
    seed_works()
    seed_admin_user()

if __name__ == "__main__":
    init_db()
