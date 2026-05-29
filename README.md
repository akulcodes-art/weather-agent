# Weather Agent

An advanced, AI-powered assistant built with Python that utilizes OpenAI's `gpt-4o` model. Unlike standard conversational bots, this agent is equipped with dynamic tool-calling capabilities and operates using a structured Chain of Thought (CoT) reasoning process. It is designed to bridge the gap between natural language processing and actionable system-level execution.

## 🚀 Core Features

### Advanced Chain of Thought (CoT) Reasoning
The agent doesn't just guess answers; it thinks through them. By implementing a strict logical flow—**Thought -> Action -> Observation -> Final Answer**—the agent evaluates what information it currently has and what is missing. This transparent reasoning process drastically reduces hallucinations and ensures the AI makes deliberate, logical decisions before executing any tool or providing a final response. 

### Autonomous Tool Selection & Execution
Powered by OpenAI's function calling API, the agent autonomously decides *when* and *how* to use its available tools. When a user submits a prompt, the model parses the context, selects the appropriate tool from its JSON schema, constructs the necessary arguments, and triggers the Python function—all without requiring explicit, manual syntax from the user.

### Real-Time Weather Integration
The agent features a built-in `get_weather` tool that integrates directly with the `wttr.in` service. Simply ask for the weather in plain English (e.g., *"How is the weather looking in Tokyo today?"*), and the agent will fetch, parse, and deliver live atmospheric data, temperatures, and conditions for any specified location worldwide.

### Local System Command Execution
One of the most powerful features of this agent is its `run_command` tool, which acts as a bridge to your local operating system. Utilizing `os.system`, the agent can execute terminal commands directly on your machine based on conversational requests. 
*   **Examples:** You can ask the agent to *"Create a new directory called 'project_files'"*, *"List all files in the current folder"*, or *"Run a specific script."*
*   *Note: Because this tool executes OS-level commands, it provides immense flexibility for automating local workflows.*

### Interactive Continuous Chat Loop
The primary `agent.py` script features a continuous, REPL-like (Read-Eval-Print Loop) terminal interface. This allows users to maintain an ongoing, context-aware conversation with the AI, seamlessly switching between casual conversation, weather inquiries, and system tasks without needing to restart the script.

### Multi-Script Architecture
The repository is structured to provide both advanced and foundational implementations:
*   **`agent.py` (The Full Agent):** The primary engine containing the complete CoT logic, tool schemas, and dynamic execution loop.
*   **`main.py` (The Lightweight Alternative):** A simplified, foundational script. It demonstrates standard OpenAI API integration and basic weather fetching, serving as a perfect starting point for understanding API connectivity without the complexity of the full agent loop.
*   **Integrated Project Demos (`todo_app/`):** The repository also includes sample directories like `todo_app` (with HTML, CSS, and JS) which can be manipulated, analyzed, or managed using the agent's local command execution capabilities.
