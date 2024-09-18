from dgtl_logging.dgtl_logging import CustomObject, EventObject, UserObject, DGTLLogging
import logging 

def test_create_event_object_without_req_params():
    try:
        event = EventObject(test='test')
        event.validate()
        assert False
    except KeyError:
        assert True
    except Exception as e:
        raise(e)
        
def test_create_event_object_without_req_params_no_raise():
    try:
        event = EventObject(test='test')
        event.validate(raise_errors=False)
        assert True
    except Exception as e:
        logging.error(e)
        assert False

def test_create_event_object_valid():
    event = EventObject(
        gebeurteniscode='geb_test',
        actiecode='test',
        utcisodatetime='test',
        aard='test',
        identificatortype='PID',
        identificator='123')
    event.validate()
    assert event.gebeurteniscode == 'geb_test'

def test_event_object():
    # Check that the utcisodatetime is not overwritten during initiation

    event = EventObject(utcisodatetime='2023-10-10T00:00:00Z')
    event.update_parameters(gebeurteniscode='code1')
    event.update_parameters(actiecode='action1')
    event.update_parameters(identificatortype='type1', identificator='id1', aard='typeA')
    event.validate()
    
    assert event.utcisodatetime == '2023-10-10T00:00:00Z'
    
def test_user_object():
    user = UserObject(gebruikersnaam='user1')
    user.update_parameters(gebruikersrol='admin')
    user.update_parameters(autorisatieprotocol='protocol1', weergave_gebruikersnaam='User One')
    
    user.validate()

    assert user.autorisatieprotocol == 'protocol1'

def test_overwrite_entry():
    user = UserObject(gebruikersnaam='user1')
    user.update_parameters(gebruikersnaam='user2')

    assert user.gebruikersnaam == 'user2'
    
def test_add_log():
    class DummyConnector:
        def __init__(self) -> None:
            pass
    dummy = DummyConnector()
    
    dgtl_logging = DGTLLogging(log_ledger_table=dummy, env='test')
    user = UserObject(gebruikersnaam='user1', gebruikersrol='admin', autorisatieprotocol='protocol1', weergave_gebruikersnaam='User One')
    event = EventObject(gebeurteniscode='code1', actiecode='action1', identificatortype='type1', identificator='id1', aard='typeA')
    
    resp = dgtl_logging.add_log(event_object=event, user_object=user, dry_run=True)
    
    assert resp['gebruikersnaam'] == 'user1'
    assert 'utcisodatetime' in resp.keys()
    
if __name__ == '__main__':
    test_add_log()
