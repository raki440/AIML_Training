#!/usr/bin/env bash
# Day 2 demo: two branches change the same line, then we resolve the conflict.
set -e
rm -rf conflict-demo && mkdir conflict-demo && cd conflict-demo
git init -b main
git config user.name "Student" && git config user.email "student@example.com"

echo "model = LogisticRegression()" > train.py
git add train.py && git commit -m "Add baseline model"

git switch -c feature/random-forest
echo "model = RandomForestClassifier()" > train.py
git commit -am "Use random forest"

git switch main
git switch -c feature/boosting
echo "model = GradientBoostingClassifier()" > train.py
git commit -am "Use gradient boosting"

git switch main
git merge feature/random-forest            # fast-forward, no conflict
git merge feature/boosting || true         # conflict: both changed line 1
git status --short
cat train.py                               # look at the conflict markers

echo "model = GradientBoostingClassifier()" > train.py   # our decision: keep boosting
git add train.py
git commit -m "Merge feature/boosting, keep gradient boosting"
git log --oneline --graph --all
