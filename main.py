from partituras.modelo.compositor import (
    ReglaTransposicion,
    ReglaFrecuencia,
    Compositor,
)
from partituras.modelo.lector import LectorPartituras
from partituras.modelo.errores import (
    ArchivoNoEncontrado,
    ArchivoCorrupto,
)

def main():
    lector = LectorPartituras("partituras_ejemplo.json")

    comp_trans = Compositor(ReglaTransposicion(2))
    comp_freq = Compositor(ReglaFrecuencia(2))

    try:
        print("=== TRANSPOSICIÓN ===")
        for r in lector.procesar_con(comp_trans):
            print(r)

        print("\n=== FRECUENCIA ===")
        for r in lector.procesar_con(comp_freq):
            print(r)

    except ArchivoNoEncontrado as e:
        print(f"Error: {e}")
    except ArchivoCorrupto as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()