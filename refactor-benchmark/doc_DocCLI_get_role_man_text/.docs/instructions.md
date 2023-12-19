# Refactor DocCLI.get_role_man_text

Refactor the `get_role_man_text` method in the `DocCLI` class to be a stand alone, top level function.
Name the new function `get_role_man_text`, exactly the same name as the existing method.
Update any existing `self.get_role_man_text` calls to work with the new `get_role_man_text` function.
