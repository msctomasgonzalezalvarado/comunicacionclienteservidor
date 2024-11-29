import socket
import time

class ServidorTransferencia:
    def __init__(self, ip='0.0.0.0', puerto=65432):
        self.ip = ip
        self.puerto = puerto
        self.tiempo_inicio = 0
        self.tiempo_fin = 0
        self.total_bytes = 0

    def iniciar(self):
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)  # 64 KB para recepción

        servidor.bind((self.ip, self.puerto))
        servidor.listen(1)
        print(f"Servidor escuchando en {self.ip}:{self.puerto}")

        conn, addr = servidor.accept()
        print(f"Conexión establecida con {addr}")
        self.tiempo_inicio = time.time()

        # Recibir nombre del archivo
        filename = conn.recv(1024).decode()
        #print(f"Recibiendo archivo: {filename}")

        # Recibir contenido del archivo con eluso de with
        with open("/home/pocoyo/intercambio/adelecover.mp3", 'wb') as f:
            while True:
                datos = conn.recv(65536)
                if not datos:
                    break
                f.write(datos)
                self.total_bytes += len(datos)
                print(self.total_bytes)

        #Recibir contenido del archivo sin el uso de with
        # f = open(filename, 'wb')
        # try:
        #     while True:
        #         datos = conn.recv(1024)
        #         if not datos:
        #             break
        #         f.write(datos)
        #         self.total_bytes += len(datos)
        # finally:
        #     f.close()

        self.tiempo_fin = time.time()
        print(f"Archivo recibido con éxito.")
        servidor.close()

    def total_megabytes(self):
        return self.total_bytes / 1024

    def tiempo_transcurrido(self):
        return self.tiempo_fin - self.tiempo_inicio


if __name__ == "__main__":
    servidor = ServidorTransferencia()
    servidor.iniciar()
    print(f"Total transferido: {servidor.total_megabytes():.2f} KB")
    print(f"Tiempo transcurrido: {servidor.tiempo_transcurrido():.2f} segundos")