# Refactor EventListenerBaseServicer._process_tensor_event_in_chunks

Refactor the `_process_tensor_event_in_chunks` method in the `EventListenerBaseServicer` class to be a stand alone, top level function.
Name the new function `_process_tensor_event_in_chunks`, exactly the same name as the existing method.
Update any existing `self._process_tensor_event_in_chunks` calls to work with the new `_process_tensor_event_in_chunks` function.
