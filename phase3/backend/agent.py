from openai import OpenAI
from tools import TOOLS, execute_tool
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """You are a helpful task management assistant. You help users manage their todo list through natural language.

When users ask you to:
- Add/create/remember tasks → use add_task
- Show/list tasks → use list_tasks
- Mark tasks complete/done → use complete_task
- Delete/remove tasks → use delete_task
- Update/change tasks → use update_task

Always confirm actions with friendly responses. Handle errors gracefully.

Examples:
- "Add a task to buy groceries" → add_task with title "Buy groceries"
- "Show me all my tasks" → list_tasks with status "all"
- "Mark task 3 as done" → complete_task with task_id 3
- "Delete the meeting task" → First list tasks to find it, then delete
"""


async def run_agent(user_id: str, messages: list) -> dict:
    """Run the OpenAI agent with function calling tools."""
    
    # Prepare messages with system prompt
    full_messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + messages
    
    # Initial API call
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Using mini for cost efficiency
        messages=full_messages,
        tools=TOOLS,
        tool_choice="auto"
    )
    
    assistant_message = response.choices[0].message
    tool_calls_log = []
    
    # Handle tool calls
    while assistant_message.tool_calls:
        # Add assistant message to history
        full_messages.append({
            "role": "assistant",
            "content": assistant_message.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in assistant_message.tool_calls
            ]
        })
        
        # Execute tool calls
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # Execute tool
            result = execute_tool(user_id, function_name, function_args)
            
            # Add tool response to messages
            full_messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
            
            tool_calls_log.append({
                "tool": function_name,
                "arguments": function_args,
                "result": json.loads(result)
            })
        
        # Get next response
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=full_messages,
            tools=TOOLS,
            tool_choice="auto"
        )
        
        assistant_message = response.choices[0].message
    
    # Return final response
    return {
        "response": assistant_message.content,
        "tool_calls": tool_calls_log
    }
