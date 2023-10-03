from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
import uvicorn

app = FastAPI()


@app.get('/')
async def hello():
    return {
        'message': 'Hello index'
    }


@app.get('/hello/')
async def get_hello(name: str = 'world'):
    name = name.strip().title()
    return {
        'message': f'Hello {name}!'
    }


class CreateUser(BaseModel):
    name: str
    email: EmailStr


@app.post('/users/')
async def create_user(user: CreateUser):
    return {
        'message': 'success',
        'email': user.email,
        'name': user.name
    }


@app.post('/calc/add/')
async def calc(a: int, b: int):
    return {
        'a': a,
        'b': b,
        'sum': a+b,
        'multiply': a*b
    }


@app.get('/items/')
async def get_item_list():
    return ['index1', 'index2', 'index3']


@app.get('/items/latest/')
async def get_latest_item():
    return {
        'item': {
            'id': 0,
            'name': 'latest'
        }
    }


@app.get('/items/{item_id}/')
async def get_item(item_id: int):
    return {
        'item_id': item_id
    }


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
