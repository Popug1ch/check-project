import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from api import router
from models import DomainError

app = FastAPI()
app.include_router(router)

@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)