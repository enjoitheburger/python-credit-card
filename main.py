#!/usr/bin/python
import sys
import fileinput
import CreditModule

if len(sys.argv[1:]) == 0:
    # If no arguments, simply exit.
    exit()

try:
    credit_system = CreditModule.CreditSystem()
    for line in fileinput.input():
        words = line.split()
        creditCommand = words[0].lower()
        if creditCommand == "add":
            credit_system.add(words[1], words[2], words[3])
        elif creditCommand == "charge":
            credit_system.charge(words[1], words[2])
        elif creditCommand == "credit":
            credit_system.credit(words[1], words[2])

    credit_system.print_customer_accounts()
except IOError as e:
    print("I/O error({0}): {1}".format(e.errno, e.strerror))

fileinput.close()





