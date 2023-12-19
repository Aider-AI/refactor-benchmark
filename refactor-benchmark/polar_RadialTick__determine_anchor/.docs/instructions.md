# Refactor RadialTick._determine_anchor

Refactor the `_determine_anchor` method in the `RadialTick` class to be a stand alone, top level function.
Name the new function `_determine_anchor`, exactly the same name as the existing method.
Update any existing `self._determine_anchor` calls to work with the new `_determine_anchor` function.
