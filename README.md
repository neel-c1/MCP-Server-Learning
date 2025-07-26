# Test MCP Server Functionality

This is a place where I learn more about how MCP servers work. Aims to use a LangGraph-based OpenAI agentic AI to grab weather information based on queries. 

## Requirements

1. An OpenAI API Key
2. Python 3.10+
3. uv Package Manager

## Set Up (for now)

```
git clone https://www.github.com/neel-c1/MCP-Server-Learning.git/
cd MCP-Server-Learning
cp -r .env.example .env
# (Copy paste in your OpenAI API key)
python3 -m venv .venv
source .venv/bin/activate
pip3 install -U pip
pip3 install -r ./docs/requirements.txt
python3 run client.py ./server/weather.py
```
