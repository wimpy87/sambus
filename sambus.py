#!/usr/bin/env python3.4
#
#   Copyright 2015 Atle Ravndal
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

__author__   = 'Atle Ravndal'
__email__    = 'atleravndal@gmail.com'
__url__      = 'https://github.com/wimpy87/sambus'
__license__  = 'Apache License, Version 2.0'


import minimalmodbus

minimalmodbus.BAUDRATE = 9600
minimalmodbus.TIMEOUT = 0.2



class SAMbus( minimalmodbus.Instrument ):
	"""Instrument class for System air\Villavent residential units. 
    
    Communicates via Modbus RTU protocol (via RS485), using the :mod:`minimalmodbus` Python module.
    This driver is intended to enable control of the ventilation from the command line.
    Args:
        * portname (str): port name
            * examples:
            * OS X: '/dev/tty.usbserial'
            * Linux: '/dev/ttyUSB0'
            * Windows: '/com3'
            
        * slaveaddress (int): slave address in the range 1 to 247 (in decimal)"""
    
    
    def __init__(self, portname, slaveaddress):
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)




    ## Registers for fan control
  
    def get_fan_lvl(self):
        """Return the fan speed level."""
        return self.read_register(100)
 
 
    def set_fan_lvl(self, value):
        """Sett the fan speed level. value = 1-3"""
        minimalmodbus._checkInt(value, minvalue=1, maxvalue=3, description='fan value')
        self.write_register(100, value)
        return self.read_register(100)


    ## Registers for heater control

    def get_temp_lvl(self):
        """Return the temperatur level."""
        return self.read_register(206)
  
  
    def set_temp_lvl(self, value):
        """sett the temperatur level. value = 0-5"""
        minimalmodbus._checkInt(value, minvalue=0, maxvalue=5, description='temp value')
        self.write_register(206, value)
        return self.read_register(206)


    def get_supply_temp(self):
        """Supply air sensor"""
        return self.read_register(213, 1)


    def get_extr_temp(self):
        """Extract air sensor"""
        return self.read_register(214, 1)


    def get_exha_temp(self):
        """Exhaust air sensor"""
        return self.read_register(215, 1)


    def get_heat_temp(self):
        """Overheat sensor"""
        return self.read_register(216, 1)


    def get_out_temp(self):
        """Outdoor air sensor"""
        return self.read_register(217, 1)


    ## Registers for system parameters

    def get_system_type(self):
        """Check Model name"""
        model_list = ['VR400', 'VR700', 'VR700DK', 'VR400DE', 'VTC300','VTC700',6,7,8,9,10,11,'VTR150K',
                      'VTR200B', 'VSR300', 'VSR500', 'VSR150', 'VTR300', 'VTR500', 'VSR300DE', 'VTC200']
        model = self.read_register(500)
        return model_list[model]


	## Registers for the filter

    def get_filter_day(self):
        """Check days since last filter change"""
        return self.read_register(601)





#inst=('/dev/ttyUSB0', 1)

#inst.debug = True



	########################
	## Testing the module ##
	########################


if __name__ == '__main__':

    print ("TESTING SYSTEMAIR MODBUS MODULE")


    PORTNAME = '/dev/ttyUSB0'
    ADDRESS = 1
    
    print ( 'Port: ' +  str(PORTNAME) + ', Address: ' + str(ADDRESS) )
    
    instr = SAMbus(PORTNAME, ADDRESS)
    
    print ( 'Model                : {0}'.format (instr.get_system_type()))
    print ( 'Last filter change   : {0} Days'.format (instr.get_filter_day()))
    print ( 'Temperatur setting   :   {0}'.format (instr.get_temp_lvl()))
    print ( 'Fan Setting          :   {0}'.format (instr.get_fan_lvl()))
    print ( 'Supply air temp      :  {0}°C'.format (instr.get_supply_temp()))
    print ( 'Extract air temp     :  {0}°C'.format (instr.get_extr_temp()))   
    print ( 'Exhaust air temp     :{0}°C'.format (instr.get_exha_temp()))  
    print ( 'Overheat sensor      :  {0}°C'.format (instr.get_heat_temp()))
    print ( 'Outdoor air          :   {0}°C'.format (instr.get_out_temp()))

    print ('DONE!')

pass
