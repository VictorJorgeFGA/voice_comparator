import librosa
import numpy

def rms_filter(data, samplerate=16000, segment_length=None, threshold=0.001135):
    segment_length = int(samplerate/100)
    
    filtered_data = numpy.array([])
    for index in range(0, len(data), segment_length):
        data_slice = data[index : index + segment_length]
        
        squared_data_slice = numpy.square(data_slice)
        mean = numpy.sqrt(numpy.mean(squared_data_slice))

        if mean > threshold:
            numpy.append(filtered_data, data_slice)

    return filtered_data

data, sr = librosa.load('ex.wav', 16000)

data = rms_filter(data)
librosa.output.write_wav('ex_filter.wav', data, sr)