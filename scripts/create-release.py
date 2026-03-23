"""
A collection of utility functions used to automate the process of creating
github releases for TouchDesigner components.
"""

__author__ = "SudoMagic"
__copyright__ = "Copyright 2026, Project Name"
__credits__ = ["Matthew Ragan", "Gemini"]
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Matthew Ragan"

from pathlib import Path
import os
import subprocess
import shutil
from datetime import datetime
from dataclasses import dataclass


@dataclass
class releaseConfig:
    releasePath: Path
    releaseType: str
    isTest: bool


def get_config() -> releaseConfig:
    release_path = Path(Path.cwd(), os.getenv("SM_RELEASE_DIR"))
    release_type = os.getenv("SM_RELEASE_TYPE")

    # check to ensure that an env var is not none
    if os.getenv("SM_IS_TEST") == None:
        isTest = False
    else:
        isTest = True if os.getenv("SM_IS_TEST").upper() == 'TRUE' else False

    config = releaseConfig(
        releasePath=release_path,
        releaseType=release_type,
        isTest=isTest
    )
    return config


def create_release():
    msg_formatter("🚀 Starting release task")
    config = get_config()

    if config.isTest:
        print(config)
        return

    check_gh_cli_status()
    check_branch_status()
    semver = "v0.1"
    has_releases = has_tags()
    has_release_dir(config=config)
    has_release_files(config=config)

    if has_releases:
        semver = get_version_info()

    else:
        print(semver)

    match config.releaseType:
        case 'packageZip':
            msg_formatter("Creating package release")
            create_package_release(semver=semver, config=config)

        case 'toxFiles':
            msg_formatter("Creating bundle release")
            create_bundle_release(semver=semver, config=config)

        case _:
            msg_formatter(
                "No matching release type - check your task file to ensure SM_RELEASE_TYPE is 'packageZip' or 'toxFiles'")


def check_branch_status():
    if is_on_main_branch():
        msg_formatter(f"✅ Currently on the main branch - ready to publish")
    else:
        exit(f"❌ You are not on the main branch, please merge up before authoring a release")


def check_gh_cli_status() -> bool:
    if is_gh_cli_installed():
        pass
    else:
        exit("You can install the GitHub CLI by visiting https://cli.github.com/")

    if is_gh_authenticated():
        msg_formatter(
            "✅ You are authenticated with gh - ready to create a release")
    else:
        exit("❌ You are not authenticated with the github cli. Please run 'gh auth login'")


def create_package_release(semver: str, config: releaseConfig):
    archive = shutil.make_archive(
        "package",
        "zip",
        root_dir=config.releasePath)

    command_list = [
        'gh',
        'release',
        'create',
        semver,
        archive
    ]
    msg_formatter(f"✅ Creating release {semver}")
    subprocess.run(command_list)

    msg_formatter(f"✅ Performing file cleanup - deleting {archive}")
    os.remove(archive)


def create_bundle_release(semver: str, config: releaseConfig):
    files_to_upload = [
        each.as_posix() for each in config.releasePath.iterdir() if each.is_file()]
    command_list = [
        'gh',
        'release',
        'create',
        semver,
        *files_to_upload
    ]
    msg_formatter(f"✅ Creating release {semver}")
    subprocess.run(command_list)


def has_release_files(config: releaseConfig) -> bool:
    file_count = sum(
        1 for each in config.releasePath.iterdir() if each.is_file())
    if file_count > 0:
        return True
    else:
        exit("❌ Release does not currently contain any files, please ensure you've successfully generated files for release")


def has_tags() -> bool:
    tag_cmd = [
        "git",
        "tag"
    ]
    results = subprocess.check_output(tag_cmd, text=True).strip()
    if len(results) > 0:
        return True
    else:
        return False


def has_release_dir(config: releaseConfig):
    if config.releasePath.exists():
        pass
    else:
        exit("❌ Repo does not have a release directory - first output your files")


