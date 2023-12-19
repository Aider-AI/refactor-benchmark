# Refactor _Curve._get_arrow_wedge

Refactor the `_get_arrow_wedge` method in the `_Curve` class to be a stand alone, top level function.
Name the new function `_get_arrow_wedge`, exactly the same name as the existing method.
Update any existing `self._get_arrow_wedge` calls to work with the new `_get_arrow_wedge` function.
