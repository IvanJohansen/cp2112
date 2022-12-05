# This is a wrapper for accessing the Totalphase Aardvark device.
# Notice that all pins will be configured as input when connection to the Aardvark terminates.
# It is not possible to read the current state of the output pins.
import os.path
from ctypes import *

# enum AardvarkI2cStatus
AA_I2C_STATUS_OK            = 0
AA_I2C_STATUS_BUS_ERROR     = 1
AA_I2C_STATUS_SLA_ACK       = 2
AA_I2C_STATUS_SLA_NACK      = 3
AA_I2C_STATUS_DATA_NACK     = 4
AA_I2C_STATUS_ARB_LOST      = 5
AA_I2C_STATUS_BUS_LOCKED    = 6
AA_I2C_STATUS_LAST_DATA_ACK = 7

I2C_StatusNames = {
AA_I2C_STATUS_BUS_ERROR:    "A bus error has occurred.",
AA_I2C_STATUS_SLA_ACK:      "Bus arbitration was lost during master transaction.",
AA_I2C_STATUS_SLA_NACK:     "The Aardvark adapter failed to receive acknowledgement for the requested slave address.",
AA_I2C_STATUS_DATA_NACK:    "The last data byte in the transaction was not acknowledged by the slave.",
AA_I2C_STATUS_ARB_LOST:     "Another master device on the bus was accessing the bus simultaneously with this Aardvark adapter.",
AA_I2C_STATUS_BUS_LOCKED:   "An I2C packet is in progress, and the time since the last I2C event executed or received on the bus has exceeded the bus lock timeout.",
AA_I2C_STATUS_LAST_DATA_ACK:"When the Aardvark slave is configured with a fixed length transmit buffer, it will detach itself from the I2C bus after the buffer is fully transmitted.",
}

#GPIO pin masks
AA_GPIO_SCL  = 0x01
AA_GPIO_SDA  = 0x02
AA_GPIO_MISO = 0x04
AA_GPIO_SCK  = 0x08
AA_GPIO_MOSI = 0x10
AA_GPIO_SS   = 0x20

# Configure the device by enabling/disabling I2C, SPI, and
# GPIO functions.
# enum AardvarkConfig
AA_CONFIG_GPIO_ONLY = 0x00
AA_CONFIG_SPI_GPIO  = 0x01
AA_CONFIG_GPIO_I2C  = 0x02
AA_CONFIG_SPI_I2C   = 0x03
AA_CONFIG_QUERY     = 0x80

# Configure the target power pins.
# This is only supported on hardware versions >= 2.00
AA_TARGET_POWER_NONE = 0x00
AA_TARGET_POWER_BOTH = 0x03
AA_TARGET_POWER_QUERY = 0x80

# enum AardvarkI2cFlags
AA_I2C_NO_FLAGS          = 0x00
AA_I2C_10_BIT_ADDR       = 0x01
AA_I2C_COMBINED_FMT      = 0x02
AA_I2C_NO_STOP           = 0x04
AA_I2C_SIZED_READ        = 0x10
AA_I2C_SIZED_READ_EXTRA1 = 0x20

#==========================================================================
# STATUS CODES
#==========================================================================
# All API functions return an integer which is the result of the
# transaction, or a status code if negative.  The status codes are
# defined as follows:
# enum AardvarkStatus
# General codes (0 to -99)
AA_OK                        =    0
AA_UNABLE_TO_LOAD_LIBRARY    =   -1
AA_UNABLE_TO_LOAD_DRIVER     =   -2
AA_UNABLE_TO_LOAD_FUNCTION   =   -3
AA_INCOMPATIBLE_LIBRARY      =   -4
AA_INCOMPATIBLE_DEVICE       =   -5
AA_COMMUNICATION_ERROR       =   -6
AA_UNABLE_TO_OPEN            =   -7
AA_UNABLE_TO_CLOSE           =   -8
AA_INVALID_HANDLE            =   -9
AA_CONFIG_ERROR              =  -10

