Logger
======
The _Logger_ block sends incoming signals to display in the service log file and System Designer's logger panel.

Properties
---
- **Log At**: The log level that determines the rank of log messages to display. Default is INFO.

Advanced Properties
---
- **Log As List**: Log incoming signals as lists. Default is `True` (checked) and signals are grouped inside their list. Setting this to `False` (unchecked) logs one signal at a time.
- **Log Hidden Attributes**: If `True` (checked) the log output will include hidden (private) attributes denoted by a leading underscore (e.g., `_signal_attribute`.)

Commands
---
- **log**: Force the logger block to log the configured phrase.
