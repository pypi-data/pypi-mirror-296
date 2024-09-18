# dgtl-logging
NEN7513 compliant logging library according to the current scope of DGTL Health BV


## Updating
- update `setup.py` with new version number
- push or merge pull request to master branch and a github action will build and publish the package

## Installing
`pip install dgtl-logging`

## Usage

### EventObject, UserObject and CustomObject
Usage of the `EventObject` and `UserObject` are similar and have a validate() method built-in. The `CustomObject` does not have predefined parameters.

Use the `validate()` method just before passing the object to your logging function.

```
from dgtl_logging.dgtl_logging import CustomObject, EventObject, UserObject

event = EventObject()
event.update_parameters(gebeurteniscode='code1')
event.update_parameters(actiecode='action1', utcisodatetime='2023-10-10T00:00:00Z')
event.update_parameters(identificatortype='type1', identificator='id1', aard='typeA')
```

To validate if all required parameters are filled: `event.validate()`

### Writing to the logging ledger
DGTLLogging can be initiated as follows `dgtl_logging = DGTLLogging(log_ledger_table=log_ledger_table, env='test', raise_errors=True)`. Where `log_ledger_table` is the logging table in the chosen ledger. `env` is the environment (i.e. dev, acc, prod, etc.). `raise_errors` is useful for production workloads and uses `logging.error()` instead of raising an error and breaking any critical processes due to logging faults.

When all required parameters are added to the `EventObject` and `UserObject` you can pass them to `resp = dgtl_logging.add_log(event_object=event, user_object=user)`, which returns `True` when the insertion was succesful and raises an error otherwise.