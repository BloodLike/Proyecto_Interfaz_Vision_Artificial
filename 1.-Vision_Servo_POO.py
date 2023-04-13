import cv2  #LIBRERIA OPENCV PARA VISION ARTIFICIAL
import numpy as np  #MANEJO DE MATRICES
import serial   #ENVIO DE DATOS POR MEDIO DEL MONITOR SERIAL
import time

class BlueTracker:      #SE CREA UNA CLASE LLAMADA "BlueTracker"
    def __init__(self, com, baud):  #CONSTRUCTOR QUE INICIALIZA ATRIBUTOS Y CARACTERISTICAS
        self.ser = serial.Serial(com, baud) #SE INICIALIZA UN OBJETO DE TIPO PYSERIAL
        self.cap = cv2.VideoCapture(0)  #SE INICIALIZA UN OBJETO DE TIPO CV
        self.azulBajo = np.array([100, 100, 20], np.uint8)  #RANGO DE COLORES DE AZUL BAJO
        self.azulAlto = np.array([120, 255, 255], np.uint8) #RANGO DE COLORES DE AZUL ALTO

    def track(self):
        while True:     #BUCLE INFINITO

            ret, frame = self.cap.read()    #SE LEE DE EL VIDEO CAPTURADO
            if ret:     #COMPROBAR SI SE INICIALIZO EL VIDEO
                frame = cv2.flip(frame, 1)  #TRANSFORMACION ESPEJO EN EL EJE HORIZONTAL
                frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)   #SE CONVIERTE LA IMAGEN A HSV
                mascara = cv2.inRange(frameHSV, self.azulBajo, self.azulAlto) #SE CREA UNA MASCARA DE PIXELES
                contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                #SE BUSCAN LOS CONTORNOS DENTRO DE LA IMAGEN
                cv2.drawContours(frame, contornos, -1, (255, 0, 0), 4)
                #SE DIBUJAN LOS CONTORNOS DIBUJADOS

                for c in contornos:
                    #SE ITERA SOBRE CADA CONTORNO ENCONTRADO
                    area = cv2.contourArea(c)
                    #SE CALCULA EL AREA DEL CONTORNO
                    if area > 6000:
                        #SI EL AREA ES MAYOR A 6000 (UMBRAL)
                        M = cv2.moments(c)
                        #SE CALCULA EL CENTROIDE DE LA IMAGEN
                        if M["m00"] == 0:
                            M["m00"] = 1
                        x = int(M["m10"] / M["m00"]) #SE CALCULA EL EJE X
                        y = int(M['m01'] / M['m00']) #SE CALCULA EL EJE Y
                        cv2.circle(frame, (x, y), 7, (0, 0, 255), -1) #SE DIBUJA UN CIRCULO EN EL CENTRO DE LA IMAGEN
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        #SE ESCOGE UNA FUENTE PARA TEXTO
                        cv2.putText(frame, '{},{}'.format(x, y), (x + 10, y), font, 1.2, (0, 0, 255), 2, cv2.LINE_AA)
                        #SE PONE LA POSICION DE LOS EJE X,Y
                        nuevoContorno = cv2.convexHull(c)
                        #SE OBTIENE EL CONTORNO CONVEXO DEL OBJETO
                        cv2.drawContours(frame, [nuevoContorno], 0, (255, 0, 0), 3)
                        #SE DIBUJA EN LA IMAGEN

                        self.move_robot(x) #SE INVOCA AL METODO "move_robot" PARA CONTROL DEL ACTUADOR

                cv2.imshow('Blue Tracker', frame)  #DESPLIEGA UNA VENTANA CON NOMBRE "Blue Tracker"
                if cv2.waitKey(1) & 0xFF == ord('s'):   #SI SE PRESIONA "s"
                    self.ser.close()    #SE CIERRA LA COMUNICACION SERIAL
                    break   #SE ROMPE EL CICLO INFINITO
        self.cap.release()
        cv2.destroyAllWindows()

    def move_robot(self, x):    #METODO "move_robot" QUE RECIBE COMO PARAMETRO EL EJE X DEL CENTROIDE
        dato_r = 0
        if 82 >= x >= 20:             #SI EL CENTROIDE SE ENCUENTRA EN LA POSICION 200
            print("Mover a la izquierda 100%")
            time.sleep(0.1)
            self.ser.write(b"izq1\n")          #ENVIO DE DATOS A ARDUINO
            dato_r = self.ser.readline()        #COMPRUEBA ENVIO DATOS
            print(f"DATO RECIBIDO {dato_r}")

        elif 239 > x >= 160:    #SI EL CENTROIDE SE ENCUENTRA EN LA POSICION 200
            print("Mover a la izquierda 60%")
            time.sleep(0.1)
            self.ser.write(b"izq2\n")          #ENVIO DE DATOS A ARDUINO
            dato_r = self.ser.readline()        #COMPRUEBA ENVIO DATOS
            print(f"DATO RECIBIDO {dato_r}")

        elif 319 >= x >= 240:    #SI EL CENTROIDE SE ENCUENTRA EN LA POSICION 200
            print("Mover a la izquierda 30%")
            time.sleep(0.1)
            self.ser.write(b"izq3\n")          #ENVIO DE DATOS A ARDUINO
            dato_r = self.ser.readline()        #COMPRUEBA ENVIO DATOS
            print(f"DATO RECIBIDO {dato_r}")

        elif 399 >= x >= 320:    #SI EL CENTROIDE SE ENCUENTRA EN LA POSICION 200
            print("Mover al centro")
            time.sleep(0.1)
            self.ser.write(b"ctr\n")           #ENVIO DE DATOS A ARDUINO
            dato_r = self.ser.readline()        #COMPRUEBA ENVIO DATOS
            print(f"DATO RECIBIDO {dato_r}")

        elif 399 >= x >= 320:    #SI EL CENTROIDE SE ENCUENTRA EN LA POSICION 200
            print("moviendo a la derecha 30%")
            time.sleep(0.1)
            self.ser.write(b"der3\n")          #ENVIO DE DATOS A ARDUINO
            dato_r = self.ser.readline()        #COMPRUEBA ENVIO DATOS
            print(f"DATO RECIBIDO {dato_r}")

        elif 479 >= x >= 400:   #SI EL CENTROIDE SE ENCUENTRA EN LA POSICION 200
            print("moviendo a la derecha 60%")
            time.sleep(0.1)
            self.ser.write(b"der2\n")          #ENVIO DE DATOS A ARDUINO
            dato_r = self.ser.readline()        #COMPRUEBA ENVIO DATOS
            print(f"DATO RECIBIDO {dato_r}")

        elif 560 >= x >= 480:     #SI EL CENTROIDE SE ENCUENTRA EN LA POSICION 200
            print("Moviendo a la derecha 100%")
            time.sleep(0.1)
            self.ser.write(b"der1\n")          #ENVIO DE DATOS A ARDUINO
            dato_r = self.ser.readline()        #COMPRUEBA ENVIO DATOS
            print(f"DATO RECIBIDO {dato_r}")

        return x

if __name__ == "__main__":      #MAIN
    tracker = BlueTracker('COM3', 9600) #SE CREA UN OBJETO DE TIPO "BlueTracker" CON VALORES DE PUERTO COM Y VELOCIDAD DE BAUDIOS
    tracker.track() #INICIO DE SEGUIMIENTO DE OBJETOS


