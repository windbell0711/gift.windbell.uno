from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os
import datetime
from pydantic import BaseModel
from typing import Optional, Literal, Never
from dotenv import load_dotenv

load_dotenv()


class Msg(BaseModel):
    id: Optional[int] = None
    author: str
    title: str
    content: str
    created_at: datetime.datetime = datetime.datetime.now()


class Postgres:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        self.cur = self.conn.cursor()
    
    def do(self, query: str, params=None) -> None:
        self.cur.execute(query, params)
        return None
    
    def get(self, query: str, params=None) -> list:
        self.cur.execute(query, params)
        return self.cur.fetchall()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        if exc_type is None:
            return False
        raise HTTPException(status_code=500, detail=f"Database error: {exc_type} {exc_val} {exc_tb}") 


if __name__ == "__main__":
    with Postgres() as pg:
        # pg.do("""INSERT INTO msgs (author, title, content) VALUES (%s, %s, %s)""", ("windbell imitater", "test2", "test222"))
        print(pg.get("SELECT * FROM msgs"))
