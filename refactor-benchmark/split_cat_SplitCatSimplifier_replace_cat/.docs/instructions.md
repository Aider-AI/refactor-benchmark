# Refactor SplitCatSimplifier.replace_cat

Refactor the `replace_cat` method in the `SplitCatSimplifier` class to be a stand alone, top level function.
Name the new function `replace_cat`, exactly the same name as the existing method.
Update any existing `self.replace_cat` calls to work with the new `replace_cat` function.
