from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.app import router as app_routes
from api.users import router as users_routes
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")


app = FastAPI(
    title="NPK MONITOR",
    description=("NPK"),
    version="1.0.0",
    terms_of_service="https://example.com/terms/",
    contact={
        "name": "SOEIL",
        "url": "https://soeil.ir",
        "email": "soheilnaderii1@gmai.com",
    },
    lifespan=lifespan,
    #openapi_tags=tags_metadata,
)

#TODO Have CORS MISCONFIGURATION 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(app_routes, prefix="/api/v1")
app.include_router(users_routes, prefix="/api/v1")

@app.get("/public")
def public_route():
    return {"message": "this is public route"}