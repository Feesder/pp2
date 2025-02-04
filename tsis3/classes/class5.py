class Account:
    def __init__(self, owner: str, balance: int):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: int):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return

        self.balance += amount
        print('You have successfully topped up your balance')

    def withdraw(self, amount: int):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return

        if self.balance - amount < 0:
            print('You do not have enough funds on your balance')
        else:
            self.balance -= amount
            print('You have successfully withdrawn money')

    def __str__(self):
        return f"Account owner: {self.owner}, Balance: ${self.balance}"

account = Account("Yerdos Yerentalov", 100)

print(account)
account.deposit(50)
account.withdraw(20)
account.withdraw(200)
account.deposit(-10)
account.withdraw(-5)
print(account)