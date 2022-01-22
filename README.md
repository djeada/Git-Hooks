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

## Bibliography

* https://githooks.com/
