# mdocr

`mdocr` is a small command-line script that converts documents into Markdown text.

It is built on top of [MarkItDown](https://github.com/microsoft/markitdown), Microsoft's library for turning many file formats into Markdown. On top of the base conversion, `mdocr` enables MarkItDown's **plugin system** and connects it to a Large Language Model (LLM) client, which adds OCR (optical character recognition) abilities for images and scanned content inside the files.

## What it does

Give it almost any document — a PDF, Word file, PowerPoint slide, image, spreadsheet, and more — and `mdocr` reads the content and returns clean, readable Markdown.

The interesting part is the LLM connection. When MarkItDown meets content it cannot parse directly (such as a picture of text or a scanned page), it sends that content to the LLM, which "reads" the image and returns the text. This means files that are mostly images can still become searchable, editable Markdown.

## How to use

> note: `ffmpeg` is required

1. Install `uv` via Homebrew

   ```bash
   brew install uv
   ```

2. Install `python` via `uv`

   ```bash
   uv python install 3.12
   ```

   then pin the current Python version

   ```bash
   uv python pin 3.12
   ```

3. Install the necessary tools in one Python environment

   ```bash
   uv tool install markitdown --with markitdown-ocr --with openai --force
   ```

4. Use this Python script

   ```bash
   uv run --with markitdown --with markitdown-ocr --with openai /path/to/your/mdocr.py document.pdf > output.md
   ```

   You can also make an alias for this command

   ```bash
   echo 'alias mdocr="uv run --with markitdown --with markitdown-ocr --with openai /path/to/your/mdocr.py"' >> ~/.zshrc
   ```

   then reload your shell (or open a new terminal)

   ```bash
   source ~/.zshrc
   ```

   Now you can use the `mdocr` command

   ```bash
   mdocr document.pdf > output.md
   ```

## How input works

`mdocr` accepts input in two ways:

- **File path** — pass the file as an argument.
- **Piped input** — pipe data in through standard input (stdin), e.g. from another command.

When input comes through a pipe, the file name is lost, so the script cannot guess the file type. The `--ext` option solves this by letting you tell the script the extension to use (for example `.pdf`). If both a file and piped input are given, the file is used and a warning is printed.

## How output works

The converted Markdown goes to one place:

- **Standard output (stdout)** — the default, so you can pipe it into other tools or just read it in the terminal.
- **File** — use the `-o` / `--output` option to write the result to a file. If that file already exists, it is replaced and a warning is printed.

## The LLM client

To power the OCR features, `mdocr` creates an OpenAI-compatible client. This means it can talk to any endpoint that speaks the OpenAI API — not only OpenAI itself, but also local models or other providers — as long as the `base_url` and `api_key` are set to match that endpoint. The model name used (`gemini-3.5-flash` in the script) can be changed to whatever model your endpoint offers.

## Error handling

The script is careful to fail cleanly:

- Conversion errors are reported on stderr and the script exits with a non-zero status.
- Missing input (no file and no pipe) prints the help text and exits.
- A broken output pipe (common when piping into commands like `head`) is handled silently so it does not look like a crash.
