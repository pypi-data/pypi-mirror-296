import os
import logging
from venv import logger
from rich.markdown import Markdown
from rich.console import Console
from prompt_toolkit import prompt
from colorama import init

from .functions import process_tool_calls
from .scan import scan, get_project_structure
from .helpers import get_string_size_kb, bindings, style, num_tousend_tokens_from_messages
from .config_loader import config
from .complection import chat_completion_request

# Initialize colorama for Windows
init()

console = Console()

logger = logging.getLogger(__name__)


def initialize_messages(scan_result: str, initial_message: str = None) -> list:
    messages = []
    # merge_functions(work_folder)

    if config.role_system_content:
        messages.append({"role": "system", "content": config.role_system_content})
        if logger.getEffectiveLevel() == logging.DEBUG:
            console.print(f"[green][bold]SYSTEM MESSAGE[/bold]\n-------------\n{config.role_system_content}[/green]")

    if config.additional_user_content:
        messages.append({"role": "user", "content": config.additional_user_content})
        if logger.getEffectiveLevel() == logging.DEBUG:
            txt = f"[green][bold]ADDITIONAL USER MESSAGE\n!Will be added before each of your requests![/bold]\n-------------\n{config.additional_user_content}[/green]"
            console.print(txt)

    if scan_result:
        messages.append({"role": "system", "content": f"Working on the project: {scan_result}."})

    if initial_message:
        messages.append({"role": "user", "content": initial_message})
        console.print(f"[blue][bold]User:[/blue][/bold] {initial_message}")

    return messages


def handle_user_interaction(messages: list) -> str:
    tokens = num_tousend_tokens_from_messages(messages)
    role_user_content = prompt([('class:prompt', 'User: ')], multiline=True, key_bindings=bindings, style=style, rprompt=f"Used ~{tokens}K tokens")
    messages.append({"role": "user", "content": role_user_content})
    return role_user_content


def conversation(work_folder: str, full_scan: bool = False, structure_only: bool = False, initial_message: str = None) -> None:
    try:
        scan_result = None
        if structure_only:
            scan_result = get_project_structure(work_folder)
        elif full_scan:
            scan_result = scan(work_folder)
            logger.debug(f"Scanning completed. Size in kilobytes: {get_string_size_kb(scan_result):.2f} KB.")
        project_abspath = os.path.abspath(work_folder)
        messages = initialize_messages(scan_result, initial_message)
        skip_user_question = bool(initial_message)
        # merged_functions = merge_functions_describes(work_folder)

        while True:

            if not skip_user_question:
                handle_user_interaction(messages)
            else:
                skip_user_question = False

            chat_response = chat_completion_request(messages, config.default_functions)
            if chat_response.choices[0].finish_reason in ('length', 'tool_calls'):
                skip_user_question = True
            assistant_message = chat_response.choices[0].message
            messages.append(assistant_message)

            console.print(f"[red][bold]GPT[/bold][/red] Finish reason: {chat_response.choices[0].finish_reason}, Used {chat_response.usage.total_tokens} tokens")
            if assistant_message.content:
                    console.print(Markdown(assistant_message.content))
            print()

            skip_user_question |= process_tool_calls(messages, assistant_message, project_abspath)
    except KeyboardInterrupt:
        logger.info("Finished")
    finally:
        logger.info("Session completed")
