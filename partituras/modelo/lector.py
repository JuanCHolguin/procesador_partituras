from partituras.modelo.compositor import Compositor
from partituras.modelo.errores import (
    ArchivoNoEncontrado,
    ArchivoCorrupto,
    ErrorPartitura,
)

class LectorPartituras:
    def __init__(self, ruta_archivo: str):
        self.ruta_archivo: str = ruta_archivo

    def cargar(self) -> list[str]:
        ...


