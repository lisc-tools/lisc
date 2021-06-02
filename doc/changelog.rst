Code Changelog
==============

This page contains the changelog for the `lisc` module and any notes on updating between versions.

Notes on the specific updates related to each release are also available on the
`release page <https://github.com/lisc-tools/lisc/releases>`_.

Note that between release versions, the general code API should stay consistent, so code from previous releases should generally be compatible with this release. However, internal objects and functions may change, such that saving / loading objects and processing already collected data may be slightly different. It is generally recommended that data be collected and processed within the same version of the module. If you need to load / process data from a different release version, you may need to check if the processing works, and update some things to make it work.

0.2.X
-----

The 0.2.X series is the current release series of the module.

This series is a non-breaking update on the prior release.

The main updates in this update include:
- Internal updates to the LISC objects, and processing (including PRs #36, #39, #50, #60,  #67, #68)
- Internal updates to the collection procedures (PR #49, #53, #61)
- Updates to available plotting utilities and saving (#41, #54, #66)
- Extended Pubmed collection to use additional settings, including setting date ranges (PR #44)
- Add OpenCitations option to collect DOIs of citing papers (PR #27)
- Miscellaneous bug fixes (including PRs #62, #69)
- General documentation updates (including PRs #30, #31, #38, #43, #45, #46, #64)

0.1.X
-----

The 0.1.X series was the initial release series of the module.
