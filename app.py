from flask import Flask, jsonify, request
import json
from .payment.paymentservices import CreditCard, ExternalServices

app = Flask(__name__)

@app.route("/processpayment", methods=['POST'])
def payment():
    if request.method == 'POST':
        data = request.get_json()

        # if there is no input is loaded
        if not data:
            return {"status code": 400}, 400


        #Now it is the time to validate
        credit_card = CreditCard()
        try:
            if not credit_card.cardValidation(**data):
                print('Credit Card information is not valid!')
                return {"status code": 400}, 400
        except:
            print("Internal Error related to credit card section")
            return {"status code": 500}, 500


        #Checking hte external payment ExternalServices
        try:
            services = ExternalServices(credit_card.amount)
            payment_type = services.gatewayType(credit_card.cardInfoDic)

            if payment_type:
                return {"status code": 200}, 200

            print('Payment process is failed!!')
            return {"status code": 400}, 400
        except:
            print("Internal Error related to External Payment section")
            return {"status code": 500}, 500

    else:
        return {"status code": 400}, 400

if __name__ == '__main__':
    app.run(debug=True)
