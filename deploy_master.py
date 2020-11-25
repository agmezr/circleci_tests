"""Deploys the develop branch to master"""
import argparse
import subprocess
import sys

VERSION_FILE = "app/version.py"

parser = argparse.ArgumentParser(description="Deploy env to the prod server")
parser.add_argument(
    "version",
    nargs=1,
    help="Version release for master, must be greater that current version",
)
parser.add_argument(
    "--tests",
    "-t",
    dest="validate",
    action="store_true",
    help="Run all the tests before creating the PR.",
)
parser.add_argument(
    "--no-tests",
    "-n",
    dest="validate",
    action="store_false",
    help="Skip the tests before the PR.",
)
parser.set_defaults(validate=True)
args = parser.parse_args()


def main():
    """Main function to make the steps needed to deploy to prod."""
    version = args.version[0]
    branch_name = f"release/{version}"
    print("Creating release for version")

    if args.validate:
        print("Checking lint")
        run_command("bash lint_check.sh", "Lint check failed, please verify it and try again.")

        print("Running tests")
        run_command("make tests_parallel", "Some tests failed, please verify it and try again.")

    # create release branch
    run_command(f"git flow release start {version}", "Could not create a release branch.")

    # bump version
    print("Bump version on version file")
    with open(VERSION_FILE, "w+") as f:
        f.write(f'APP_VERSION = "{version}"')

    print("Creating and pushing release")
    # commit new version
    run_command("git add .")
    run_command(f"git commit -m {version}")
    run_command(f"git tag -a {version} -m {version}")
    run_command(f"git push origin {branch_name}")

    for env in ("develop", "master"):
        print("Merge to ", env)
        run_command(f"git checkout {env}")
        run_command(f'git merge {branch_name} -m "Merge with {version}"')
        run_command(f"git push origin {env} --follow-tags")

    print("Deploy done!")


def run_command(cmd, error="Error, return code not 0"):
    """Runs a given command and verified that the return code is correct."""
    commands = cmd.strip().split(" ")
    result = subprocess.run(commands)
    if result.returncode != 0:
        print(error)
        sys.exit(1)


if __name__ == "__main__":
    main()

