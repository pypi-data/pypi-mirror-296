# Altcolor

A package designed to add color to text in console based applications.

## All predefined colors(colors that are not RGB) [Credit to 'colorama' ('https://pypi.org/project/colorama/') for these]: 
"BLACK"
"RED"
"GREEN"
"YELLOW"
"BLUE"
"MAGENTA"
"CYAN"
"WHITE"
"LIGHTBLACK"
"LIGHTRED"
"LIGHTGREEN"
"LIGHTYELLOW"
"LIGHTBLUE"
"LIGHTMAGENTA"
"LIGHTCYAN"
"LIGHTWHITE"

## Installation

Install via pip:

```bash
pip install altcolor
```

Example code: 

```py
from altcolor.altcolor import colored_text

print(colored_text((244, 5, 7), "Hello World!"))

print("Hello World!")

print(colored_text("BLUE", "Hello World!"))
```