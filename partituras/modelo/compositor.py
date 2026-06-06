from abc import ABC, abstractmethod
import json
from partituras.modelo.errores import (
    ContieneNumero,
    ContieneCaracterInvalido,
    SinNotas,
    EspacioMultiple,
    EspacioBordes,
    ArchivoNoEncontrado,
    ArchivoCorrupto,
)

NOTAS_VALIDAS = ["do", "re", "mi", "fa", "sol", "la", "si"]
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


# ================= TRANSPOSICION =================

class ReglaTransposicion(ReglaTransformacion):

    def partitura_valida(self, partitura: str) -> bool:
        errores = []
        partitura = partitura.lower()

        numeros = self.encontrar_numeros_partitura(partitura)
        ascii_invalidos = self.encontrar_caracteres_invalidos(partitura)

        if numeros:
            errores.append(ContieneNumero(str(numeros)))

        if ascii_invalidos:
            errores.append(ContieneCaracterInvalido(str(ascii_invalidos)))

        tokens = partitura.split()

        invalidos = [
            (i, token)
            for i, token in enumerate(tokens)
            if token not in NOTAS_VALIDAS and token not in SIMBOLOS_VALIDOS
        ]

        if invalidos:
            errores.append(ContieneCaracterInvalido(str(invalidos)))

        if not any(token in NOTAS_VALIDAS for token in tokens):
            errores.append(SinNotas("SinNotas"))

        if errores:
            raise ExceptionGroup(
                " ".join(type(e).__name__ for e in errores),
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
                pos = NOTAS_VALIDAS.index(t)
                # ✅ ajuste clave
                nueva_pos = (pos + self.token) % len(NOTAS_VALIDAS)
                resultado.append(NOTAS_VALIDAS[nueva_pos])
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
                pos = NOTAS_VALIDAS.index(t)
                # ✅ ajuste inverso
                nueva_pos = (pos - self.token) % len(NOTAS_VALIDAS)
                resultado.append(NOTAS_VALIDAS[nueva_pos])
            else:
                resultado.append(t)

        return " ".join(resultado)


# ================= FRECUENCIA =================

class ReglaFrecuencia(ReglaTransformacion):

    FRECUENCIAS = {
        "do": 261,
        "re": 293,
        "mi": 329,
        "fa": 349,
        "sol": 392,
        "la": 440,
        "si": 493,
    }

    def partitura_valida(self, partitura: str) -> bool:
        errores = []
        partitura = partitura.lower()

        if partitura.startswith(" ") or partitura.endswith(" "):
            errores.append(EspacioBordes("EspacioBordes"))

        if "  " in partitura:
            errores.append(EspacioMultiple("EspacioMultiple"))

        numeros = self.encontrar_numeros_partitura(partitura)
        invalidos = self.encontrar_caracteres_invalidos(partitura)

        if numeros:
            errores.append(ContieneNumero("ContieneNumero"))

        if invalidos:
            errores.append(ContieneCaracterInvalido("ContieneCaracterInvalido"))

        tokens = partitura.split()

        invalidos_tokens = [
            t
            for t in tokens
            if t not in NOTAS_VALIDAS
        ]

        if invalidos_tokens:
            errores.append(ContieneCaracterInvalido("ContieneCaracterInvalido"))

        if errores:
            raise ExceptionGroup(
                " ".join(type(e).__name__ for e in errores),
                errores
            )

        return True

    def transformar(self, partitura: str) -> str:
        self.partitura_valida(partitura)

        tokens = partitura.split()

        resultado = [
            str(self.FRECUENCIAS[t] * self.token)
            for t in tokens
        ]

        return " ".join(resultado)

    def revertir(self, partitura: str) -> str:
        tokens = partitura.split()
        resultado = []

        for v in tokens:
            base = int(v) // self.token
            for nota, freq in self.FRECUENCIAS.items():
                if freq == base:
                    resultado.append(nota)
                    break

        return " ".join(resultado)


# ================= COMPOSITOR =================

class Compositor:

    def __init__(self, interprete: ReglaTransformacion):
        self.interprete = interprete

    def transformar(self, partitura: str) -> str:
        return self.interprete.transformar(partitura)

    def revertir(self, partitura: str) -> str:
        return self.interprete.revertir(partitura)


# ================= LECTOR =================

class LectorPartituras:

    def __init__(self, ruta_archivo: str):
        self.ruta_archivo: str = ruta_archivo

    def cargar(self) -> list[str]:
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data["partituras"]


        except FileNotFoundError:

            raise ArchivoNoEncontrado()


        except json.JSONDecodeError:

            raise ArchivoCorrupto()

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
            errores = [type(e).__name__ for e in eg.exceptions]

        return {
            "original": partitura,
            "transformada": None,
            "revertida": None,
            "exito": False,
            "errores": errores
        }