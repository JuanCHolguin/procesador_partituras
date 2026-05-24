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
        errores = []
        partitura = partitura.lower()

        #validar caracteres:
        # for i, c in enumerate(partitura):
        #     if c.isdigit():
        #         raise ContieneNumero(
        #             f"La partitura contiene un número en la posición: {i}: {c}"
        #             )
        #     elif not c.isascii():
        #         raise ContieneCaracterInvalido(
        #             f"caracter inválido en la posición {i}: {c}"
        #            )
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
            mensaje = ",".join(
                f"La partitura contiene un número en la posición {i}: {c}"
                for (i, c) in numeros
            )

            errores.append(
                ContieneNumero(mensaje)
            )


        if ascii_invalidos:
            mensaje = ",".join(
                f"la partitura contiene un caracter inválido en la posición {i}: {c}"
                for (i, c) in ascii_invalidos
            )

            errores.append(
                ContieneCaracterInvalido(mensaje)
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
            mensaje = ",".join(
            f"posición {i}: {token}"
            for i, token in invalidos
            )

            errores.append(
                ContieneCaracterInvalido(mensaje)
            )

        if not any(token in NOTAS_VALIDAS for token in tokens):
            errores.append(
                SinNotas(
                f"No hay notas musicales en la partitura")
            )

        if errores:
            raise ExceptionGroup(
                "errores en la partitura",
                errores
            )

        return True

    def transformar(self, partitura: str) -> str:
        self.partitura_valida(partitura) #verifica que la partitura sea valida
        partitura = partitura.lower()

        partitura = partitura.strip()

        numeros = [
            (i, c)
            for (i, c) in enumerate(partitura)
            if c.isdigit()
        ]
        if numeros:
            mensaje = ",".join(
                f"la partitura contiene numeros en la posición {i}: {c}"
                for i, c in numeros
            )
            raise ContieneNumero(mensaje)










    def revertir(self, partitura: str) -> str:
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


class Compositor:

    def transformar(self, partitura: str) -> str:
        pass

    def revertir(self, partitura: str) -> str:
        pass

    def partitura_valida(self, partitura: str) -> bool:
        pass