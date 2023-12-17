# Refactor DatabaseOperations.bulk_insert_sql

Refactor the `bulk_insert_sql` method in the `DatabaseOperations` class to be a stand alone, top level function.
Name the new function `bulk_insert_sql`, exactly the same name as the existing method.
Update any existing `self.bulk_insert_sql` calls to work with the new `bulk_insert_sql` function.
