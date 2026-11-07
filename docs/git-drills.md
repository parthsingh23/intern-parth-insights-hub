# Git Workflow Drills

## Drill 1: Branch Creation and Commit

- Starting branch: `week1-setup`
- Created branch: `drill/branch-commit`
- Objective: Practised creating a new branch from the assignment branch.

## Drill 2: Amend Commit Message

- Created `docs/drills/amend-practice.txt` as a practice file.
- Initially committed the file with an incorrect commit message: `update`.
- Corrected the commit message using `git commit --amend -m "docs(git): add amend practice file"`.
- Verified the updated commit message using `git log`.
- Observed that amending a commit creates a new commit hash, replacing the previous commit.

**Final commit:** `83fc94c docs(git): add amend practice file`

## Drill 3: Merge Conflict Resolution

- Created a base file: `docs/drills/conflict/status.txt`.
- Created two independent branches: `drill/conflict-a` and `drill/conflict-b`.
- Team A and Team B modified the same line independently.
- Merging Team A into Team B produced a content conflict.
- Inspected the conflict markers and manually resolved the file, preserving both contributions.
- Staged the resolved file using `git add`.
- Completed the merge with a merge commit.
- Integrated the conflict exercise into `drill/branch-commit` using `git merge --no-ff`.
- Resolution: `Project status: reviewed by team A and team B`.

## Drill 4: Reverting a Commit

- Created `docs/drills/revert-practice.txt` as a practice file.
- Committed it using `test(git): add revert practice file`.
- Used `git revert` to reverse the commit.
- Verified that the original commit remained in Git history.
- Verified that the practice file was removed by the revert commit.

**Original commit:** `874d88d`  
**Revert commit:** `b1db45e`

## Drill 5: Merge vs Rebase

1. **Merge** combines changes from different branches and can create a merge commit.
2. **Rebase** reapplies commits onto another base commit, creating new commit hashes.
3. Merge preserves the existing branch history and is useful for collaborative workflows.
4. Rebase can create a cleaner, linear commit history.
5. Avoid rebasing commits that have already been shared with others, because rewriting shared history can disrupt collaborators.
