""" CLI tool to automate git push commands """

import os
import sys

from ..general_modules import utils


def get_branch() -> str:
    """Get the current git branch

    Returns:
        str: The current git branch
    """

    return utils.cmdx("git branch --show-current")


def main():
    """Main function"""

    branch = get_branch()

    if not branch:
        print("No branch found")
        sys.exit(1)

    print(f"Pushing branch {branch}")

    # utils.cmdx(f"git push origin {branch}")


if __name__ == "__main__":
    main()
