# Refactor CUDACPPScheduling._can_fuse_epilogue_impl

Refactor the `_can_fuse_epilogue_impl` method in the `CUDACPPScheduling` class to be a stand alone, top level function.
Name the new function `_can_fuse_epilogue_impl`, exactly the same name as the existing method.
Update any existing `self._can_fuse_epilogue_impl` calls to work with the new `_can_fuse_epilogue_impl` function.
