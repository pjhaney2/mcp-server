#!/usr/bin/env python3

import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="MCP Server Health Check")

@app.get("/")
async def root():
    return {"message": "MCP Server is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "server": "MCP Demo Server"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)