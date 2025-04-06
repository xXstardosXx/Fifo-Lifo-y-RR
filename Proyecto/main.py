import time
from typing import List

# Clase que representa un proceso con sus atributos y métodos
class Data:
    def __init__(self, name: str, initial_time: int, duration_time: int):
        self.name = name  # Nombre del proceso
        self.initial_time = initial_time  # Tiempo de llegada del proceso
        self.duration_time = duration_time  # Duración del proceso
        self.final_time = 0  # Tiempo final del proceso
        self.total_time = 0  # Tiempo total del proceso
        self.wait_time = 0  # Tiempo de espera del proceso
        self.service_index = 0.0  # Índice de servicio del proceso
        self.visited = False  # Indica si el proceso ya fue atendido
    
    # Método para reiniciar los datos del proceso
    def reset_data(self):
        self.final_time = 0
        self.total_time = 0
        self.wait_time = 0
        self.service_index = 0.0
        self.visited = False

# Variables globales
times: List[Data] = []  # Lista de procesos
best_service_value = 0.0  # Mejor índice de servicio
best_algorithm_index = 0  # Índice del mejor algoritmo
names = ["FIFO", "LIFO", "Round Robin"]  # Nombres de los algoritmos
DEFAULT_QUANTUM = 4  # Quantum por defecto para Round Robin

# Función para cargar los datos desde el archivo data.txt
def load_data() -> int:
    try:
        with open("data.txt", 'r') as file:
            for line in file:
                # Limpiar línea y dividir por comas (soporta ambos formatos)
                line = line.strip().replace('(', ',').replace(')', '').replace(' ', '')
                parts = [p for p in line.split(',') if p]
                if len(parts) != 3:
                    continue
                name = parts[0]
                initial_time = int(parts[1])
                duration_time = int(parts[2])
                times.append(Data(name, initial_time, duration_time))
        return 0
    except FileNotFoundError:
        print("❌ Error: No se encontró 'data.txt' en la carpeta actual.")
        return -1
    except Exception as e:
        print(f"❌ Error al cargar datos: {e}")
        return -1

# Función para reiniciar los datos de todos los procesos
def reset_data():
    """Reinicia los datos de todos los procesos en la lista 'times'."""
    for process in times:
        process.reset_data()
    print("🔄 Datos reiniciados correctamente.")  # Mensaje de depuración

# Función para determinar el algoritmo ganador
def winner():
    print(f"\n🏆 El algoritmo más eficiente fue: {names[best_algorithm_index]}")
    print(f"📊 Índice de servicio: {best_service_value:.2f}")

# Implementación del algoritmo FIFO
def fifo():
    global best_service_value, best_algorithm_index
    start_time = time.time()
    clock = 0
    count = 0
    total_time_t = wait_time_t = service_index_t = 0.0
    finished = False

    while not finished:
        for process in times:
            if process.initial_time <= clock and not process.visited:
                ft = clock + process.duration_time
                T = ft - process.initial_time
                e = T - process.duration_time
                I = process.duration_time / T

                process.final_time = ft
                process.total_time = T
                process.wait_time = e
                process.service_index = I
                process.visited = True

                time.sleep(0.01)  # Simulación
                clock += process.duration_time
                count += 1

                total_time_t += T
                wait_time_t += e
                service_index_t += I
                break
        else:
            if count >= len(times):
                finished = True
            else:
                clock += 1

    # Imprimir resultados del algoritmo FIFO
    print("\n" + "="*100)
    print("Proceso\t| ti\t| t\t| tf\t| T\t| E\t| I")
    print("-"*100)
    for p in times:
        print(f"{p.name}\t| {p.initial_time}\t| {p.duration_time}\t| {p.final_time}\t| {p.total_time}\t| {p.wait_time}\t| {p.service_index:.2f}")
    print("-"*100)

    avg_service = service_index_t / len(times)
    if avg_service > best_service_value:
        best_service_value = avg_service
        best_algorithm_index = 0

    print(f"\n⏱️ Tiempos promedio: T={total_time_t/len(times):.2f}, E={wait_time_t/len(times):.2f}, I={avg_service:.2f}")
    print(f"⏳ Reloj final: {clock} | Tiempo real: {(time.time()-start_time)*1000:.2f}ms")

