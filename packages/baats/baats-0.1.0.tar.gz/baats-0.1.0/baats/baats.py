from typing import List, Optional, Union

class Tool:
    """
    Clase para manejar operaciones de lectura y escritura de archivos binarios.
    """
    def __init__(self, archivo: str) -> None:
        """
        Inicializa la instancia con la ruta del archivo.

        Args:
            archivo (str): Ruta del archivo a manejar.
        """
        self.objetivo = archivo

    def __leer(self) -> Optional[bytes]:
        """
        Lee el contenido del archivo binario.

        Returns:
            Optional[bytes]: Contenido del archivo en bytes, o None si ocurre un error.
        """
        try:
            with open(self.objetivo, 'rb') as archivo:
                return archivo.read()
        except IOError:
            return None

    def __guardar(self, datos: bytes) -> bool:
        """
        Guarda datos en el archivo binario.

        Args:
            datos (bytes): Datos a guardar en el archivo.

        Returns:
            bool: True si se guardó correctamente, False si ocurre un error.
        """
        try:
            with open(self.objetivo, 'wb') as archivo:
                archivo.write(datos)
            return True
        except IOError:
            return False

    def sacar_100_bytes(self) -> Union[List[int], bool]:
        """
        Extrae los últimos 100 bytes del archivo.

        Returns:
            List[int]: Lista de los últimos 100 bytes.
            bool: False si ocurre un error al leer el archivo.
        """
        datos = self.__leer()
        if datos is None:
            return False

        start_index = max(len(datos) - 100, 0)
        return [byte for byte in datos[start_index:]]

    def agregar_100_bytes(self, contenido: str) -> bool:
        """
        Agrega un bloque de 100 bytes al final del archivo.
        Si el contenido es menor de 100 bytes, lo rellena con ceros. Si es mayor, lo trunca.

        Args:
            contenido (str): Contenido a agregar al archivo.

        Returns:
            bool: True si se guardó correctamente, False si ocurre un error.
        """
        block_size = 100
        contenido_bytes = contenido.encode('utf-8')[:block_size]
        contenido_bytes = contenido_bytes.ljust(block_size, b'\x00')

        archivo_datos = self.__leer()
        if archivo_datos is None:
            return False

        nuevo_contenido = archivo_datos + contenido_bytes
        return self.__guardar(nuevo_contenido)

    def agregar_100_bytes_directo(self, datos: bytes) -> bool:
        """
        Agrega un bloque de 100 bytes al final del archivo.
        Si el bloque de datos es menor de 100 bytes, lo rellena con ceros. Si es mayor, lo trunca.

        Args:
            datos (bytes): Bloque de bytes a agregar al archivo.

        Returns:
            bool: True si se guardó correctamente, False si ocurre un error.
        """
        block_size = 100
        datos_truncados = datos[:block_size]
        datos_rellenos = datos_truncados.ljust(block_size, b'\x00')

        archivo_datos = self.__leer()
        if archivo_datos is None:
            return False

        nuevo_contenido = archivo_datos + datos_rellenos
        return self.__guardar(nuevo_contenido)

    def eliminar_100_bytes(self) -> bool:
        """
        Elimina los últimos 100 bytes del archivo.

        Returns:
            bool: True si se guardó correctamente después de eliminar, False si ocurre un error.
        """
        datos = self.__leer()
        if datos is None:
            return False

        nuevo_contenido = datos[:-100]  # Eliminar los últimos 100 bytes
        return self.__guardar(nuevo_contenido)

    def extractor(self) -> bool:
        """
        Lee el contenido del archivo, lo convierte en una representación de bytes, y guarda el resultado en "resulta.txt".

        Returns:
            bool: True si se guardó correctamente en resulta.txt, False si ocurre un error.
        """
        datos = self.__leer()
        if datos is None:
            return False

        try:
            with open("resulta.txt", 'w') as resultado:
                resultado.write(', '.join(f'{byte}' for byte in datos))
            return True
        except IOError:
            return False