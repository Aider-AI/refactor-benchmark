# Refactor Command.normalize_col_name

Refactor the `normalize_col_name` method in the `Command` class to be a stand alone, top level function.
Name the new function `normalize_col_name`, exactly the same name as the existing method.
Update any existing `self.normalize_col_name` calls to work with the new `normalize_col_name` function.
