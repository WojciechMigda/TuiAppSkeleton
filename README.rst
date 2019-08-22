TUI App Skeleton
================

Skeleton code for a TUI (Text User Interface) app in python.

It requires at least version 3.6 of python due to asyncio features being used.

You may first want to create boilerplate code with ``cookie-cutter`` and then copy
contents of this repository into provided source tree.

Design
******

There is one task being run in this basic setup and it is the TUI task.
The app should be extended by creating more tasks, which communicate through queues. 

Loggers can setup to send logs both to the log file in the ``.logs`` subfolder as well as to
the TUI where they end up shown in one of the scrollable windows.

There are three sources of configuration params:
 * command line parameters,
 * hardcoded INI-style params,
 * INI-style file.

Inspiration
***********

Asyncio usage and architectural setup was heavily inspired by ``cbconsumer`` repository on github.
