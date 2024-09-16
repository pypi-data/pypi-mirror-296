'''
Este módulo nos permite ...\n
y también nos permite ...
'''
class Player:
    '''
    Esta clase cre un reproductor de música.
    '''
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return f'Reproductor de música {123}'
    
    def play(self, song):
        '''
        Reproduce la canción recibida como argumento.

        Parameters:
            son (str): Ruta del fichero que contiene la canción.
        Returns:
            int: Devuelve 1 si la reproducción fue exitosa, 0 en otro caso.
        '''
        print(f'Reproduciendo {song}')
    
    def stop(self):
        '''Detiene el reproductor de música'''
        print(f'Reproductor de música detenido')