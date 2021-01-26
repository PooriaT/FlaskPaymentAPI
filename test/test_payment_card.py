import unittest
import json
import requests

url = 'http://127.0.0.1:5000/processpayment'

class ClockTest(unittest.TestCase):
    #Checking the status of url
    def test_url(self):
        response = requests.get(url)

        self.assertEqual(response.status_code, 405)

    #Checking the status with not importing any card information
    def test_emptyInput(self):
        card_info = {}
        response = requests.post(
                                 url,
                                 data=json.dumps(card_info),
                                 headers={"Content-Type": "application/json"})
        self.assertEqual(response.status_code, 400)

    #Checking the status with importing wrong card information
    def test_invalidInput(self):
        #Invalid Amount
        card_info1 = {"creditCardNumber": "1234567890123456", "cardHolder": "Pooria T",
                      "expirationDate": "2021/10", "securityCode": "123", "amount": -10}

        #Invalid Card Number
        card_info2 = {"creditCardNumber": "12345we890123456", "cardHolder": "Pooria T",
                      "expirationDate": "2021/10", "securityCode": "123", "amount": 100}

        #Expired Card
        card_info3 = {"creditCardNumber": "1234567890123456", "cardHolder": "Pooria T",
                      "expirationDate": "2020/10", "securityCode": "123", "amount": 200}

        response1 = requests.post(
                                 url,
                                 data=json.dumps(card_info1),
                                 headers={"Content-Type": "application/json"})
        response2 = requests.post(
                                 url,
                                 data=json.dumps(card_info2),
                                 headers={"Content-Type": "application/json"})
        response3 = requests.post(
                                 url,
                                 data=json.dumps(card_info3),
                                 headers={"Content-Type": "application/json"})


        self.assertEqual(response1.status_code, 400)
        self.assertEqual(response2.status_code, 400)
        self.assertEqual(response3.status_code, 400)

    #Checking the status with importing correct card information
    def test_payment(self):
        card_info1 = {"creditCardNumber": "1234567890123456", "cardHolder": "Pooria T",
                      "expirationDate": "2021/10", "securityCode": "123", "amount": 550}

        response1 = requests.post(
                                 url,
                                 data=json.dumps(card_info1),
                                 headers={"Content-Type": "application/json"})
        self.assertEqual(response1.status_code, 200)



if __name__ == '__main__':
    unittest.main()
