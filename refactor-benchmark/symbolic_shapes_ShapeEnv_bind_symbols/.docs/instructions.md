# Refactor ShapeEnv.bind_symbols

Refactor the `bind_symbols` method in the `ShapeEnv` class to be a stand alone, top level function.
Name the new function `bind_symbols`, exactly the same name as the existing method.
Update any existing `self.bind_symbols` calls to work with the new `bind_symbols` function.
