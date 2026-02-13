import sys
from typing import List, Optional

from diba._cli import options
from diba._cli.commands.bench import run_bench_state_base_command
from diba._cli.commands.vedic_d1 import run_vedic_d1_command
from diba._cli.errors import CLIError
from diba._cli.output import render_json, render_pretty_bench, render_pretty_d1


def dispatch(argv: Optional[List[str]] = None) -> int:
    parser = options.build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "vedic" and args.vedic_command == "d1":
            result = run_vedic_d1_command(args)
            fmt = options.parse_output_format(args.format)
            if fmt.value == "json":
                print(render_json(result))
            else:
                print(render_pretty_d1(result))
            return 0
        if args.command == "bench" and args.bench_command == "state-base":
            result = run_bench_state_base_command(args)
            fmt = options.parse_output_format(args.format)
            if fmt.value == "json":
                print(render_json(result))
            else:
                print(render_pretty_bench(result))
            return 0
        parser.print_help()
        return 1
    except CLIError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


def main(argv: Optional[List[str]] = None) -> None:
    sys.exit(dispatch(argv))
