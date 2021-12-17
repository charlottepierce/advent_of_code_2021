class Packet(object):
    def __init__(self, packet_version):
        self.packet_version = packet_version


class LiteralValuePacket(Packet):
    def __init__(self, packet_version, value):
        super().__init__(packet_version)
        self.value = value

    def evaluate(self):
        return self.value

    def __str__(self, depth):
        return "-" * depth + " literal value = " + str(self.value)


class OperatorPacket(Packet):
    def __init__(self, packet_version, packet_type):
        super().__init__(packet_version)
        self.subpackets = []
        self.packet_type = packet_type

    def evaluate(self):
        if self.packet_type == 0:
            return sum([sp.evaluate() for sp in self.subpackets])
        elif self.packet_type == 1:
            product = self.subpackets[0].evaluate()
            for x in range(1, len(self.subpackets)):
                product *= self.subpackets[x].evaluate()
            return product
        elif self.packet_type == 2:
            return min([sp.evaluate() for sp in self.subpackets])
        elif self.packet_type == 3:
            return max([sp.evaluate() for sp in self.subpackets])
        elif self.packet_type == 5:
            return 1 if self.subpackets[0].evaluate() > self.subpackets[1].evaluate() else 0
        elif self.packet_type == 6:
            return 1 if self.subpackets[0].evaluate() < self.subpackets[1].evaluate() else 0
        elif self.packet_type == 7:
            return 1 if self.subpackets[0].evaluate() == self.subpackets[1].evaluate() else 0

    def __str__(self, depth):
        s = "-" * depth + "Operator with type: " + str(self.packet_type) + "\n"
        for sp in self.subpackets:
            s += sp.__str__(depth + 1) + "\n"
        return s


def read_literal_value(binary_input, packet_version):
    total_number_bits_read = 0
    last_digit = False
    number_in_binary = ""
    while not last_digit:
        if binary_input[0] == "0":
            last_digit = True
        number_in_binary += binary_input[1:5]
        binary_input = binary_input[5:]
        total_number_bits_read += 5

    packet_read = LiteralValuePacket(packet_version, int(number_in_binary, base=2))

    return binary_input, total_number_bits_read, packet_read


def read_operator_value(binary_input, packet_version, packet_type_id):
    packet_read = OperatorPacket(packet_version, packet_type_id)

    length_type_id = binary_input[0]
    binary_input = binary_input[1:]
    total_number_bits_read = 1

    if length_type_id == "0":
        total_length_of_subpackets = int(binary_input[0:15], base=2)
        binary_input = binary_input[15:]
        total_number_bits_read += 15
        subpacket_bits_read = 0
        while subpacket_bits_read < total_length_of_subpackets:
            binary_input, bits_read_this_packet, subpacket = read_packet(binary_input)
            subpacket_bits_read += bits_read_this_packet
            packet_read.subpackets.append(subpacket)
        total_number_bits_read += subpacket_bits_read
    else:
        number_of_subpackets = int(binary_input[0:11], base=2)
        binary_input = binary_input[11:]
        total_number_bits_read += 11
        for x in range(number_of_subpackets):
            binary_input, num_bits_read, subpacket = read_packet(binary_input)
            total_number_bits_read += num_bits_read
            packet_read.subpackets.append(subpacket)

    return binary_input, total_number_bits_read, packet_read


def read_packet(binary_input):
    packet_version = binary_input[0:3]
    packet_version = int(packet_version, base=2)
    binary_input = binary_input[3:]

    packet_type_id = binary_input[0:3]
    packet_type_id = int(packet_type_id, base=2)
    binary_input = binary_input[3:]

    total_number_bits_read = 6

    if packet_type_id == 4:
        binary_input, number_bits_read, packet_read = read_literal_value(binary_input, packet_version)
        total_number_bits_read += number_bits_read
    else:
        binary_input, number_bits_read, packet_read = read_operator_value(binary_input, packet_version, packet_type_id)
        total_number_bits_read += number_bits_read

    return binary_input, total_number_bits_read, packet_read


def part_two(binary_input):
    binary_input, total_number_bits_read, packet_read = read_packet(binary_input)
    print("Packet read:")
    print(packet_read.__str__(0))

    return packet_read.evaluate()


def part_one(binary_input):
    binary_input, total_number_bits_read, packet_read = read_packet(binary_input)
    print("Packet read:")
    print(packet_read.__str__(0))

    version_num_total = 0
    packets = [packet_read]
    while len(packets) > 0:
        p = packets.pop()
        version_num_total += p.packet_version
        if isinstance(p, OperatorPacket):
            packets.extend(p.subpackets)

    return version_num_total


if __name__ == "__main__":
    f = open("input.txt")
    hex_code = f.readline().strip()
    f.close()

    binary_input = ""
    for c in hex_code:
        int_value = int(c, base=16)
        binary_input += bin(int_value)[2:].zfill(4)

    # print(part_one(binary_input))
    print(part_two(binary_input))