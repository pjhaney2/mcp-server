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
from typing import Optional, Dict, Union, Any, List, Tuple

from config import TOOL_CONFIGS, PROMPT_CONFIGS, RESOURCE_CONFIGS, SERVER_CONFIG
from tools.calculator import add, subtract, multiply, divide
from tools.acs_data.acs_social_county import acs_social_county_pull
from tools.acs_data.acs_economic_county import acs_economic_county_pull
from tools.acs_data.acs_housing_county import acs_housing_county_pull
from tools.acs_data.acs_social_place import acs_social_place_pull
from tools.acs_data.acs_economic_place import acs_economic_place_pull
from tools.acs_data.acs_housing_place import acs_housing_place_pull
from tools.acs_data.acs_social_msa import acs_social_msa_pull
from tools.acs_data.acs_economic_msa import acs_economic_msa_pull
from tools.acs_data.acs_housing_msa import acs_housing_msa_pull
from tools.acs_data.acs_social_state import acs_social_state_pull
from tools.acs_data.acs_economic_state import acs_economic_state_pull
from tools.acs_data.acs_housing_state import acs_housing_state_pull
from tools.acs_data.acs_social_national import acs_social_national_pull
from tools.acs_data.acs_economic_national import acs_economic_national_pull
from tools.acs_data.acs_housing_national import acs_housing_national_pull
from tools.acs_data.acs_county_fips import search_county_fips
from tools.acs_data.acs_place_fips import search_place_fips
from tools.acs_data.acs_msa_fips import search_msa_fips
from tools.acs_data.acs_state_fips import search_state_fips
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

