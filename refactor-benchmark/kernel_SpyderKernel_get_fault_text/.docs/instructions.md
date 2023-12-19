# Refactor SpyderKernel.get_fault_text

Refactor the `get_fault_text` method in the `SpyderKernel` class to be a stand alone, top level function.
Name the new function `get_fault_text`, exactly the same name as the existing method.
Update any existing `self.get_fault_text` calls to work with the new `get_fault_text` function.
