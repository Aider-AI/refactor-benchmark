# Refactor BaseHandler.adapt_method_mode

Refactor the `adapt_method_mode` method in the `BaseHandler` class to be a stand alone, top level function.
Name the new function `adapt_method_mode`, exactly the same name as the existing method.
Update any existing `self.adapt_method_mode` calls to work with the new `adapt_method_mode` function.
