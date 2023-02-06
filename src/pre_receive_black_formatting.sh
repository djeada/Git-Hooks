#!/bin/bash

# Check if black is installed
if ! command -v black &> /dev/null; then
  echo "black formatter is not installed, please install it"
  exit 1
fi

while read oldrev newrev refname; do

  # Get the name of the branch being pushed
  branch=$(git rev-parse --symbolic --abbrev-ref $refname)

  # Check only if the branch is master
  if [ "$branch" != "master" ]; then
   exit 0
  fi

  # Create an empty dir
  tmptree=$(mktemp -d)

  # Extract the content from the new revision
  git archive $newrev | tar x --warning=none -C ${tmptree}

  echo "$tmptree"

  # Navigate to the temporary directory
  cd $tmptree


  # Check if the code is formatted correctly
  black --check .

  # Exit with an error if black returns any issues
  if [ $? -ne 0 ]; then
    echo "The code is not formatted correctly, please run black on the code before pushing"
    exit 1
  fi
done
