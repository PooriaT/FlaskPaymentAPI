#Here the related services for the card and payment will be defined
#Importing the required library
import re
from datetime import datetime



# - CreditCardNumber (mandatory, string, it should be a valid credit card number)
# - CardHolder: (mandatory, string)
# - ExpirationDate (mandatory, DateTime, it cannot be in the past)
# - SecurityCode (optional, string, 3 digits)
# - Amount (mandatoy decimal, positive amount)

class CreditCard():
    def __init__(self):
        self.creditCardNumber = None
        self.cardHolder = None
        self.expirationDate = None
        self.securityCode = None
        self.amount = None
        self.cardInfoDic = None

    def  cardValidation(self, **kwargs):

        self.creditCardNumber = kwargs['creditCardNumber']
        self.cardHolder = kwargs['cardHolder']
        self.expirationDate = kwargs['expirationDate']
        self.securityCode = kwargs['securityCode']
        self.amount = kwargs['amount']
        self.cardInfoDic = kwargs

        #Checking the credit card number, 16 numbers only
        if not re.match('^\d{16}$', kwargs['creditCardNumber']):
            print('Invalid Credit card number!')
            return False

        #Checking the card holder, 16 numbers only
        if not type(kwargs['cardHolder']) == str:
            print('Invalid Card Holder')
            return False

        #Checking the Expiry date,
        try:
            today = datetime.now()
            expiryDate = datetime.strptime(kwargs['expirationDate'], '%Y/%m')
            if expiryDate < today:
                print('The card was expired!')
                return False
        except ValueError:
            print('Invalid date input!')
            return False

        #Checking the security code, 3 numbers only
        if not re.match('^\d{3}$', kwargs['securityCode']):
            print('Invalid Security code')
            return False

        #Checking the Amount, Should be decimal and positive
        try:
            if float(kwargs['amount']) < 0:
                print('The amount should be positive!')
                return False
        except ValueError:
            print('Invalid amount')
            return False

        #Otherwise
        return True


# - PremiumPaymentGateway
# - ExpensivePaymentGateway
# - CheapPaymentGateway.
# a) If the amount to be paid is less than £20, use CheapPaymentGateway.
# b) If the amount to be paid is £21-500, use ExpensivePaymentGateway if available.
# Otherwise, retry only once with CheapPaymentGateway.
# c) If the amount is > £500, try only PremiumPaymentGateway and retry up to 3 times
# in case payment does not get processed
class ExternalServices():
    def __init__(self, amount):
        self.amount = amount

    #Checkng the validity of credit card
    def cardVerifying(self, cardInfo):
        if cardInfo == None:
            return False

        return True

    #Method of choosing gateway
    def gatewayType(self, cardInfo):
        print('Welcome To Gateway')
        gateway_stat = None
        times = 0
        if self.amount < 20:
            gateway_stat = 'CheapPaymentGateway'
            times = 1
        elif 21 <= self.amount <= 500:
            gateway_stat = 'ExpensivePaymentGateway'
            times = 2
        elif 500 < self.amount:
            gateway_stat = 'PremiumPaymentGateway'
            times = 3
        else:
            return False

        while times:
            if self.cardVerifying(cardInfo):
                print('Payment is done via ' + gateway_stat + ' service.')
                return True

            times -= 1

        print('Payment process is failed.')
        return False
