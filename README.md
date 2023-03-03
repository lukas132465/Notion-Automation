# Notion Automation

## Description

This script is used to generate a random quote in a notion block.

## Usage

After downloading:
- Fill out the `quotes.txt` file according to the example format
- Open the `generate_quote.py` file and fill out the first three variables:
    - `file_path` is the path of your quote .txt file
    - `cookie` is the token_v2 cookie of notion, this can be found in your browser
    - `block` is a link to the block you want to contain the quote
- Open startup by pressing Windows + r and running `shell:common startup`, then move the `notion.bat` script there after including your script path

## Warning

The script will delete the specified block completeley before adding the quote.