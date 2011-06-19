'''Data transformation functions.

From bytes to a number, number to bytes, base64-like-encoding, etc.
'''

import math
import types

def bit_size(number):
    """Returns the number of bits required to hold a specific long number"""

    return int(math.ceil(math.log(number,2)))

def bytes2int(bytes):
    """Converts a list of bytes or a string to an integer

    >>> (((128 * 256) + 64) * 256) + 15
    8405007
    >>> l = [128, 64, 15]
    >>> bytes2int(l)              #same as bytes2int('\x80@\x0f')
    8405007
    """

    if not (type(bytes) is types.ListType or type(bytes) is types.StringType):
        raise TypeError("You must pass a string or a list")

    # Convert byte stream to integer
    integer = 0
    for byte in bytes:
        integer *= 256
        if type(byte) is types.StringType: byte = ord(byte)
        integer += byte

    return integer

def int2bytes(number):
    """Converts a number to a string of bytes
    
    >>>int2bytes(123456789)
    '\x07[\xcd\x15'
    >>> bytes2int(int2bytes(123456789))
    123456789
    """

    if not (type(number) is types.LongType or type(number) is types.IntType):
        raise TypeError("You must pass a long or an int")

    string = ""

    while number > 0:
        string = "%s%s" % (chr(number & 0xFF), string)
        number /= 256
    
    return string


def to64(number):
    """Converts a number in the range of 0 to 63 into base 64 digit
    character in the range of '0'-'9', 'A'-'Z', 'a'-'z','-','_'.
    
    >>> to64(10)
    'A'
    """

    if not (type(number) is types.LongType or type(number) is types.IntType):
        raise TypeError("You must pass a long or an int")

    if 0 <= number <= 9:            #00-09 translates to '0' - '9'
        return chr(number + 48)

    if 10 <= number <= 35:
        return chr(number + 55)     #10-35 translates to 'A' - 'Z'

    if 36 <= number <= 61:
        return chr(number + 61)     #36-61 translates to 'a' - 'z'

    if number == 62:                # 62   translates to '-' (minus)
        return chr(45)

    if number == 63:                # 63   translates to '_' (underscore)
        return chr(95)

    raise ValueError(u'Invalid Base64 value: %i' % number)


def from64(number):
    """Converts an ordinal character value in the range of
    0-9,A-Z,a-z,-,_ to a number in the range of 0-63.
    
    >>> from64(49)
    1
    """

    if not (type(number) is types.LongType or type(number) is types.IntType):
        raise TypeError("You must pass a long or an int")

    if 48 <= number <= 57:         #ord('0') - ord('9') translates to 0-9
        return(number - 48)

    if 65 <= number <= 90:         #ord('A') - ord('Z') translates to 10-35
        return(number - 55)

    if 97 <= number <= 122:        #ord('a') - ord('z') translates to 36-61
        return(number - 61)

    if number == 45:               #ord('-') translates to 62
        return(62)

    if number == 95:               #ord('_') translates to 63
        return(63)

    raise ValueError(u'Invalid Base64 value: %i' % number)


def int2str64(number):
    """Converts a number to a string of base64 encoded characters in
    the range of '0'-'9','A'-'Z,'a'-'z','-','_'.
    
    >>> int2str64(123456789)
    '7MyqL'
    """

    if not (type(number) is types.LongType or type(number) is types.IntType):
        raise TypeError("You must pass a long or an int")

    string = ""

    while number > 0:
        string = "%s%s" % (to64(number & 0x3F), string)
        number /= 64

    return string


def str642int(string):
    """Converts a base64 encoded string into an integer.
    The chars of this string in in the range '0'-'9','A'-'Z','a'-'z','-','_'
    
    >>> str642int('7MyqL')
    123456789
    """

    if not (type(string) is types.ListType or type(string) is types.StringType):
        raise TypeError("You must pass a string or a list")

    integer = 0
    for byte in string:
        integer *= 64
        if type(byte) is types.StringType: byte = ord(byte)
        integer += from64(byte)

    return integer
