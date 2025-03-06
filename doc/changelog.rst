Code Changelog
==============

This page contains the changelog for the `lisc` module.

This page primarily notes changes for major version updates, as well as any notes on updating between versions. For notes on the specific updates included within minor releases, see the
`release page <https://github.com/lisc-tools/lisc/releases>`_.

Note that between release versions, the general code API should stay consistent, so code from previous releases should generally be compatible with this release. However, internal objects and functions may change, such that saving / loading objects and processing already collected data may be slightly different. It is generally recommended that data be collected and processed within the same version of the module. If you need to load / process data from a different release version, you may need to check if the processing works, and update some things to make it work.

0.X.X Series
------------

The 0.X.X series, starting with 0.1.0 and currently ongoing is the initial major version and release series of the module.
