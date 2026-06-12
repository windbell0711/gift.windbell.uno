from backend.utils import *

app = FastAPI()
limiter = slowapi.Limiter(key_func=slowapi.util.get_remote_address)
app.state.limiter = limiter

# 允许前端调用（通过环境变量控制，本地 .env 为空则允许所有来源）
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").strip()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if ALLOWED_ORIGINS == "*" else ALLOWED_ORIGINS.split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"Hello": "World"}

@app.get("/msgs/")
@limiter.limit("100/day")
def get_msgs(request: Request) -> list[Msg]:
    with Postgres() as pg:
        return [
            Msg(id=r[0], author=r[1], title=r[2], content=r[3], created_at=r[4])
            for r in pg.get("SELECT * FROM msgs")
        ]

@app.post("/msgs/")
@limiter.limit("5/hour")
def create_msg(request: Request, msg: Msg) -> None:
    with Postgres() as pg:
        pg.do("""INSERT INTO msgs (author, title, content) VALUES (%s, %s, %s)""", (msg.author, msg.title, msg.content))
    return None
