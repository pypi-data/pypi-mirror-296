import argparse
import logging
import os
from .helpers import check_git_presence
from .conversation import conversation
from .config_loader import open_config_file, config
from .version import PROGRAM_NAME, PROGRAM_VERSION
import sys

# Добавляем корневую директорию в PYTHONPATH, если она не там
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME, description="Scanning the folder and sending to GPT")
    parser.add_argument('path', nargs='?', default=os.getcwd(), help="Path to the directory to scan")
    parser.add_argument("-c", "--contents", action="store_true", help="Scan directory structure and files content")
    parser.add_argument("-s", "--structure-only", action="store_true", help="Scan directory structure")
    parser.add_argument("--config", action="store_true", help="Open configuration file")
    parser.add_argument('-v', '--version', action='version', version=f"%(prog)s {PROGRAM_VERSION}")
    parser.add_argument('-m', '--message', help="Message to send as initial user input")
    parser.add_argument('-vvv', '--verbose', action='store_true', help="Enable verbose/debug mode")
    return parser.parse_args()


def handle_command(args: argparse.Namespace):
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.debug(f"Using configs in: {config.path}")

    if args.config:
        open_config_file()
    else:
        work_folder = args.path

        _text = ""
        full_scan, structure_only = False, False
        if args.structure_only:
            structure_only = True
            _text = "with scan structure only"
        elif args.contents:
            full_scan = True
            _text = "with full scan"

        logger.info(f"Starting work on the project at: {os.path.abspath(work_folder)} {_text}")

        if not os.path.isdir(work_folder):
            logger.error(f"Error: Path '{work_folder}' is not a directory.")
            raise SystemExit(1)

        if not check_git_presence(work_folder):
            logger.warning("No .git directory found in the working directory")

        conversation(work_folder, full_scan, structure_only, args.message)

def main() -> None:
    args = parse_args()
    handle_command(args)

if __name__ == '__main__':
    main()
