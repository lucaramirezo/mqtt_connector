import subprocess
import os
import signal
import time
import psutil

def start_scripts():
    # Iniciar el simulador y el conector
    simulator_process = subprocess.Popen(["python", "simulator.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    connector_process = subprocess.Popen(["python", "connector.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Guardar PIDs en archivos para seguimiento
    with open("simulator.pid", "w") as sim_pid_file:
        sim_pid_file.write(str(simulator_process.pid))
    with open("connector.pid", "w") as con_pid_file:
        con_pid_file.write(str(connector_process.pid))

    print(f"Simulador iniciado con PID: {simulator_process.pid}")
    print(f"Conector iniciado con PID: {connector_process.pid}")

    # Esperar 10 segundos antes de detener los procesos
    time.sleep(10)
    stop_scripts()

def stop_scripts():
    # Leer los PIDs desde los archivos y matar los procesos
    if os.path.exists("simulator.pid") and os.path.exists("connector.pid"):
        with open("simulator.pid", "r") as sim_pid_file:
            simulator_pid = int(sim_pid_file.read())
        with open("connector.pid", "r") as con_pid_file:
            connector_pid = int(con_pid_file.read())

        print(f"Deteniendo simulador (PID: {simulator_pid})...")
        try:
            process = psutil.Process(simulator_pid)
            process.terminate()
        except psutil.NoSuchProcess:
            print(f"El proceso {simulator_pid} no existe.")
        except psutil.AccessDenied:
            print(f"Acceso denegado al proceso {simulator_pid}. Intenta ejecutar como administrador.")

        print(f"Deteniendo conector (PID: {connector_pid})...")
        try:
            process = psutil.Process(connector_pid)
            process.terminate()
        except psutil.NoSuchProcess:
            print(f"El proceso {connector_pid} no existe.")
        except psutil.AccessDenied:
            print(f"Acceso denegado al proceso {connector_pid}. Intenta ejecutar como administrador.")

        # Eliminar archivos de PID
        os.remove("simulator.pid")
        os.remove("connector.pid")
    else:
        print("No se encontraron archivos PID. Asegúrate de que los procesos estén en ejecución.")

if __name__ == "__main__":
    start_scripts()
