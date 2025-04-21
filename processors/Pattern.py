import re

class Pattern:
    @staticmethod
    def is_in_phrase(flag, text, ignorecase=re.IGNORECASE):
        """
        Verifica si una palabra clave (flag) aparece como palabra completa en el texto dado.

        Parámetros:
        - flag (str): La palabra que se busca en el texto.
        - text (str): El texto donde se buscará la palabra clave.
        - ignorecase (int, opcional): Modificador de la búsqueda (por defecto, se ignoran mayúsculas y minúsculas).

        Retorna:
        - bool: True si la palabra clave aparece como palabra completa en el texto, de lo contrario False.
        """
        # Crea una expresión regular para buscar la palabra clave como una palabra completa (usando delimitadores de palabra)
        flag_pattern = rf'(?<!\w){re.escape(flag)}(?!\w)'
        
        # Retorna True si la palabra clave se encuentra en el texto, de lo contrario False
        return bool(re.search(flag_pattern, text, ignorecase))

    @staticmethod
    def find_all(flag, text, ignorecase=re.IGNORECASE):
        """
        Encuentra todas las apariciones de una palabra clave (flag) en el texto dado.

        Parámetros:
        - flag (str): La palabra que se busca en el texto.
        - text (str): El texto donde se buscará la palabra clave.
        - ignorecase (int, opcional): Modificador de la búsqueda (por defecto, se ignoran mayúsculas y minúsculas).

        Retorna:
        - list: Lista de todas las coincidencias de la palabra clave en el texto.
        """
        # Compila la expresión regular con el patrón de búsqueda
        flag_pattern = re.compile(flag, ignorecase)
        
        # Devuelve todas las coincidencias de la palabra clave en el texto
        return flag_pattern.findall(text)
