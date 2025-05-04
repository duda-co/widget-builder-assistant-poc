from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Dict, Type, Any, Tuple
import asyncio

from pydantic_ai import Agent
import logfire

from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich import print as rprint
import pyperclip

# configure logfire
logfire.configure(token='pylf_v1_us_83GrqsMh3gsjRMxy6JntXTYHxm0YmmjjYyZYsPzBcj1S')
logfire.instrument_openai()

@dataclass
class WidgetBuilderState:
    current_html: str = ""
    current_css: str = ""
    current_javascript: str = ""
    current_content: str = ""
    current_design: str = ""
    updated_html: str = ""
    updated_css: str = ""
    updated_javascript: str = ""
    updated_content: str = ""
    updated_design: str = ""

class SubAgentPlan(BaseModel):
    html_agent: Any | None = None
    css_agent: Any | None = None
    javascript_agent: Any | None = None
    content_config_agent: Any | None = None
    design_config_agent: Any | None = None
    
class ArchitectPlan(BaseModel):
    planning: str
    general_plan: str
    human_readiable_plan: str
    sub_agent_plans: SubAgentPlan


with open('src/pydantic_ai_learn/architect_system_prompt.md', 'r') as f:
    architect_prompt_template = f.read()
with open('src/pydantic_ai_learn/widget_builder_docs.md', 'r') as f:
    widget_builder_docs = f.read()



architectAgent = Agent[WidgetBuilderState, ArchitectPlan](
    'openai:gpt-4.1', 
    deps_type=WidgetBuilderState, 
    output_type=ArchitectPlan
)

@architectAgent.system_prompt
def widget_builder_docs_prompt():
    return widget_builder_docs

@architectAgent.system_prompt
def architect_prompt():
    return architect_prompt_template

@architectAgent.system_prompt
def current_widget_state(ctx: RunContext[WidgetBuilderState]):
    return f"""
            # Current widget state:

            ## HTML:
            {ctx.deps.current_html}

            ## JS:
            {ctx.deps.current_javascript}

            ## CSS:
            {ctx.deps.current_css}

            ## Content Configuration:
            {ctx.deps.current_content}

            ## Design Configuration:
            {ctx.deps.current_design}
            
            
        """

javascriptAgent = Agent[WidgetBuilderState, str]('openai:gpt-4.1-mini', deps_type=WidgetBuilderState)
htmlAgent = Agent[WidgetBuilderState, str]('openai:gpt-4.1-mini', deps_type=WidgetBuilderState)
cssAgent = Agent[WidgetBuilderState, str]('openai:gpt-4.1-mini', deps_type=WidgetBuilderState)
contentConfigAgent = Agent[WidgetBuilderState, str]('openai:gpt-4.1-mini', deps_type=WidgetBuilderState)
designConfigAgent = Agent[WidgetBuilderState, str]('openai:gpt-4.1-mini', deps_type=WidgetBuilderState)

@javascriptAgent.system_prompt
def javascript_prompt():
    return f"""
    {widget_builder_docs}
    
    You are a javascript expert, follow the instructions in the widget_builder_docs.md file and build the javascript code for the widget only.
    Follow the instructions provided to you and do not deviate from them.
    """

@htmlAgent.system_prompt
def html_prompt():
    return f"""
    {widget_builder_docs}
    
    You are a html expert, follow the instructions in the widget_builder_docs.md file and build the html code for the widget only.
    Follow the instructions provided to you and do not deviate from them.
    """

@cssAgent.system_prompt
def css_prompt():
    return f"""
    {widget_builder_docs}
    
    You are a css expert, follow the instructions in the widget_builder_docs.md file and build the css code for the widget only.
    Follow the instructions provided to you and do not deviate from them.
    """
    

@contentConfigAgent.system_prompt
def content_config_prompt():
    return f""" 
    {widget_builder_docs}
    
    You are a content configuration expert, follow the instructions in the widget_builder_docs.md file and build the content configuration for the widget only.
    Follow the instructions provided to you and do not deviate from them.
    """

