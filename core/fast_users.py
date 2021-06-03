from fastapi_users import FastAPIUsers
from user.logic import user_db, auth_backends, SECRET
from user.schemas import User, UserCreate, UserUpdate, UserDB

fastapi_users = FastAPIUsers(
    user_db,  # об'єкт користувач
    auth_backends,  # список наших методів авторизації, в нашому випадку JWT auth
    User,
    UserCreate,
    UserUpdate,
    UserDB,
    SECRET,  # secret key
)
