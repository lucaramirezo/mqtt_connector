import pigpio
import random

# Dirección I2C predeterminada del TMP117
TMP117_ADDR = 0x48
TMP117_TEMP_REG = 0x00  # Registro de temperatura


class TMP117Reader:
    def __init__(self, pi, use_hardware=True):
        """
        Inicializa el lector TMP117.

        :param pi: Instancia de pigpio.
        :param use_hardware: Si True, incluye el bus I2C por hardware.
        """
        self.pi = pi
        self.use_hardware = use_hardware
        self.i2c_handlers = []
        self.locations = []  # Lista para almacenar ubicaciones de sensores

    def setup_buses(self, num_sensors, locations=None):
        """
        Configura los buses I2C según la cantidad de sensores requerida.

        :param num_sensors: Número de sensores a configurar.
        :param locations: Lista opcional de ubicaciones para los sensores.
        """
        self.i2c_handlers = []
        self.locations = locations if locations else [f"Sensor_{i + 1}" for i in range(num_sensors)]
        if len(self.locations) < num_sensors:
            raise ValueError("Debe proporcionar una ubicación para cada sensor.")

        gpio_pairs = [
            {"hardware": True, "sda": 2, "scl": 3},  # Bus I²C por hardware
            {"hardware": False, "sda": 4, "scl": 5},  # Bus I²C por software 1
            {"hardware": False, "sda": 6, "scl": 7},  # Bus I²C por software 2
            {"hardware": False, "sda": 8, "scl": 9},  # Bus I²C por software 3
            {"hardware": False, "sda": 10, "scl": 11},  # Bus I²C por software 4..
        ]

        if num_sensors > len(gpio_pairs):
            raise ValueError(f"Máximo soportado: {len(gpio_pairs)} sensores.")

        for i in range(num_sensors):
            bus = gpio_pairs[i]
            if self.use_hardware and bus["hardware"]:
                handler = self.pi.i2c_open(1, TMP117_ADDR)
            else:
                self.pi.set_mode(bus["sda"], pigpio.ALT0)
                self.pi.set_mode(bus["scl"], pigpio.ALT0)
                handler = self.pi.i2c_open(1, TMP117_ADDR, flags=0)
            self.i2c_handlers.append(handler)

    def read_temperature(self, handler):
        """
        Lee la temperatura del TMP117 en grados Celsius.

        :param handler: Handler I2C del bus.
        :return: Temperatura en °C o None si falla.
        """
        try:
            count, data = self.pi.i2c_read_i2c_block_data(handler, TMP117_TEMP_REG, 2)
            if count == 2:
                raw_temp = (data[0] << 8) | data[1]
                temperature = raw_temp * 0.0078125  # Conversión a Celsius
                return temperature
        except Exception as e:
            print(f"Error al leer datos: {e}")
        return None

    def close_buses(self):
        """
        Cierra todos los buses I²C y libera recursos.
        """
        for handler in self.i2c_handlers:
            self.pi.i2c_close(handler)
        self.pi.stop()

    def read_all_sensors(self):
        """
        Lee la temperatura de todos los sensores conectados.
        """
        for i, handler in enumerate(self.i2c_handlers):
            temp = self.read_temperature(handler)
            if temp is not None:
                print(f"Sensor {i + 1}: {temp:.2f}°C")
            else:
                print(f"Sensor {i + 1}: Error al leer datos")