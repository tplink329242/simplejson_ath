import sys
import atheris
import json
import random

from ofunctions.json_sanitize import json_sanitize

with atheris.instrument_imports(key="simplejson"):
    import simplejson as json


@atheris.instrument_func    
def RunTest (InputData):

    try:
        decoder = json.JSONDecoder()
        encoder = json.JSONEncoderForHTML()

        fdp = atheris.FuzzedDataProvider(InputData)
        original = fdp.ConsumeString(sys.maxsize)

        original = json_sanitize(original)

        file_num = random.randint(1, 4)

        file_path = "tests/generated(" + str(file_num) + ").json"

        with open(file_path, 'r') as input_file:
            input_str = input_file.read()
            json_ogn = json.loads(input_str)
            json_ogn.append(original)
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