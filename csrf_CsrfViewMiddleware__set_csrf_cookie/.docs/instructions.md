# Refactor CsrfViewMiddleware._set_csrf_cookie

Refactor the `_set_csrf_cookie` method in the `CsrfViewMiddleware` class to be a stand alone, top level function.
Name the new function `_set_csrf_cookie`, exactly the same name as the existing method.
Update any existing `self._set_csrf_cookie` calls to work with the new `_set_csrf_cookie` function.
