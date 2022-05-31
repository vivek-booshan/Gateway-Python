def text2bin(text):
    """
    Converts text to binary string
    """
    binStr = ""
    for letter in text:
        binary = bin(ord(letter))[2:]
        pad    = 8 - len(binary)
        binStr += pad*'0' + binary
    return binStr

def bin2text(binStr):
    """
    Converts binary string to text
    """
    text = ""
    for i in range(0,len(binStr),8):
        text += chr(int(binStr[i:i+8],2))
    return text

def dna2bin(dna):
    binary = []
    for base in dna:
        if base == 'A':
            binary.append('00')
        elif base == 'T':
            binary.append('01')
        elif base == 'C':
            binary.append('10')
        elif base == 'G':
            binary.append('11')
    binStr = ''.join(binary)
    return binStr

def bin2dna(bin):
    bases = []
    basebin = [bin[i:i+2] for i in range(0, len(bin), 2)]
    for i in basebin:
        if i == '00':
            bases.append('A')
        elif i == '01':
            bases.append('T')
        elif i == '10':
            bases.append('C')
        elif i == '11':
            bases.append('G')
    dna = ''.join(bases)
    return dna

def text2dna(text):
    binStr = text2bin(text)
    dnaStr = bin2dna(binStr)
    return dnaStr

def dna2text(text):
    binStr = dna2bin(text)
    textStr = bin2text(binStr)
    return textStr

# dna = 'TAATCG'
# binary = '10001101'
# print(dna2bin(dna), bin2dna(binary))
# text = 'bye'
# print(text2dna(text))
# print(dna2text(text2dna(text)))

if __name__ == "__main__":
    text = input("enter string: ")
    print('\'bye\' is {} in binary and {} in dna'.format(text2bin(text), text2dna(text)))

     
 