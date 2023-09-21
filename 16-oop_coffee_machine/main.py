from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

drinks_menu = Menu()
oop_coffee_machine = CoffeeMaker()
money_machine = MoneyMachine()

while True:
    options = drinks_menu.get_items()
    prompt = input(f"What would you like? {options}: ")

    if prompt == "off":
        break
    elif prompt == "report":
        oop_coffee_machine.report()
        money_machine.report()
    elif drinks_menu.find_drink(prompt):
        order = drinks_menu.find_drink(prompt)
        if oop_coffee_machine.is_resource_sufficient(order):
            if money_machine.make_payment(order.cost):
                oop_coffee_machine.make_coffee(order)
            else:
                print("Sorry that's not enough money. Money refunded.")
        else:
            pass
    else:
        pass

