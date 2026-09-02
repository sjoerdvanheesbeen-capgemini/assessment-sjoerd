from fastapi import FastAPI
from fastapi.responses import JSONResponse

from postgres.api import router as postgresqlrouter
from restapi.api import router as restapirouter
app = FastAPI()

@app.get("/")
def root():
    return JSONResponse(content={"message": "Welcome to the Service Monitor API"})

@app.get("/health", tags=["health"])
def health_check():
    return JSONResponse(content={"status": "ok"})

app.include_router(postgresqlrouter, prefix="/api", tags=["api"])
app.include_router(restapirouter, prefix="/api", tags=["api"])