#!/usr/bin/env python3
import os
import sys
import argparse
from markitdown import MarkItDown
from openai import OpenAI

def main():
    parser = argparse.ArgumentParser(
        description="Convert files to Markdown using MarkItDown with OCR plugin support."
    )
    # File input
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to the input file (optional if piped via standard input)"
    )
    # Output path (-o / --output)
    parser.add_argument(
        "-o", "--output",
        dest="output",
        help="Path to the output Markdown file"
    )
    # File extension hint for piped input (stdin has no name/extension)
    parser.add_argument(
        "--ext",
        dest="ext",
        default=None,
        help="File extension hint for piped input, e.g. --ext .pdf"
    )
    args = parser.parse_args()

    client = OpenAI(
        api_key="your-api-key",
        base_url="https://your-llm-endpoint/v1"
    )

    md = MarkItDown(
        enable_plugins=True,
        llm_client=client,
        llm_model="gemini-3.5-flash"
    )

    piped = not sys.stdin.isatty()
    if args.file and piped:
        print(
            "mdocr: warning: both stdin and a file argument given; using the file.",
            file=sys.stderr
        )

    try:
        # 1. Handle piped input (e.g., cat file.pdf | mdocr)
        if piped and not args.file:
            result = md.convert_stream(sys.stdin.buffer, file_extension=args.ext)
        # 2. Handle file path input
        elif args.file:
            result = md.convert(args.file)
        else:
            parser.print_help()
            sys.exit(1)
    except Exception as e:
        print(f"mdocr: conversion failed: {e}", file=sys.stderr)
        sys.exit(1)

    # Output to file or standard stdout
    try:
        if args.output:
            if os.path.exists(args.output):
                print(
                    f"mdocr: warning: overwriting existing file: {args.output}",
                    file=sys.stderr
                )
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(result.text_content)
        else:
            sys.stdout.buffer.write(result.text_content.encode("utf-8"))
    except BrokenPipeError:
        sys.exit(0)
    except Exception as e:
        print(f"mdocr: writing output failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
