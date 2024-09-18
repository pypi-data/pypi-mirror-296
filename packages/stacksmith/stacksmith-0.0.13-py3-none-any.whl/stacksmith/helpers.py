from collections import deque
import sys
import subprocess
import re
from typing import Tuple, List, Dict, Optional, Set

PULL_REQUEST_LABEL = "merge-to-trunk-only"

# helpers to run commands
def run_command(command: str) -> Tuple[str, str, int]:
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    return stdout.decode().strip(), stderr.decode().strip(), process.returncode

def run_git_command(args: List[str]) -> None:
    try:
        subprocess.run(['git'] + args, check=True, text=True)
    except subprocess.CalledProcessError as e:
        print(e.stderr, file=sys.stderr, end='')
        sys.exit(e.returncode)

# helpers to perform git operations
def checkout_branch(branch_name: str):
    return run_command(f'git checkout {branch_name}')

def create_branch(branch_name: str, parent_branch: str) -> Tuple[str, str, int]:
    return run_command(f'git checkout -b "{branch_name}" "{parent_branch}"')

def create_empty_commit(message: str) -> Tuple[str, str, int]:
    return run_command(f'git commit --allow-empty -m "{message}"')

def create_pull_request(base_branch: str, title: str, description: str, label: str = PULL_REQUEST_LABEL) -> Tuple[str, str, str]:
    return run_command(f'gh pr create --base "{base_branch}" --title "{title}" --body "{description}" --label "{label}" --draft')

def does_remote_branch_exist(branch: str) -> bool:
    return run_command(f'git ls-remote --exit-code --heads origin {branch}')[2] == 0

def get_commit_message(commit_hash: str) -> str:
    return run_command(f'git log -1 --pretty=%B {commit_hash}')[0]

def get_commit_with_message(branch: str, message: str, max_count: int = 100) -> Tuple[str, str, int]:
    return run_command(f'git log {branch} --format=%H --max-count=1 --grep="{message}" -n {max_count}')

def get_current_branch() -> str:
    return run_command('git rev-parse --abbrev-ref HEAD')[0]

def get_local_branches() -> Set[str]:
    return set(run_command('git branch --format="%(refname:short)"')[0].split('\n'))

def get_merged_branches(trunk: str) -> Set[str]:
    return set(run_command(f'git branch --remotes --merged origin/{trunk} --format="%(refname:short)"')[0].split('\n'))

def get_pr_output(branch: str) -> str:
    return run_command(f'gh pr view {branch} --json url')[0]

def get_trunk_name() -> str:
    return run_command('git remote show origin | sed -n "/HEAD branch/s/.*: //p"')[0]

def push_and_set_upstream(branch: str, remote: str = 'origin') -> Tuple[str, str, int]:
    return run_command(f'git push --set-upstream {remote} {branch}')

def push_with_lease(branch: str) -> Tuple[str, str, int]:
    return run_command(f'git push origin {branch} --force-with-lease')

def rebase_onto(base_branch: str, starting_commit: str, target_branch: str) -> Tuple[str, str, int]:
    return run_command(f'git rebase --onto {base_branch} {starting_commit}^ {target_branch}')

def update_remote_refs() -> Tuple[str, str, int]:
    return run_command('git fetch origin')

# internal helpers
def get_creation_commit(branch_name: str, max_search_depth: int = 100) -> Optional[str]:
    grep_pattern = f"Created branch {branch_name} from"
    creation_commit, _, return_code = get_commit_with_message(branch_name, grep_pattern, max_search_depth)
    return creation_commit.strip() if return_code == 0 and creation_commit else None

def get_children_dict() -> Dict[str, List[str]]:
    trunk, local_branches = get_trunk_name(), get_local_branches(), 
    if trunk in local_branches:
        local_branches.remove(trunk)

    parent_dict: Dict[str, str] = {}
    children_dict: Dict[str, List[str]] = {branch: [] for branch in local_branches}
    merged_branches = get_merged_branches(trunk)

    for local_branch in local_branches:
        if f'origin/{local_branch}' in merged_branches:
            continue

        parent_commit = get_creation_commit(branch_name=local_branch)
        if parent_commit:
            commit_message = get_commit_message(parent_commit)
            parent_match = re.search(r'Created branch .* from (.*)', commit_message)
            if parent_match:
                parent = parent_match.group(1)
                if parent in local_branches:
                    parent_dict[local_branch] = parent
                    children_dict[parent].append(local_branch)

    return children_dict

def recursive_rebase(root_branch: Optional[str] = None) -> None:
    children_dict, current_branch = get_children_dict(), get_current_branch()
    
    if root_branch: # hoisting
        children_dict[root_branch] = [current_branch]
    else: # propagating
        root_branch = current_branch

    queue = deque([root_branch])
    while queue:
        parent_branch = queue.popleft()
        children_branches = children_dict.get(parent_branch, [])
        for child_branch in children_branches:
            creation_commit = get_creation_commit(branch_name=child_branch)
            if not creation_commit:
                print(f"Skipping {child_branch} since creation commit was not found.")
            else:
                rebase_onto(parent_branch, creation_commit, child_branch)
        queue.extend(children_branches)
    checkout_branch(current_branch)
    