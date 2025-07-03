#!/usr/bin/env python3
"""
MCP Demo Server using FastMCP
Supports both local stdio and remote streamable-http transports

This server provides calculator tools and PDF resources.
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
from tools.oews_data.oews_data import get_oews_data
from tools.oews_data.oews_fips import search_oews_fips
from tools.oews_data.oews_soc import search_oews_soc
from tools.qcew_data.qcew_data import get_qcew_data
from tools.qcew_data.qcew_fips import search_qcew_fips
from tools.qcew_data.qcew_naics import search_qcew_naics
from prompts.case_study_creator import get_case_study_prompt

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create the MCP server
mcp = FastMCP(SERVER_CONFIG["name"])


@mcp.tool()
def get_acs_county_social_data(geo_fips: List[str], state_fips: str, year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls county-level social characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates. Supports multiple counties in a single request by passing multiple FIPS codes in the array."""
    try:
        return acs_social_county_pull(geo_fips, state_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_social_county_pull: {e}")
        raise ValueError("Invalid input: Please provide valid FIPS codes and optional year")

@mcp.tool()
def get_acs_county_economic_data(geo_fips: List[str], state_fips: str, year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls county-level economic characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates. Supports multiple counties in a single request by passing multiple FIPS codes in the array."""
    try:
        return acs_economic_county_pull(geo_fips, state_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_economic_county_pull: {e}")
        raise ValueError("Invalid input: Please provide valid FIPS codes and optional year")

@mcp.tool()
def get_acs_county_housing_data(geo_fips: List[str], state_fips: str, year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls county-level housing characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates. Supports multiple counties in a single request by passing multiple FIPS codes in the array."""
    try:
        return acs_housing_county_pull(geo_fips, state_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_housing_county_pull: {e}")
        raise ValueError("Invalid input: Please provide valid FIPS codes and optional year")

@mcp.tool()
def get_acs_place_social_data(place_fips: List[str], state_fips: str, year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls place-level social characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates. Supports multiple places in a single request by passing multiple FIPS codes in the array."""
    try:
        return acs_social_place_pull(place_fips, state_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_social_place_pull: {e}")
        raise ValueError("Invalid input: Please provide valid FIPS codes and optional year")

@mcp.tool()
def get_acs_place_economic_data(place_fips: List[str], state_fips: str, year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls place-level economic characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates. Supports multiple places in a single request by passing multiple FIPS codes in the array."""
    try:
        return acs_economic_place_pull(place_fips, state_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_economic_place_pull: {e}")
        raise ValueError("Invalid input: Please provide valid FIPS codes and optional year")

@mcp.tool()
def get_acs_place_housing_data(place_fips: List[str], state_fips: str, year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls place-level housing characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates. Supports multiple places in a single request by passing multiple FIPS codes in the array."""
    try:
        return acs_housing_place_pull(place_fips, state_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_housing_place_pull: {e}")
        raise ValueError("Invalid input: Please provide valid FIPS codes and optional year")

@mcp.tool()
def lookup_county_fips(keyword: List[str], max_results: Optional[int] = 20) -> List[Tuple[str, str]]:
    """Search for counties by keyword(s) and return their FIPS codes"""
    try:
        return search_county_fips(keyword, max_results)
    except Exception as e:
        logger.error(f"Error in search_county_fips: {e}")
        raise ValueError("Invalid input: Please provide a valid search keyword")

@mcp.tool()
def lookup_place_fips(keyword: List[str], max_results: Optional[int] = 20) -> List[Tuple[str, str]]:
    """Search for places (cities, towns, CDPs) by keyword(s) and return their FIPS codes"""
    try:
        return search_place_fips(keyword, max_results)
    except Exception as e:
        logger.error(f"Error in search_place_fips: {e}")
        raise ValueError("Invalid input: Please provide a valid search keyword")

@mcp.tool()
def lookup_msa_fips(keyword: List[str], max_results: Optional[int] = 20) -> List[Tuple[str, str]]:
    """Search for MSA/Micropolitan areas by keyword(s) and return their FIPS codes"""
    try:
        return search_msa_fips(keyword, max_results)
    except Exception as e:
        logger.error(f"Error in search_msa_fips: {e}")
        raise ValueError("Invalid input: Please provide a valid search keyword")

@mcp.tool()
def lookup_state_fips(keyword: List[str], max_results: Optional[int] = 20) -> List[Tuple[str, str]]:
    """Search for states by keyword(s) and return their FIPS codes"""
    try:
        return search_state_fips(keyword, max_results)
    except Exception as e:
        logger.error(f"Error in search_state_fips: {e}")
        raise ValueError("Invalid input: Please provide a valid search keyword")

@mcp.tool()
def get_acs_msa_social_data(msa_fips: List[str], year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls MSA/Micropolitan area-level social characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates. Supports multiple MSAs in a single request by passing multiple FIPS codes in the array."""
    try:
        return acs_social_msa_pull(msa_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_social_msa_pull: {e}")
        raise ValueError("Invalid input: Please provide valid MSA FIPS code and optional year")

@mcp.tool()
def get_acs_msa_economic_data(msa_fips: List[str], year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls MSA/Micropolitan area-level economic characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates. Supports multiple MSAs in a single request by passing multiple FIPS codes in the array."""
    try:
        return acs_economic_msa_pull(msa_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_economic_msa_pull: {e}")
        raise ValueError("Invalid input: Please provide valid MSA FIPS code and optional year")

@mcp.tool()
def get_acs_msa_housing_data(msa_fips: List[str], year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls MSA/Micropolitan area-level housing characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates. Supports multiple MSAs in a single request by passing multiple FIPS codes in the array."""
    try:
        return acs_housing_msa_pull(msa_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_housing_msa_pull: {e}")
        raise ValueError("Invalid input: Please provide valid MSA FIPS code and optional year")

@mcp.tool()
def get_acs_state_social_data(state_fips: List[str], year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls state-level social characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates. Supports multiple states in a single request by passing multiple FIPS codes in the array."""
    try:
        return acs_social_state_pull(state_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_social_state_pull: {e}")
        raise ValueError("Invalid input: Please provide valid state FIPS code and optional year")

@mcp.tool()
def get_acs_state_economic_data(state_fips: List[str], year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls state-level economic characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates. Supports multiple states in a single request by passing multiple FIPS codes in the array."""
    try:
        return acs_economic_state_pull(state_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_economic_state_pull: {e}")
        raise ValueError("Invalid input: Please provide valid state FIPS code and optional year")

@mcp.tool()
def get_acs_state_housing_data(state_fips: List[str], year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls state-level housing characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates. Supports multiple states in a single request by passing multiple FIPS codes in the array."""
    try:
        return acs_housing_state_pull(state_fips, year)
    except Exception as e:
        logger.error(f"Error in acs_housing_state_pull: {e}")
        raise ValueError("Invalid input: Please provide valid state FIPS code and optional year")

@mcp.tool()
def get_acs_national_social_data(year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls national-level social characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates"""
    try:
        return acs_social_national_pull(year)
    except Exception as e:
        logger.error(f"Error in acs_social_national_pull: {e}")
        raise ValueError("Invalid input: Please provide valid optional year")

@mcp.tool()
def get_acs_national_economic_data(year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls national-level economic characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates"""
    try:
        return acs_economic_national_pull(year)
    except Exception as e:
        logger.error(f"Error in acs_economic_national_pull: {e}")
        raise ValueError("Invalid input: Please provide valid optional year")

@mcp.tool()
def get_acs_national_housing_data(year: Optional[str] = None) -> Dict[str, Any]:
    """Pulls national-level housing characteristics data from the US Census Bureau's American Community Survey (ACS) 5-year estimates"""
    try:
        return acs_housing_national_pull(year)
    except Exception as e:
        logger.error(f"Error in acs_housing_national_pull: {e}")
        raise ValueError("Invalid input: Please provide valid optional year")

@mcp.tool()
def get_oews_occupation_wage_data(geo_codes: List[str], occ_codes: List[str]) -> Dict[str, Any]:
    """Get simplified OEWS occupation and wage data for multiple locations and occupations with location quotients. Uses BLS OEWS API to fetch employment and wage data."""
    try:
        return get_oews_data(geo_codes, occ_codes)
    except Exception as e:
        logger.error(f"Error in get_oews_data: {e}")
        raise ValueError("Invalid input: Please provide valid geographic area codes and occupation codes")

@mcp.tool()
def lookup_oews_area_fips(keyword: List[str], max_results: Optional[int] = 20) -> List[Tuple[str, str]]:
    """Search for OEWS geographic areas by keyword(s) and return their FIPS codes. Includes states, metros, and nonmetropolitan areas."""
    try:
        return search_oews_fips(keyword, max_results)
    except Exception as e:
        logger.error(f"Error in search_oews_fips: {e}")
        raise ValueError("Invalid input: Please provide a valid search keyword")

@mcp.tool()
def lookup_oews_occupation_codes(keyword: List[str], max_results: Optional[int] = 20) -> List[Tuple[str, str]]:
    """Search for occupations by keyword(s) and return their SOC (Standard Occupational Classification) codes. Find jobs and careers by title or description."""
    try:
        return search_oews_soc(keyword, max_results)
    except Exception as e:
        logger.error(f"Error in search_oews_soc: {e}")
        raise ValueError("Invalid input: Please provide a valid search keyword")

@mcp.tool()
def get_qcew_industry_employment_data(geo_codes: List[str], industry_codes: List[str], year: Optional[str] = None) -> Dict[str, Any]:
    """Get simplified QCEW industry establishment and employee data for multiple locations and industries with location quotients. Uses BLS QCEW API to fetch employment and establishment data. Optionally specify a year for historical data."""
    try:
        return get_qcew_data(geo_codes, industry_codes, year)
    except Exception as e:
        logger.error(f"Error in get_qcew_data: {e}")
        raise ValueError("Invalid input: Please provide valid geographic area codes, industry codes, and optional year")

@mcp.tool()
def lookup_qcew_area_fips(keyword: List[str], max_results: Optional[int] = 20) -> List[Tuple[str, str]]:
    """Search for QCEW geographic areas by keyword(s) and return their FIPS codes. Includes counties, states, and other geographic areas used in QCEW data."""
    try:
        return search_qcew_fips(keyword, max_results)
    except Exception as e:
        logger.error(f"Error in search_qcew_fips: {e}")
        raise ValueError("Invalid input: Please provide a valid search keyword")

@mcp.tool()
def lookup_qcew_industry_codes(keyword: List[str]) -> List[Tuple[str, str]]:
    """Search for industries by keyword(s) and return their NAICS (North American Industry Classification System) codes. Find industries by name or description."""
    try:
        return search_qcew_naics(keyword)
    except Exception as e:
        logger.error(f"Error in search_qcew_naics: {e}")
        raise ValueError("Invalid input: Please provide a valid search keyword")


@mcp.prompt(name="case_study_creator", description="Create a one-page case study from reports or documents")
def create_case_study(client_name: str = "the client", focus_area: str = "general") -> list:
    """Generate a professional case study from provided documents"""
    try:
        # Validate inputs
        if not client_name or not client_name.strip():
            client_name = "the client"
        if not focus_area or not focus_area.strip():
            focus_area = "general"
        
        prompt_content = get_case_study_prompt(
            client_name.strip(),
            focus_area.strip()
        )
        
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
        logger.error(f"Error in case_study_creator: {e}")
        raise ValueError("Invalid input: Please provide valid parameters for case study creation")

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
    try:
        logger.info("MCP Server starting up...")
        logger.info(f"Environment - PORT: {os.getenv('PORT')}, MCP_TRANSPORT: {os.getenv('MCP_TRANSPORT')}")
        logger.info(f"Command line args: {sys.argv}")
        
        if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
            logger.info("Starting MCP server with stdio transport")
            mcp.run(transport="stdio")
        elif len(sys.argv) > 1 and sys.argv[1] == "--web":
            # For Cloud Run deployment
            logger.info("Creating app with endpoints...")
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
            logger.info(f"Transport mode: {transport}")
            if transport == "streamable-http":
                logger.info("Creating app with endpoints...")
                app = create_app_with_endpoints()
                port = int(os.getenv("PORT", SERVER_CONFIG["port"]))
                logger.info(f"Starting MCP server on port {port}")
                uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
            else:
                logger.info("Starting MCP server with stdio transport")
                mcp.run(transport="stdio")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise

if __name__ == "__main__":
    main()