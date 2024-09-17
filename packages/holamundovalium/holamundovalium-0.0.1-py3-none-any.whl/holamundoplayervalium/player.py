'''
Este es el módulo que incluye la clase de reproductor de música.
'''


class Player:
    '''
    Esta clase crea un reproductor de música.
    '''
    def play(self, song):
        '''
        Reproduce el audio que recibió como parámetro.
        
        Parameters:
        song (str): este es un string con el path del audio.
        
        Returns:
        int: devuelve 1 si reproduce con éxito en caso contrario devuelve 0.
        '''
        print('Reproduciendo audio.')
        
    def stop(self):
        '''
        Para el audio que está reproduciendo.
        '''
        print('Stopping')