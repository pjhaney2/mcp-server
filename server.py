#!/usr/bin/env python3
"""
MCP Demo Server using FastMCP
Supports both local stdio and remote streamable-http transports

This server provides calculator tools, pirate talk prompts, and PDF resources.
"""
import os
import sys
import logging
from pathlib import Path
from fastmcp import FastMCP
import uvicorn
import PyPDF2
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from starlette.routing import Route
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from datetime import datetime
from typing import Optional

from config import TOOL_CONFIGS, PROMPT_CONFIGS, RESOURCE_CONFIGS, SERVER_CONFIG
from tools.calculator import add, subtract, multiply, divide
from prompts.pirate_talk import get_pirate_prompt

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create the MCP server
mcp = FastMCP(SERVER_CONFIG["name"])

@mcp.tool()
def calculator_add(a: float, b: float) -> float:
    """Add two numbers"""
    try:
        return add(a, b)
    except Exception as e:
        logger.error(f"Error in calculator_add: {e}")
        raise ValueError("Invalid input: Please provide valid numbers")

@mcp.tool()
def calculator_subtract(a: float, b: float) -> float:
    """Subtract two numbers"""
    try:
        return subtract(a, b)
    except Exception as e:
        logger.error(f"Error in calculator_subtract: {e}")
        raise ValueError("Invalid input: Please provide valid numbers")

@mcp.tool()
def calculator_multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    try:
        return multiply(a, b)
    except Exception as e:
        logger.error(f"Error in calculator_multiply: {e}")
        raise ValueError("Invalid input: Please provide valid numbers")

@mcp.tool()
def calculator_divide(a: float, b: float) -> float:
    """Divide two numbers"""
    try:
        return divide(a, b)
    except Exception as e:
        logger.error(f"Error in calculator_divide: {e}")
        raise ValueError("Invalid input: Please provide valid numbers")

@mcp.prompt(name="pirate_talk", description="Transform text to sound like a pirate")
def pirate_talk(text: str) -> list:
    """Transform text to sound like a pirate"""
    try:
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        prompt_content = get_pirate_prompt(text.strip())
        
        return [
            {
                "role": "user", 
                "content": {
                    "type": "text",
                    "text": prompt_content
                }
            }
        ]
    except Exception as e:
        logger.error(f"Error in pirate_talk: {e}")
        raise ValueError("Invalid input: Please provide valid text")

@mcp.resource("waupaca://report")
def get_waupaca_report() -> str:
    """Get the Waupaca draft report content"""
    pdf_path = Path(__file__).parent / "resources" / "waupaca_report.pdf"
    
    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text_content = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += f"--- Page {page_num + 1} ---\n"
                text_content += page.extract_text()
                text_content += "\n\n"
            
            return text_content
    except Exception as e:
        logger.error(f"Error reading PDF: {e}")
        return f"Error reading PDF: {str(e)}"

async def health_check(request: Request):
    """Health check endpoint for monitoring."""
    return JSONResponse({
        "status": "ok", 
        "service": SERVER_CONFIG["name"],
        "version": SERVER_CONFIG["version"],
        "timestamp": datetime.now().isoformat(),
        "tools": list(TOOL_CONFIGS.keys()),
        "prompts": list(PROMPT_CONFIGS.keys()),
        "resources": list(RESOURCE_CONFIGS.keys())
    })

async def mcp_redirect(request: Request):
    """Redirect /mcp to /mcp/ for proper MCP handling."""
    # Build the redirect URL maintaining HTTPS and the same path structure
    host = request.headers.get('host', request.url.hostname)
    scheme = "https" if "run.app" in str(host) else request.url.scheme
    redirect_url = f"{scheme}://{host}/mcp/"
    return RedirectResponse(url=redirect_url, status_code=307)

class SecurityMiddleware(BaseHTTPMiddleware):
    """Security middleware following MCP best practices."""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        # Handle MCP redirect before security checks
        if request.url.path == "/mcp" and request.method == "POST":
            return await mcp_redirect(request)
        
        # Add security headers
        response = await call_next(request)
        
        # Security headers following best practices
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # For MCP endpoints, ensure proper content type
        if request.url.path in ["/mcp/", "/mcp"]:
            if "accept" in request.headers:
                accept_header = request.headers["accept"]
                if "text/event-stream" not in accept_header and "application/json" not in accept_header:
                    return JSONResponse(
                        {"error": "Client must accept text/event-stream and application/json"},
                        status_code=406
                    )
        
        return response

def create_app_with_endpoints():
    """Create Starlette app with security and monitoring endpoints."""
    app = mcp.streamable_http_app()
    
    # Add security middleware
    app.add_middleware(SecurityMiddleware)
    
    # Add health check route
    app.routes.append(Route("/health", health_check))
    
    return app

def main():
    """Main function to run the MCP server"""
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        logger.info("Starting MCP server with stdio transport")
        mcp.run(transport="stdio")
    elif len(sys.argv) > 1 and sys.argv[1] == "--web":
        # For Cloud Run deployment
        app = create_app_with_endpoints()
        port = int(os.getenv("PORT", SERVER_CONFIG["port"]))
        logger.info(f"Starting MCP server on port {port}")
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
    else:
        print(f"Starting {SERVER_CONFIG['name']} v{SERVER_CONFIG['version']}")
        print(f"Available tools: {list(TOOL_CONFIGS.keys())}")
        print(f"Available prompts: {list(PROMPT_CONFIGS.keys())}")
        print(f"Available resources: {list(RESOURCE_CONFIGS.keys())}")
        print("\nUsage:")
        print("  python server.py --stdio  (for local MCP client connections)")
        print("  python server.py --web    (for web deployment like Cloud Run)")
        print("  mcp dev server.py         (for local development with inspector)")
        
        # Default to checking environment variable like the working server
        transport = os.getenv("MCP_TRANSPORT", "stdio")
        if transport == "streamable-http":
            app = create_app_with_endpoints()
            port = int(os.getenv("PORT", SERVER_CONFIG["port"]))
            logger.info(f"Starting MCP server on port {port}")
            uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
        else:
            logger.info("Starting MCP server with stdio transport")
            mcp.run(transport="stdio")

if __name__ == "__main__":
    main()