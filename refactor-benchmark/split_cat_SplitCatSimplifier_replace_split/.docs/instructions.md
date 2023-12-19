# Refactor SplitCatSimplifier.replace_split

Refactor the `replace_split` method in the `SplitCatSimplifier` class to be a stand alone, top level function.
Name the new function `replace_split`, exactly the same name as the existing method.
Update any existing `self.replace_split` calls to work with the new `replace_split` function.
