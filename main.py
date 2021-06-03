import uvicorn
from fastapi import FastAPI
from core.db import database
from blog.routes import blog_api
from core.fast_users import fastapi_users

app = FastAPI(title="Blog", description="Very simple blog for training school", version="0.1.0")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(blog_api, prefix="/blog", tags=["blog"])
app.include_router(fastapi_users.router, prefix="/users", tags=["users"])

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)
