# Refactor GradScaler._unscale_grads_

Refactor the `_unscale_grads_` method in the `GradScaler` class to be a stand alone, top level function.
Name the new function `_unscale_grads_`, exactly the same name as the existing method.
Update any existing `self._unscale_grads_` calls to work with the new `_unscale_grads_` function.
