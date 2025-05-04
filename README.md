# Widget Builder AI Assistant

This project demonstrates an AI-powered assistant that helps build web widgets (HTML, CSS, JavaScript) based on user requests. It utilizes multiple AI agents coordinated by an architect agent.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd elements-api-agent
    ```
2.  **Set up a Python virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **OpenAI API Key:** The project uses OpenAI models. Ensure you have an OpenAI API key. The `logfire` library will typically prompt you for it or you can set it as an environment variable:
    ```bash
    export OPENAI_API_KEY='your-openai-api-key'
    ```
2.  **Logfire Token:** The project uses Logfire for tracing. The token seems to be hardcoded in `src/pydantic_ai_learn/hello_world.py`. If you need to change it, update the line:
    ```python
    logfire.configure(token='pylf_v1_us_83GrqsMh3gsjRMxy6JntXTYHxm0YmmjjYyZYsPzBcj1S')
    ```

## How to Run

Execute the main script from the root directory:

```bash
python src/pydantic_ai_learn/hello_world.py
```

This will start the interactive chat interface in your terminal.

## Workflow Explained

The application follows a multi-agent workflow orchestrated by an "Architect" agent:

1.  **User Input:** You provide a request for a widget feature or modification in the chat interface (e.g., "Create a button that alerts 'Hello World' when clicked").
2.  **Architect Agent Planning:**
    - The `architectAgent` receives your request and the current state of the widget (HTML, CSS, JS, etc.).
    - It consults the `widget_builder_docs.md` and its system prompts.
    - It generates a plan (`ArchitectPlan`) which includes:
      - `planning`: Internal reasoning steps.
      - `general_plan`: An overall goal for the current request.
      - `human_readiable_plan`: A summary of the plan shown to the user.
      - `sub_agent_plans`: Specific instructions delegated to specialized sub-agents (HTML, CSS, JS, Content Config, Design Config).
3.  **Sub-Agent Execution:**
    - The main script (`cli_chat` function) identifies which sub-agents need to run based on the `sub_agent_plans`.
    - It calls the corresponding asynchronous functions (`go_to_html_agent`, `go_to_javascript_agent`, etc.).
    - Each function invokes its dedicated agent (`htmlAgent`, `javascriptAgent`, etc.) with the specific instructions from the plan and the current widget state.
    - The sub-agents are experts in their domain (HTML, CSS, JS) and generate the required code or configuration, referencing the `widget_builder_docs.md`.
    - The results from the sub-agents update the `updated_` fields in the `WidgetBuilderState` (e.g., `state.updated_html`).
4.  **State Update & Display:**
    - After all relevant sub-agents complete, the `cli_chat` function updates the `current_` fields in the state with the new content from the `updated_` fields.
    - The new widget state (HTML, CSS, JS, etc.) is pretty-printed to the console with syntax highlighting.
    - The combined code (HTML, CSS, JS) is copied to the clipboard.
5.  **Loop:** The application prompts for the next user input, feeding the _updated_ state back to the `architectAgent` for the next planning cycle. The conversation history is maintained.

This cycle repeats, allowing you to iteratively build and refine the widget through conversation.
