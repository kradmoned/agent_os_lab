# OS AI Agent (Python)

A  coding agent built with the Google Gemini API. It can explore a working directory, read files, pdf ,write files, and execute Python scripts in a sandboxed location to iteratively complete tasks. This agent is optimized to complete my operating system labs

## Features
- Function calling via Gemini's tool API
- Iterative agent loop with bounded iterations
- Tools: get_files_info, get_file_content, write_file, run_python_file, get_pdf_content

## Setup
1. Install dependencies with `uv sync`
2. Add your `GEMINI_API_KEY` to a `.env` file
3. Set `WORKING_DIRECTORY` in `config.py`
4. Run: `uv run main.py "your prompt here"`

## Project Structure
- `main.py` — entry point and agent loop
- `functions/` — tool implementations
- `call_function.py` — dispatches function calls from the model
- `prompts.py` — system prompt
- `config.py` — configuration constants

## Prompt for OS Lab
- "Find the pdf file in the directory and extract examples from it in the form of ex1.c and so on and write all the example in seperate .c files in the convention ex1.c also complete all the tasks and write them in seperate .c file" 