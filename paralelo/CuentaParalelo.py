import time
from multiprocessing import Process, cpu_count, Queue

def Contar(num,cola):
    cont=0
    while(cont<num):
        cont+=1
    cola.put(cont)

def Proceso()->Queue:
    inicio=time.perf_counter()

    cola=Queue()
    p1=Process(target=Contar, args=(250_000_000,cola ))
    p2=Process(target=Contar, args=(250_000_000,cola ))
    p3=Process(target=Contar, args=(250_000_000,cola ))
    p4=Process(target=Contar, args=(250_000_000,cola ))

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()

    final=time.perf_counter()
    print(f"Tiempo trasncurrido: {final-inicio:0.2f} segundos")

    return cola


if __name__ == '__main__':

    print("Tu PC tiene ",cpu_count()," núcleos")

    cola=Proceso()
    p=1
    while not cola.empty():
        elemento=cola.get()
        print(f"Proceso {p}: ", elemento)
        p+=1
