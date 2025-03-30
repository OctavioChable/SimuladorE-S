import time
import random
import matplotlib.pyplot as plt

class colaOperacion: 
    def __init__(self, valorError):
        self.valorError = valorError
        self.cola = []
        self.NoOperacion = 0 
        self.colaFinal = []
        self.procesados = 0
        self.completados = 0
        self.fallidos = 0  # Contador de fallos
        self.reintentados = 0  # Contador de reintentos
        self.tiempos_procesamiento = []  # Almacena los tiempos de procesamiento exitoso
        self.latencias = []  # Almacena las latencias totales (incluyendo fallos y reintentos)

    def encolar(self, datosRecibidos):
        self.NoOperacion +=1
        datosXEncolar = [datosRecibidos[0], datosRecibidos[1], datosRecibidos[2], 'En espera', 0, self.NoOperacion]  # Contador de intentos en índice [4]
        self.cola.append(datosXEncolar)

    def actualizarValorError(self, valorErr):
        self.valorError = valorErr 

    def devolverProcesados(self):
        return self.procesados
    
    def devolverFallidos(self):
        return self.fallidos
    
    def devolverReintendados(self):
        return self.reintentados
    
    def devolverRealizados(self):
        return self.completados

    def desencolar(self):
        if self.cola: 
            elemento = self.cola.pop(0)  # Extrae el primer elemento
            return elemento
        else:
            return None
        
    def infoProcesos(self, ventana): 
        for i in range(len(self.colaFinal)):
            elemento = self.colaFinal[i]
            j = 0
            for elementos in elemento:
                textoTabla = ""
                if j != 3: 
                    textoTabla = str(elementos)
                elif (len(self.colaFinal)-1) == i:
                    textoTabla = 'Procesando'
                else:
                    textoTabla = str(elementos)
                ventana.modificar_celdaTabla(i, j, textoTabla)
                j+=1

    def infoFinal(self, ventana): 
        for i in range(len(self.colaFinal)):
            elemento = self.colaFinal[i]
            j = 0
            for elementos in elemento:
                textoTabla = str(elementos)
                ventana.modificar_celdaTabla(i, j, textoTabla)
                j+=1

    def obtener_fallidos(self):
        # Devuelve una lista con los procesos fallidos
        return [proceso for proceso in self.colaFinal if proceso[3] == 'Fallido']

    def obtener_reintentos(self):
        # Devuelve una lista con los procesos que han sido reintentados
        return [proceso for proceso in self.colaFinal if proceso[4] > 0]

    def Procesar(self, datosCola):
        inicio = time.time()  # Inicio del cronómetro
        datosCola[3] = 'Procesando'
        
        # Simular un fallo con probabilidad del 20% (ajustable)
        if random.random() < self.valorError:
            datosCola[4] += 1  # Incrementa el contador de intentos
            print(f"⚠️ Fallo en la operación: {datosCola}")
            
            # Verificar si se alcanzó el límite de intentos
            if datosCola[4] >= 2:
                datosCola[3] = 'Fallido'  # Marcar como fallido
                self.fallidos += 1
                print("Se ignoró el proceso después de 2 intentos fallidos.")
                fin = time.time()
                self.latencias.append(fin - inicio)  # Registrar latencia total
                return datosCola
            else:
                print("Reintentando operación...")
                self.reintentados += 1
                return self.Procesar(datosCola)  # Reintenta la operación
        else:
            time.sleep(1)  # Simula el tiempo de procesamiento
            datosCola[3] = 'Procesado'
            self.completados += 1
        
        fin = time.time()  # Fin del cronómetro
        self.tiempos_procesamiento.append(fin - inicio)  # Registrar tiempo exitoso
        self.latencias.append(fin - inicio)  # Registrar latencia total
        return datosCola

    def graficar_rendimiento(self):
        # Graficar los tiempos de procesamiento
        plt.figure(figsize=(12, 6))
        
        # Gráfica 1: Tiempo de procesamiento por operación
        plt.subplot(1, 2, 1)
        plt.plot(self.tiempos_procesamiento, label="Tiempo de Procesamiento (s)", marker='o')
        plt.title("Tiempos de Procesamiento")
        plt.xlabel("Número de Operación")
        plt.ylabel("Tiempo (s)")
        plt.legend()
        plt.grid()

        # Gráfica 2: Latencia total por operación
        plt.subplot(1, 2, 2)
        plt.plot(self.latencias, label="Latencia Total (s)", color="orange", marker='x')
        plt.title("Latencias Totales")
        plt.xlabel("Número de Operación")
        plt.ylabel("Tiempo (s)")
        plt.legend()
        plt.grid()

        plt.tight_layout()
        plt.show()


    def Inspeccion(self):
        print(f"Estado actual de la cola: {self.cola}")

    def actualizar_lista_estado(self, mensaje):
        self.lista_estado_cola.addItem(mensaje)

    def actualizarCola(self, ventana):
        fila = 0
        columna = 0 
        for procesos in self.cola:
            textoTabla = "Proceso:"+str(procesos[5])
            print(textoTabla)
            ventana.modificar_celdaTablaCola(fila, columna, textoTabla)
            columna += 1

    def Automatizado(self, ventana, procesados):
        numerocondicional = 0
        self.actualizarCola(ventana)
        if self.cola: 
            ventana.texto_notificaciones.append(f"\nProceso número: {procesados}")
            self.procesados = procesados

            # Extraer y procesar el elemento en la cola
            datos = self.desencolar()
            resultado = self.Procesar(datos)
            self.colaFinal.append(resultado)

            # Actualizar el estado en la interfaz gráfica
            ventana.actualizar_lista_estado(f"Procesado: {resultado[3]} | Dispositivo: {resultado[2]} | Operación: {resultado[1]}")
            ventana.lista_estado_cola.addItem(f"Estado del proceso: {resultado[3]}")
        
            ventana.actualizarResultados(self.procesados, self.fallidos, self.reintentados, self.completados)
        else: 
            ventana.texto_notificaciones.append("\n--- Resumen Final ---")
            ventana.texto_notificaciones.append(f"Operaciones Procesadas: {self.procesados}")
            ventana.texto_notificaciones.append(f"Fallidas: {self.fallidos}")
            ventana.texto_notificaciones.append(f"Reintentos: {self.reintentados}")
            numerocondicional = 1

        if numerocondicional == 0:
            self.infoProcesos(ventana)
        else:
            self.infoFinal(ventana)
        self.actualizarCola(ventana)
        


    def agregar_proceso_por_nombre(self, nombre_dispositivo, operacion):
        # Crear instancias de dispositivos para buscar el correcto
        dispositivos = {
            "mouse": mouse("mouse1"),
            "teclado": teclado("teclado1")
        }

        # Verificar si el dispositivo es válido
        if nombre_dispositivo.lower() in dispositivos:
            dispositivo = dispositivos[nombre_dispositivo.lower()]

            # Verificar qué operaciones son válidas para el dispositivo actual
            if isinstance(dispositivo, mouse):
                operaciones = {
                    "movimiento": dispositivo.movimiento,
                    "click": dispositivo.clicks,
                    "scroll": dispositivo.Scroll
                }
            elif isinstance(dispositivo, teclado):
                operaciones = {
                    "tecla presionada": dispositivo.teclaPresionada,
                    "teclas modificadoras": dispositivo.teclasModificadoras,
                    "combinacion": dispositivo.combinaciones,
                    "mantener presionado": dispositivo.mantenerPresionado
                }
            else:
                print(f"❌ El dispositivo '{nombre_dispositivo}' no tiene operaciones válidas")
                return

            # Verificar si la operación es válida para este dispositivo
            if operacion.lower() in operaciones:
                proceso = operaciones[operacion.lower()]()  # Ejecutar la operación
                self.encolar(proceso)  # Encolar el proceso
                print(f"✔️ Proceso agregado a la cola: {proceso}")
            else:
                print(f"❌ Operación '{operacion}' no encontrada para el dispositivo '{nombre_dispositivo}'")
        else:
            print(f"❌ Dispositivo '{nombre_dispositivo}' no encontrado")





    
