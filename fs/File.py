import os

class File:

    def __init__(self, path):
        """
        Constructor de la clase File.

        Parámetros:
        - path (str): Ruta del archivo que se va a leer.
        """
        self.path = path
        self._collect_lines()  # Llama al método para recolectar las líneas del archivo

    @staticmethod
    def get_last_subdirectory(path):
        """
        Obtiene el nombre del último subdirectorio en la ruta.

        Retorna:
        - str: Nombre del último subdirectorio.
        """
        return os.path.basename(os.path.dirname(path))
    
    @staticmethod
    def get_file_name(path):
        """
        Obtiene el nombre del archivo.

        Retorna:
        - str: Nombre del archivo.
        """
        return os.path.basename(path)

    def _collect_lines(self):
        """
        Método privado que lee todas las líneas del archivo y las guarda en la lista 'lines'.

        Este método abre el archivo en modo de lectura, usando la codificación UTF-8 y configurando el manejo de errores
        en caso de caracteres no válidos. Luego recorre el archivo línea por línea y agrega cada línea a la lista 'lines'.
        """
        self.lines = []  # Lista que almacenará las líneas del archivo

        with open(self.path, "r", encoding="utf-8", errors="ignore") as f:
            self.lines = f.readlines()  # Lee todas las líneas y las almacena en la lista 'lines'

    def get_lines(self):
        """
        Devuelve la lista de líneas del archivo.

        Retorna:
        - list: Lista de todas las líneas leídas del archivo.
        """
        return self.lines
