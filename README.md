# Git-Hooks
A collection of useful git hooks. 

## Set Up for Unix, MacOS

1. Download the code from the repository:
    
```Bash
git clone https://github.com/djeada/Git-Hooks.git
cd Git-Hooks
```

2. Install modules via VENV:

```Bash
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

3. Run any script from src directory:

```Bash
python src/example_script.py
```

## What are hooks?

When you open any decent repository, you'll see a <code>hooks</code> folder. Git iteslf contains a collection of hooks that can run scripts in a variety of scenarios. For example, before attempting to push your code to the repository, after pulling it from the remote, or before creating a new commit. 

## Pre-commit

When the <code>git commit</code> command is used, pre-commit scripts are run.

Pre-commit is frequently used to run tasks that check your code to ensure that it fits the code style used by the rest of programming team.
For Python projects, for example, there are tools like <code>black</code> and <code>flake8</code> that check code to ensure that it adheres to established standards. 

If it does not, they will block you from making a new commit and will change your code.

Then you can review your code to see that everything is still in order, and try to commit again, which should be successful this time.
 
You can also run tests, although this normally takes more than a few seconds. As a result, we discourage running tests on pre-commit. 

## How to use a custom hook?

You have to create a file named <code>pre-commit</code> in the <code>.git/hooks</code> directory. The name is crucial, you can't change it if you want git to recognize your script. Now edit the <code>pre-commit</code> file and put whatever commands you want git to execute whenever you will attempt to make a commit. For this repository we use the following script:

    #!/usr/bin/env bash
    hooks/_run_all.sh

Don't forget to add execution permissions to the <code>pre-commit</code> script!

## Available scripts

| Script | Description | Python | Bash |
|:------:|:-----------:|:------:|:----:|
| remove diacritics | Removes diacritics from every file in a given directory. | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/remove_diacritics.py">remove_diacritics.py</a> | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/remove_diacritics.sh">remove_diacritics.sh</a> |
| remove carriage return | Removes carriage returns from every file in a given directory. | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/remove_carriage_return.py">remove_carriage_returns.py</a> | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/remove_carriage_return.sh">remove_carriage_returns.sh</a> |
| remove trailing whitespace | Removes trailing whitespaces from every file in a given directory. | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/remove_trailing_whitespaces.py">remove_trailing_whitespaces.py</a> | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/remove_trailing_whitespaces.sh">remove_trailing_whitespaces.sh</a> |
| last line empty | Ensures that every file a given directory ends with a newline. | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/last_line_empty.py">last_line_empty.py</a> | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/last_line_empty.sh">last_line_empty.sh</a> |
| no binaries | Checks if there are any binaries in the staging area. | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/no_binaries.py">no_binaries.py</a> | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/no_binaries.sh">no_binaries.sh</a> |
| correct file names | Ensures that no filename has spaces in it. | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/correct_file_names.py">correct_file_names.py</a> | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/correct_file_names.sh">correct_file_names.sh</a> 
| correct docstrings | Unify formatting in Python docstrings. | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/correct_docstrings.py">correct_docstrings.py</a> | <a>correct_docstrings.sh</a> |
| python formatter | Beautify and format every python file found in the current repository. | <a>python_format.py</a> | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/python_format.sh">python_format.sh</a> |
| cpp formatter | Beautify and format every cpp file found in the current repository. | <a>cpp_format.py</a> | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/cpp_format.sh">cpp_format.sh</a> |
| shell formatter | Beautify and format every shell script found in the current repository. | <a>shell_format.py</a> | <a href="https://github.com/djeada/Git-Hooks/blob/main/src/shell_format.sh">shell_format.sh</a> |

## Refrences

* https://www.git-scm.com/docs/githooks
* https://githooks.com/
* https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
