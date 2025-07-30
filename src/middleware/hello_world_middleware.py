from fastapi import Request

def hello_middleware(app):
    @app.middleware("http")
    async def print_hello_middleware(request: Request, call_next):
        # request.url
        print("Hello, world")
        return await call_next(request)
    return print_hello_middleware
