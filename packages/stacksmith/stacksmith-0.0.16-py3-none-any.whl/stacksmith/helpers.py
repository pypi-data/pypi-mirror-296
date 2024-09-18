from collections import deque
import re
import subprocess
import sys
from typing import Callable, List, Dict, Optional, Set, Tuple

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

def update_commit_parent(commit_hash: str, new_parent: str) -> Tuple[str, str, str]:
    return run_command(f"git filter-branch -f --msg-filter 'sed -E \"s/(Branch .* is child of ).*/\\1{new_parent}/\"' -- {commit_hash}^..HEAD")

def update_remote_refs() -> Tuple[str, str, int]:
    return run_command('git fetch origin')

# internal helpers
def bfs_tree_traversal(
    root: str,
    children_dict: Dict[str, List[str]],
    node_callback: Callable[[str, List[str]], None]
) -> None:
    queue = deque([root])
    while queue:
        current_node = queue.popleft()
        children = children_dict.get(current_node, [])
        node_callback(current_node, children)
        queue.extend(children)

def get_creation_commit(branch_name: str, max_search_depth: int = 100) -> Optional[str]:
    grep_pattern = f"Branch {branch_name} is child of"
    creation_commit, _, return_code = get_commit_with_message(branch_name, grep_pattern, max_search_depth)
    return creation_commit.strip() if return_code == 0 and creation_commit else None

def get_parent_branch(child_branch: str) -> Optional[str]:
    creation_commit = get_creation_commit(child_branch)
    if not creation_commit:
        print(f"Could not find commit with lineage information for branch {child_branch}")
        return None
    
    commit_message = get_commit_message(creation_commit)
    parent_match = re.search(r'Branch .* extends (.*)', commit_message)
    if not parent_match:
        print(f"Could not find parent branch in commit message:\n{commit_message}")
        return None
    
    return parent_match.group(1)

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

        parent_branch = get_parent_branch(local_branch)

        if parent_branch and parent_branch in local_branches:
            parent_dict[local_branch] = parent_branch
            children_dict[parent_branch].append(local_branch)

    return children_dict

def recursive_rebase(root_branch: Optional[str] = None) -> None:
    children_dict, current_branch = get_children_dict(), get_current_branch()
    
    if root_branch:  # hoisting
        children_dict[root_branch] = [current_branch]
        new_parent = root_branch.split("origin/")[-1]
        print(f"Updating parent of {current_branch} to {new_parent}")
        update_commit_parent(get_creation_commit(current_branch), new_parent)
    else:  # propagating
        root_branch = current_branch

    def rebase_action(branch: str, children: List[str]) -> None:
        for child_branch in children:
            creation_commit = get_creation_commit(branch_name=child_branch)
            if not creation_commit:
                print(f"Skipping {child_branch} since creation commit was not found.")
            else:
                rebase_onto(branch, creation_commit, child_branch)
                print(f"Rebased {child_branch} onto {branch}")

    bfs_tree_traversal(root_branch, children_dict, rebase_action)
    checkout_branch(current_branch)
    