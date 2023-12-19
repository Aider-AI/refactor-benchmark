# Refactor PylintWidget.parse_output

Refactor the `parse_output` method in the `PylintWidget` class to be a stand alone, top level function.
Name the new function `parse_output`, exactly the same name as the existing method.
Update any existing `self.parse_output` calls to work with the new `parse_output` function.
