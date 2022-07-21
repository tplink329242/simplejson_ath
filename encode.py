import sys
import atheris
import json

from ofunctions.json_sanitize import json_sanitize

with atheris.instrument_imports(key="simplejson"):
    import simplejson as json


@atheris.instrument_func    
def RunTest (InputData):

    try:
        decoder = json.JSONDecoder()
        encoder = json.JSONEncoderForHTML()

        fdp = atheris.FuzzedDataProvider(InputData)
        original = fdp.ConsumeString(InputData)

        original = json_sanitize(original)

        with open("tests/generated.json", 'r') as input_file:
            input_str = input_file.read()
            json_ogn = json.loads(input_str)
            json_ogn['extra'] = original
            input_str = json.dumps(json_ogn)



        en = encoder.encode(input_str)
        decoder.decode(en)

        input_file.close()
        
    except Exception as e:
        print(e)
        return
        

if __name__ == '__main__':
    atheris.Setup(sys.argv, RunTest, enable_python_coverage=True)
    atheris.Fuzz()