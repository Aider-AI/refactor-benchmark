# Refactor BaseConverter.convert

Refactor the `convert` method in the `BaseConverter` class to be a stand alone, top level function.
Name the new function `convert`, exactly the same name as the existing method.
Update any existing `self.convert` calls to work with the new `convert` function.
