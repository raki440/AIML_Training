#!/usr/bin/env bash
# Day 1 demo: Git basics. Run it whole (bash day1_basics.sh) or paste it line by line in class.
set -e
rm -rf demo-repo && mkdir demo-repo && cd demo-repo
git init -b main
git config user.name "Student" && git config user.email "student@example.com"

echo "# Churn project" > README.md
git status                       # README.md is untracked
git add README.md
git status                       # now staged
git commit -m "Add README"

mkdir src data
echo 'print("training...")' > src/train.py
echo "data/" > .gitignore
echo "a,b" > data/raw.csv         # inside an ignored folder
git status --short               # data/raw.csv is not listed
git add .
git commit -m "Add training script and .gitignore"

echo 'print("evaluating...")' >> src/train.py
git diff                         # see the change before staging
git restore src/train.py         # throw the change away
git log --oneline

echo "oops" > bug.txt && git add bug.txt && git commit -m "Add bug file"
git revert --no-edit HEAD        # undo it with a new commit, history stays
git log --oneline
