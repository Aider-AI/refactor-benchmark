# Refactor DataFrameView.next_index_name

Refactor the `next_index_name` method in the `DataFrameView` class to be a stand alone, top level function.
Name the new function `next_index_name`, exactly the same name as the existing method.
Update any existing `self.next_index_name` calls to work with the new `next_index_name` function.
