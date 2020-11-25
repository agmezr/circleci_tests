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
        result = subprocess.run(["bash", "lint_check.sh"])
        if result.returncode != 0:
            print("Lint check failed, please verify it and try again.")
            sys.exit(1)

        print("Running tests")
        result = subprocess.run(["make", "tests_parallel"])
        if result.returncode != 0:
            print("Some tests failed, please verify it and try again.")
            sys.exit(1)



    # create release branch
    result = subprocess.run(["git", "flow", "release", "start", version])
    if result.returncode != 0:
        print("Could not create a release branch.")
        sys.exit(1)

    # bump version
    print("Bump version on version file")
    with open(VERSION_FILE, "w+") as f:
        f.write(f'APP_VERSION = "{version}"')

    print("Creating and pushing release")
    # commit new version
    result = subprocess.run(["git", "commit", "-m", version])
    if result.returncode != 0:
        print("Could not create commit for branch")
        sys.exit(1)

    subprocess.run(["git", "tag", "-a", version, "-m", version])

    # push new version
    subprocess.run(["git", "push", "origin", branch_name])

    subprocess.run(["git", "flow", "feature", "finish", version])

    for env in ("develop", "master"):
        print("Merge to ", env)
        subprocess.run(["git", "checkout", env])
        subprocess.run(["git", "merge", branch_name])
        subprocess.run(["git", "push", "origin", env, "--follow-tags"])

    print("Deploy done!")


if __name__ == "__main__":
    main()

