import os
import argparse
import fnmatch
import json
import platform
from datetime import datetime
from collections import defaultdict
from rich.console import Console
from rich.style import Style


# Function to read the configuration file and return relevant settings
def load_config(config_file):
    config = {}
    default_backup_config = {}

    try:
        with open(config_file, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                # Skip blank lines and comments
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.split("#", 1)[0].strip().strip('"')

    except FileNotFoundError:
        print(f"Config file '{config_file}' not found. Using default settings.")
        config = default_backup_config

    except UnicodeDecodeError:
        print(
            f"Error decoding the config file '{config_file}'. Please check the file encoding."
        )

    return config


def load_pywal_colors(config):
    os_name = platform.system()

    if os_name == "Windows":
        user = os.getlogin()
        colors_path = os.path.expanduser(f"C:\\Users\\{user}\\.cache\\wal\\colors.json")
    else:
        colors_path = os.path.expanduser("~/.cache/wal/colors.json")

    try:
        with open(colors_path, "r", encoding="utf-8") as file:
            colors = json.load(file)
            return colors["colors"]  # Extract the 'colors' dictionary

    except FileNotFoundError:
        if config.get("enable_pywal_not_found_error") == "on":
            print("Pywal colors file not found. Using default colors.")

        return {
            f"color{i}": "#FFFFFF" for i in range(0, 16)
        }  # Fallback to white for all colors

    except json.JSONDecodeError as e:
        if config.get("enable_json_decode_error") == "on":
            print(f"JSONDecodeError: {e.msg} at line {e.lineno} column {e.colno}")

        return {
            f"color{i}": "#FFFFFF" for i in range(0, 16)
        }  # Fallback to white for all colors
    

def print_ascii_art(config):
    # Read the path to the ASCII art file from the config
    ascii_art_file = config.get(
        "ascii_art_file", "assets/ascii/aboutme.txt"
    )  # Default path if not specified

    # Read the ASCII art from the file
    try:
        with open(ascii_art_file, "r") as file:
            ascii_art = file.read()

    except FileNotFoundError:
        if config.get("enable_ascii_not_found_error") == "on":
            print(
                f"Error: The ASCII art file '{ascii_art_file}' was not found. Trying to use the default ASCII art file."
            )

            if ascii_art_file != "assets/ascii/aboutme.txt":
                try:
                    with open("assets/ascii/aboutme.txt", "r") as file:
                        ascii_art = file.read()

                except FileNotFoundError:
                    print(f"Error: Default ASCII art file not found.")

        return "", 0  # Return empty art and 0 width in case of error

    # Calculate the width of the ASCII art (longest line + 1)
    ascii_lines = ascii_art.splitlines()
    ascii_width = max(len(line) for line in ascii_lines) + 1

    return ascii_art, ascii_width


def apply_fstring(config_str, local_vars):
    # Make sure we're inserting colors in Rich's format
    for var_name, var_value in local_vars.items():
        if var_name.startswith("cl") and isinstance(var_value, str):
            # Used for colour variables
            config_str = config_str.replace(f"{{{var_name}}}", f"[{var_value}]")
        else:
            # Used for other variables
            config_str = config_str.replace(f"{{{var_name}}}", f"{var_value}")

    return config_str


def generate_output(config):
    colors = load_pywal_colors(config)
    console = Console()

     # Map pywal colors to variables
    cl0 = f"{colors['color0']}"
    cl1 = f"{colors['color1']}"
    cl2 = f"{colors['color2']}"
    cl3 = f"{colors['color3']}"
    cl4 = f"{colors['color4']}"
    cl5 = f"{colors['color5']}"
    cl6 = f"{colors['color6']}"
    cl7 = f"{colors['color7']}"
    cl8 = f"{colors['color8']}"
    cl9 = f"{colors['color9']}"
    cl10 = f"{colors['color10']}"
    cl11 = f"{colors['color11']}"
    cl12 = f"{colors['color12']}"
    cl13 = f"{colors['color13']}"
    cl14 = f"{colors['color14']}"
    cl15 = f"{colors['color15']}"
    cl16 = "reset"
    clb = f"{Style(bold=True)}"

    ascii_art, ascii_width = print_ascii_art(config)

    if not ascii_art:
        return  # Exit if ASCII art could not be loaded
    
    aboutme = ""
    aboutme += "elo"
    # aboutme += config.get('test')

    lines = max(len(ascii_art.splitlines()), len(aboutme.splitlines()))

    for i in range(lines):
        ascii_line = (ascii_art.splitlines() + [""] * lines)[i]  # Ensure equal length
        info_line = (aboutme.splitlines() + [""] * lines)[
            i
        ]  # Ensure equal length
        console.print(f"{ascii_line:<{ascii_width}} {info_line}")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Fetch directory information with customizable options.\n\n"
            "Example usage:\n"
            "  python dirfetch.py /path/to/dir -fd -c custom.conf -e '*.log' -d 2"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Configuration Group
    config_group = parser.add_argument_group("Configuration")
    config_group.add_argument(
        "-c",
        "--config",
        default="config/aboutme.conf",
        help="Path to the config file (default: config/dirfetch.conf).",
    )

    args = parser.parse_args()

    config = load_config(args.config)
    generate_output(config)

if __name__ == "__main__":
    main()
