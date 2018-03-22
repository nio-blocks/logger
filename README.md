Logger
======
The _Logger_ block sends incoming signals to display in the terminal and System Designer's logger panel.

Properties
----------
- **log_as_list**: Whether to log incoming signals as lists. Default is `False` and each incoming signal list is logged one signal at a time. Setting this to `True` logs signals grouped inside their list.
- **log_at**: The log level that determines the rank of log messages to display. Default is INFO.
- **log_hidden_attributes**: If `True` (checked) the log output will include hidden (private) attributes denoted by a leading underscore (e.g., `_signal_attribute`.)

Inputs
------
- **default**: Any list of signals.

Outputs
-------
None

Commands
--------
- **log**: Force the logger block to log the configured phrase.

