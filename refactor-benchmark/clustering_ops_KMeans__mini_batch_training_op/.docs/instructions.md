# Refactor KMeans._mini_batch_training_op

Refactor the `_mini_batch_training_op` method in the `KMeans` class to be a stand alone, top level function.
Name the new function `_mini_batch_training_op`, exactly the same name as the existing method.
Update any existing `self._mini_batch_training_op` calls to work with the new `_mini_batch_training_op` function.
