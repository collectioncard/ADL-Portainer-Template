"""Small, dependency-free example of a command-line research job."""

import argparse
import json
from pathlib import Path


def calculate(operation: str, a: float, b: float) -> float:
    if operation == "add":
        return a + b
    if operation == "subtract":
        return a - b
    if operation == "multiply":
        return a * b
    if operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    raise ValueError(f"Unknown operation: {operation}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple Python calculator experiment")
    parser.add_argument("operation", choices=["add", "subtract", "multiply", "divide"])
    parser.add_argument("a", type=float, help="First number")
    parser.add_argument("b", type=float, help="Second number")
    parser.add_argument("--output", type=Path, help="Optional JSON result file (use /results in Docker)")
    args = parser.parse_args()

    try:
        result = calculate(args.operation, args.a, args.b)
    except ValueError as error:
        parser.error(str(error))

    data = {"operation": args.operation, "a": args.a, "b": args.b, "result": result}
    result_json = json.dumps(data, indent=2) + "\n"
    print(result_json, end="")

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result_json, encoding="utf-8")
        print(f"Saved result to {args.output}")


if __name__ == "__main__":
    main()
