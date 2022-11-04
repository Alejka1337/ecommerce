from shop.settings import LIQPAY_PUBLIC_KEY, LIQPAY_PRIVATE_KEY
import base64
import hashlib
import json
import requests
import random


class LiqpayChekout():

    order_id = None

    def __init__(self, total=None):
        self.total = total
        self.order_id = self.generate_random_order_id()

    @staticmethod
    def generate_random_order_id():
        order_id = random.getrandbits(99)
        return order_id

    def get_order_id(self):
        return self.order_id

    def set_order_id(self):
        LiqpayChekout.order_id = self.order_id
        return

    def create_param_checkout(self):
        param = {"public_key": LIQPAY_PUBLIC_KEY,
                 "version": 3,
                 "action": "pay",
                 "amount": f"{self.total}",
                 "currency": "UAH",
                 "description": "buy in test shop",
                 "order_id": f"{self.order_id}",
                 "language": "ru",
                 "result_url": "http://127.0.0.1:8000/orders/thanks/",
                 }

        json_string = json.dumps(param)
        data = base64.b64encode(json_string.encode())
        sigh_string = LIQPAY_PRIVATE_KEY + f"{data}"[2:-1] + LIQPAY_PRIVATE_KEY
        signature = base64.standard_b64encode(hashlib.sha1(sigh_string.encode()).digest())
        return [f'{data}'[2:-1], f'{signature}'[2:-1]]


class LiqpayCallback(LiqpayChekout):

    def __init__(self):
        self.order_id = LiqpayChekout.order_id

    def create_param_callback(self):
        param = {
            "version": 3,
            "action": "status",
            "public_key": LIQPAY_PUBLIC_KEY,
            "order_id": self.order_id,
        }

        json_string = json.dumps(param)
        data = base64.b64encode(json_string.encode())
        sigh_string = LIQPAY_PRIVATE_KEY + f"{data}"[2:-1] + LIQPAY_PRIVATE_KEY
        signature = base64.standard_b64encode(hashlib.sha1(sigh_string.encode()).digest())
        return [f'{data}'[2:-1], f'{signature}'[2:-1]]

    def send_request(self):
        order_info = {"data": self.create_param_callback()[0], "signature": self.create_param_callback()[1]}
        res = requests.post('https://www.liqpay.ua/api/request', data=order_info)
        return res.content

    def get_response_status(self, response_str):
        json_obj = json.loads(response_str)
        return json_obj['status']