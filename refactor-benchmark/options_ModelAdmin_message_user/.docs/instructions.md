# Refactor ModelAdmin.message_user

Refactor the `message_user` method in the `ModelAdmin` class to be a stand alone, top level function.
Name the new function `message_user`, exactly the same name as the existing method.
Update any existing `self.message_user` calls to work with the new `message_user` function.
