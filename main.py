from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.slide_routes import router as slide_router
from routes.noticias_routes import router as noticias_router


# Create FastAPI application instance
app = FastAPI()


# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
    expose_headers=["*"],  
)

# Include routers from other modules to organize API endpoints
app.include_router(slide_router) 
app.include_router(noticias_router)  
