from .exec import exec_flumina_script, _ExecMode
from .logging import get_logger
from .util import log_time

import argparse
import os
import json


def export_command(args):
    file_path = args.path

    # First try to run the script under 'meta' device
    with log_time(f"Running script {file_path} under meta device context"):
        try:
            exec_flumina_script(file_path, exec_mode=_ExecMode.SERVE, device="meta")
        except Exception as e:
            get_logger().exception(
                f"Flumina script failed while running under meta device context. It is "
                f"highly recommended that Flumina scripts be made to "
                f"run where all parameters are initialized as meta device. "
                f"This ensures fast load times and efficiency when deployed "
                f"to Fireworks. Please check your script and try again"
            )

    with log_time(f"Running script {file_path} for export"):
        exported_mod, code = exec_flumina_script(file_path)

        dir = args.output_path
        if not os.path.exists(dir):
            os.mkdir(dir)

        with open(os.path.join(dir, "model.safetensors"), "wb") as f, log_time(
            "Writing exported weights to disk"
        ):
            f.write(exported_mod.serialized_weights)

        with open(os.path.join(dir, "flumina.py"), "w") as f, log_time(
            "Writing exported code to disk"
        ):
            f.write(code)

        with open(os.path.join(dir, "fireworks.json"), "w") as f, log_time(
            "Writing model metadata to disk"
        ):
            json.dump(
                {"_is_flumina_model": True, "paths": exported_mod.path_to_method_name},
                f,
            )


def main():
    # Create the top-level parser
    parser = argparse.ArgumentParser(description="Flumina CLI Tool")
    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="The Flumina command to run",
    )

    # Create the parser for the "run" command
    parser_run = subparsers.add_parser(
        "export", help="Run a Flumina script and upload contained Models"
    )
    parser_run.add_argument("path", type=str, help="Path to the Flumina script to run")
    parser_run.add_argument(
        "--output-path",
        type=str,
        required=False,
        help="Output directory to which to serialize the model.",
    )
    parser_run.set_defaults(func=export_command)

    # Parse the arguments
    args = parser.parse_args()

    # Dispatch to the appropriate function based on the command
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
