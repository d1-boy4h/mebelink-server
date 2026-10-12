import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class TimingMiddleware(BaseHTTPMiddleware):
    '''Подсчёт времени выполнения запроса.'''

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()

        response = await call_next(request)

        time_diff = str(time.perf_counter() - start)
        response.headers['X-Process-Time'] = time_diff

        return response
