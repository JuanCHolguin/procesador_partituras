from abc import ABC, abstractmethod
from partituras.modelo.errores import (
    ContieneNumero,
    ContieneCaracterInvalido,
    SinNotas,
    EspacioMultiple,
    EspacioBordes,
)
NOTAS_VALIDAS = ["do","re","mi","fa","sol","la","si"]
SIMBOLOS_VALIDOS = ["|","-"]

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
                if c.isdigit()
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
        errores = []
        partitura = partitura.lower()

        numeros = self.encontrar_numeros_partitura(partitura)
        ascii_invalidos = self.encontrar_caracteres_invalidos(partitura)

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
        self.partitura_valida(partitura)
        partitura = partitura.lower()

        tokens = partitura.split()

        resultado = []

        for t in tokens:
            if t in NOTAS_VALIDAS:
                resultado.append(
                    NOTAS_VALIDAS[(NOTAS_VALIDAS.index(t) + self.token) % len(NOTAS_VALIDAS)]
                )
            else:
                resultado.append(t)

        return " ".join(resultado)

    def revertir(self, partitura: str) -> str:
        self.partitura_valida(partitura)
        partitura = partitura.lower()

        tokens = partitura.split()

        resultado = []

        for t in tokens:
            if t in NOTAS_VALIDAS:
                resultado.append(
                    NOTAS_VALIDAS[(NOTAS_VALIDAS.index(t) - self.token) % len(NOTAS_VALIDAS)]
                )
            else:
                resultado.append(t)

        return " ".join(resultado)

class ReglaFrecuencia(ReglaTransformacion):

    def __init__ (self, token: int):
        super().__init__(token)

    def partitura_valida(self, partitura: str) -> bool:
        errores = []
        partitura = partitura.lower()

        numeros = self.encontrar_numeros_partitura(partitura)
        invalidos = self.encontrar_caracteres_invalidos(partitura)

        if numeros:
            mensaje = ",".join(
                f"la partitura contiene numeros en: {i}: {c}"
                for (i,c) in numeros
            )
            errores.append(
                ContieneNumero(mensaje)
            )
        if invalidos:
            mensaje = ",".join(
                f"existen caracteres inválidos en: {i}: {c}"
                for (i,c) in invalidos
            )
            errores.append(
                ContieneCaracterInvalido(mensaje)
            )

        tokens = partitura.split()
        invalidos = [
            (i,token)
            for (i,token) in enumerate(tokens)
            if token not in NOTAS_VALIDAS
        ]
        if invalidos:
            mensaje = ",".join(
                f"existen caracteres inválidos en: {i}: {token}"
                for (i, token) in invalidos
            )
            errores.append(
                ContieneCaracterInvalido(mensaje)
            )

        if partitura.startswith(" ") or partitura.endswith(" "):
            errores.append(EspacioBordes("Espacios al inicio o al final"))

        if "  " in partitura:
            errores.append(EspacioMultiple("Espacios múltiples"))

        if errores:
            raise ExceptionGroup(
                "Errores en la partitura", errores
            )
        return True

    def transformar(self, partitura: str) -> str:
        self.partitura_valida(partitura)
        return partitura

    def revertir(self, partitura: str) -> str:
        self.partitura_valida(partitura)
        return partitura



class Compositor:

    def __init__ (self, interprete: ReglaTransformacion ):
        self.interprete = interprete

    def transformar(self, partitura: str) -> str:
        return self.interprete.transformar(partitura)

    def revertir(self, partitura: str) -> str:
        return self.interprete.revertir(partitura)

    def compositor(self, interprete: ReglaTransformacion):
        self.partitura_valida(interprete)
        return interprete


class LectorPartituras:
    def __init__(self, ruta_archivo: str):
        self.ruta_archivo: str = ruta_archivo

    def cargar (self) -> list[str]:
        pass
    def procesar_con (self, compositor: Compositor) -> list[dict]:
        pass
