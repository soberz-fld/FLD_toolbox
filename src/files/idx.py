import numpy
import struct


def decode_idx(name_of_idx_file) -> numpy.ndarray:
    with open(name_of_idx_file, 'rb') as f:
        # Read the magic number
        z1, z2, value_type_int, dimensions = struct.unpack(">BBBB", f.read(4))  # Format by https://docs.python.org/3.11/library/struct.html and http://yann.lecun.com/exdb/mnist/

        if z1 != 0 or z2 != 0:
            raise ValueError('The given file is not a valid .idx3 file')

        if value_type_int == 0x08:
            value_type = numpy.uint8
        elif value_type_int == 0x09:
            value_type = numpy.int8
        elif value_type_int == 0x0b:
            value_type = numpy.int16
        elif value_type_int == 0x0c:
            value_type = numpy.int32
        elif value_type_int == 0x0d:
            value_type = numpy.float32
        elif value_type_int == 0x0e:
            value_type = numpy.float64
        else:
            raise ValueError('Third bit of the file does not correspond to a valid data type')

        if dimensions < 1:
            raise ValueError('Fourth bit giving number of dimensions is below one')

        dimensions_struct_format = '>'
        for i in range(0, dimensions):
            dimensions_struct_format += 'I'

        # Read the dimensions
        d = struct.unpack(dimensions_struct_format, f.read(4 * dimensions))

        # Read the raw data as a byte array
        raw_values = numpy.fromfile(f, dtype=value_type)

        # Reshape the image data into an array with dimensions given by head of file
        dimensional_data = raw_values.reshape(d)

        return dimensional_data


def store_as_idx(array: numpy.ndarray, name_of_idx_file):
    # Validate the input array
    if not isinstance(array, numpy.ndarray):
        raise ValueError("Input 'array' must be a NumPy array")

    # Validate the dimensions of the input array
    if len(array.shape) == 0:
        raise ValueError("Input 'array' must have at least one dimension")

    # Determine the data type of the input array
    value_type_int = None
    if array.dtype == numpy.uint8:
        value_type_int = 0x08
    elif array.dtype == numpy.int8:
        value_type_int = 0x09
    elif array.dtype == numpy.int16:
        value_type_int = 0x0b
    elif array.dtype == numpy.int32:
        value_type_int = 0x0c
    elif array.dtype == numpy.float32:
        value_type_int = 0x0d
    elif array.dtype == numpy.float64:
        value_type_int = 0x0e
    else:
        raise ValueError("Unsupported data type: {}".format(array.dtype))

    # Get the number of dimensions and dimensions sizes
    dimensions = len(array.shape)
    dimension_sizes = array.shape

    # Open the IDX3 file in binary mode for writing
    with open(name_of_idx_file, 'wb') as f:
        # Write the magic number, value type, and dimensions to the file
        f.write(struct.pack(">BBBB", 0x00, 0x00, value_type_int, dimensions))

        # Write the dimension sizes to the file
        dimensions_struct_format = ">" + "I" * dimensions
        dimension_bytes = struct.pack(dimensions_struct_format, *dimension_sizes)
        f.write(dimension_bytes)

        # Write the array data to the file
        array.tofile(f)
