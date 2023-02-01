#!/bin/sh

# Check if black is installed
if ! command -v black &> /dev/null; then
  echo "black formatter is not installed, please install it"
  exit 1
fi

# Get the name of the branch being pushed
branch=$(git rev-parse --symbolic --abbrev-ref $1)

# Check only if the branch is master
if [ "$branch" != "master" ]; then
  exit 0
fi

# Check if the code is formatted correctly
black --check .

# Exit with an error if black returns any issues
if [ $? -ne 0 ]; then
  echo "The code is not formatted correctly, please run black on the code before pushing"
  exit 1
fi

# Continue with the push if everything is ok
exit 0