@designConfigAgent.system_prompt
def design_config_prompt():
    return f"""
    {widget_builder_docs}
    
    You are a design configuration expert, follow the instructions in the widget_builder_docs.md file and build the design configuration for the widget only.
    Follow the instructions provided to you and do not deviate from them.
    """

# --- Define the asynchronous plan execution function ---
async def execute_plan(plan: ArchitectPlan, state: WidgetBuilderState):
    """
    Executes the sub-agent plans concurrently based on the architect's plan.
    Updates the state object in place.
    """
    tasks = []
    sub_plans = plan.sub_agent_plans

    if sub_plans.html_agent:
        tasks.append(asyncio.create_task(go_to_html_agent(state, plan.general_plan, sub_plans.html_agent)))
    if sub_plans.css_agent:
        tasks.append(asyncio.create_task(go_to_css_agent(state, plan.general_plan, sub_plans.css_agent)))
    if sub_plans.javascript_agent:
        tasks.append(asyncio.create_task(go_to_javascript_agent(state, plan.general_plan, sub_plans.javascript_agent)))
    if sub_plans.content_config_agent:
        tasks.append(asyncio.create_task(go_to_content_config_agent(state, plan.general_plan, sub_plans.content_config_agent)))
    if sub_plans.design_config_agent:
        tasks.append(asyncio.create_task(go_to_design_config_agent(state, plan.general_plan, sub_plans.design_config_agent)))

    if tasks:
        await asyncio.gather(*tasks)
    else:
        rprint("[yellow]No sub-agent plans to execute.[/yellow]")


def get_user_plan_message(general_plan: str, plan: Any):
    return f"""
    {general_plan}
    
    {plan}
    """

# --- Remove @architectAgent.tool decorators and keep functions ---

async def go_to_html_agent(state: WidgetBuilderState, general_plan: str, html_plan: Any):
    """
    execute the html_plan and update the html code
    """
    print("Going to html agent")
    result = await htmlAgent.run(get_user_plan_message(general_plan, html_plan), deps=state)
    state.updated_html = result.output
    return f"Updated HTML: {state.updated_html}"

async def go_to_javascript_agent(state: WidgetBuilderState, general_plan: str, javascript_plan: Any):
    """
    execute the javascript_plan and update the javascript code
    """
    print("Going to javascript agent")
    result = await javascriptAgent.run(get_user_plan_message(general_plan, javascript_plan), deps=state)
    state.updated_javascript = result.output
    return f"Updated JavaScript: {state.updated_javascript}"

async def go_to_css_agent(state: WidgetBuilderState, general_plan: str, css_plan: Any):
    """
    execute the css_plan and update the css code
    """
    print("Going to css agent")
    result = await cssAgent.run(get_user_plan_message(general_plan, css_plan), deps=state)
    state.updated_css = result.output
    return f"Updated CSS: {state.updated_css}"

async def go_to_content_config_agent(state: WidgetBuilderState, general_plan: str, content_config_plan: Any):
    """
    execute the content_config_plan and update the content configuration
    """
    print("Going to content config agent")
    result = await contentConfigAgent.run(get_user_plan_message(general_plan, content_config_plan), deps=state)
    state.updated_content = result.output
    return f"Updated Content: {state.updated_content}"

async def go_to_design_config_agent(state: WidgetBuilderState, general_plan: str,    design_config_plan: Any):
    """
    execute the design_config_plan and update the design configuration
    """
    print("Going to design config agent")
    result = await designConfigAgent.run(get_user_plan_message(general_plan, design_config_plan), deps=state)
    state.updated_design = result.output
    return f"Updated Design: {state.updated_design}"

# --- Utility functions for CLI ---
def pretty_print_state(state: WidgetBuilderState):
    """Pretty print the current widget state with syntax highlighting"""
    console = Console()
    
    if state.updated_html or state.current_html:
        console.print("\n[bold cyan]HTML:[/bold cyan]")
        html_code = state.updated_html or state.current_html
        console.print(Syntax(html_code, "html", theme="monokai"))
        
    if state.updated_javascript or state.current_javascript:
        console.print("\n[bold yellow]JavaScript:[/bold yellow]")
        js_code = state.updated_javascript or state.current_javascript
        console.print(Syntax(js_code, "javascript", theme="monokai"))
        
    if state.updated_css or state.current_css:
        console.print("\n[bold magenta]CSS:[/bold magenta]")
        css_code = state.updated_css or state.current_css
        console.print(Syntax(css_code, "css", theme="monokai"))
        
    if state.updated_content or state.current_content:
        console.print("\n[bold green]Content Configuration:[/bold green]")
        content = state.updated_content or state.current_content
        console.print(Syntax(content, "json", theme="monokai"))
        
    if state.updated_design or state.current_design:
        console.print("\n[bold blue]Design Configuration:[/bold blue]")
        design = state.updated_design or state.current_design
        console.print(Syntax(design, "json", theme="monokai"))

