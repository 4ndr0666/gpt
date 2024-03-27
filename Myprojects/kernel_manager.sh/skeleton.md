Expanded and Detailed API List for Version 1.1:

1. list_installed_kernels(): Uses `pacman` directly to list installed kernels.
2. list_available_kernels(): Queries repository data to list available kernels.
3. identify_running_kernel(): Utilizes `uname` to identify the currently running kernel.
4. install_kernel(kernel_name): Simplifies the process of installing a specified kernel.
5. remove_kernel(kernel_name): Simplifies the process of removing a specified kernel.
6. upgrade_kernel(kernel_name): (Optional) Handles upgrading a specified kernel to its latest version.
7. FormatVersion: Formats kernel versions for display.
8. FormatName: Formats kernel names for display.
9. Header: Generates headers for different sections of the utility output.
10. LocalVersion: Retrieves the local version of a specified kernel.
11. Exist: Checks if a specified kernel exists.
12. Choose: Handles user selection for kernel installation/removal.
13. PkgName: Displays the package name of kernels.
14. Installed: Lists installed kernels with details.
15. StableVersion: Fetches the stable version of kernels from the repositories.
16. Stable: Lists stable kernels available for installation.
17. TestingVersion: Fetches the testing version of kernels if available.
18. Testing: Lists testing kernels available for installation.
19. KernelOrgVersion: Retrieves kernel versions available at kernel.org.
20. KernelOrg: Lists kernel categories and versions as per kernel.org.
21. KOVersion: Displays the latest kernel version announced at kernel.org.
22. IsLatestKO: Checks if an installed kernel is the latest as per kernel.org.
23. DIE: Handles error messages and exits the utility.
24. UniqueArr: Removes duplicates from a list.
25. Options: Processes command-line options for the utility.
26. AvailableKernelsAndHeaders: Identifies available kernels and their headers.
27. Error Handling: Integral to all functions for robustness.
28. User Interaction: CLI-based choices for interacting with the utility.
