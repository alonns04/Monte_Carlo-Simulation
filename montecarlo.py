import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Definir las actividades con sus estimaciones PERT
activities = {
    'A': {'optimistic': 2, 'most_likely': 4, 'pessimistic': 6},
    'B': {'optimistic': 1, 'most_likely': 3, 'pessimistic': 5},
    'C': {'optimistic': 2, 'most_likely': 2, 'pessimistic': 8},
    'D': {'optimistic': 3, 'most_likely': 5, 'pessimistic': 7}
}

# Definir las dependencias (simplificadas)
dependencies = {
    'A': [],
    'B': ['A'],
    'C': ['A'],
    'D': ['B', 'C']
}

# Número de simulaciones
num_simulations = 10000

# Función para generar una duración simulada usando distribución PERT (Beta)
def pert_random(optimistic, most_likely, pessimistic, size=1):
    alpha = ((4 * (most_likely - optimistic) + (pessimistic - optimistic)) / 6) ** 2
    beta = ((4 * (pessimistic - most_likely) + (pessimistic - optimistic)) / 6) ** 2
    mean = (optimistic + 4 * most_likely + pessimistic) / 6
    return np.random.beta(alpha, beta, size) * (pessimistic - optimistic) + optimistic

# Simulación Monte Carlo
results = []

for _ in range(num_simulations):
    durations = {}
    for task, estimates in activities.items():
        durations[task] = pert_random(estimates['optimistic'], estimates['most_likely'], estimates['pessimistic'])
    
    # Calcular el tiempo total del proyecto considerando las dependencias
    project_time = 0
    task_completion_times = {}
    for task in dependencies:
        if dependencies[task]:
            max_dependency_time = max(task_completion_times[dep] for dep in dependencies[task])
            task_completion_times[task] = durations[task] + max_dependency_time
        else:
            task_completion_times[task] = durations[task]
        project_time = max(project_time, task_completion_times[task])
    
    results.append(project_time)

# Convertir resultados a DataFrame para análisis
results_df = pd.DataFrame(results, columns=['Project Duration'])

# Estadísticas descriptivas de la duración del proyecto
statistics = results_df.describe(percentiles=[0.5, 0.75, 0.95])
print(statistics)

# Histograma de los resultados
results_df.hist(bins=50)
plt.title('Distribución de la Duración del Proyecto')
plt.xlabel('Duración del Proyecto')
plt.ylabel('Frecuencia')
plt.show()
