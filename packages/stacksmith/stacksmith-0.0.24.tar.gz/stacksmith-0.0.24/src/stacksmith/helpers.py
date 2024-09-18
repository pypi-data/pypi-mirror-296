from collections import deque
import re
import subprocess
import sys
from typing import Callable, List, Dict, Optional, Set, Tuple

def run_command(command: str) -> str:
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, command, stderr.decode().strip())
    return stdout.decode().strip()

def run_git_command(args: List[str]) -> str:
    try:
        subprocess.run(['git'] + args, check=True, text=True)
    except subprocess.CalledProcessError as e:
        print(e.stderr, file=sys.stderr, end='')
        sys.exit(e.returncode)

# Update other helper functions to use the new run_command
def checkout_branch(branch_name: str) -> str:
    return run_command(f'git checkout {branch_name}')

def create_branch(branch_name: str, parent_branch: str) -> str:
    return run_command(f'git checkout -b "{branch_name}" "{parent_branch}"')

def create_empty_commit(message: str) -> str:
    return run_command(f'git commit --allow-empty -m "{message}"')

def create_pull_request(base_branch: str, title: str, description: str, label: str = "merge-to-trunk-only") -> str:
    return run_command(f'gh pr create --base "{base_branch}" --title "{title}" --body "{description}" --label "{label}" --draft')

def does_remote_branch_exist(branch: str) -> bool:
    try:
        run_command(f'git ls-remote --exit-code --heads origin {branch}')
        return True
    except subprocess.CalledProcessError:
        return False

def get_commit_message(commit_hash: str) -> str:
    return run_command(f'git log -1 --pretty=%B {commit_hash}')

def get_commit_with_message(branch: str, message: str, max_count: int = 100) -> str:
    return run_command(f'git log {branch} --format=%H --max-count=1 --grep="{message}" -n {max_count}')

def get_current_branch() -> str:
    return run_command('git rev-parse --abbrev-ref HEAD')

def get_local_branches() -> Set[str]:
    return set(run_command('git branch --format="%(refname:short)"').split('\n'))

def get_merged_branches(trunk: str) -> Set[str]:
    return set(run_command(f'git branch --remotes --merged origin/{trunk} --format="%(refname:short)"').split('\n'))

def get_pr_output(branch: str) -> str:
    return run_command(f'gh pr view {branch} --json url')

def get_trunk_name() -> str:
    return run_command('git remote show origin | sed -n "/HEAD branch/s/.*: //p"')

def push_and_set_upstream(branch: str, remote: str = 'origin') -> str:
    return run_command(f'git push --set-upstream {remote} {branch}')

def push_with_lease(branch: str) -> str:
    return run_command(f'git push origin {branch} --force-with-lease')

def rebase_onto(base_branch: str, starting_commit: str, target_branch: str) -> str:
    return run_command(f'git rebase --onto {base_branch} {starting_commit}^ {target_branch}')

def update_commit_parent(commit_hash: str, new_parent: str) -> str:
    return run_command(f"git filter-branch -f --msg-filter 'sed -E \"s/(Branch .* extends ).*/\\1{new_parent}/\"' -- {commit_hash}^..HEAD")

def update_remote_refs() -> str:
    return run_command('git fetch origin')

# Internal helpers
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
    grep_pattern = f"Branch {branch_name} extends"
    creation_commit = get_commit_with_message(branch_name, grep_pattern, max_search_depth)
    return creation_commit.strip() if creation_commit else None

def get_parent_branch(child_branch: str) -> Optional[str]:
    creation_commit = get_creation_commit(child_branch)
    if not creation_commit:
        return None
    
    commit_message = get_commit_message(creation_commit)
    parent_match = re.search(r'Branch .* extends (.*)', commit_message)    
    return parent_match.group(1) if parent_match else None

def get_children_dict() -> Dict[str, List[str]]:
    trunk = get_trunk_name()
    local_branches = get_local_branches()
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
    children_dict = get_children_dict()
    current_branch = get_current_branch()
    
    if root_branch:  # anchoring
        children_dict[root_branch] = [current_branch]
    else:  # propagating
        root_branch = current_branch

    def rebase_action(branch: str, children: List[str]) -> None:
        for child_branch in children:
            creation_commit = get_creation_commit(branch_name=child_branch)
            if not creation_commit:
                print(f"Creation commit not found for branch {child_branch}")
                return
            rebase_onto(branch, creation_commit, child_branch)
            print(f"Rebased {child_branch} onto {branch}")
            if child_branch == current_branch:  # base was anchored successfully
                new_parent = root_branch.split("origin/")[-1]
                print(f"Updating parent of {current_branch} to {new_parent}")
                update_commit_parent(get_creation_commit(current_branch), new_parent)

    bfs_tree_traversal(root_branch, children_dict, rebase_action)
    checkout_branch(current_branch)