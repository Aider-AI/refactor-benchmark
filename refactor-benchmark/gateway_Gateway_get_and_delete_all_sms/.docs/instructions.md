# Refactor Gateway.get_and_delete_all_sms

Refactor the `get_and_delete_all_sms` method in the `Gateway` class to be a stand alone, top level function.
Name the new function `get_and_delete_all_sms`, exactly the same name as the existing method.
Update any existing `self.get_and_delete_all_sms` calls to work with the new `get_and_delete_all_sms` function.
