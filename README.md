# Test MCP Server Functionality

This is a place where I learn more about how MCP servers work. Aims to use a LangGraph-based OpenAI agentic AI to grab weather information based on queries. Currently is just a wrapper for whatever is found [here](https://github.com/modelcontextprotocol/quickstart-resources, but will expand on it as needed)

## Requirements (for now)

1. An Anthropic API Key (will migrate to OpenAI)
2. Python 3.10+
3. uv Package Manager

## Set Up (for now)

```
git clone https://www.github.com/neel-c1/MCP-Server-Learning.git/
cd MCP-Server-Learning
cp -r .env.example .env
# (Copy paste in your Anthropic key)
uv venv
source .venv/bin/activate
uv add "mcp[cli]" httpx anthropic python-dotenv
uv run client.py ./server/weather.py
```
