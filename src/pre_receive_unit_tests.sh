#!/bin/sh

# Check if Python is installed
if ! command -v python &> /dev/null; then
  echo "Python is not installed, please install it"
  exit 1
fi

# Get the name of the branch being pushed
branch=$(git rev-parse --symbolic --abbrev-ref $1)

# Check only if the branch is master
if [ "$branch" != "master" ]; then
  exit 0
fi

# Run unit tests using unittest discover
python -m unittest discover -v

# Exit with an error if any tests fail
if [ $? -ne 0 ]; then
  echo "Unit tests failed, please fix the tests before pushing"
  exit 1
fi

# Continue with the push if everything is ok
exit 0
