# Refactor FigureBase.colorbar

Refactor the `colorbar` method in the `FigureBase` class to be a stand alone, top level function.
Name the new function `colorbar`, exactly the same name as the existing method.
Update any existing `self.colorbar` calls to work with the new `colorbar` function.
