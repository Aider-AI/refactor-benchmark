# Refactor DebugAnalyzer._make_source_table

Refactor the `_make_source_table` method in the `DebugAnalyzer` class to be a stand alone, top level function.
Name the new function `_make_source_table`, exactly the same name as the existing method.
Update any existing `self._make_source_table` calls to work with the new `_make_source_table` function.
