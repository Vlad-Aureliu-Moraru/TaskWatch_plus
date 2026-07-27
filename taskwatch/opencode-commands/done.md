---
description: Commit changes, finish the related TaskWatch task via the CLI, and push to GitHub
agent: build
---

You are the `/done` command. Execute the following steps in order using the available tools.

## 1. Stage changes

1. Run `git add -A` to stage all changes.
2. Run `git status --short` to see what was staged.
3. If nothing is staged, print "No changes to commit." and stop.

## 2. Gather context

1. Run `git diff --cached --stat` for the changed file summary.
2. Run `git branch --show-current` for the branch name.
3. Run `git remote -v` to check if a remote exists.

## 3. Load TaskWatch context

1. Try to read `.taskwatch-directory` in the current working directory.
2. Extract `directory_id` and `directory_name` if the file exists and is valid.
3. If invalid or missing, set `taskwatch_dir_id` to empty — skip all TaskWatch steps.

## 4. Find the related task

1. If `taskwatch_dir_id` is set, run `taskwatch task list --directory-id <directory_id> --unfinished --json`.
2. Search for the completed task using this priority:
   - **Branch match**: Look for an unfinished task whose name case-insensitively matches or contains the current branch name from step 2.
   - **Context match**: Scan the conversation history for task names, keywords, or project references that match an unfinished task.
3. If a single match is found, that is the **selected task**.
4. If multiple matches are found, present them to the user and ask which one was completed.
5. If no match is found, skip all TaskWatch steps — you will not finish a task or create a note.

## 5. Build commit message

1. If a task was matched, propose: `<task name>`
2. If no task was matched, propose a concise message from the changed file paths (e.g., "Update config and fix login handler").
3. Use the Question tool to ask: "Commit with this message?"
   - Options: "Yes", "Edit"
   - If "Edit", use the Question tool to ask: "Enter commit message:" with a custom text input.
   - If the user cancels, print "Cancelled." and stop.

## 6. Execute

1. Run `git commit -m "<message>"`.
2. If a task was matched:
   - Run `taskwatch task done <task_id>`.
   - Run `git diff --cached --stat` and use its output as the note content.
   - Run `taskwatch note create <task_id> <today_date> "<diff stat>"`.
3. If a remote exists for the current branch, run `git push` to push the commit.

## 7. Summary

Print:

```
Done.
  Committed: <N> files
  Task:      <task_name> (ID: <task_id>) — finished    (if applicable)
  Pushed:    origin/<branch>                            (if pushed)
```