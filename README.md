
## Aider's refactoring benchmark

This repository holds exercises for a coding benchmark used by the
[aider](https://github.com/paul-gauthier/aider) AI coding tool.  This
benchmark was designed to provoke "lazy coding" in the GPT-4 Turbo
models, which have this widely reported problem.

This benchmarked assisted in the design and evaluation of a solution
to the lazy coding problem.  [Asking GPT-4 Turbo to format code
changes as unified diffs](https://aider.chat/docs/unified-diffs.html)
reduced lazy coding by 3X.

## Benchmark details

Aider has long used a [benchmark suite based on 133 Exercism python
exercises]().  But these are mostly small coding problems, usually
requiring only a few dozen lines of code.  GPT-4 Turbo is typically
only lazy on 2-3 of these exercises: the ones with the most code and
which involve refactoring.

Based on this observation, I set out to build a benchmark based on
refactoring a non-trivial amount of code found in fairly large files.
To do this, I used python's `ast` module to analyze [9 popular open
source python
repositories](https://github.com/paul-gauthier/refactor-benchmark) to
identify challenging refactoring tasks.  The goal was to find:

- Source files that contain classes with non-trivial methods, having 100-250+ AST nodes in their implementation.
- Focus on methods that are part of a larger class, which has at least twice as much code as the method itself.
- Select methods that don't use their `self` parameter, so they can be trivially refactored out of the class.

We can then turn each of these source files into a task for the
benchmark, where we ask GPT to do something like:

> Refactor the `_set_csrf_cookie` method in the `CsrfViewMiddleware` class to be a stand alone, top level function.
> Name the new function `_set_csrf_cookie`, exactly the same name as the existing method.
> Update any existing `self._set_csrf_cookie` calls to work with the new `_set_csrf_cookie` function.

A [simple python AST scanning
script](https://github.com/paul-gauthier/aider/blob/main/benchmark/refactor_tools.py)
found 89 suitable files and packaged them up as benchmark tasks.  Each
task has a test that checks if the refactor was performed roughly
correctly:

- The updated source file must parse as valid python, to detect misapplied edits which produce invalid code.
- The target method must now exist as a top-level function in the file.
- This new top-level function must contain approximately the same number of AST nodes as the original class method. This ensures that GPT didn't elide code and replace it with comments.
- The original class must still be present in the file, and it must be smaller by about the number of AST nodes in the method which was removed. This helps confirm that the method was removed from the class, without other significant modifications.

To be clear, this is not a rigorous test that the refactor was
performed correctly.  But it does serve as a basic sanity check that
the refactor was essentially done as a cut & paste, without eliding
any code as comments.  And it correlates well with other laziness
metrics gathered during benchmarking like the introduction of new
comments that contain "...".

The result is a pragmatic
[benchmark suite that provokes, detects and quantifies GPT coding laziness](https://github.com/paul-gauthier/refactor-benchmark).


# Credits

The refactoring exercises are based on code from the following repositories:

- https://github.com/ansible/ansible
- https://github.com/django/django
- https://github.com/home-assistant/core
- https://github.com/matplotlib/matplotlib
- https://github.com/pandas-dev/pandas
- https://github.com/pytorch/pytorch
- https://github.com/scikit-learn/scikit-learn
- https://github.com/spyder-ide/spyder
- https://github.com/tensorflow/tensorflow

