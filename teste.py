import json
import numpy
from python_speech_features import mfcc

arr = [2*x for x in range(32000)]
arr = mfcc( numpy.array(arr), 16000 )
arr = json.dumps(arr.tolist())
print(arr)
