from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes

# Create a FastAPI application instance
app = FastAPI(
    title="AutoMicro Patch Extraction",
    version="1.0.0"
)

# Enable CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins; customize in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Register API routes from the routes module
app.include_router(routes.router)
