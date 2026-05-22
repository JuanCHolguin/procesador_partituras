from partituras.modelo.errores import (
    ContieneNumero,
    ContieneCaracterInvalido,
    SinNotas,
    EspacioMultiple,
    EspacioBordes,
)
from abc import ABC, abstractmethod

class ReglaTransformacion(ABC):

    def __init__(self, token: int):
        self.token: int = token

    @abstractmethod
    def transformar(self, partitura: str) -> str:
        pass

    @abstractmethod
    def revertir(self, partitura: str) -> str:
        pass

    @abstractmethod
    def partitura_valida(self, partitura: str) -> bool:
        pass

    def encontrar_numeros_partitura(self, partitura: str) -> list:
        pass

    def encontrar_caracteres_invalidos(self, partitura: str) -> list:
        pass

class ReglaTransposicion(ReglaTransformacion):
    def __init__ (self, token: int):
        super().__init__(token)
    def transformar(self, partitura: str) -> str:
        pass

    def revertir(self, partitura: str) -> str:
        pass

    def partitura_valida(self, partitura: str) -> bool:
        pass

class ReglaFrecuencia(ReglaTransformacion):
    def __init__ (self, token: int):
        super().__init__(token)

    def transformar(self, partitura: str) -> str:
        pass

    def revertir(self, partitura: str) -> str:
        pass

    def partitura_valida(self, partitura: str) -> bool:
        pass


class Compositor(ReglaTransformacion):

    def __init__ (self, token: int):
        super().__init__(token)

    def transformar(self, partitura: str) -> str:
        pass

    def revertir(self, partitura: str) -> str:
        pass

    def partitura_valida(self, partitura: str) -> bool:
        pass