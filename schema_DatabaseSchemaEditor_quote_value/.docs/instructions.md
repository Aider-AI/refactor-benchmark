# Refactor DatabaseSchemaEditor.quote_value

Refactor the `quote_value` method in the `DatabaseSchemaEditor` class to be a stand alone, top level function.
Name the new function `quote_value`, exactly the same name as the existing method.
Update any existing `self.quote_value` calls to work with the new `quote_value` function.
