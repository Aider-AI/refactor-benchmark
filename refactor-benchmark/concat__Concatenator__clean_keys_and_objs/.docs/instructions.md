# Refactor _Concatenator._clean_keys_and_objs

Refactor the `_clean_keys_and_objs` method in the `_Concatenator` class to be a stand alone, top level function.
Name the new function `_clean_keys_and_objs`, exactly the same name as the existing method.
Update any existing `self._clean_keys_and_objs` calls to work with the new `_clean_keys_and_objs` function.
