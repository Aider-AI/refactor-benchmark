# Refactor _EagerSavedModelLoader._extract_signatures

Refactor the `_extract_signatures` method in the `_EagerSavedModelLoader` class to be a stand alone, top level function.
Name the new function `_extract_signatures`, exactly the same name as the existing method.
Update any existing `self._extract_signatures` calls to work with the new `_extract_signatures` function.
