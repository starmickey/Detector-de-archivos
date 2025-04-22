import os
import re

class Directory:
    files = None  # Lista que almacenará los archivos encontrados en el directorio

    def __init__(self, path, omit_directories = []):
        """
        Constructor de la clase Directory.

        Parámetros:
        - path (str): Ruta del directorio donde se buscarán los archivos.
        """
        self.path = path
        self.omit_directories = omit_directories

    def _collect_files(self):
        """
        Método privado para recolectar todos los archivos en el directorio y subdirectorios.

        Este método recorre el directorio y sus subdirectorios usando os.walk() y almacena las rutas de los archivos
        en la lista 'files'.
        """
        self.files = []  # Inicializa la lista de archivos

        for root, dirs, files in os.walk(self.path):  # Recorre el directorio y subdirectorios
            # Filter directories to omit
            dirs[:] = [d for d in dirs if d not in self.omit_directories]

            for file in files:
                self.files.append(os.path.join(root, file))  # Añade la ruta completa del archivo a la lista

    def get_all_files(self):
        """
        Devuelve todos los archivos encontrados en el directorio y sus subdirectorios.

        Si la lista de archivos aún no ha sido recolectada, llama a _collect_files() para obtenerla.

        Retorna:
        - list: Lista de rutas completas de todos los archivos en el directorio.
        """
        if self.files is None:  # Si no se han recolectado los archivos, lo hacemos
            self._collect_files()

        return self.files
    
    def get_files_by_extensions(self, allowed_extensions):
        """
        Filtra los archivos por su extensión, devolviendo solo aquellos que coinciden con las extensiones permitidas.

        Parámetros:
        - allowed_extensions (list): Lista de extensiones permitidas (por ejemplo, ['.txt', '.pdf']).

        Retorna:
        - list: Lista de rutas completas de archivos que tienen una extensión permitida.
        """
        if self.files is None:  # Si no se han recolectado los archivos, lo hacemos
            self._collect_files()

        # Crea una expresión regular para las extensiones permitidas
        pattern = r'\.(' + '|'.join(map(re.escape, allowed_extensions)) + r')$'

        # Filtra los archivos que coinciden con el patrón de extensiones permitidas
        return [filename for filename in self.files if re.search(pattern, filename, re.IGNORECASE)]
