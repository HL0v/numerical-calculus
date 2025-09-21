import struct

def get_binary(num, precision='single'):
    """Converts a float to its IEEE 754 binary representation."""
    if precision == 'single':
        # Pack as 32-bit float (big-endian)
        packed = struct.pack('>f', num)
        # Unpack as an integer to easily convert to binary
        integer_val = struct.unpack('>I', packed)[0]
        # Format as a 32-bit binary string, zero-padded
        return format(integer_val, '032b')
    elif precision == 'double':
        # Pack as 64-bit float (big-endian)
        packed = struct.pack('>d', num)
        # Unpack as a long long
        integer_val = struct.unpack('>Q', packed)[0]
        # Format as a 64-bit binary string, zero-padded
        return format(integer_val, '064b')
    return ""

def get_float_details(num_str):
    """
    Analyzes a float string and returns its single and double precision
    IEEE 754 representations and details.
    """
    try:
        num = float(num_str)
    except (ValueError, TypeError):
        return None

    # Single Precision (32-bit)
    bin32 = get_binary(num, 'single')
    sign32 = bin32[0]
    exponent32 = bin32[1:9]
    mantissa32 = bin32[9:]
    reconstructed32 = struct.unpack('>f', struct.pack('>I', int(bin32, 2)))[0]

    # Double Precision (64-bit)
    bin64 = get_binary(num, 'double')
    sign64 = bin64[0]
    exponent64 = bin64[1:12]
    mantissa64 = bin64[12:]
    reconstructed64 = struct.unpack('>d', struct.pack('>Q', int(bin64, 2)))[0]

    return {
        "single": {
            "sign": sign32,
            "exponent": exponent32,
            "mantissa": mantissa32,
            "reconstructed": reconstructed32
        },
        "double": {
            "sign": sign64,
            "exponent": exponent64,
            "mantissa": mantissa64,
            "reconstructed": reconstructed64
        }
    }