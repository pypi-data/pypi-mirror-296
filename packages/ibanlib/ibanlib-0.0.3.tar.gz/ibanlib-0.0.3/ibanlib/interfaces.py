from zope.interface import Interface
from zope.schema import TextLine

class IIntAccount(Interface):
    """ Schema for International Account IntAccount class """
    country = TextLine(
        title="Country", 
        description="Two-letter country ISO-code",
        min_length=2,
        max_length=2,
        required=True)

    bank = TextLine(
        title="Bank", 
        description="Bank code")

    branche = TextLine(
        title="Branche",
        description="Branche code")

    account = TextLine(
        title = "Account number",
        description = "Account number")

    checksum = TextLine(
        title = "Checksum",
        description = "Checksum of account number")

    iban = TextLine(
        title = "IBAN",
        description = "International Bank Account Number")
    
