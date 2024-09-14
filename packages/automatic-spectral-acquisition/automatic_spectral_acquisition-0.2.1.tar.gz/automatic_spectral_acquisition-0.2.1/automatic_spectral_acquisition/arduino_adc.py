import serial

import numpy as np
from statemachine import State, StateMachine
from statemachine.exceptions import TransitionNotAllowed

from automatic_spectral_acquisition.config import ConfigHandler
from automatic_spectral_acquisition.helper import error_message
from automatic_spectral_acquisition.constants import *
from automatic_spectral_acquisition.arduino import Arduino, ArduinoStateMachine


class ArduinoADCStateMachine(ArduinoStateMachine):
    """State machine for the Arduino connection. This version is used for the ADC measurements."""
    # Define states
    start = State('Start', initial=True)
    connected = State('Connected') 
    requested = State('Requested') # Requested a change in position
    measured = State('Measured') # Requested a measurement
    completed = State('Completed') # Received confirmation by the arduino
    disconnected = State('Disconnected')

    # Define transitions
    connect = start.to(connected) | disconnected.to(connected)
    request = connected.to(requested) | completed.to(requested)
    measure = connected.to(measured) | completed.to(measured)
    wait = requested.to.itself()
    complete = requested.to(completed) | measured.to(completed)
    disconnect = completed.to(disconnected) | connected.to(disconnected)
    
    # Define transition actions
    def on_measure(self, *args, **kwargs):
        # Check if number_of_measurements is passed
        number_of_measurements:int = kwargs.get('number_of_measurements')
        if not isinstance(number_of_measurements, int):
            error_message('TypeError', 'Position not passed or not a int.')
        
        # Check if arduino_instance is passed
        arduino_instance:ArduinoADC = kwargs.get('arduino_instance')
        if not isinstance(arduino_instance, ArduinoADC):
            error_message('TypeError', 'ArduinoADC object not passed.')
        
        measurements = []
        for _ in range(number_of_measurements):
            arduino_instance.arduino_connection.write(bytes(f'{MEAS}~', 'UTF-8'))
            while True:
                if arduino_instance.arduino_connection.in_waiting: # check if there is data to read
                    received_bytes = arduino_instance.arduino_connection.read_until(expected=b'~')
                    try:
                        message = received_bytes.decode('UTF-8')[:-1]
                    except UnicodeDecodeError:
                        error_message('UnicodeDecodeError', f'Could not decode command from arduino. Received: {received_bytes}')
                    
                    try:
                        measurements.append(float(message))
                        break
                    except ValueError:
                        if message == ERROR:
                            error_message('CommandError', 'Error occurred when using ADC.')
                        else:
                            error_message('CommandError', f'Unknown message received: {message}')
        
        measurements = np.asarray(measurements)
        return np.mean(measurements), np.std(measurements)
                    

    
class ArduinoADC(Arduino):
    """Class for controlling the Arduino connection. This version is used for the ADC measurements."""
    def __init__(self, config_handler:ConfigHandler) -> None:
        self.config_handler:ConfigHandler = config_handler
        self.state_machine:ArduinoADCStateMachine = ArduinoADCStateMachine()
        self.arduino_connection:serial.Serial = None
    
    def get_measurement(self, number_of_measurements:int=DEFAULT_NUMBER_OF_MEASUREMENTS) -> tuple[float, float]:
        """Returns an ADC measurement.

        Args:.
            number_of_measurements (int, optional): The number of measurements to take. Defaults to DEFAULT_NUMBER_OF_MEASUREMENTS.

        Returns:
            tuple[float, float]: The ADC measurement average and its standard deviation.
        """
        val = self._send('measure', number_of_measurements=number_of_measurements, arduino_instance=self)
        self._send('complete')
        return val
