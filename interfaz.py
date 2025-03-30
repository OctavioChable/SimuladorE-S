import sys
import MejoraNoImplementada
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, 
    QProgressBar, QListWidget, QFormLayout, QComboBox, QSlider, QTextEdit, QDialog, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt

class SimuladorEIO(QMainWindow):
    def __init__(self):
        self.valorError = 0.2
        super().__init__()
        self.Procesos = []
        self.procesados = 0
        self.cola = MejoraNoImplementada.colaOperacion(self.valorError)
        self.setWindowTitle("Simulador de Procesos de Entrada/Salida")
        self.setGeometry(100, 100, 800, 600)

        # Diccionario para mapear dispositivos a operaciones
        self.operaciones_por_dispositivo = {
            "Mouse": ["Movimiento", "Click", "Scroll"],
            "Teclado": ["Tecla Presionada", "Mantener Presionado", "Teclas Modificadoras"]
        }

        # Widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout principal
        self.layout_principal = QVBoxLayout()
        self.central_widget.setLayout(self.layout_principal)

        # Cabecera: Título
        self.titulo = QLabel("Simulador de Procesos de Entrada/Salida")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titulo.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout_principal.addWidget(self.titulo)

        # Panel de Control: Botones en una línea
        self.panel_botones = QWidget()
        self.layout_botones = QHBoxLayout()
        self.panel_botones.setLayout(self.layout_botones)

        self.boton_iniciar = QPushButton("Iniciar Simulación")
        self.boton_pausar = QPushButton("Siguiente")
        self.boton_reiniciar = QPushButton("Reiniciar Simulación")
        self.layout_botones.addWidget(self.boton_iniciar)
        self.layout_botones.addWidget(self.boton_pausar)
        self.layout_botones.addWidget(self.boton_reiniciar)

        self.layout_principal.addWidget(self.panel_botones)

        # Sección: Agregar Procesos con Comboboxes
        self.seccion_agregar_procesos = QWidget()
        self.layout_agregar_procesos = QFormLayout()
        self.seccion_agregar_procesos.setLayout(self.layout_agregar_procesos)

        self.combo_dispositivo = QComboBox()
        self.combo_dispositivo.addItems(["Mouse", "Teclado"])  # Opciones de dispositivos
        self.combo_dispositivo.currentIndexChanged.connect(self.actualizar_operaciones)

        self.combo_operacion = QComboBox()
        self.actualizar_operaciones()  # Configura inicialmente las operaciones

        self.boton_agregar_proceso = QPushButton("Agregar Proceso")
        self.layout_agregar_procesos.addRow("Seleccionar Dispositivo:", self.combo_dispositivo)
        self.layout_agregar_procesos.addRow("Seleccionar Operación:", self.combo_operacion)
        self.layout_agregar_procesos.addWidget(self.boton_agregar_proceso)

        self.layout_principal.addWidget(QLabel("Agregar Procesos:"))
        self.layout_principal.addWidget(self.seccion_agregar_procesos)

        #definir tablitas 
        self.tabla = QTableWidget()
        self.tabla.setRowCount(0)
        self.tabla.setColumnCount(6)

        self.tablaCola = QTableWidget()
        self.tablaCola.setRowCount(1)
        self.tablaCola.setColumnCount(0)

        # Sección: Modificador de Margen de Error con porcentaje
        self.slider_error = QSlider(Qt.Orientation.Horizontal)
        self.slider_error.setMinimum(0)
        self.slider_error.setMaximum(50)
        self.slider_error.setValue(20)
        self.slider_error.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_error.setTickInterval(5)
        self.slider_error.valueChanged.connect(self.actualizar_margen_error)
        self.label_error = QLabel("Margen de Error: 20%")

        self.layout_principal.addWidget(QLabel("Modificador de Margen de Error:"))
        self.layout_principal.addWidget(self.slider_error)
        self.layout_principal.addWidget(self.label_error)

        # Sección: Estado de la Cola (dividida en dos)
        self.seccion_estado_cola = QWidget()
        self.layout_estado_cola = QVBoxLayout()
        self.seccion_estado_cola.setLayout(self.layout_estado_cola)

        # Subsección 1: Procesos Agregados
        self.lista_procesos_agregados = QListWidget()
        self.layout_estado_cola.addWidget(QLabel("Procesos Agregados (Estáticos):"))
        self.layout_estado_cola.addWidget(self.lista_procesos_agregados)

        # Subsección 2: Estado Actual de la Cola
        self.lista_estado_cola = QListWidget()
        self.layout_estado_cola.addWidget(QLabel("Estado Actual de la Cola:"))
        self.layout_estado_cola.addWidget(self.lista_estado_cola)

        self.layout_principal.addWidget(self.tablaCola)

        #subseccion 3: informacion procesos 
        self.layout_estado_cola.addWidget(QLabel("Informacion procesos"))

        self.layout_principal.addWidget(self.tabla)

        # Sección: Notificaciones (QTextEdit)
        self.seccion_notificaciones = QWidget()
        self.layout_notificaciones = QVBoxLayout()
        self.seccion_notificaciones.setLayout(self.layout_notificaciones)

        self.label_notificaciones = QLabel("Notificaciones:")
        self.texto_notificaciones = QTextEdit()
        self.texto_notificaciones.setReadOnly(True)  # Solo lectura
        self.layout_notificaciones.addWidget(self.label_notificaciones)
        self.layout_notificaciones.addWidget(self.texto_notificaciones)

        self.layout_principal.addWidget(self.seccion_notificaciones)

        # Sección: Resultados
        self.seccion_resultados = QWidget()
        self.layout_resultados = QVBoxLayout()
        self.seccion_resultados.setLayout(self.layout_resultados)

        self.resultados = QLabel("Resultados:\nOperaciones Procesadas: 0\nFallidas: 0\nReintentos Realizados: 0\nCompletadas: 0")
        self.resultados.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layout_resultados.addWidget(self.resultados)

        self.layout_principal.addWidget(QLabel("Resultados:"))
        self.layout_principal.addWidget(self.seccion_resultados)

        # Panel de botones en la esquina inferior derecha
        self.panel_inferior = QWidget()
        self.layout_inferior = QHBoxLayout()
        self.layout_inferior.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.panel_inferior.setLayout(self.layout_inferior)

        self.boton_rendimiento = QPushButton("Mostrar Rendimiento")
        self.boton_fallidos = QPushButton("Procesos Fallidos")
        self.boton_reintentos = QPushButton("Procesos Reintentados")
        self.layout_inferior.addWidget(self.boton_rendimiento)
        self.layout_inferior.addWidget(self.boton_fallidos)
        self.layout_inferior.addWidget(self.boton_reintentos)

        self.layout_principal.addWidget(self.panel_inferior)

        # Eventos para botones principales
        self.boton_iniciar.clicked.connect(self.iniciar_simulacion)
        self.boton_pausar.clicked.connect(self.Siguientes)
        self.boton_reiniciar.clicked.connect(self.reiniciar_simulacion)
        self.boton_agregar_proceso.clicked.connect(self.agregar_proceso)
        self.boton_rendimiento.clicked.connect(self.mostrar_graficas)
        self.boton_fallidos.clicked.connect(self.mostrar_fallidos)
        self.boton_reintentos.clicked.connect(self.mostrar_reintentos)


    def actualizar_lista_estado(self, mensaje):
        self.lista_estado_cola.addItem(mensaje)

    def agregar_fila(tabla):
        filas = tabla.rowCount()
        tabla.setRowCount(filas + 1)  # Aumenta el número de filas
        for columna in range(tabla.columnCount()):  # Llena la fila con datos iniciales
            tabla.setItem(filas, columna, QTableWidgetItem(f"Fila {filas + 1}, Columna {columna + 1}"))

    def agregar_columna(tabla):
        columnas = tabla.columnCount()
        tabla.setColumnCount(columnas + 1)  # Aumenta el número de columnas
        for fila in range(tabla.rowCount()):  # Llena la columna con datos iniciales
            tabla.setItem(fila, columnas, QTableWidgetItem(f"Fila {fila + 1}, Columna {columnas + 1}"))

    def eliminar_fila(tabla):
        filas = tabla.rowCount()
        if filas > 0:  # Verifica si hay filas para eliminar
            tabla.removeRow(filas - 1)  # Elimina la última fila

    def eliminar_columna(tabla):
        columnas = tabla.columnCount()
        if columnas > 0:  # Verifica si hay columnas para eliminar
            tabla.removeColumn(columnas - 1)  # Elimina la última columna


    def mostrar_fallidos(self):
        # Crear ventana para mostrar los procesos fallidos
        ventana_fallidos = QDialog(self)
        ventana_fallidos.setWindowTitle("Procesos Fallidos")
        ventana_fallidos.setGeometry(150, 150, 400, 300)

        layout = QVBoxLayout()
        label = QLabel("Lista de Procesos Fallidos:")
        text_area = QTextEdit()
        text_area.setReadOnly(True)

        # Obtener los procesos fallidos desde la lógica
        fallidos = self.cola.obtener_fallidos()
        if fallidos:
            text_area.setText("\n".join([str(proceso) for proceso in fallidos]))
        else:
            text_area.setText("No hay procesos fallidos.")

        # Botón de cerrar
        boton_cerrar = QPushButton("Cerrar")
        boton_cerrar.clicked.connect(ventana_fallidos.close)

        layout.addWidget(label)
        layout.addWidget(text_area)
        layout.addWidget(boton_cerrar)
        ventana_fallidos.setLayout(layout)
        ventana_fallidos.exec()

    def mostrar_reintentos(self):
        # Crear ventana para mostrar los procesos reintentados
        ventana_reintentos = QDialog(self)
        ventana_reintentos.setWindowTitle("Procesos Reintentados")
        ventana_reintentos.setGeometry(150, 150, 400, 300)

        layout = QVBoxLayout()
        label = QLabel("Lista de Procesos Reintentados:")
        text_area = QTextEdit()
        text_area.setReadOnly(True)

        # Obtener los procesos reintentados desde la lógica
        reintentos = self.cola.obtener_reintentos()
        if reintentos:
            text_area.setText("\n".join([str(proceso) for proceso in reintentos]))
        else:
            text_area.setText("No hay procesos reintentados.")

        # Botón de cerrar
        boton_cerrar = QPushButton("Cerrar")
        boton_cerrar.clicked.connect(ventana_reintentos.close)

        layout.addWidget(label)
        layout.addWidget(text_area)
        layout.addWidget(boton_cerrar)
        ventana_reintentos.setLayout(layout)
        ventana_reintentos.exec()


    def actualizar_operaciones(self):
        dispositivo = self.combo_dispositivo.currentText()
        operaciones = self.operaciones_por_dispositivo.get(dispositivo, [])
        self.combo_operacion.clear()
        self.combo_operacion.addItems(operaciones)
    #Iniciar Simulacion 
    def iniciar_simulacion(self):
        self.texto_notificaciones.clear()
        self.lista_estado_cola.clear()
        self.cola = MejoraNoImplementada.colaOperacion(self.valorError)
        nuevolista = self.clonarlista()
        self.vaciar_lista(self.Procesos)
        self.Procesos = nuevolista
        print(self.Procesos)
        self.texto_notificaciones.append("Simulación iniciada...")
        self.procesados += 1
        self.cola.Automatizado(self,self.procesados)  # Pasamos la ventana como referencia

    def clonarlista(self):
        listanueva = []
        for elemento in self.Procesos:
            listanueva.append(elemento)
        return listanueva
    
    def vaciar_lista(self, lista):
        # Crear una variable para almacenar los valores sacados
        valores_sacados = []
        numeroprocesos = 0
        # Extraer cada elemento de la lista y vaciarla
        while lista:
            elemento = lista.pop(0)  # Extrae el primer elemento (una sublista)
            valores_sacados.append(elemento)  # Agrega la sublista extraída a valores_sacados

            # Asegúrate de que el elemento tiene la estructura correcta (2 dimensiones)
            if len(elemento) >= 2:
                self.cola.agregar_proceso_por_nombre(elemento[0], elemento[1])  # Usa los valores específicos
            else:
                print(f"⚠️ El elemento no tiene el formato esperado: {elemento}")
            numeroprocesos += 1
            
        self.tablaCola.setColumnCount(numeroprocesos)
        self.tabla.setRowCount(numeroprocesos)
    


    def modificar_celdaTablaCola(self, fila, columna, texto):
        """
        Modifica el contenido de una celda específica en una tabla QTableWidget.

        Parámetros:
            tabla (QTableWidget): La tabla en la que se realizará la modificación.
            fila (int): El índice de la fila de la celda.
            columna (int): El índice de la columna de la celda.
            texto (str): El texto que se asignará a la celda.
        """
        # Crear un nuevo elemento de tabla con el texto proporcionado
        nuevo_item = QTableWidgetItem(texto)
        # Asignar el nuevo elemento a la celda específica
        self.tablaCola.setItem(fila, columna, nuevo_item)

    def modificar_celdaTabla(self, fila, columna, texto):
        """
        Modifica el contenido de una celda específica en una tabla QTableWidget.

        Parámetros:
            tabla (QTableWidget): La tabla en la que se realizará la modificación.
            fila (int): El índice de la fila de la celda.
            columna (int): El índice de la columna de la celda.
            texto (str): El texto que se asignará a la celda.
        """
        # Crear un nuevo elemento de tabla con el texto proporcionado
        nuevo_item = QTableWidgetItem(texto)
        # Asignar el nuevo elemento a la celda específica
        self.tabla.setItem(fila, columna, nuevo_item)


        
        
    def mostrar_graficas(self):
        self.texto_notificaciones.append("Mostrando gráficos de rendimiento...")
        self.cola.graficar_rendimiento()  # Llama al método para generar las gráficas


    def Siguientes(self):
        self.procesados +=1
        self.tablaCola.removeColumn(0)
        self.cola.Automatizado(self, self.procesados)

    def reiniciar_simulacion(self):
        self.procesados = 0
        self.resultados.setText("Resultados:\nOperaciones Procesadas: 0\nFallidas: 0\nReintentos Realizados: 0\nCompletadas: 0")
        self.texto_notificaciones.clear()
        self.cola = MejoraNoImplementada.colaOperacion(self.valorError)
        self.texto_notificaciones.append("Simulación reiniciada.")
        self.lista_estado_cola.clear()
        self.lista_estado_cola.addItem("Cola reiniciada.")
        self.lista_procesos_agregados.clear()
    
    def agregar_proceso(self):
        dispositivo = self.combo_dispositivo.currentText()
        operacion = self.combo_operacion.currentText()
    
        # Agregar el proceso a la interfaz gráfica
        self.lista_procesos_agregados.addItem(f"{dispositivo} - {operacion}")
        self.texto_notificaciones.append(f"Proceso agregado: {dispositivo} - {operacion}")
    
        # Almacenar el proceso en la lista de procesos
        self.Procesos.append((dispositivo, operacion))
        self.texto_notificaciones.append(f"Procesos almacenados: {self.Procesos}")

    def actualizar_margen_error(self):
        valor = self.slider_error.value()
        self.label_error.setText(f"Margen de Error: {valor}%")
        self.valorError = valor/100
        self.cola.actualizarValorError(self.valorError)

    def actualizarResultados(self, procesados, fallidos, reintentos, completos):
        self.resultados.setText(f"Resultados:\nOperaciones Procesadas: {procesados}\nFallidas: {fallidos}\nReintentos Realizados: {reintentos}\nCompletadas: {completos}")

# Crear la aplicación
app = QApplication(sys.argv)
ventana = SimuladorEIO()
ventana.show()
sys.exit(app.exec())
