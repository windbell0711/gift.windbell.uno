from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import slowapi, slowapi.util
import psycopg2
import datetime
import os
import dotenv
from pydantic import BaseModel, Field
from typing import Optional, Literal, Never


dotenv.load_dotenv()


class Msg(BaseModel):
    id: Optional[int] = None
    author: str = Field(max_length=20)
    title: str = Field(max_length=50)
    content: str = Field(max_length=250)
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
        if exc_type is None:
            self.conn.rollback()
            self.cur.close()
            self.conn.close()
            print(f"Database error: {exc_type} {exc_val} {exc_tb}")
            raise HTTPException(status_code=500, detail="Internal server error") 
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        return False


if __name__ == "__main__":
    with Postgres() as pg:
        # pg.do("""INSERT INTO msgs (author, title, content) VALUES (%s, %s, %s)""", ("windbell imitater", "test2", "test222"))
        print(pg.get("SELECT * FROM msgs"))