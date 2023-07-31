from abc import ABC, abstractmethod


class Order:

    def __init__(self):
        self.items = []
        self.quantities = []
        self.prices = []
        self.status = "open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        return sum(quantities * prices for quantities, prices in zip(self.quantities, self.prices))


class PaymentProcessor(ABC):

    @abstractmethod
    def pay(self, order):
        pass


class PaymentProcessorSMS(PaymentProcessor):

    @abstractmethod
    def pay(self, order):
        pass

    @abstractmethod
    def auth_sms(self):
        pass


class Authorizer(ABC):

    @abstractmethod
    def is_authorized(self):
        pass


class AuthorizerSMS(Authorizer):

    def __init__(self):
        self.authorized = False

    def is_authorized(self):
        return self.authorized

    def auth_sms(self):
        self.authorized = True


class AuthorizerRobot(Authorizer):

    def __init__(self):
        self.authorized = False

    def is_authorized(self):
        return self.authorized

    def is_not_robot(self):
        self.authorized = True


class DebitPaymentProcessor(PaymentProcessorSMS):

    def __init__(self, security_code, authorizer):
        self.security_code = security_code
        self.is_verified = False
        self.authorizer = authorizer

    def auth_sms(self):
        print(f"Проверка кода безопасности: {self.security_code}")
        self.is_verified = True

    def pay(self, order):
        if not self.is_verified:
            raise Exception('Необходимо авторизоваться по SMS')
        print("Обработка дебетового типа платежа")
        order.status = "paid"


class CreditPaymentProcessor(PaymentProcessor):

    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order):
        print("Обработка кредитного типа платежа")
        print(f"Проверка кода безопасности: {self.security_code}")
        order.status = "paid"


class PayPalPaymentProcessor(PaymentProcessorSMS):

    def __init__(self, email_address, authorizer):
        self.email_address = email_address
        self.is_verified = False
        self.authorizer = authorizer

    def auth_sms(self):
        print(f"Проверка почты: {self.email_address}")
        self.is_verified = True

    def pay(self, order):
        if not self.authorizer.is_authorized():
            raise Exception('Необходимо авторизоваться по SMS')

        print("Обработка платежа при помощи PayPal")
        order.status = "paid"


# Создаем заказ
order = Order()
# Добавляем товары в заказ
order.add_item("Клавиатура", 1, 2500)
order.add_item("SSD", 1, 7500)
order.add_item("USB-кабель", 2, 250)
# Печатаем стоимость заказа
print(order.total_price())
# Оплачиваем заказ
authorizer = AuthorizerSMS()
authorizer.auth_sms()
debit_processor = DebitPaymentProcessor("0372846", authorizer)
debit_processor.pay(order)

# credit_processor = CreditPaymentProcessor("7383903")
# credit_processor.pay(order)

authorizer = AuthorizerRobot()
authorizer.is_not_robot()
paypal_processor = PayPalPaymentProcessor("some@mail.com", authorizer)
paypal_processor.pay(order)
