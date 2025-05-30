from fastapi import FastAPI
from app.lifespan import lifespan
from routers.user_field_router import user_field_router
from routers.user_router import user_router

app = FastAPI(
    title='RWS Auth',
    description='A simple, pluggable, authentication system.',
    version='0.0.1',
    lifespan=lifespan,
)

app.include_router(user_router, prefix='/auth')
app.include_router(user_field_router, prefix='/auth')