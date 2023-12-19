# Refactor foreach_inputs_sample_func._sample_rightmost_arg

Refactor the `_sample_rightmost_arg` method in the `foreach_inputs_sample_func` class to be a stand alone, top level function.
Name the new function `_sample_rightmost_arg`, exactly the same name as the existing method.
Update any existing `self._sample_rightmost_arg` calls to work with the new `_sample_rightmost_arg` function.
