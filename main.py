from fastdtw import fastdtw
import timeit
import sounddevice
import soundfile
import time

SAMPLE_RATE = 4000
CHANNELS = 1
DURATION = 2

sounddevice.default.samplerate = SAMPLE_RATE
sounddevice.default.channels = CHANNELS

people_set = list()

class PersonVoiceData():
    def __init__( self, name = "unknow", voice_data_samples = list() ):
        self.name = name
        self._samples = voice_data_samples

    def distance_from_this_sample( self , voice_data_sample ):
        lowest_distance = 10**9
        print('\t\tComparando com', self.name)
        
        for current_voice_data in self._samples:
            distance, _ignore = fastdtw( current_voice_data , voice_data_sample )

            if lowest_distance > distance:
                lowest_distance = distance

        print('\t\tMenor distancia = ', lowest_distance)
        return lowest_distance

def nearest_person_voice( voice_data_sample ):
    lowest_distance = 10**9
    person = 0

    for current_person in people_set:
        distance = current_person.distance_from_this_sample( voice_data_sample )

        if lowest_distance > distance:
            lowest_distance = distance
            person = current_person

    return person

def record_voice_sample():
    record = 0
    print('\tQuando eu disser "Gravando" diga em tom alto e sem pausas a frase "ABC"')
    while True:
        time.sleep(2)
        record = sounddevice.rec( int( DURATION * SAMPLE_RATE ) )
        print('\tGravando ...')
        sounddevice.wait()

        print('\tEstou reproduzindo o que foi gravado. Tenha certeza que o audio nao foi cortado ou teve trechos com pausa.')
        print('\tCaso o audio nao tenha ficado bom, REGRAVE!.')
        sounddevice.play( record )
        sounddevice.wait()

        print('\tDeseja regravar a amostra? (Y / n)' , end= ' ')
        if input().lower() == 'y':
            continue
        break
    return record

def register_person():
    print("\tVamos iniciar um novo registro.\n")
    print("\tForneça um nome:" , end = ' ' )
    person_name = input()
    print('\tVamos registrar um exemplos de sua voz.')

    voice_sample1 = record_voice_sample()
    time.sleep(2)
    # print('Ok, vamos para a proxima amostra.')
    # voice_sample2 = VoiceData( record_voice_sample() )

    new_person = PersonVoiceData( person_name , [voice_sample1] )
    people_set.append( new_person )

    print( '\t' + person_name , 'registrado com sucesso!\n' )

def single_test():
    print('Vamos iniciar o teste')
    voice_sample = record_voice_sample()

    print('\tFazendo comparacoes...')

    start_time = timeit.default_timer()
    print('\tEssa voz se parece mais com a do(a)', nearest_person_voice( voice_sample ).name )
    end_time = timeit.default_timer()
    print('\tEsse teste levou', end_time - start_time , 'segundos para ser computado\n')

if __name__ == '__main__':
    
    print("Nao ha pessoas registradas!")
    register_person()

    print("E necessario que mais uma pessoa se registre.")
    register_person()

    while True:
        time.sleep(2)
        print("Digite 1 para registrar uma nova pessoa.\n2 para fazer um teste.\n3 para sair.")

        command = int(input())
        if command == 1:
            register_person()
        elif command == 2:
            single_test()
        else:
            break

    print('Fim da execucao')

    

    
