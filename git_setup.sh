#!/bin/bash
# Initialize git repository
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit"

# Rename branch to main
git branch -M main

# Add remote origin
git remote add origin https://github.com/ali050786/agenticDS.git

# Push to origin
git push -u origin main
