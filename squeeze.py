def squeeze(x):
    if x == 0:
        return b"\x00"
    elif x < 0:
        length = (x.bit_length() + 8) // 8
        data = x.to_bytes(length, 'big', signed=True)
        lengthBytes = (-length).to_bytes(1, 'big', signed=True)
        return lengthBytes + data
    else: # x > 0
        length = (x.bit_length() + 7) // 8
        data = x.to_bytes(length, 'big', signed=False)
        lengthBytes = length.to_bytes(1, 'big', signed=True)
        return lengthBytes + data

def expand(x):
    lengthBytes = x[0:1]
    rest = x[1:]
    length = int.from_bytes(lengthBytes, 'big', signed=True)
    if length < 0:
        length = -length
        data = rest[:length]
        rest = rest[length:]

        y = int.from_bytes(data, 'big', signed=True)
        return y, rest
    else:
        data = rest[:length]
        rest = rest[length:]

        y = int.from_bytes(data, 'big', signed=False)
        return y, rest
