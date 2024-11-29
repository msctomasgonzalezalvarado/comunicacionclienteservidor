import socket
import time
import os
from tqdm import tqdm

class ClienteTransferencia:
    def __init__(self, ip, puerto, archivo):
        self.ip = ip
        self.puerto = puerto
        self.archivo = archivo
        self.tiempo_inicio = 0
        self.tiempo_fin = 0
        self.total_bytes = 0


    def enviar(self):
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)  # 64 KB para envío
        cliente.settimeout(15)
        cliente.connect((self.ip, self.puerto))
        print(f"Conectado al servidor en {self.ip}:{self.puerto}\n\n")
        self.tiempo_inicio = time.time()

        # Enviar nombre del archivo
        filename=self.archivo.encode()
        filename=os.path.basename(filename)

        cliente.sendall(filename)

        time.sleep(0.8)

        try:
            # Enviar contenido del archivo con el uso de with
            with open(self.archivo, 'rb') as f:
                tamano_archivo = f.seek(0, 2)  # Obtén el tamaño total del archivo
                f.seek(0)  # Regresa al inicio del archivo

                with tqdm(total=tamano_archivo, unit="B", unit_scale=True, ncols=120,ascii=True, desc="Enviando", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as barra:
                    while (datos := f.read(65536)):
                        cliente.sendall(datos)
                        time.sleep(0.8)
                        self.total_bytes += len(datos)
                        barra.update(len(datos))  # Actualiza la barra de progreso

                # Enviar contenido del archivo sin el iso de with
                # f = open(self.archivo, 'rb')
                # try:
                #     while (datos = f.read(1024)):
                #         if not datos:
                #             break
                #         cliente.sendall(datos)
                #         self.total_bytes += len(datos)
                # finally:
                #     f.close()

            self.tiempo_fin = time.time()
            print(f"Archivo {filename} enviado con éxito.")
            cliente.close()
        except Exception as e:
            print(f"Error: {e}")

    def total_megabytes(self):
        return self.total_bytes / 1024

    def tiempo_transcurrido(self):
        return self.tiempo_fin - self.tiempo_inicio


if __name__ == "__main__":
    cliente = ClienteTransferencia(ip='127.0.0.1', puerto=65432, archivo="C:\\Users\\Socrates\\Documents\\Intercambio\\AdeleCover.MP3")
    cliente.enviar()
    print(f"Total transferido: {cliente.total_megabytes():.2f} KB")
    print(f"Tiempo transcurrido: {cliente.tiempo_transcurrido():.2f} segundos")