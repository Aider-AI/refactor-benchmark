# Refactor Atom1Feed.add_item_elements

Refactor the `add_item_elements` method in the `Atom1Feed` class to be a stand alone, top level function.
Name the new function `add_item_elements`, exactly the same name as the existing method.
Update any existing `self.add_item_elements` calls to work with the new `add_item_elements` function.