# I2C codes (-100 to -199)
AA_I2C_NOT_AVAILABLE         = -100
AA_I2C_NOT_ENABLED           = -101
AA_I2C_READ_ERROR            = -102
AA_I2C_WRITE_ERROR           = -103
AA_I2C_SLAVE_BAD_CONFIG      = -104
AA_I2C_SLAVE_READ_ERROR      = -105
AA_I2C_SLAVE_TIMEOUT         = -106
AA_I2C_DROPPED_EXCESS_BYTES  = -107
AA_I2C_BUS_ALREADY_FREE      = -108

# SPI codes (-200 to -299)
AA_SPI_NOT_AVAILABLE         = -200
AA_SPI_NOT_ENABLED           = -201
AA_SPI_WRITE_ERROR           = -202
AA_SPI_SLAVE_READ_ERROR      = -203
AA_SPI_SLAVE_TIMEOUT         = -204
AA_SPI_DROPPED_EXCESS_BYTES  = -205

# GPIO codes (-400 to -499)
AA_GPIO_NOT_AVAILABLE        = -400

# I2C bus monitor codes (-500 to -599)
AA_I2C_MONITOR_NOT_AVAILABLE = -500
AA_I2C_MONITOR_NOT_ENABLED   = -501


aardvark_dll = WinDLL(os.path.dirname(__file__) + "\\aardvark.dll")
aa_open = CFUNCTYPE(c_int, c_int)(("c_aa_open", aardvark_dll))
aa_status_string = CFUNCTYPE(c_char_p, c_int)(("c_aa_status_string", aardvark_dll))
aa_configure = CFUNCTYPE(c_int, c_int, c_int)(("c_aa_configure", aardvark_dll))
aa_i2c_pullup = CFUNCTYPE(c_int, c_int, c_uint8)(("c_aa_i2c_pullup", aardvark_dll))
aa_i2c_bus_timeout = CFUNCTYPE(c_int, c_int, c_uint16)(("c_aa_i2c_bus_timeout", aardvark_dll))
aa_target_power = CFUNCTYPE(c_int, c_int, c_uint8)(("c_aa_target_power", aardvark_dll))
aa_close = CFUNCTYPE(c_int, c_int)(("c_aa_close", aardvark_dll))
aa_gpio_direction = CFUNCTYPE(c_int, c_int, c_uint8)(("c_aa_gpio_direction", aardvark_dll))
aa_gpio_pullup = CFUNCTYPE(c_int, c_int, c_uint8)(("c_aa_gpio_pullup", aardvark_dll))
aa_gpio_get = CFUNCTYPE(c_int, c_int)(("c_aa_gpio_get", aardvark_dll))
aa_gpio_set = CFUNCTYPE(c_int, c_int, c_uint8)(("c_aa_gpio_set", aardvark_dll))
aa_gpio_change = CFUNCTYPE(c_int, c_int, c_uint16)(("c_aa_gpio_change", aardvark_dll))
aa_find_devices_ext = CFUNCTYPE(c_int, c_int, POINTER(c_uint16), c_int, POINTER(c_uint32))(("c_aa_find_devices_ext", aardvark_dll))
aa_i2c_write_read = CFUNCTYPE(c_int, c_int, c_uint16, c_uint, c_uint16, POINTER(c_uint8), POINTER(c_uint16), c_uint16, POINTER(c_uint8), POINTER(c_uint16))(("c_aa_i2c_write_read", aardvark_dll))
aa_i2c_write_ext = CFUNCTYPE(c_int, c_int, c_uint16, c_int, c_uint16, POINTER(c_uint8), POINTER(c_uint16))(("c_aa_i2c_write_ext", aardvark_dll))
aa_i2c_read_ext = CFUNCTYPE(c_int, c_int, c_uint16, c_int, c_uint16, POINTER(c_uint8), POINTER(c_uint16))(("c_aa_i2c_read_ext", aardvark_dll))

