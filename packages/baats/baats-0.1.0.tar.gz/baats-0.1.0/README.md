# Tool

La clase `Tool` proporciona una interfaz para realizar operaciones básicas de lectura y escritura en archivos binarios.

## Instalación

No se requiere instalación adicional, solo asegúrate de tener Python instalado en tu sistema.

## Uso

#### Nota
`Se usaron imágenes como prueba, añadiendo 100 bytes con mensajes como: "Hola mundo", "Hola Pana", etc. La imagen sigue siendo visualizable aunque contenga los bytes extras.`

### Inicialización

```python
tool = Tool(archivo: str)
```

- **archivo** (str): Ruta del archivo binario que se va a manejar.

### Métodos

#### `sacar_100_bytes() -> Union[List[int], bool]`

Extrae los últimos 100 bytes del archivo.

- **Returns**: 
  - `List[int]`: Lista de los últimos 100 bytes si la operación es exitosa.
  - `bool`: `False` si ocurre un error al leer el archivo.

**Ejemplo:**

```python
ultimos_bytes = tool.sacar_100_bytes()
```

#### `agregar_100_bytes(contenido: str) -> bool`

Agrega un bloque de 100 bytes al final del archivo. Si el contenido es menor de 100 bytes, se rellena con ceros. Si es mayor, se trunca.

- **Args**:
  - **contenido** (str): Contenido a agregar al archivo.
- **Returns**:
  - `bool`: `True` si se guardó correctamente, `False` si ocurre un error.

**Ejemplo:**

```python
exito = tool.agregar_100_bytes("Texto de ejemplo")
```

#### `agregar_100_bytes_directo(datos: bytes) -> bool`

Agrega un bloque de 100 bytes al final del archivo. Si el bloque de bytes es menor de 100 bytes, se rellena con ceros. Si es mayor, se trunca.

- **Args**:
  - **datos** (bytes): Bloque de bytes a agregar al archivo.
- **Returns**:
  - `bool`: `True` si se guardó correctamente, `False` si ocurre un error.

**Ejemplo:**

```python
datos = b'\x01\x02\x03...'  # Datos en formato de bytes
exito = tool.agregar_100_bytes_directo(datos)
```

#### `eliminar_100_bytes() -> bool`

Elimina los últimos 100 bytes del archivo.

- **Returns**:
  - `bool`: `True` si se guardó correctamente después de eliminar, `False` si ocurre un error.

**Ejemplo:**

```python
exito = tool.eliminar_100_bytes()
```

#### `extractor() -> bool`

Lee el contenido del archivo, lo convierte en una representación de bytes, y guarda el resultado en un archivo llamado `resulta.txt`. La función opera de forma autónoma.

- **Returns**:
  - `bool`: `True` si se guardó correctamente en `resulta.txt`, `False` si ocurre un error.

**Ejemplo:**

```python
exito = tool.extractor()
```

## Ejemplo Completo

```python
# Crear una instancia de Tool con el archivo deseado
tool = Tool("ejemplo.bin")

# Agregar 100 bytes al final del archivo usando una cadena de texto
tool.agregar_100_bytes("Contenido de ejemplo")

# Agregar 100 bytes al final del archivo usando datos en bytes
datos = b'\x01\x02\x03...'  # Datos en formato de bytes
tool.agregar_100_bytes_directo(datos)

# Extraer los últimos 100 bytes del archivo
bytes_extraidos = tool.sacar_100_bytes()
print(bytes_extraidos)

# Eliminar los últimos 100 bytes del archivo
tool.eliminar_100_bytes()

# Guardar el contenido en resulta.txt
tool.extractor()
```