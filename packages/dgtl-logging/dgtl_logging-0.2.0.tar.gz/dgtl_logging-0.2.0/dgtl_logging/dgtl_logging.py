import datetime
import logging
import uuid
from typing import Any, Dict, Optional


class DGTLLogging:
    def __init__(self, log_ledger_table, env, raise_errors=True) -> None:
        self.log_ledger_table = log_ledger_table
        self.env = env
    
    def add_log(self, event_object, user_object, dry_run=False):
        """
        :param gebeurteniscode: 7.2.1 Gebeurtenissoort - [R&R, Grading, Upload, etc.]
        :param actiecode: 7.2.2 Soort handeling op de gebeurtenis - [C, R, U, D, E]
        :param utcisodatetime: 7.2.3 utc datetime in isoformat string - iso8601-string
        :param aard: 7.2.4 logging-events v1 - [behandel, vrijgeven, versturen, etc.]
        :param weergave_gebruikersnaam: nvt - Firstname Lastname
        :param gebruikersnaam: 7.3.1 identificator - username_domain
        :param gebruikersrol: 7.3.4 gebruikersrol in Sinus - [admin, tech, customer, manager, supervisor, etc.]
        :param identificatortype: 7.4.1 Proces ID or in some cases nothing - [PID, None]
        :param identificator: 7.4.3 PID as string - ######
        :param autorisatieprotocol: 7.4.6 - [JWT]
        :param bron: 7.5.2 - [prod, acc, dev]
        :return:
        """
        event_object.validate()
        if(user_object is None):
            user_object = UserObject(gebruikersnaam='DGTL bot', gebruikersrol='bot')
        user_object.validate()

        month = "-".join(str(datetime.datetime.utcnow().isoformat()).split("T")[0].split("-")[:2])
        
        legacy_fields = {
            'id': str(uuid.uuid4()),
            'datum': event_object.utcisodatetime,
            'gebruiker': user_object.weergave_gebruikersnaam or "",
            'PID': str(event_object.identificator) or "",
            'bericht': str(event_object.aard),
            'maand': str(month)}
        
        data = user_object.__dict__ | event_object.__dict__ | {'bron': self.env} | legacy_fields
        logging.info(f'data: {data}')
        
        if not dry_run:
            self.log_ledger_table.add_entry(data=data)
            return True
        else:
            return data
    

class EventObject:
    """
    A class representing an event with required parameters and validation.

    Attributes
    ----------
    gebeurteniscode : Optional[str]
        Code representing the event.
    actiecode : Optional[str]
        Code representing the action.
    utcisodatetime : Optional[str]
        Timestamp in ISO format, defaults to current UTC time if not provided.
    identificatortype : Optional[str]
        Type of the identifier.
    identificator : Optional[str]
        The identifier itself.
    aard : Optional[str]
        Nature or type of the event.

    Methods
    -------
    update_parameters(**eventParameters)
        Update the attributes of the event with provided parameters.
    validate()
        Validate that all required parameters are set.
    """
    
    requiredParameters = ['gebeurteniscode', 'actiecode', 'utcisodatetime', 'identificatortype', 'identificator', 'aard']
    
    def __init__(self, **eventParameters: str) -> None:
        """
        Initialize an EventObject with optional parameters.

        Parameters
        ----------
        **eventParameters : dict
            An optional dictionary of event parameters.
            Can include 'gebeurteniscode', 'actiecode', 'utcisodatetime',
            'identificatortype', 'identificator', and 'aard'.
        """
        # Initialize with default empty values or with provided parameters
        for param in self.requiredParameters:
            setattr(self, param, eventParameters.get(param, None))
        
        if self.utcisodatetime is None:
            self.utcisodatetime = datetime.datetime.utcnow().isoformat()

    def update_parameters(self, **eventParameters: str) -> None:
        """
        Update existing event parameters.

        Parameters
        ----------
        **eventParameters : dict
            A dictionary of event parameters to update.
        """
        for param, value in eventParameters.items():
            setattr(self, param, value)

    def validate(self, raise_errors=True) -> None:
        """
        Validate that all required parameters are set.

        Raises
        ------
        KeyError
            If any required parameter is missing.
        """
        missing_params = []
        for param in self.requiredParameters:
            if getattr(self, param) is None:
                missing_params.append(param)
        if len(missing_params) > 0:
            if raise_errors:
                raise KeyError(f"Missing required parameters: {', '.join(missing_params)}")
            else:
                logging.error(f"Missing required parameters in validate function: {', '.join(missing_params)}")

class UserObject:
    """
    A class representing a user with required parameters and validation.

    Attributes
    ----------
    gebruikersnaam : Optional[str]
        Username of the user.
    gebruikersrol : Optional[str]
        Role of the user.
    weergave_gebruikersnaam : Optional[str]
        Display name of the user.

    Methods
    -------
    update_parameters(**userParameters)
        Update the attributes of the user with provided parameters.
    validate()
        Validate that all required parameters are set.
    """
    requiredParameters = ['gebruikersnaam', 'gebruikersrol', 'weergave_gebruikersnaam']
    
    def __init__(self, **userParameters: str) -> None:
        """
        Initialize a UserObject with optional parameters.

        Parameters
        ----------
        **userParameters : dict
            An optional dictionary of user parameters.
            Can include 'gebruikersnaam', 'gebruikersrol',
            and 'weergave_gebruikersnaam'.
        """
        # Initialize with default empty values or with provided parameters
        for param in self.requiredParameters:
            setattr(self, param, userParameters.get(param, None))

    def update_parameters(self, **userParameters: str) -> None:
        """
        Update existing user parameters.

        Parameters
        ----------
        **userParameters : dict
            A dictionary of user parameters to update.
        """
        for param, value in userParameters.items():
            setattr(self, param, value)

    def validate(self, raise_errors=True) -> None:
        """
        Validate that all required parameters are set.

        Raises
        ------
        KeyError
            If any required parameter is missing.
        """
        missing_params = []
        for param in self.requiredParameters:
            if getattr(self, param) is None:
                missing_params.append(param)
        if len(missing_params) > 0:
            if raise_errors:
                raise KeyError(f"Missing required parameters: {', '.join(missing_params)}")
            else:
                logging.error(f"Missing required parameters in validate function: {', '.join(missing_params)}")
        

class CustomObject:
    """
    A class for creating objects with custom parameters.

    Methods
    -------
    None
    """
    
    def __init__(self, **customParameters: Any) -> None:
        """
        Initialize a CustomObject with custom parameters.

        Parameters
        ----------
        **customParameters : dict
            A dictionary of custom parameters.
        """
        for param in customParameters:
            setattr(self, param, customParameters[param])

if __name__ == '__main__':
    event = EventObject()
    event.update_parameters(aard='test')
    event.update_parameters(identificatortype='test2')
    # event.validate()
    print(event.__dict__)
    pass