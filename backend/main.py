from backend.utils import *

app = FastAPI()

# 允许前端调用（Vercel 域名或本地）
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],   # 开发阶段用 *，上线后换成你的前端域名
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/msgs/")
def get_msgs() -> list[Msg]:
    with Postgres() as pg:
        return [
            Msg(id=r[0], author=r[1], title=r[2], content=r[3], created_at=r[4])
            for r in pg.get("SELECT * FROM msgs")
        ]

@app.post("/msgs/")
def create_msg(msg: Msg) -> None:
    with Postgres() as pg:
        pg.do("""INSERT INTO msgs (author, title, content) VALUES (%s, %s, %s)""", (msg.author, msg.title, msg.content))
    return None
