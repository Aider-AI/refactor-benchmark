# Refactor HERETransitDataUpdateCoordinator._parse_transit_response

Refactor the `_parse_transit_response` method in the `HERETransitDataUpdateCoordinator` class to be a stand alone, top level function.
Name the new function `_parse_transit_response`, exactly the same name as the existing method.
Update any existing `self._parse_transit_response` calls to work with the new `_parse_transit_response` function.
