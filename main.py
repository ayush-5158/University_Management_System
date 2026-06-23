from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/")
def get_root():
    return {
        "messgae":"Server is running...."
    }

@app.get("/greet/{user_name}")
def greet_user(user_name:str, age:Optional[int]=0):
    return {
        "messgae": f"Good Morning {user_name} and your age is {age}."
    }