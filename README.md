## Requirements
This project requires Python to be installed. It should be compatible with Python 2.X.X or Python 3.X.X. I had success on 2.7.1 and 3.4.1 specifically.

## How to Run
Run using an `Input.txt` file

`./main.py Input.txt`

Run using STDIN

`./main.py < Input.txt`

Run unit tests

`./CreditModuleTest.py`


## Assumptions and Implementation
  * If we attempt to CHARGE or CREDIT a non-existent user, command is ignored.
  * CHARGE and CREDIT will apply to the first credit card added by the user (accessed in a dictionary with index 0). This will likely be changed in the future to specify the particular credit card.
  * There is no such thing as negative credit. This is a confusing concept and thus will be disallowed.
  * Negative balance is allowed. You can also charge a negative amount which can be thought of as a "reimbursement" to the customer.
