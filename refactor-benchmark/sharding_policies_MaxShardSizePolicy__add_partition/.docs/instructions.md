# Refactor MaxShardSizePolicy._add_partition

Refactor the `_add_partition` method in the `MaxShardSizePolicy` class to be a stand alone, top level function.
Name the new function `_add_partition`, exactly the same name as the existing method.
Update any existing `self._add_partition` calls to work with the new `_add_partition` function.
