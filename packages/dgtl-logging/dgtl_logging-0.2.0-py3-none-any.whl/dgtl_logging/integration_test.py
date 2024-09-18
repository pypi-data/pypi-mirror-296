from dgtl_logging.dgtl_logging import CustomObject, EventObject, UserObject
from dgtl_logging import integration_test_sub

def test_integration():
    event = EventObject(identificatortype='PID', indentificator='test_001', gebeurteniscode='R&R')
    
    integration_test_sub.sub_integration_add(event=event, sub_test_key='test_value')
    
    print(event.__dict__)
    
if __name__ == '__main__':
    test_integration()
    