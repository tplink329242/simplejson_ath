import sys
import atheris

import re
from typing import Union

with atheris.instrument_imports(key="simplejson"):
    import simplejson as json

def json_sanitize(value: Union[str, dict, list], is_value=True) -> Union[str, dict, list]:
    """
    Modified version of https://stackoverflow.com/a/45526935/2635443

    Recursive function that allows to remove any special characters from json, especially unknown control characters
    """
    if isinstance(value, dict):
        value = {json_sanitize(k, False):json_sanitize(v, True) for k, v in value.items()}
    elif isinstance(value, list):
        value = [json_sanitize(v, True) for v in value]
    elif isinstance(value, str):
        if not is_value:
            # Remove dots from value names
            value = re.sub(r"[.]", "", value)
        else:
            # Remove all control characters
            value = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', value)
    return value

@atheris.instrument_func    
def RunTest (InputData):

    try:
        decoder = json.JSONDecoder()
        encoder = json.JSONEncoderForHTML()


        InputData = json_sanitize(InputData)
        en = encoder.encode(InputData)
        decoder.decode(en)
        
    except Exception as e:
        return
        

if __name__ == '__main__':
    atheris.Setup(sys.argv, RunTest, enable_python_coverage=True)
    atheris.Fuzz()