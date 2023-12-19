# Refactor NetworkConfig.parse

Refactor the `parse` method in the `NetworkConfig` class to be a stand alone, top level function.
Name the new function `parse`, exactly the same name as the existing method.
Update any existing `self.parse` calls to work with the new `parse` function.
