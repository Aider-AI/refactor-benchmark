# Refactor RunSQL._run_sql

Refactor the `_run_sql` method in the `RunSQL` class to be a stand alone, top level function.
Name the new function `_run_sql`, exactly the same name as the existing method.
Update any existing `self._run_sql` calls to work with the new `_run_sql` function.
