import numpy as np
from multiprocessing import Process, Array
import time

def sumar_segmento(arreglo, inicio, fin, resultado, indice):
    """Suma una parte del arreglo y guarda el resultado."""
    suma = sum(arreglo[inicio:fin])
    print(f"Finaliza la suma del rango [{inicio} - {fin}]")
    resultado[indice] = suma


if __name__ == "__main__":
    # Número de elementos y procesos
    total_numeros = 100_000_000  # Usaremos 100 millones para pruebas
    num_procesos = 4

    # Generar arreglo de números aleatorios
    print("Generando números aleatorios...")
    numeros = np.random.randint(1, 100, size=total_numeros,dtype=np.int64)  # Enteros entre 1 y 100

    # Dividir el trabajo entre procesos
    tamaño_segmento = total_numeros // num_procesos
    resultados = Array('i', num_procesos)  # Arreglo compartido para guardar resultados
    procesos = []

    inicio_tiempo = time.time()

    # Crear procesos
    for i in range(num_procesos):
        print(f"Inicia el proceso {i+1}...")
        inicio = i * tamaño_segmento
        fin = inicio + tamaño_segmento if i < num_procesos - 1 else total_numeros
        p = Process(target=sumar_segmento, args=(numeros, inicio, fin, resultados, i))
        procesos.append(p)
        p.start()

    # Esperar a que todos los procesos terminen
    for p in procesos:
        p.join()

    # Calcular la suma total
    suma_total = sum(resultados)

    fin_tiempo = time.time()
    print(f"Suma total: {suma_total}")
    print(f"Tiempo total: {fin_tiempo - inicio_tiempo:.2f} segundos")