@mcp.tool()
def acs_social_county_pull_tool(geo_fips: str, state_fips: str, year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls county-level social characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates"""
    try:
        return acs_social_county_pull(geo_fips, state_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_social_county_pull: {e}")
        raise ValueError("Invalid input: Please provide valid FIPS codes and optional year")

@mcp.tool()
def acs_economic_county_pull_tool(geo_fips: str, state_fips: str, year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls county-level economic characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates"""
    try:
        return acs_economic_county_pull(geo_fips, state_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_economic_county_pull: {e}")
        raise ValueError("Invalid input: Please provide valid FIPS codes and optional year")

@mcp.tool()
def acs_housing_county_pull_tool(geo_fips: str, state_fips: str, year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls county-level housing characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates"""
    try:
        return acs_housing_county_pull(geo_fips, state_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_housing_county_pull: {e}")
        raise ValueError("Invalid input: Please provide valid FIPS codes and optional year")

@mcp.tool()
def acs_social_place_pull_tool(place_fips: str, state_fips: str, year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls place-level social characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates"""
    try:
        return acs_social_place_pull(place_fips, state_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_social_place_pull: {e}")
        raise ValueError("Invalid input: Please provide valid FIPS codes and optional year")

@mcp.tool()
def acs_economic_place_pull_tool(place_fips: str, state_fips: str, year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls place-level economic characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates"""
    try:
        return acs_economic_place_pull(place_fips, state_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_economic_place_pull: {e}")
        raise ValueError("Invalid input: Please provide valid FIPS codes and optional year")

@mcp.tool()
def acs_housing_place_pull_tool(place_fips: str, state_fips: str, year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls place-level housing characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates"""
    try:
        return acs_housing_place_pull(place_fips, state_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_housing_place_pull: {e}")
        raise ValueError("Invalid input: Please provide valid FIPS codes and optional year")

@mcp.tool()
def search_county_fips_tool(keyword: str, max_results: Optional[int] = 20) -> List[Tuple[str, str]]:
    """Search for counties by keyword and return their FIPS codes"""
    try:
        return search_county_fips(keyword, max_results)
    except Exception as e:
        logger.error(f"Error in search_county_fips: {e}")
        raise ValueError("Invalid input: Please provide a valid search keyword")

@mcp.tool()
def search_place_fips_tool(keyword: str, max_results: Optional[int] = 20) -> List[Tuple[str, str]]:
    """Search for places (cities, towns, CDPs) by keyword and return their FIPS codes"""
    try:
        return search_place_fips(keyword, max_results)
    except Exception as e:
        logger.error(f"Error in search_place_fips: {e}")
        raise ValueError("Invalid input: Please provide a valid search keyword")

@mcp.tool()
def search_msa_fips_tool(keyword: str, max_results: Optional[int] = 20) -> List[Tuple[str, str]]:
    """Search for MSA/Micropolitan areas by keyword and return their FIPS codes"""
    try:
        return search_msa_fips(keyword, max_results)
    except Exception as e:
        logger.error(f"Error in search_msa_fips: {e}")
        raise ValueError("Invalid input: Please provide a valid search keyword")

@mcp.tool()
def search_state_fips_tool(keyword: str, max_results: Optional[int] = 20) -> List[Tuple[str, str]]:
    """Search for states by keyword and return their FIPS codes"""
    try:
        return search_state_fips(keyword, max_results)
    except Exception as e:
        logger.error(f"Error in search_state_fips: {e}")
        raise ValueError("Invalid input: Please provide a valid search keyword")

@mcp.tool()
def acs_social_msa_pull_tool(msa_fips: str, year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls MSA/Micropolitan area-level social characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates"""
    try:
        return acs_social_msa_pull(msa_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_social_msa_pull: {e}")
        raise ValueError("Invalid input: Please provide valid MSA FIPS code and optional year")

@mcp.tool()
def acs_economic_msa_pull_tool(msa_fips: str, year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls MSA/Micropolitan area-level economic characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates"""
    try:
        return acs_economic_msa_pull(msa_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_economic_msa_pull: {e}")
        raise ValueError("Invalid input: Please provide valid MSA FIPS code and optional year")

@mcp.tool()
def acs_housing_msa_pull_tool(msa_fips: str, year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls MSA/Micropolitan area-level housing characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates"""
    try:
        return acs_housing_msa_pull(msa_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_housing_msa_pull: {e}")
        raise ValueError("Invalid input: Please provide valid MSA FIPS code and optional year")

@mcp.tool()
def acs_social_state_pull_tool(state_fips: str, year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls state-level social characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates"""
    try:
        return acs_social_state_pull(state_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_social_state_pull: {e}")
        raise ValueError("Invalid input: Please provide valid state FIPS code and optional year")

@mcp.tool()
def acs_economic_state_pull_tool(state_fips: str, year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls state-level economic characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates"""
    try:
        return acs_economic_state_pull(state_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_economic_state_pull: {e}")
        raise ValueError("Invalid input: Please provide valid state FIPS code and optional year")

@mcp.tool()
def acs_housing_state_pull_tool(state_fips: str, year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls state-level housing characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates"""
    try:
        return acs_housing_state_pull(state_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_housing_state_pull: {e}")
        raise ValueError("Invalid input: Please provide valid state FIPS code and optional year")

@mcp.tool()
def acs_social_national_pull_tool(year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls national-level social characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates"""
    try:
        return acs_social_national_pull(year)
    except Exception as e:
        logger.error(f"Error in acs_social_national_pull: {e}")
        raise ValueError("Invalid input: Please provide valid optional year")

@mcp.tool()
def acs_economic_national_pull_tool(year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls national-level economic characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates"""
    try:
        return acs_economic_national_pull(year)
    except Exception as e:
        logger.error(f"Error in acs_economic_national_pull: {e}")
        raise ValueError("Invalid input: Please provide valid optional year")

@mcp.tool()
def acs_housing_national_pull_tool(year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls national-level housing characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates"""
    try:
        return acs_housing_national_pull(year)
    except Exception as e:
        logger.error(f"Error in acs_housing_national_pull: {e}")
        raise ValueError("Invalid input: Please provide valid optional year")

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