#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.CRITICAL)

logging.debug('Start of program')

variable = "var"

# print the variable with logging
logging.debug("Variable value: {}".format(variable))
print("Program doing regular stuff...")
print("Now its over...")

logging.debug("End of program")
