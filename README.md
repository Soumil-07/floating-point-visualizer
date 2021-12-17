# Floating Point Visualizer

Converts a decimal number into its IEEE 754 representation, optionally showing each step of conversion.

## Example output:

1. Without steps

```
Enter a decimal number: 34.7561

S <--exp--> <---------mantissa--------->
0 1000 0100 000 1011 0000 0110 0011 1111
```

2. With steps:
```
Enter a decimal number: -12.076

Step 1: Convert the decimal number to its binary representation
12.076 = 1100 . 0001 0011 0111 0100 1011 1100

Step 2: Normalize the binary representation of the number.
Sign = 1 (negative)
Exponent (unadjusted) = 3
Mantissa (not normalized) = 1.0100 0001 0011 0111 0100 1011 1100

Step 3: Normalize the mantissa and adjust the exponent.
    To normalize the mantissa, remove the leading 1. (it is assumed) and truncate it to 23 bits.
    Mantissa (normalized) = 100 0001 0011 0111 0100 1011

    To adjust the exponent, add (2^8 - 1) to it.
    Exponent (adjusted) = 130 (1000 0010)

Step 4: Put them all together to get the IEEE754 Single Precision Floating Point representation of a decimal number!
S <--exp--> <---------mantissa--------->
1 1000 0010 100 0001 0011 0111 0100 1011```
