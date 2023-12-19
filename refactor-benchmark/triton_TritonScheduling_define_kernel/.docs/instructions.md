# Refactor TritonScheduling.define_kernel

Refactor the `define_kernel` method in the `TritonScheduling` class to be a stand alone, top level function.
Name the new function `define_kernel`, exactly the same name as the existing method.
Update any existing `self.define_kernel` calls to work with the new `define_kernel` function.
