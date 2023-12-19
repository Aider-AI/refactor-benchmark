# Refactor GenOpTestCase.out_variant_op_test_case_generator

Refactor the `out_variant_op_test_case_generator` method in the `GenOpTestCase` class to be a stand alone, top level function.
Name the new function `out_variant_op_test_case_generator`, exactly the same name as the existing method.
Update any existing `self.out_variant_op_test_case_generator` calls to work with the new `out_variant_op_test_case_generator` function.
