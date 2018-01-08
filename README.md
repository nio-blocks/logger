Logger
======
The Logger blocks outputs incoming signals into the terminal and system designer's logger panel.

Properties
----------
- **log_as_list**: Hidden property defaulted to `False`. Whether to log incoming signals as lists. The default behavior is to log lists of incoming signals one at a time. Setting this to True allows one to see if the block received multiple signals at once or multiple signals sequentially.
- **log_at**: The log level that incoming signals show up as in the logs. Default is INFO.
- **log_hidden_attributes**: If `True` (checked) the log output will include hidden (private) attributes denoted by a leading underscore (eg: `_signal_attribute`.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
None

Commands
--------
- **log**: Force the logger block to log the configured phrase.

