# Refactor ProfileAnalyzer._get_list_profile_lines

Refactor the `_get_list_profile_lines` method in the `ProfileAnalyzer` class to be a stand alone, top level function.
Name the new function `_get_list_profile_lines`, exactly the same name as the existing method.
Update any existing `self._get_list_profile_lines` calls to work with the new `_get_list_profile_lines` function.
