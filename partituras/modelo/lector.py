import json
from partituras.modelo.compositor import Compositor
from partituras.modelo.errores import (
    ArchivoNoEncontrado,
    ArchivoCorrupto,
    ErrorPartitura,
)

class LectorPartituras:

    def __init__(self, ruta_archivo: str):
        self.ruta_archivo = ruta_archivo

    def cargar(self) -> list[str]:
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data["partituras"]
        except FileNotFoundError as e:
            raise ArchivoNoEncontrado("Archivo no encontrado") from e
        except json.JSONDecodeError as e:
            raise ArchivoCorrupto("JSON corrupto") from e

    def procesar_con(self, compositor: Compositor) -> list[dict]:
        partituras = self.cargar()

        return [
            self._procesar_una(p, compositor)
            for p in partituras
        ]

    def _procesar_una(self, partitura, compositor):
        try:
            transformada = compositor.transformar(partitura)
            revertida = compositor.revertir(transformada)

            return {
                "original": partitura,
                "transformada": transformada,
                "revertida": revertida,
                "exito": True,
                "errores": []
            }

        except ExceptionGroup as eg:
            errores = [str(e) for e in eg.exceptions]

        except ErrorPartitura as e:
            errores = [str(e)]

        return {
            "original": partitura,
            "transformada": None,
            "revertida": None,
            "exito": False,
            "errores": errores
        }