def get_version_info() -> str:
    """Pulls version info from the latest version tag off of the repo itself"""

    # 1. Get the latest tag name (matching your vX.Y pattern)
    # Using the same logic as your GitHub Action
    tag_cmd = [
        "git",
        "describe",
        "--tags",
        "--abbrev=0",
        "--match",
        "v[0-9]*.[0-9]*",
    ]
    latest_tag = result_from_subprocess(tag_cmd)

    major_minor_patch = latest_tag.split(".")
    major_minor = ".".join([major_minor_patch[0], major_minor_patch[1]])

    # 2. Get the count of commits from that tag to the current HEAD
    count_cmd = ["git", "rev-list", "--count", f"{major_minor}..HEAD"]
    num_commits = result_from_subprocess(count_cmd)

    semver = f"{major_minor}.{num_commits}"
    return semver


def result_from_subprocess(cmdList: list[str]) -> str:
    """
    """
    result = subprocess.run(
        cmdList, stdin=subprocess.DEVNULL, capture_output=True, text=True, check=True)
    result_str = result.stdout.strip()
    return result_str


def msg_formatter(msg: str, indent: int = 0, displayInTextport: bool = True) -> str:
    '''Prints and returns a string with a time stamp and indent - suitable for logs
    and the textport
    '''
    indentText = f"{'--' * indent}> "
    formattedMsg = f"{get_pretty_timestamp()} [~] {indentText if indent > 0 else ''}{msg}"
    if displayInTextport:
        print(formattedMsg)
    return formattedMsg

# NOTE gemini generated function


def get_pretty_timestamp():
    """Returns the current time formatted as YYYY-MM-DD | HH:MM:SS"""
    now = datetime.now()
    return now.strftime("%Y-%m-%d | %H:%M:%S")

# NOTE - Gemini generated


def is_gh_cli_installed():
    try:
        # Run 'gh --version' and capture output.
        # check=True raises CalledProcessError if the command fails (e.g., gh is not found)
        result = subprocess.run(
            ["gh", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # Decode output as text
        )
        msg_formatter(
            f"✅ GitHub CLI is installed. Version: {result.stdout.strip()}\n")
        return True
    except FileNotFoundError:
        # This error is raised if the 'gh' executable is not found in the PATH
        msg_formatter("❌ GitHub CLI is not installed (File Not Found Error).")

        return False
    except subprocess.CalledProcessError as e:
        # This handles cases where 'gh' is found but exits with a non-zero status
        msg_formatter(
            f"GitHub CLI check failed with error: {e.stderr.strip()}")
        return False

# NOTE - Gemini generated


def is_gh_authenticated():
    """
    Checks if the current user is authenticated with the GitHub CLI.
    Returns:
        bool: True if authenticated, False otherwise.
    """
    try:
        # We use 'gh auth status' to check connection.
        # 'capture_output=True' keeps the terminal clean.
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True
        )

        # GitHub CLI returns exit code 0 if authenticated
        return result.returncode == 0

    except FileNotFoundError:
        # This happens if 'gh' is not installed on the system at all
        print("Error: GitHub CLI (gh) is not installed or not in PATH.")
        return False


# NOTE - Gemini generated
def is_on_main_branch():
    """
    Checks if the current Git HEAD is pointing to the 'main' branch.
    Returns:
        bool: True if on 'main', False otherwise.
    """
    try:
        # 'symbolic-ref --short HEAD' returns the branch name (e.g., 'main')
        # It returns a non-zero exit code if you are not on a branch.
        result = subprocess.run(
            ["git", "symbolic-ref", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )

        current_branch = result.stdout.strip()
        return current_branch == "main"

    except subprocess.CalledProcessError:
        # This happens if:
        # 1. You are in a 'detached HEAD' state (pointing to a specific commit)
        # 2. You are not in a git repository
        return False
    except FileNotFoundError:
        # Git is not installed
        return False


if __name__ == "__main__":
    create_release()
