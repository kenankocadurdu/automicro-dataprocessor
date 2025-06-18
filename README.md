# AutoMicro Dataprocessor

**AutoMicro Dataprocessor** is a high-performance, container-ready FastAPI service for **digital pathology** and **Whole Slide Image (WSI)** processing. It provides robust APIs for patch extraction, WSI manipulation, and cloud storage integration with **MinIO** or **AWS S3**.

## Features

### Whole Slide Image Processing
- Efficiently reads and processes large WSI files using **TIA Toolbox** and **OpenSlide**.
- Multi-resolution support via pyramid level selection.

### Patch Extraction
- Extracts patches at given coordinates or default regions.
- Supports multiple output formats (PNG, JPEG, etc.).

### Cloud Integration
- Uploads and downloads files to/from **MinIO** or **S3-compatible** storage.
- Uses structured object keys for organization.

### Data Validation
- Enforces input schemas using **Pydantic v2**.

### FastAPI + Uvicorn
- Asynchronous and production-ready by default.

### 📦 Docker-Ready
- Comes with a `Dockerfile` for easy deployment on local or cloud environments.
