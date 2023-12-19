# Refactor DocCLI.display_plugin_list

Refactor the `display_plugin_list` method in the `DocCLI` class to be a stand alone, top level function.
Name the new function `display_plugin_list`, exactly the same name as the existing method.
Update any existing `self.display_plugin_list` calls to work with the new `display_plugin_list` function.
