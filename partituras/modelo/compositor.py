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
             return [
                (i, c)
                for i, c in enumerate(partitura)
                if not c.isdigit()
            ]

    def encontrar_caracteres_invalidos(self, partitura: str) -> list:
        return [
            (i, c)
            for i, c in enumerate(partitura)
            if not c.isascii()
        ]

class ReglaTransposicion(ReglaTransformacion):
    def __init__ (self, token: int):
        super().__init__(token)

    def partitura_valida(self, partitura: str) -> bool:
        NOTAS_VALIDAS = ["do", "re", "mi", "fa", "sol", "la", "si"]
        SIMBOLOS_VALIDOS = ["|", "-"]
        partitura = partitura.lower()

        #validar caracteres:
        # for i, c in enumerate(partitura):
        #     if c.isdigit():
        #         raise ContieneNumero(
        #             f"La partitura contiene un número en la posición: {i}: {c}")
        #     elif not c.isascii():
        #         raise ContieneCaracterInvalido(
        #             f"caracter inválido en la posición {i}: {c}")
        numeros = [
            (i, c)
            for (i, c) in enumerate(partitura)
            if c.isdigit()
            ]
        ascii_invalidos = [
            (i, c)
            for (i, c) in enumerate(partitura)
            if not c.isascii()
            ]
        if numeros:
            raise ContieneNumero(
                f"La partitura contiene un número en la posición {numeros}"
            )
        if ascii_invalidos:
            raise ContieneCaracterInvalido(
                f"la partitura contiene un caracter inválido en la posición {ascii_invalidos}"
            )

        #validar token
        tokens = partitura.split()

        invalidos = [
            (i, token)
            for i, token in enumerate(tokens)
            if token not in NOTAS_VALIDAS
               and token not in SIMBOLOS_VALIDOS
        ]

        if invalidos:
            raise ContieneCaracterInvalido(
                f"La partitura contiene caracteres inválidos: {invalidos}"
            )

        if not any( token in NOTAS_VALIDAS for token in tokens):
            raise SinNotas(
                f"No hay notas musicales en la partitura"
            )

        return True

class ReglaFrecuencia(ReglaTransformacion):
    def __init__ (self, token: int):
        super().__init__(token)

    def transformar(self, partitura: str) -> str:
        pass

    def revertir(self, partitura: str) -> str:
        pass

    def partitura_valida(self, partitura: str) -> bool:
        pass


class Compositor:

    def __init__ (self, token: int):
        super().__init__(token)

    def transformar(self, partitura: str) -> str:
        pass

    def revertir(self, partitura: str) -> str:
        pass

    def partitura_valida(self, partitura: str) -> bool:
        pass