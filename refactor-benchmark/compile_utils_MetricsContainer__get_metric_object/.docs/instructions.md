# Refactor MetricsContainer._get_metric_object

Refactor the `_get_metric_object` method in the `MetricsContainer` class to be a stand alone, top level function.
Name the new function `_get_metric_object`, exactly the same name as the existing method.
Update any existing `self._get_metric_object` calls to work with the new `_get_metric_object` function.
