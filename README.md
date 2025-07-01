# MCP Demo Server

A fully functional Model Context Protocol (MCP) server implementation with tools, prompts, and resources. Supports both local development and remote deployment on Google Cloud Run.

## ✨ Features

- **🧮 Calculator Tools**: Basic math operations (add, subtract, multiply, divide)
- **🏴‍☠️ Pirate Talk Prompt**: Transform text to pirate speak
- **📄 PDF Resource**: Access to Waupaca draft report content
- **🔧 Local Development**: MCP Inspector support for testing
- **☁️ Cloud Deployment**: Ready for Google Cloud Run
- **🎯 Claude Integration**: Works with Claude Desktop

## 📁 Project Structure

```
mcp-server-v2/
├── tools/
│   └── calculator.py              # Clean calculator functions
├── prompts/
│   └── pirate_talk.py             # Pirate talk prompt template
├── resources/
│   └── waupaca_report.pdf         # PDF resource
├── server.py                      # Main MCP server (FastMCP)
├── config.py                      # Centralized configurations
├── requirements.txt               # Python dependencies
├── Dockerfile                     # Container configuration
├── deploy.sh                      # Google Cloud Run deployment script
├── claude_config.json             # Example Claude Desktop config
├── test_server.py                 # Server testing utility
├── run_inspector.sh               # Inspector launcher script
└── README.md                      # This file
```

## 🚀 Quick Start

### Local Development

1. **Set up environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   # Activate virtual environment first
   source .venv/bin/activate
   
   # For MCP client connections (Claude Desktop)
   python server.py --stdio
   
   # For web-based inspector (debugging/testing)
   mcp dev server.py
   ```

3. **Test with Inspector:**
   The inspector provides a web interface where you can:
   - Test calculator tools interactively
   - Try pirate talk prompt transformations
   - Access PDF resource content
   - Debug server functionality
   - **Requires Node.js installed**

## ☁️ Cloud Deployment

### Deploy to Google Cloud Run

1. **Prerequisites:**
   ```bash
   # Install Google Cloud CLI if not already installed
   # Authenticate with your Google account
   gcloud auth login
   
   # Set your project
   gcloud config set project agents-460202
   ```

2. **Deploy:**
   ```bash
   ./deploy.sh
   ```

3. **Live Server:** https://mcp-server-613421470956.us-central1.run.app

### Health Check
```bash
curl https://mcp-server-613421470956.us-central1.run.app/health
```

## 🔗 Claude Desktop Integration

### Option 1: Remote Server (Recommended)
Add this to your Claude Desktop `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-demo-server-remote": {
      "transport": {
        "type": "streamable-http",
        "url": "https://mcp-server-613421470956.us-central1.run.app/mcp/"
      }
    }
  }
}
```

### Option 2: Local Development
For local testing with Claude Desktop:

```json
{
  "mcpServers": {
    "mcp-demo-server": {
      "command": "python",
      "args": ["server.py", "--stdio"],
      "cwd": "/Users/peterhaney/code/mcp-server-v2"
    }
  }
}
```

**Claude Desktop config location:**
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

## 📋 Available Tools & Resources

### 🧮 Calculator Tools
- `calculator_add(a, b)` - Add two numbers
- `calculator_subtract(a, b)` - Subtract two numbers  
- `calculator_multiply(a, b)` - Multiply two numbers
- `calculator_divide(a, b)` - Divide two numbers

**Example:** "Calculate 15 + 27" → Uses `calculator_add(15, 27)` → Returns 42

### 🏴‍☠️ Pirate Talk Prompt
- `pirate_talk(text)` - Transform text to pirate speak

**Example:** "Hello, how are you?" → "Ahoy there, matey! How be ye farin' on this fine day?"

### 📄 Waupaca Report Resource
- `waupaca://report` - Access full PDF content

**Usage:** "Show me the Waupaca report" → Returns extracted PDF text content

## ⚙️ Configuration

All configurations are centralized in `config.py`:

- **`TOOL_CONFIGS`**: Calculator tool definitions and schemas
- **`PROMPT_CONFIGS`**: Pirate talk prompt template
- **`RESOURCE_CONFIGS`**: PDF resource configuration
- **`SERVER_CONFIG`**: Server settings (name, version, host, port)

## 🏗️ Architecture

This implementation follows MCP best practices:

- **Clean Separation**: Tools are pure functions, MCP logic is separate
- **Configuration-Driven**: All tool/prompt/resource definitions in config files
- **Modular Design**: Easy to add new tools, prompts, or resources
- **Dual Deployment**: Supports both local (stdio) and remote (HTTP) transports
- **Security**: Includes middleware, headers, and proper error handling
- **Scalable**: Ready for serverless deployment on Google Cloud Run

## 🛠️ Technical Details

### Dependencies
- **FastMCP**: Modern MCP server framework
- **FastAPI/Starlette**: Web framework for HTTP transport
- **PyPDF2**: PDF text extraction
- **Uvicorn**: ASGI server for production

### Transport Types
- **stdio**: For local Claude Desktop integration
- **streamable-http**: For remote web deployment

### Environment Variables
- `MCP_TRANSPORT`: Set to `streamable-http` for web deployment
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)

## 🧪 Testing

Test server functionality:
```bash
source .venv/bin/activate
python test_server.py
```

Test specific endpoints:
```bash
# Health check
curl https://mcp-server-613421470956.us-central1.run.app/health

# Local testing
curl http://localhost:8000/health
```

## 🔧 Development Commands

```bash
# Run with stdio (for Claude Desktop)
python server.py --stdio

# Run with web server (for remote access)  
python server.py --web

# Run with environment variable (Cloud Run style)
MCP_TRANSPORT=streamable-http python server.py

# Run inspector for testing
./run_inspector.sh
```

## 📝 Adding New Features

### Add a New Tool
1. Create function in `tools/` directory
2. Add configuration to `TOOL_CONFIGS` in `config.py`
3. Register with `@mcp.tool()` decorator in `server.py`

### Add a New Prompt
1. Create function in `prompts/` directory
2. Add configuration to `PROMPT_CONFIGS` in `config.py`
3. Register with `@mcp.prompt()` decorator in `server.py`

### Add a New Resource
1. Add file to `resources/` directory
2. Add configuration to `RESOURCE_CONFIGS` in `config.py`
3. Register with `@mcp.resource()` decorator in `server.py`

## 🎯 Success Criteria Met

✅ **Three-folder structure** (tools/, prompts/, resources/)  
✅ **Config-driven architecture** (clean functions, centralized config)  
✅ **Local + Remote deployment** (stdio + streamable-http)  
✅ **Google Cloud Run deployment** (agents-460202 project)  
✅ **Claude Desktop integration** (working remote connection)  
✅ **MCP Inspector support** (local development testing)  
✅ **Production-ready** (security, error handling, logging)

---

**🎉 Your MCP server is ready for production use with Claude Desktop!**