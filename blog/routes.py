from typing import List
from fastapi import APIRouter, Depends, HTTPException
from core.fast_users import fastapi_users
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from user.models import User
from . import service
from .schemas import PostCreate, PostList, PostSingle

blog_api = APIRouter()

templates = Jinja2Templates(directory="templates")


@blog_api.get("/", response_model=List[PostList])
async def post_list():
    return await service.get_post_list()


@blog_api.get("/posts2", response_model=List[PostList])
async def posts_user(request: Request):
    posts = await service.get_post_list()
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})


@blog_api.post("/", status_code=201, response_model=PostSingle)
async def post_create(item: PostCreate, user: User = Depends(fastapi_users.get_current_active_user)):
    return await service.create_post(item, user)


@blog_api.get("/my-posts", response_model=List[PostList])
async def posts_user(user: User = Depends(fastapi_users.get_current_active_user)):
    return await service.get_post_list_user(user)


@blog_api.get("/{pk}", response_model=PostSingle)
async def post_single(pk: int):
    post = await service.get_post(pk)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@blog_api.get("/children/{pk}", response_model=List[PostList])
async def post_children(pk: int):
    post = await service.get_post_list_children(pk)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@blog_api.put("/{pk}", status_code=201, response_model=PostSingle)
async def post_create(
        pk: int, item: PostCreate, user: User = Depends(fastapi_users.get_current_active_user)
):
    return await service.update_post(pk, item, user)


@blog_api.delete("/{pk}", status_code=204)
async def post_create(pk: int, user: User = Depends(fastapi_users.get_current_active_user)):
    return await service.delete_post(pk, user)