class mouse:
    def __init__(self, nombre):
        self.nombre = nombre

    def movimiento(self):
        tipoOperacion = 'entrada'
        nombreOperacion = 'movimientoMouse'
        dispositivo = self.nombre 
        return [tipoOperacion, nombreOperacion, dispositivo]
    
    def clicks(self):
        tipoOperacion = 'entrada'
        nombreOperacion = 'click'
        dispositivo = self.nombre 
        return [tipoOperacion, nombreOperacion, dispositivo]
    
    def Scroll(self):
        tipoOperacion = 'entrada'
        nombreOperacion = 'scroll'
        dispositivo = self.nombre 
        return [tipoOperacion, nombreOperacion, dispositivo]
    

class teclado: 
    def __init__(self, nombre):
        self.nombre = nombre

    def teclaPresionada(self):
        tipoOperacion = 'entrada'
        nombreOperacion = 'teclaPresionada'
        dispositivo = self.nombre 
        return [tipoOperacion, nombreOperacion, dispositivo]
    
    def teclasModificadoras(self):
        tipoOperacion = 'entrada'
        nombreOperacion = 'teclasModificadoras'
        dispositivo = self.nombre 
        return [tipoOperacion, nombreOperacion, dispositivo]
    
    def combinaciones(self):
        tipoOperacion = 'entrada'
        nombreOperacion = 'combinacion'
        dispositivo = self.nombre 
        return [tipoOperacion, nombreOperacion, dispositivo]
    
    def mantenerPresionado(self):
        tipoOperacion = 'entrada'
        nombreOperacion = 'mantenerPresionado'
        dispositivo = self.nombre 
        return [tipoOperacion, nombreOperacion, dispositivo]




