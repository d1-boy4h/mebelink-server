import uvicorn
from fastapi import FastAPI

from src.api.middleware import TimingMiddleware
from src.api.routers import auth_router, projects_router

app = FastAPI()

app.include_router(projects_router)
app.include_router(auth_router)
app.add_middleware(TimingMiddleware)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', reload=True)
