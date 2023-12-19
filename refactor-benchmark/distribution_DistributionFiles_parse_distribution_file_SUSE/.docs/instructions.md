# Refactor DistributionFiles.parse_distribution_file_SUSE

Refactor the `parse_distribution_file_SUSE` method in the `DistributionFiles` class to be a stand alone, top level function.
Name the new function `parse_distribution_file_SUSE`, exactly the same name as the existing method.
Update any existing `self.parse_distribution_file_SUSE` calls to work with the new `parse_distribution_file_SUSE` function.
