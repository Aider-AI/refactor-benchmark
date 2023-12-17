# Refactor MigrationGraph.iterative_dfs

Refactor the `iterative_dfs` method in the `MigrationGraph` class to be a stand alone, top level function.
Name the new function `iterative_dfs`, exactly the same name as the existing method.
Update any existing `self.iterative_dfs` calls to work with the new `iterative_dfs` function.
