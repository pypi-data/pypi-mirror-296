"""
Indala26 Decoder
A Python library for decoding 32-bit Indala26 codes into facility code and card numbers, and vice versa

By: Logan Nommensen
"""


def hex_to_bin(hex: str or hex) -> str:
    """
    Converts hex to binary
    :param hex: 4-byte hex string in format "FF:FF:FF:FF"
    :return: 32-bit binary string
    """
    return bin(int(hex.replace(':', ''), 16))[2:].zfill(32)


def bin_to_hex(bin: str or bin) -> str:
    """
    Converts binary to hex
    :param bin: 32-bit binary string
    :return: 4-byte hex string in format "FF:FF:FF:FF"
    """
    if type(bin) == bin:
        bin = str(bin)[2:].zfill(32)
    return ':'.join([hex(int(bin[i:i + 8], 2))[2:].zfill(2).upper() for i in range(0, len(bin), 8)])


def bin_to_dec(bin: str or bin) -> int:
    """
    Converts binary to decimal
    :param bin: 32-bit binary string or bin
    :return: integer the binary represents
    """
    return int(bin, 2)


def bin_to_fc(data: str or bin) -> int:
    """
    Reads a 32-bit binary Indala26 code and returns the facility code
    :param data: 32-bit binary string
    :return: facility code as integer
    """
    fc = 0
    for i in [24, 16, 11, 14, 15, 20, 6, 25]:
        fc = (fc << 1) | int(data[i])
    return fc


def bin_to_cn(data: str or bin) -> int:
    """
    Reads a 32-bit binary Indala26 code and returns the card number
    :param data: 32-bit binary string
    :return: card number as 16-bit integer (from 0 to 65535)
    """
    cn = 0
    for i in [9, 12, 10, 7, 19, 3, 2, 18, 13, 0, 4, 21, 23, 26, 17, 8]:
        cn = (cn << 1) | int(data[i])
    return cn


def bin_to_summary(data: str or bin) -> str:
    """
    Reads a 32-bit binary Indala26 code and returns a string summary of the data
    :param data: 32-bit binary string
    :return: string summary of the data
    """
    fc = bin_to_fc(data)
    cn = bin_to_cn(data)

    wiegand_correct = True
    checksum_correct = True

    fc_and_card = fc << 16 | cn
    checksum = int(data[27]) << 1 | int(data[28])
    even_parity = int(data[1])
    odd_parity = int(data[5])

    # indala checksum
    checksum_sum = 0
    checksum_sum += ((fc_and_card >> 14) & 1)
    checksum_sum += ((fc_and_card >> 12) & 1)
    checksum_sum += ((fc_and_card >> 9) & 1)
    checksum_sum += ((fc_and_card >> 8) & 1)
    checksum_sum += ((fc_and_card >> 6) & 1)
    checksum_sum += ((fc_and_card >> 5) & 1)
    checksum_sum += ((fc_and_card >> 2) & 1)
    checksum_sum += ((fc_and_card >> 0) & 1)
    checksum_sum &= 0b1

    if not (checksum_sum == 1 and checksum == 0b01) and \
            not (checksum_sum == 0 and checksum == 0b10):
        checksum_correct = False

    # wiegand parity
    even_parity_sum = 0
    for i in range(12, 24):
        if ((fc_and_card >> i) & 1) == 1:
            even_parity_sum += 1
    if even_parity_sum % 2 != even_parity:
        wiegand_correct = False

    odd_parity_sum = 1
    for i in range(0, 12):
        if ((fc_and_card >> i) & 1) == 1:
            odd_parity_sum += 1
    if odd_parity_sum % 2 != odd_parity:
        wiegand_correct = False

    return "FC: %u" % fc + "\r\n" + \
        "Card: %u" % cn + "\r\n" + \
        "Checksum: %s" % ("+" if checksum_correct else "-") + "\r\n" + \
        "W26 Parity: %s" % ("+" if wiegand_correct else "-")


def summary_to_bin(fc: int, cn: int) -> str:
    """
    Converts facility code and card number to a 32-bit binary Indala26 code
    :param fc: facility code as a 8-bit integer (from 0 to 255)
    :param cn: card number as a 16-bit integer (from 0 to 65535)
    :return: 32-bit binary string
    """
    card = "" + "0" * 32  # 32 bit binary string

    # facility code
    fc_str = bin(fc)[2:].zfill(8)
    order = [24, 16, 11, 14, 15, 20, 6, 25]
    for i in range(8):
        card = card[:order[i]] + fc_str[i] + card[order[i] + 1:]

    # card number
    cn_str = bin(cn)[2:].zfill(16)
    order = [9, 12, 10, 7, 19, 3, 2, 18, 13, 0, 4, 21, 23, 26, 17, 8]
    for i in range(16):
        card = card[:order[i]] + cn_str[i] + card[order[i] + 1:]

    # wiegand parity
    fc_and_card = fc << 16 | cn  # 32 bit integer
    even_parity_sum = 0
    for i in range(12, 24):
        if ((fc_and_card >> i) & 1) == 1:
            even_parity_sum += 1
    even_parity = even_parity_sum % 2

    card = card[:1] + str(even_parity) + card[2:]

    odd_parity_sum = 1
    for i in range(0, 12):
        if ((fc_and_card >> i) & 1) == 1:
            odd_parity_sum += 1
    odd_parity = odd_parity_sum % 2

    card = card[:5] + str(odd_parity) + card[6:]

    # Indala checksum
    checksum_sum = 0
    order = [14, 12, 9, 8, 6, 5, 2, 0]
    for i in range(8):
        checksum_sum += ((fc_and_card >> order[i]) & 1)
    checksum_sum = checksum_sum & 0b1

    if checksum_sum == 1:
        checksum = "01"
    else:
        checksum = "10"

    card = card[:27] + checksum[0] + card[28:]
    card = card[:28] + checksum[1] + card[29:]

    return card


if __name__ == "__main__":
    print("Raw data to summary (r) or summary to raw data (s)?")
    mode = input()
    if mode == "r":
        print("Enter raw data (binary or hex):")
        raw = input()
        if raw.isalnum():
            print(bin_to_summary(hex_to_bin(raw)))
        else:
            print(bin_to_summary(raw))

    elif mode == "s":
        print("Enter facility code:")
        fc = int(input())
        print("Enter card number:")
        cn = int(input())
        binary = summary_to_bin(fc, cn)
        print(binary, bin_to_hex(binary))
    else:
        print("Invalid input")
