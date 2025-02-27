# Detector de archivos

## Descripción

Provee diversas funcionalidades para localizar patrones de palabras en un directorio.

## Estructura del directorio

- `scripts` --> Funciones para que el usuario pueda encontrar distintos patrones de palabras
- `lib` --> Funciones que comparten los scripts

## Scripts

| Script                 | Descripción                                                                  |
| ---------------------- | ---------------------------------------------------------------------------- |
| find_components_pyN.py | Localiza las llamadas a componentes que se encuentren en un directorio determinado. Exceptúa aquellas indicadas dentro del mismo script. La N de pyN representa la versión de Python con la que es compatible. La de Python 3 exporta los resultados a Excel y la de Python 2 los exporta a un txt |
