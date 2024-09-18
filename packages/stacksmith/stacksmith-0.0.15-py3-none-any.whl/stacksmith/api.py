import re
import json
from typing import Optional
from .helpers import (
    get_children_dict,
    create_branch as _create_branch,
    create_empty_commit,
    create_pull_request,
    does_remote_branch_exist,
    get_commit_message,
    get_creation_commit,
    get_current_branch,
    get_pr_output,
    get_trunk_name,
    recursive_rebase,
    push_and_set_upstream,
    push_with_lease,
    update_remote_refs
)

def create_branch(branch_name: str) -> None:
    parent_branch = get_current_branch()
    
    _create_branch(branch_name, parent_branch)
    
    commit_message = f"Created branch {branch_name} from {parent_branch}"
    create_empty_commit(commit_message)
    
    print(f"Created new branch {branch_name}")

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
    
    trunk_name = get_trunk_name()
    if not trunk_name:
        print("Error: Could not determine trunk name.")
        return
        
    if does_remote_branch_exist(parent_branch):
        base_branch = parent_branch
    else:
        print(f"Parent branch {parent_branch} not found remotely. Defaulting to trunk branch.")
        base_branch = trunk_name
    
    if title is None:
        title = f"Pull request for {current_branch}"
    
    parent_pr_url = None
    if base_branch != trunk_name:
        parent_pr_output = get_pr_output(base_branch)
        if parent_pr_output:
            try:
                parent_pr_url = json.loads(parent_pr_output)['url']
            except json.JSONDecodeError:
                print("Warning: Could not parse parent PR URL.")

    description = f"Depends on: {parent_pr_url}" if parent_pr_url else ""

    output, error, return_code = create_pull_request(base_branch, title, description)
    
    if return_code == 0:
        print(f"Successfully created draft PR: {output}")
    else:
        print(f"Error creating PR: {error}")

def hoist_stack(base_branch: str) -> None:
    recursive_rebase(base_branch)
    print(f"Hoisted stack onto {base_branch} successfully")
    
def propagate_commits() -> None:
    recursive_rebase()
    print("Propagated changes successfully")

def publish_stack() -> None:
    children_dict, current_branch = get_children_dict(), get_current_branch()
    
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
                if "Everything up-to-date" in error:
                    print(f"Branch {branch} is already up-to-date with remote")
                else:
                    print(f"Force-pushed updates to existing branch {branch}")
            else:
                print(f"Error force-pushing updates to {branch}: {error}")
        else:
            _, error, return_code = push_and_set_upstream(branch)
            if return_code == 0:
                print(f"Pushed new branch {branch} to remote")
            else:
                print(f"Error pushing new branch {branch}: {error}")