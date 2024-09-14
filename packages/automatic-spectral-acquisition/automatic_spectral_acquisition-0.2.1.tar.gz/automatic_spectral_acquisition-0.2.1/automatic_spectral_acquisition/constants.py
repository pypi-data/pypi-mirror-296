############################# Debug options #############################
DEBUG:bool = False # Changes how exceptions are dealt with.
IGNORE_CONNECTIONS:bool = False # Ignore connections and fakes parts in order to test the program without the hardware.
IGNORE_REQUESTS:bool = False # Ignore requests.

############################# Arduino settings #############################
ARDUINO_BAUDRATE:int = 9600 # Baudrate for the arduino
ARDUINO_TIMEOUT:float = 0.1 # Timeout for the arduino
USE_ADC:bool = True # Use the ADC for measurements instead of the oscilloscope

############################# Arduino commands #############################
GOTO:str = "GOTO" # Send - move motor to position
MEAS:str = "MEAS" # Send - take measurement
DONE:str = "DONE" # Receive - completed request
INVALID:str = "INVALID" # Receive - invalid request
RUNNING:str = "RUNNING" # Receive - motor is moving
STOP:str = "STOP" # Receive - stop button was pressed
ERROR:str = "ERROR" # Receive - error occurred when using ADC

############################# Oscilloscope settings #############################
OSCILLOSCOPE_TIMEOUT:float = 1000 # Timeout for the oscilloscope (ms)
OSCILLOSCOPE_HORIZONTAL_SCALE:float = 100e-3 # Time scale for the oscilloscope
OSCILLOSCOPE_VERTICAL_SCALE:float = 5e-3 # Vertical scale for the oscilloscope
OSCILLOSCOPE_OFFSET:float = 0 # Offset for the oscilloscope
OSCILLOSCOPE_SCALES = [5.e-3, 10.e-3, 20.e-3, 50.e-3, 100.e-3, 200.e-3, 500.e-3, 1000.e-3, 2000.e-3] # List of vertical scales for the oscilloscope

############################# Measurements options #############################
DEFAULT_NUMBER_OF_MEASUREMENTS:int = 3 # Default number of measurements to take for take for each wavelength.
WAVELENGTH_MIN:float = 200 # Minimum wavelength that can be measured.
WAVELENGTH_MAX:float = 1050 # Maximum wavelength that can be measured.
DEFAULT_POSITION:int = 0 # Default position for the motor.
CALIBRATION_POSITIONS:list[int] = [-7194 ,-3597 , 0, 3597, 7194] # Position of wavelengths used for calibration.

############################# File options #############################
OUTPUT_DIRECTORY:str = 'output' # Directory to save the output files.
TEMP_DIRECTORY:str = 'temp' # Directory to save the temporary files.
OUTPUT_FILE:str = 'output_{time}.csv' # Name of the output file. {time} will be replaced by the current time.
TIME_FORMAT:str = '%Y-%m-%d_%H-%M-%S' # Time format for the output file.
LOG_FILE:str = 'log.txt' # Name of the log file.
CONFIG_FILE:str = 'config.pkl' # Name of the configuration file.
if USE_ADC: # Default header for the output file.
    DEFAULT_HEADER:list[str]=['wavelength(nm)', 'voltage(au)', 'uncertainty(au)']
else:
    DEFAULT_HEADER:list[str]=['wavelength(nm)', 'voltage(V)', 'uncertainty(V)']