def copy_to_clipboard(state: WidgetBuilderState):
    """Copy the current widget code to clipboard"""
    code_parts = []
    if state.updated_html or state.current_html:
        code_parts.append(f"/* HTML */\n{state.updated_html or state.current_html}")
    if state.updated_javascript or state.current_javascript:
        code_parts.append(f"/* JavaScript */\n{state.updated_javascript or state.current_javascript}")
    if state.updated_css or state.current_css:
        code_parts.append(f"/* CSS */\n{state.updated_css or state.current_css}")
    
    all_code = "\n\n".join(code_parts)
    pyperclip.copy(all_code)
    rprint("[green]✓[/green] Code copied to clipboard!")


# --- Refactor cli_chat ---
def cli_chat():
    console = Console()
    console.print(Panel("[bold green]Welcome to the Widget Builder AI Assistant![/bold green]\nType 'exit' to quit.", title="Chat Interface", border_style="blue"))
    
    state = WidgetBuilderState()
    user_input = input("\nYou: ").strip()
    turn_count = 0
    # Initial planning (outside the main loop span)
    response = None
        
    while True:
        turn_count += 1
        with logfire.span(f"Widget Builder AI Assistant: Chat Turn {turn_count}"):
            # 1. Extract the plan from the architect's response
            with logfire.span("Planning"):
                if (response is None):
                    response = architectAgent.run_sync(user_input, deps=state)
                else:
                    response = architectAgent.run_sync(user_input, deps=state, message_history=response.all_messages())
            
            plan: ArchitectPlan = response.output
            # Use rich Panel for better display
            plan_details = f"[bold]Planning:[/bold] {plan.planning}\n[bold]General Plan:[/bold] {plan.general_plan}\n[bold]Sub-agent Plans:[/bold] {plan.sub_agent_plans}"
            rprint(Panel(plan_details, title="[bold blue]Architect's Plan[/bold blue]", border_style="blue", expand=False))

            
            rprint(f"[bold]Assistant:[/bold] {plan.human_readiable_plan}")
            # 2. Execute the plan asynchronously, updating the state
            # Wrap execution in its own sub-span
            with logfire.span("Plan Execution"):
                rprint("\n[yellow]Executing plan...[/yellow]")
                asyncio.run(execute_plan(plan, state))
                rprint("[green]Plan execution complete.[/green]")

            # Pretty print the state and copy code
            pretty_print_state(state)
            copy_to_clipboard(state) # Already includes a confirmation message

            # 3. Generate Summary (currently commented out)
            # # rprint("\n[yellow]Generating summary...[/yellow]")
            # # summary_response = summaryAgent.run_sync(deps=(plan, state))
            # # rprint(Panel(summary_response.output, title="[bold green]Execution Summary[/bold green]", border_style="green", expand=False))

            # 5. Prepare state for the next planning phase
            # Wrap state update in its own sub-span
            with logfire.span("State Update"):
                state.current_html = state.updated_html or state.current_html
                state.current_css = state.updated_css or state.current_css
                state.current_javascript = state.updated_javascript or state.current_javascript
                state.current_content = state.updated_content or state.current_content
                state.current_design = state.updated_design or state.current_design

                state.updated_html = ""
                state.updated_css = ""
                state.updated_javascript = ""
                state.updated_content = ""
                state.updated_design = ""
        print("--------------------------------")
                    # 4. Get next user input
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'exit':
            console.print("[bold red]Exiting chat. Goodbye![/bold red]")
            break


if __name__ == "__main__":
    cli_chat()
