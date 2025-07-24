import asyncio
import sys
import os
from typing import Optional
from contextlib import AsyncExitStack

import openai
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_script_path: str):
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        await self.session.initialize()

    async def process_query(self, query: str) -> str:
        messages = [{"role": "user", "content": query}]

        tool_response = await self.session.list_tools()
        available_tools = tool_response.tools

        functions = []
        tool_map = {}
        for tool in available_tools:
            func_def = {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
            functions.append(func_def)
            tool_map[tool.name] = tool

        response = openai.ChatCompletion.create(
            model="gpt-4.1-mini",
            messages=messages,
            functions=functions,
            function_call="auto",
        )

        reply = response.choices[0].message
        final_output = []

        if reply.get("content"):
            final_output.append(reply["content"])

        while reply.get("function_call"):
            tool_name = reply["function_call"]["name"]
            arguments = eval(reply["function_call"]["arguments"])

            tool_result = await self.session.call_tool(tool_name, arguments)

            messages.append(reply)
            messages.append({
                "role": "function",
                "name": tool_name,
                "content": str(tool_result.content)
            })

            response = openai.ChatCompletion.create(
                model="gpt-4.1-mini",
                messages=messages,
                functions=functions,
                function_call="auto",
            )

            reply = response.choices[0].message
            if reply.get("content"):
                final_output.append(reply["content"])

        return "\n".join(final_output)

    async def chat_loop(self):
        print("Type your queries or 'quit' to exit.")
        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
