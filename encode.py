import sys
import atheris

from ofunctions.json_sanitize import json_sanitize

with atheris.instrument_imports(key="simplejson"):
    import simplejson as json


@atheris.instrument_func    
def RunTest (InputData):

    try:
        decoder = json.JSONDecoder()
        encoder = json.JSONEncoderForHTML()

        InputData = json_sanitize(InputData)

        en = encoder.encode(InputData)
        decoder.decode(en)
        
    except Exception as e:
        print(e)
        return
        

if __name__ == '__main__':
    atheris.Setup(sys.argv, RunTest, enable_python_coverage=True)
    atheris.Fuzz()