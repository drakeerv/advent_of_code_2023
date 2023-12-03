import argparse
import pathlib
import logging
import subprocess
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run specified day")
    parser.add_argument("-d", "--day", type=int, help="Day to run", required=True)
    parser.add_argument("-p", "--part", type=int, help="Part to run", default=1)
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-o", "--output", action="store_true", help="Show output")
    args = parser.parse_args()

    level = (logging.DEBUG if args.verbose else logging.INFO)

    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=level
    )

    folder = pathlib.Path(f"days/{args.day}/parts/{args.part}")
    if not folder.exists():
        logging.error(f"Day {args.day} does not exist")
        sys.exit(1)

    in_file = folder / "input.in"
    if not in_file.exists():
        logging.error(f"Input file for day {args.day} does not exist")
        sys.exit(1)

    output_file = folder / "output.out"
    if output_file.exists():
        logging.warning(f"Output file for day {args.day} already exists")

    python_file = folder / "main.py"
    if not python_file.exists():
        logging.error(f"Python file for day {args.day} does not exist")
        sys.exit(1)

    logging.info(f"Running day {args.day} part {args.part}")
    logging.debug(f"Input file: {in_file}")
    logging.debug(f"Python file: {python_file}")

    command = f"{sys.executable} {python_file}"
    logging.debug(f"Command: {command}")

    with open(in_file, "r") as f:
        input_data = f.read()

    logging.info(f"Running day")
    output = subprocess.check_output(command, input=input_data, shell=False, text=True)
    logging.info(f"Done running day")

    if args.output:
        logging.info(f"Output:\n{output}")

    with open(output_file, "w") as f:
        f.write(output)

    logging.info(f"Output written to {output_file}")
    logging.info("Done")