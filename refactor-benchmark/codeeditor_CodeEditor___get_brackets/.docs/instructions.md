# Refactor CodeEditor.__get_brackets

Refactor the `__get_brackets` method in the `CodeEditor` class to be a stand alone, top level function.
Name the new function `__get_brackets`, exactly the same name as the existing method.
Update any existing `self.__get_brackets` calls to work with the new `__get_brackets` function.
