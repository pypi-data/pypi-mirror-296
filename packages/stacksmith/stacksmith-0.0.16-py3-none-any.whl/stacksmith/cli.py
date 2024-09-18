import sys
from .api import create_branch, hoist_stack, create_pr, propagate_commits, publish_stack
from .helpers import run_git_command

def print_usage():
    print("Usage: ss <command> [<args>]")
    print("\nCustom commands:")
    print("  create <branch_name>                  Create a new branch with an empty initial commit")
    print("  hoist                                 Hoist (rebase) the stack onto the trunk")
    print("  pr [title]                            Create a pull request with automatic parent branch detection")
    print("  propagate                             Propagate commits from the current branch to all descendant branches")
    print("  publish                               Push all branches in the stack to remote")
    print("\nAll other commands are passed through to git.")

def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command == "create":
        if len(args) < 1:
            print("Error: Branch name is required for 'create' command.")
            sys.exit(1)
        create_branch(args[0])
    elif command == "hoist":
        if len(args) < 1:
            print("Error: Base branch is required for 'hoist' command.")
            sys.exit(1)
        hoist_stack(args[0])
    elif command == "pr":
        create_pr(args[0] if args else None)
    elif command == "propagate":
        propagate_commits()
    elif command == "publish":
        publish_stack()
    elif command in ["--help", "-h", "help"]:
        print_usage()
    else:
        # Passthrough to Git for unknown commands
        run_git_command([command] + args)

if __name__ == "__main__":
    main()