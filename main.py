from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import slide_routes
from routes.slide_routes import router as slide_router


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],

)

app.include_router(slide_router)
