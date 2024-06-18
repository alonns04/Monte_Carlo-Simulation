import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def simulaciones(): # Cuantas simulaciones?
    global numero_simulaciones  # Declarar la variable como global
    numero_simulaciones = int(input("Ingrese la cantidad de simulaciones: "))

def extraer_actividades(): # Extrae actividades
    global actividades
    global dependencias
    actividades = {} # Crea el diccionario de las actividades
    dependencias = {} # Crea el diccionario de las dependencias
    df = pd.read_excel(ruta)
    for indice, valor in df['medio'].items():
        if pd.notna(valor) and isinstance(valor, (int, float)):
            # Obtener los valores de pesimista y optimista correspondientes
            pesimista = df.at[indice, 'pesimista']
            optimista = df.at[indice, 'optimista']
            nombre = df.at[indice, 'nombre_actividad']
            codigo = df.at[indice, 'código']
            medio = valor
            actividades_previas = df.at[indice, 'actividades_previas']
            actividades[str(codigo)] = {'nombre': nombre, 'pesimista': pesimista, 'medio': medio, 'optimista': optimista}
            if str(actividades_previas).strip().lower() == 'nan': # Si está vacío
                dependencias[str(codigo)] = [] # Pone una lista vacía
            else:
                dependencias[str(codigo)] = str(actividades_previas).split(',') # Sino, pone el código de las actividades previas

def triangular_aleatorio(optimista, esperado, pesimista, size=1):
    return np.random.triangular(optimista, esperado, pesimista, size)

def valores_totales_aleatorios(): # Genera los valores totales aleatorios en base a cada actividad aleatoria con beta pert
    global resultados
    resultados = []
    for _ in range(numero_simulaciones): # Para cada simulación...
        duracion = {} # Duración diccionario vacío
        for tareas, valor in actividades.items(): # Para la llave 
            # "valor" es el diccionario que está adentro de actividades
            # Genera un valor aleatorio con la distribución beta pert y crea una llave con ese valor en el diccionario "duracion"
            duracion[tareas] = triangular_aleatorio(valor['optimista'], valor['medio'], valor['pesimista']) 
        # Calcular el tiempo total del proyecto considerando las dependencias
        tiempo_proyecto = 0 # Tiempo del proyecto 
        tiempo_completado_tareas = {} # Diccionario para las tareas y su tiempo máximo aleatorio de finalización
        for tarea in dependencias: # Para cada tarea
            if dependencias[tarea]: # Si existe dependencias
                # Genera un objeto iterable con los tiempos de cada actividad con dependencias
                maximo_tiempo_dependencia = max(tiempo_completado_tareas[dep] for dep in dependencias[tarea])
                # Le asigna en el diccionario el tiempo aleatorio de la tarea ( duración[tarea] ) sumado a la suma de la iteración, es decir, crea el tiempo aleatorio total
                tiempo_completado_tareas[tarea] = duracion[tarea] + maximo_tiempo_dependencia
            else:
                # Si no tiene dependencias, el tiempo aleatorio total es igual al tiempo aleatorio de esa actividad
                tiempo_completado_tareas[tarea] = duracion[tarea]
            # Elige el número máximo entre tiempo_proyecto y el tiempo aleatorio total de la tarea.
            tiempo_proyecto = max(tiempo_proyecto, tiempo_completado_tareas[tarea])
        # Cuando termina la iteración de cada tarea, añade a resultados el tiempo más grande entre todos los tiempos aleatorios totales de todas las tareas. ( Añade el tiempo aleatorio total del proyecto )
        resultados.append(tiempo_proyecto) # Lo repite la cantidad de veces que sean las simulaciones
    return resultados

def estadisticas(q1 = 0.5, q2 = 0.75, q3 = 0.95):
    global resultados_df
    # Estadísticas descriptivas de la duración del proyecto
    resultados_df = pd.DataFrame(valores_totales_aleatorios(), columns=['Project Duration'])
    estadistica = resultados_df.describe(percentiles=[q1, q2, q3])
    return estadistica

ruta = r'c:\UNI\Materias\Formulación y evaluación\Proyecto\Python\excel\PERT.xlsx'

def mostrar_datos():
    resultados_df.hist(bins=50)
    plt.title('Distribución de la Duración del Proyecto')
    plt.xlabel('Duración del Proyecto')
    plt.ylabel('Frecuencia')
    plt.show()

def main():
    simulaciones()
    extraer_actividades()
    print(estadisticas())
    mostrar_datos()