class AardvarkError(Exception):
    """Class used for all Aardvark errors."""
    pass

def check_status(status):
    if isinstance(status, int) and status < AA_OK:
        raise AardvarkError(aa_status_string(status))
    return status

class Aardvark:
    def __init__(self, port=0, pull_up=True):
        self.handle = check_status(aa_open(port))
        check_status(aa_configure(self.handle, AA_CONFIG_GPIO_I2C))
        check_status(aa_i2c_pullup(self.handle, pull_up))
        check_status(aa_i2c_bus_timeout(self.handle, 400))
        self.out_port = 0
        
    def __del__(self):
        try:
            aa_close(self.handle)     
        except AttributeError:
            pass
    
    def write_i2c(self, address, tx_data):
        data_out = (c_uint8 * len(tx_data))(*tx_data)
        num_written = c_uint16()
        result = check_status(aa_i2c_write_ext(self.handle, address, AA_I2C_NO_FLAGS, len(tx_data), data_out, num_written))
        if result != AA_I2C_STATUS_OK:
            raise AardvarkError(I2C_StatusNames[result] + " Written=%u" % num_written)
        
    def read_i2c(self, address, rx_size):
        in_data = (c_uint8 * rx_size)()
        num_read = c_uint16()
        result = check_status(aa_i2c_read_ext(self.handle, address, AA_I2C_NO_FLAGS, rx_size, in_data, num_read))
        if result != AA_I2C_STATUS_OK:
            raise AardvarkError(I2C_StatusNames[result] + " Read=%u" % num_read)
        return bytes(in_data)

    def write_read_i2c(self, address, tx_data, rx_size):
        out_data = (c_uint8 * len(tx_data))(*tx_data)
        in_data = (c_uint8 * rx_size)()
        num_written = c_uint16()
        num_read = c_uint16()
        result = check_status(aa_i2c_write_read(self.handle, address, AA_I2C_NO_FLAGS, len(tx_data), out_data, num_written, rx_size, in_data, num_read))        
        if result != AA_I2C_STATUS_OK:
            raise AardvarkError(I2C_StatusNames[result] + " Written=%u, Read=%u" % (num_written.value, num_read.value))        
        return bytes(in_data)
    
    def set_gpio_config(self, dir, pull_up):
        check_status(aa_gpio_direction(self.handle, dir))
        check_status(aa_gpio_pullup(self.handle, pull_up))

    def set_gpio(self, value):
        check_status(aa_gpio_set(self.handle, value))
        self.out_port = value
        
    def get_gpio(self):
        return check_status(aa_gpio_get(self.handle))
        
    def set_pin(self, pin_mask, value):
        if value:
            self.set_gpio(self.out_port | pin_mask)
        else:
            self.set_gpio(self.out_port & ~pin_mask)
        
    def get_pin(self, pin_mask):
        return (self.get_gpio() & pin_mask) != 0

    def set_target_power(self, power):
        aa_target_power(self.handle, AA_TARGET_POWER_BOTH if power else AA_TARGET_POWER_NONE)

    def wait_pin_change(self):
        check_status(aa_gpio_change(self.handle))
    
def enumerate():
    AA_PORT_NOT_FREE = 0x8000
    count = check_status(aa_find_devices_ext(0, None, 0, None))
    if count > 0:
        ports = (c_uint16 * count)()
        serials = (c_uint32 * count)()        
        count2 = check_status(aa_find_devices_ext(count, ports, count, serials))
        assert count2 == count
        return [(ports[i] & ~AA_PORT_NOT_FREE, serials[i], True if ports[i] & AA_PORT_NOT_FREE else False) for i in range(count)]
    return []

if __name__ == '__main__':
    print("Available devices:")
    for (port, serial_number, in_use) in enumerate():
        print("Port %u - serial %04d-%06d (%s)" % (port, serial_number // 1000000, serial_number % 1000000, "In use" if in_use else "Available"))
