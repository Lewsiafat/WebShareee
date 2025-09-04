#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# The script should be run from the project root (web-hosting-service).
# cd to the script's directory to ensure paths are correct
cd "$(dirname "$0")/.."

# Check if a version type is provided (patch, minor, major)
if [ -z "$1" ]; then
  echo "Error: Version type not specified."
  echo "Usage: $0 <patch|minor|major>"
  exit 1
fi

VERSION_TYPE=$1

# Validate version type
if [ "$VERSION_TYPE" != "patch" ] && [ "$VERSION_TYPE" != "minor" ] && [ "$VERSION_TYPE" != "major" ]; then
  echo "Error: Invalid version type '$VERSION_TYPE'."
  echo "Please use one of: patch, minor, major"
  exit 1
fi

echo "Bumping version type: $VERSION_TYPE"

# Ensure we are on the master branch and the working directory is clean
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" != "master" ]; then
  echo "Error: You must be on the 'master' branch to bump the version."
  exit 1
fi

if ! git diff-index --quiet HEAD --; then
    echo "Error: Working directory is not clean. Please commit or stash your changes."
    exit 1
fi

echo "Pulling latest changes from master..."
git pull origin master

# Use npm version to update package.json, create a commit, and tag it.
# The -m flag provides a custom commit message.
npm version "$VERSION_TYPE" -m "chore(release): Bump version to %s"

# Push the commit and the new tag to the remote repository
echo "Pushing new version commit and tag to origin..."
git push origin master
git push --tags

echo "Version bump complete."
NEW_VERSION=$(node -p "require('./package.json').version")
echo "New version: $NEW_VERSION"
