# Use a lightweight Python 3.11 base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system-level dependencies required by OpenSlide, Pillow, and general builds
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libopenslide-dev \
    openslide-tools \
    build-essential \
    gcc \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy the entire application directory into the container
COPY automicro-dataprocessor /app
# Upgrade pip and install Python dependencies from requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
# Expose the FastAPI application's port
EXPOSE 8002
# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
