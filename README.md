# Git-Hooks
A collection of useful git hooks. 

## What are hooks?

When you open any decent repository, you'll see a Hooks folder. Git iteslf contains a collection of hooks that can run scripts in a variety of scenarios. For example, before attempting to push your code to the repository, after pulling it from the remote, or before creating a new commit. 

## Pre-commit

When the <code>git commit</code> command is used, pre-commit scripts are run.

Pre-commit is frequently used to run tasks that check your code to ensure that it fits the code style used by the rest of programming team.
For Python projects, for example, there are programs like <code>black</code> and <code>flake8</code> that validate that code complies to established standards.

If it does not, they will block you from making a new commit and will change your code.

Then you can review your code to see that everything is still in order, and try to commit again, which should be successful this time.
 
You can also run tests, although this normally takes more than a few seconds. As a result, we discourage running tests on pre-commit. 

## How to use a custom hook?

You have to create a file named <code>pre-commit</code> in the <code>.git/hooks</code> directory. The name is crucial, you can't change it if you want git to recognize your script. Now edit the <code>pre-commit</code> file and put whatever commands you want git to execute whenever you will attempt to make a commit. For this repository we use the following script:

    #!/usr/bin/env bash
    hooks/_run_all.sh

## Available scripts

create a table with links to all available scripts in src. first column is the name of the script, second column is the description, third column is the link to python script, fourth column is the link to bash script.

| Script | Description | Python | Bash |
|:------:|:-----------:|:------:|:----:|
| remove diacritics | Removes diacritics from every file in a given directory. | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/remove_diacritics.py">remove_diacritics.py</a> | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/remove_diacritics.sh">remove_diacritics.sh</a> |
| remove carriage returns | Removes carriage returns from every file in a given directory. | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/remove_carriage_returns.py">remove_carriage_returns.py</a> | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/remove_carriage_returns.sh">remove_carriage_returns.sh</a> |
| last line empty | Ensures that every file a given directory ends with a newline. | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/last_line_empty.py">last_line_empty.py</a> | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/last_line_empty.sh">last_line_empty.sh</a> |
| no binaries | Checks if there are any binaries in the staging area. | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/no_binaries.py">no_binaries.py</a> | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/no_binaries.sh">no_binaries.sh</a> |
| correct file names | Ensures that no filename has spaces in it. | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/correct_file_names.py">correct_file_names.py</a> | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/correct_file_names.sh">correct_file_names.sh</a> |
## Bibliography

* https://www.git-scm.com/docs/githooks
* https://githooks.com/
