# Refactor BuiltinVariable.call_setattr

Refactor the `call_setattr` method in the `BuiltinVariable` class to be a stand alone, top level function.
Name the new function `call_setattr`, exactly the same name as the existing method.
Update any existing `self.call_setattr` calls to work with the new `call_setattr` function.
