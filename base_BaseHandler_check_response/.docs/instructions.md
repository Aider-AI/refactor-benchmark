# Refactor BaseHandler.check_response

Refactor the `check_response` method in the `BaseHandler` class to be a stand alone, top level function.
Name the new function `check_response`, exactly the same name as the existing method.
Update any existing `self.check_response` calls to work with the new `check_response` function.
