import sounddevice as sd
import numpy

'''
Este filtro remove partes silenciosas do sinal de fala, inclusive pausas.
Este filtro não se aplica a audio com ruidos de fundo
É necessário tratar o ruido do audio antes de utilizar este filtro
'''

#threshold=0.001135
def rms_filter(data, samplerate=16000, segment_length=None, threshold=0.001135):
    segment_length = int(samplerate/100)
    
    filtered_data = numpy.array([])
    for index in range(0, len(data), segment_length):
        data_slice = data[index : index + segment_length]
        
        squared_data_slice = numpy.square(data_slice)
        mean = numpy.sqrt(numpy.mean(squared_data_slice))

        if mean > threshold:
            filtered_data = numpy.append(filtered_data, data_slice)

    return filtered_data

sd.default.channels = 1
sd.default.samplerate = 16000

print('Rodando demonstração.')

while True:
    audio = sd.rec(int(10 * 16000))
    print('Gravando por 10s.')
    sd.wait()

    sd.play(audio)
    print('Reproduzindo audio gravado.')
    sd.wait()

    if input('Deseja regravar? y/n').lower() == 'y':
        continue

    audio = rms_filter(audio)
    sd.play(audio)
    print('Reproduzindo audio filtrado.')
    sd.wait()

    if input('Novo teste? y/n').lower() == 'y':
        continue
    break