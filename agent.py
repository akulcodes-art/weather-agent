import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize the OpenAI client
client = OpenAI()

def run_command(command: str) -> str:
    """Executes a shell command using os.system."""
    # os.system executes the command and returns the exit status code (0 usually means success)
    status_code = os.system(command)
    
    if status_code == 0:
        return f"Command '{command}' executed successfully."
    else:
        return f"Command '{command}' failed with status code {status_code}."
# 1. Define the actual tool/function the agent can use
def get_weather(city: str) -> str:
    """Fetches the current weather for a given city."""
    url = f"https://wttr.in/{city.lower()}?format=%c+%t"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return f"The weather in {city} is {response.text.strip()}"
        return "Error: Unable to fetch weather data from the service."
    except Exception as e:
        return f"Error connecting to weather service: {str(e)}"

# 2. Map string names to the actual python functions
available_tools = {
    "get_weather": get_weather,
    "run_command": run_command
}

# 3. Describe the tool for the OpenAI API
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather data for a specific city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city, e.g., Delhi, London, New York"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Execute a terminal command on the local machine. Use this to create folders, files, or run scripts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The exact terminal command to execute, e.g., 'mkdir new_folder'"
                    }
                },
                "required": ["command"]
            }
        }
    }

]

# 4. Enforce Chain of Thought via System Instructions
SYSTEM_PROMPT = """
You are an expert AI Assistant that operates using a Chain of Thought (CoT) process.
When a user asks a question, you must thoroughly think through the steps required to answer it.
You now have the ability to manage the file system and execute terminal commands to achieve user goals.
A quick heads-up on how os.system works: It will execute the command (like creating a folder), but it only returns an integer status code (where 0 means success), rather than the actual text output of the terminal.

If you ask the agent to "list the files in this directory", os.system('ls') will print the files to your screen, but the agent will only see "Command executed successfully," meaning it won't actually know what files are there!

Follow this exact loop:
1. **Thought**: Explain to yourself what you need to do, what information is missing, and which tool to use.
2. **Action**: Call the appropriate tool if you need external data.
3. **Observation**: Review the tool's output.
4. **Final Answer**: Once you have all the facts, provide a concise and accurate response to the user.

Always maintain this logical flow in your reasoning.
"""

def run_agent():
    user_query = input("Ask the Weather Agent: ")
    
    # Initialize the conversation state
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]
    
    print("\n--- Agent is Thinking ---")
    
    # First LLM Call: Expecting a Thought + Tool Call
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto" 
    )
    
    response_message = response.choices[0].message
    messages.append(response_message)
    
    # Check if the model decided it needs to use a tool (Action)
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"🤖 [Thought]: {response_message.content or 'Analyzing request details...'}")
            print(f"⚙️ [Action]: Calling tool '{function_name}' with arguments {function_args}")
            
            # Execute the python function matching the tool name
            # Execute the python function matching the tool name
            tool_function = available_tools[function_name]
            # Unpack the dynamically generated arguments into the function
            tool_output = tool_function(**function_args)
            print(f"👀 [Observation]: {tool_output}")
            
            # Feed the observation back to the model
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": tool_output
            })
        
        # Second LLM Call: Generate final answer based on the tool's observation
        final_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        
        print("\n--- Final Agent Response ---")
        print(final_response.choices[0].message.content)
        
    else:
        # If no tool was needed (e.g., the user just said "Hi")
        print("\n--- Final Agent Response ---")
        print(response_message.content)

if __name__ == "__main__":
    run_agent()