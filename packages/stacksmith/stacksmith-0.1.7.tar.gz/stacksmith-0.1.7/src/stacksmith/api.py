import re
import json
from collections import deque
from typing import Optional
from .helpers import (
    build_branch_structure,
    checkout_branch,
    create_empty_commit,
    create_new_branch,
    does_remote_branch_exist,
    get_commit_message,
    get_creation_commit,
    get_current_branch,
    get_pr_output,
    get_trunk_name,
    push_and_set_upstream,
    push_with_lease,
    rebase_and_update_refs,
    rebase_onto,
    run_command,
    update_remote_refs
)

def create_branch(branch_name: str, parent_branch: Optional[str] = None) -> None:
    if parent_branch is None:
        parent_branch = get_current_branch()
    
    create_new_branch(branch_name, parent_branch)
    
    commit_message = f"Created branch {branch_name} from {parent_branch}"
    create_empty_commit(commit_message)
    
    print(f"Created new branch {branch_name}")

def hoist_stack() -> None:
    _, children_dict, trunk_name = build_branch_structure()
    root = f"origin/{trunk_name}"
    current_branch = get_current_branch()
    children_dict[root] = [current_branch]
    queue = deque([root])
    while queue:
        parent_branch = queue.popleft()
        children_branches = children_dict.get(parent_branch, [])
        for child_branch in children_branches:
            creation_commit = get_creation_commit(branch_name=child_branch)
            if not creation_commit:
                print("Can't hoist {child_branch} since creation commit was not found.")
            else:
                rebase_onto(parent_branch, creation_commit, child_branch)
        queue.extend(children_branches)
    checkout_branch(current_branch)
    print(f"Hoisted stack from {current_branch} onto {root}")

def create_pr(title: Optional[str] = None) -> None:
    current_branch = get_current_branch()
    
    creation_commit = get_creation_commit(current_branch)
    
    if not creation_commit:
        print("Error: Branch creation commit not found. Please recreate the branch using 'ss create'.")
        return
    
    commit_message = get_commit_message(creation_commit)
    match = re.search(r'Created branch .* from (.*)', commit_message)
    if match:
        parent_branch = match.group(1)
    else:
        print("Error: Could not determine parent branch from commit message.")
        return
    
    update_remote_refs()
    
    default_branch = get_trunk_name()
        
    if does_remote_branch_exist(parent_branch):
        base_branch = parent_branch
    else:
        print(f"Parent branch {parent_branch} not found remotely. Defaulting to trunk branch.")
        base_branch = default_branch
    
    if title is None:
        title = f"Pull request for {current_branch}"
    
    parent_pr_url = None
    if base_branch != default_branch:
        parent_pr_output = get_pr_output(base_branch)
        if parent_pr_output:
            try:
                parent_pr_url = json.loads(parent_pr_output)['url']
            except json.JSONDecodeError:
                print("Warning: Could not parse parent PR URL.")

    description = f"This PR branches off of {base_branch}."
    if parent_pr_url:
        description += f"\n\nParent PR: {parent_pr_url}"

    create_pr_command = f'gh pr create --base "{base_branch}" --title "{title}" --body "{description}" --draft'
    output, error, return_code = run_command(create_pr_command)
    
    if return_code == 0:
        print(f"Successfully created draft PR: {output}")
    else:
        print(f"Error creating PR: {error}")

def propagate_commits() -> None:
    current_branch = get_current_branch()
    
    _, children_dict, _ = build_branch_structure()
    
    if current_branch not in children_dict:
        print(f"{current_branch} is either already merged or has no children.")
        return
    
    descendants = []
    to_visit = [current_branch]
    while to_visit:
        branch = to_visit.pop(0)
        descendants.extend(children_dict[branch])
        to_visit.extend(children_dict[branch])
    
    if not descendants:
        print(f"No descendant branches found for {current_branch}.")
        return
    
    print(f"Branch structure from {current_branch}:")
    def print_tree(branch: str, level: int = 0) -> None:
        print("  " * level + branch)
        for child in children_dict[branch]:
            print_tree(child, level + 1)
    print_tree(current_branch)
    
    tip_branches = [branch for branch in descendants if not children_dict[branch]]
    
    for tip_branch in tip_branches:
        print(f"Propagating commits up to {tip_branch}")
        _, error, return_code = rebase_and_update_refs(current_branch, tip_branch)
        
        if return_code != 0:
            print(f"Error during rebase of {tip_branch}: {error}")
            print("Please resolve conflicts and run 'git rebase --continue' manually.")
            return
        
        print(f"Successfully rebased branch stack from {current_branch} to {tip_branch}")

    checkout_branch(current_branch)

def publish_stack() -> None:
    current_branch = get_current_branch()
    _, children_dict, _ = build_branch_structure()
    
    if current_branch not in children_dict:
        branches_to_push = [current_branch]
    else:
        descendants = []
        to_visit = [current_branch]
        while to_visit:
            branch = to_visit.pop(0)
            descendants.extend(children_dict[branch])
            to_visit.extend(children_dict[branch])
        branches_to_push = [current_branch] + descendants

    for branch in branches_to_push:
        if does_remote_branch_exist(branch):
            _, error, return_code = push_with_lease(branch)
            if return_code == 0:
                print(f"Force-pushed updates to existing branch {branch}")
            else:
                print(f"Error force-pushing updates to {branch}: {error}")
        else:
            _, error, return_code = push_and_set_upstream(branch)
            if return_code == 0:
                print(f"Pushed new branch {branch} to remote")
            else:
                print(f"Error pushing new branch {branch}: {error}")