# Implementación del algoritmo LIFO
def lifo():
    global best_service_value, best_algorithm_index
    start_time = time.time()
    clock = 0
    count = 0
    total_time_t = wait_time_t = service_index_t = 0.0
    finished = False

    while not finished:
        for process in reversed(times):
            if process.initial_time <= clock and not process.visited:
                ft = clock + process.duration_time
                T = ft - process.initial_time
                e = T - process.duration_time
                I = process.duration_time / T

                process.final_time = ft
                process.total_time = T
                process.wait_time = e
                process.service_index = I
                process.visited = True

                time.sleep(0.01)
                clock += process.duration_time
                count += 1

                total_time_t += T
                wait_time_t += e
                service_index_t += I
                break
        else:
            if count >= len(times):
                finished = True
            else:
                clock += 1

    # Imprimir resultados del algoritmo LIFO
    print("\n" + "="*100)
    print("Proceso\t| ti\t| t\t| tf\t| T\t| E\t| I")
    print("-"*100)
    for p in times:
        print(f"{p.name}\t| {p.initial_time}\t| {p.duration_time}\t| {p.final_time}\t| {p.total_time}\t| {p.wait_time}\t| {p.service_index:.2f}")
    print("-"*100)

    avg_service = service_index_t / len(times)
    if avg_service > best_service_value:
        best_service_value = avg_service
        best_algorithm_index = 1

    print(f"\n⏱️ Tiempos promedio: T={total_time_t/len(times):.2f}, E={wait_time_t/len(times):.2f}, I={avg_service:.2f}")
    print(f"⏳ Reloj final: {clock} | Tiempo real: {(time.time()-start_time)*1000:.2f}ms")

# Implementación del algoritmo Round Robin
def round_robin(quantum: int = DEFAULT_QUANTUM):
    global best_service_value, best_algorithm_index
    start_time = time.time()
    clock = 0
    remaining_time = [p.duration_time for p in times]
    total_time_t = wait_time_t = service_index_t = 0.0
    completed = 0

    while completed < len(times):
        for i, process in enumerate(times):
            if process.initial_time <= clock and remaining_time[i] > 0:
                exec_time = min(quantum, remaining_time[i])
                time.sleep(0.01 * exec_time)
                clock += exec_time
                remaining_time[i] -= exec_time

                if remaining_time[i] == 0:
                    ft = clock
                    T = ft - process.initial_time
                    e = T - process.duration_time
                    I = process.duration_time / T

                    process.final_time = ft
                    process.total_time = T
                    process.wait_time = e
                    process.service_index = I

                    total_time_t += T
                    wait_time_t += e
                    service_index_t += I
                    completed += 1
        else:
            if all(p.initial_time > clock for p in times if remaining_time[times.index(p)] > 0):
                clock += 1

    # Imprimir resultados del algoritmo Round Robin
    print("\n" + "="*100)
    print("Proceso\t| ti\t| t\t| tf\t| T\t| E\t| I")
    print("-"*100)
    for p in times:
        print(f"{p.name}\t| {p.initial_time}\t| {p.duration_time}\t| {p.final_time}\t| {p.total_time}\t| {p.wait_time}\t| {p.service_index:.2f}")
    print("-"*100)

    avg_service = service_index_t / len(times)
    if avg_service > best_service_value:
        best_service_value = avg_service
        best_algorithm_index = 2

    print(f"\n⏱️ Tiempos promedio: T={total_time_t/len(times):.2f}, E={wait_time_t/len(times):.2f}, I={avg_service:.2f}")
    print(f"⏳ Reloj final: {clock} | Tiempo real: {(time.time()-start_time)*1000:.2f}ms")

# Función principal que ejecuta los algoritmos
def main():
    print("\n" + "="*50 + " SIMULADOR DE PLANIFICACIÓN " + "="*50)
    if load_data() == -1:
        return  # Termina si no se pudo cargar data.txt

    print("\n" + "="*50 + " FIFO " + "="*50)
    fifo()
    reset_data()  # Reinicia los datos antes de LIFO

    print("\n" + "="*50 + " LIFO " + "="*50)
    lifo()
    reset_data()  # Reinicia los datos antes de Round Robin

    print("\n" + "="*50 + f" ROUND ROBIN (Q={DEFAULT_QUANTUM}) " + "="*50)
    round_robin(DEFAULT_QUANTUM)

    winner()

# Punto de entrada del programa
if __name__ == "__main__":
    main()