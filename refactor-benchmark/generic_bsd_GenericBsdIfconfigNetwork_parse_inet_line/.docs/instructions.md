# Refactor GenericBsdIfconfigNetwork.parse_inet_line

Refactor the `parse_inet_line` method in the `GenericBsdIfconfigNetwork` class to be a stand alone, top level function.
Name the new function `parse_inet_line`, exactly the same name as the existing method.
Update any existing `self.parse_inet_line` calls to work with the new `parse_inet_line` function.
