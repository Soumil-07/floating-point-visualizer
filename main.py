from math import floor
from argparse import ArgumentParser

argp = ArgumentParser()
argp.add_argument('-v', action='store_true')

# Prints a binary string by splitting it into groups of 4, and optionally padding it with 0
def prettyPrintBinary(n, pad=False):
    # if the length isn't a multiple of 4, pad it with zeroes to properly group
    if pad:
        mod4 = len(n) % 4
        if (mod4 != 0):
            n = ('0' * (4 - mod4)) + n

    n = n[::-1]
    ret = ""
    for i, digit in enumerate(n, 1):
        ret = digit + ret
        if (i % 4 == 0 and i != len(n)):
            ret = " " + ret
    return ret

# Returns the binary representation of the fractional part of a number (< 1)
def decToBinary(dec):
    result = ''

    # after 24 consecutive binary digits we have to stop counting to fit into the IEEE754 format
    iterations = 0
    while (iterations != 24):
        iterations += 1

        dec = dec * 2
        integralPart = floor(dec)
        result = result + str(integralPart) 

        # get the fractional part
        dec = dec - integralPart
        # if the fractional part is 0, the binary representation is complete!
        if (dec == 0):
            break

    return result

def normalize(wholeBin, decBin):
    exp = 0

    while (wholeBin & 0xffffffff != 0x1):
        exp += 1
        binDigit = wholeBin & 0x1
        decBin = str(binDigit) + decBin
        wholeBin = wholeBin >> 1

    return decBin, exp

def adjustExponent(exp):
    return exp + (2**7 - 1)

def normalizeMantissa(mantissa):
    truncatedMantissa = mantissa[0:23]
    return truncatedMantissa

args = argp.parse_args()
debug = args.v

def printDebug(*args, **kwargs):
    if (debug):
        print(*args, **kwargs)

n = float(input("Enter a decimal number: "))
sign = 1 if n < 0 else 0

# The only difference between a negative and positive floating point number is the sign bit, so we can store it and treat the
# number as positive
n = abs(n)

decBin = decToBinary(n % 1)
wholeBin = floor(n)
printDebug()
printDebug("Step 1: Convert the decimal number to its binary representation")
printDebug("{} = {} . {}".format(n, prettyPrintBinary(format(wholeBin, 'b'), pad=True), prettyPrintBinary(decBin, pad=True)))

mantissa, exp = normalize(wholeBin, decBin)
printDebug()
printDebug("Step 2: Normalize the binary representation of the number.")
printDebug("Sign = {} ({})".format(sign, 'negative' if sign == 1 else 'positive'))
printDebug("Exponent (unadjusted) = {}".format(exp))
printDebug("Mantissa (not normalized) = 1.{}".format(prettyPrintBinary(mantissa, pad=True)))
# print("Mantissa = {}".format(mantissa)
# print("Exp = {:b}".format(exp))

exp = adjustExponent(exp)
mantissa = normalizeMantissa(mantissa)
printDebug()
printDebug("Step 3: Normalize the mantissa and adjust the exponent.")
printDebug("    To normalize the mantissa, remove the leading 1. (it is assumed) and truncate it to 23 bits.")
printDebug("    Mantissa (normalized) = {}".format(prettyPrintBinary(mantissa)))
printDebug()
printDebug("    To adjust the exponent, add (2^8 - 1) to it.")
printDebug("    Exponent (adjusted) = {0} ({1})".format(exp, prettyPrintBinary(format(exp, 'b'))))

print()
printDebug("Step 4: Put them all together to get the IEEE754 Single Precision Floating Point representation of a decimal number!")
print("S <--exp--> <---------mantissa--------->")
print("{sign} {exp} {mantissa}".format(sign=sign, mantissa=prettyPrintBinary(mantissa), exp=prettyPrintBinary(format(exp, 'b'))))

