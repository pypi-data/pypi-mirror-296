import logging
import pyvisa
from retry.api import retry_call


class KeySightPsuE36154A:
    """
    ``Base class for the Keysight E36154A PSU``
    """
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.resource_manager = None
        self.keysight_psu = None
        self.max_tries = 5

    def open_connection(self, open_timeout = 5000):
        """
        ``Opens a TCP/IP connection to the Keysight E36154A PSU``\n
        """
        self.resource_manager = pyvisa.ResourceManager()
        try:
            logging.info(f": Opening PSU Resource at {self.connection_string}")
            self.keysight_psu = retry_call(self.resource_manager.open_resource,
                                           fargs=[self.connection_string], 
                                           fkwargs={"open_timeout":open_timeout},
                                           tries=self.max_tries)
            self.keysight_psu.read_termination = '\n'
            self.keysight_psu.write_termination = '\n'
        except Exception as e:
            raise Exception(f": ERROR {e}: Could not open Resource\n")

    def close_connection(self):
        """
        ``Closes the TCP/IP connection to the Keysight E36154A PSU``\n
        """
        self.resource_manager.close()

    def factory_reset(self):
        """
        ``This function helps factory reset the Keysight E36154A PSU``\n
        """
        # System reset
        retry_call(self.keysight_psu.write,
                                           fargs=[f'*RST'],
                                           tries=self.max_tries)

    def selftest(self):
        """
        ``This function self tests the Keysight E36154A PSU``\n
        """
        try:
            test = self.keysight_psu.query(f'*TST?')
            if test == "+0":
                logging.info(f"PASS")
                return True
            else:
                err = self.keysight_psu.query(f'SYST:ERR?')
                return err
        except Exception as e:
            logging.info(f"ERROR: Cannot run Selftest: {e}")

    def id_number(self):
        """
        ``This function returns the ID number of the Keysight E36154A PSU``\n
        """
        self.keysight_psu.write('*IDN?')
        idn = self.keysight_psu.read()
        logging.info(f': *IDN? returned: {idn}')
        return str(idn)

    def set_voltage(self, voltage):
        """
        ``Sets voltage output for E36154A PSU``\n
        :param voltage: `float` : in Volts\n
        :return: None
        """
        try:
            retry_call(self.keysight_psu.write,
                       fargs=[f'VOLT {voltage}'],
                       tries=self.max_tries)
        except Exception as e:
            raise Exception(f": {e} Could not set Voltage")

    def set_current(self, current):
        """
        ``Sets current output for E36154A PSU``\n
        :param current: `float`: in Amps\n
        :return: None
        """
        try:
            retry_call(self.keysight_psu.write,
                       fargs=[f'CURR {current}'],
                       tries=self.max_tries)
        except Exception as e:
            raise Exception(f": {e} Could not set Current")

    def output_state_on(self):
        """
        ``This command control the output power-on function.``\n
        """
        try:
            retry_call(self.keysight_psu.write,
                       fargs=[f'OUTP ON'],
                       tries=self.max_tries)
            logging.info(f"Output ON")
        except Exception as e:
            raise Exception(f": {e} Could not switch ON Output")

    def output_state_off(self):
        """
        ``This command control the output power-off function.``\n
        """
        try:
            retry_call(self.keysight_psu.write,
                       fargs=[f'OUTP OFF'],
                       tries=self.max_tries)
            logging.info(f"Output OFF")
        except Exception as e:
            raise Exception(f": {e} Could not switch OFF Output")

    def check_output_state(self):
        """
        ``This command control the output, power-on function.``\n
        :return: `int` : "0" (OFF) or "1" (ON)\n
        """
        try:
            op_state = retry_call(self.keysight_psu.query,
                       fargs=[f'OUTP?'],
                       tries=self.max_tries)
            logging.info(f": Output: {op_state}")
            return op_state
        except Exception as e:
            raise Exception(f": {e} Could not check Output state")

    def check_voltage(self):
        """
        ``Checks the set voltage for E36154A PSU``\n
        :return: `float` : voltage in Volts\n
        """
        try:
            psu_volt = retry_call(self.keysight_psu.query,
                       fargs=[f'VOLT?'],
                       tries=self.max_tries)
            logging.info(f": Set Voltage: {psu_volt} V")
            return float(psu_volt)
        except Exception as e:
            raise Exception(f": {e} Could not check Voltage measurement")

    def check_current(self):
        """
        ``Checks the set current for E36154A PSU``\n
        :return: `float` : current in Amps
        """
        try:
            psu_curr = retry_call(self.keysight_psu.query,
                       fargs=[f'CURR?'],
                       tries=self.max_tries)
            logging.info(f": Set Current: {psu_curr} A")
            return float(psu_curr)
        except Exception as e:
            raise Exception(f": {e} Could not check Current measurement")

    def measure_voltage(self):
        """
        ``Measures output voltage for E36154A PSU``\n
        :return: `float` : voltage in Volts
        """
        try:
            psu_volt = retry_call(self.keysight_psu.query,
                       fargs=[f'MEAS:VOLT?'],
                       tries=self.max_tries)
            logging.info(f": Voltage measurement: {psu_volt} V")
            return float(psu_volt)
        except Exception as e:
            raise Exception(f": {e} Could not get Voltage measurement")

    def measure_current(self):
        """
        ``Measures output current for E36154A PSU``\n
        :return: `float` : current in Amps
        """
        try:
            psu_curr = retry_call(self.keysight_psu.query,
                       fargs=[f'MEAS:CURR?'],
                       tries=self.max_tries)
            logging.info(f": Current measurement: {psu_curr} A")
            return float(psu_curr)
        except Exception as e:
            raise Exception(f": {e} Could not get Current measurement")

    def check_min_max_voltage(self):
        """
        ``Check the minimum and maximum voltage range``\n
        :return: `Tuple`: Voltage in Volts
        """
        try:
            min_volt = retry_call(self.keysight_psu.query,
                       fargs=[f'VOLT? MIN'],
                       tries=self.max_tries)
            max_volt = retry_call(self.keysight_psu.query,
                       fargs=[f'VOLT? MAX'],
                       tries=self.max_tries)
            logging.info(f": Min, Max voltage range: {float(min_volt), float(max_volt)} V")
            return float(min_volt), float(max_volt)
        except Exception as e:
            raise Exception(f": {e} Could not get Voltage measurement")

    def check_min_max_current(self):
        """
        ``Check the minimum and maximum current range``\n
        :return: `Tuple`: Current in Amps
        """
        try:
            min_curr = retry_call(self.keysight_psu.query,
                       fargs=[f'CURR? MIN'],
                       tries=self.max_tries)
            max_curr = retry_call(self.keysight_psu.query,
                       fargs=[f'CURR? MAX'],
                       tries=self.max_tries)
            logging.info(f": Min, Max current range: {float(min_curr), float(max_curr)} A")
            return float(min_curr), float(max_curr)
        except Exception as e:
            raise Exception(f": {e} Could not get Current measurement")
