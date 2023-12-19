# Refactor CountVectorizer._limit_features

Refactor the `_limit_features` method in the `CountVectorizer` class to be a stand alone, top level function.
Name the new function `_limit_features`, exactly the same name as the existing method.
Update any existing `self._limit_features` calls to work with the new `_limit_features` function.
