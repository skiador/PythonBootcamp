from data import MENU

profit = 0
resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}


def user_prompt():
    request = input("What would you like? (espresso/latte/cappuccino): ")
    return request


def print_report():
    for key, value in resources.items():
        if key != "coffee":
            print(f"{key.title()}: {value}ml")
        else:
            print(f"{key.title()}: {value}g")

    print(f"Money: {profit}€")


def enough_resources(chosen_drink):
    ingredients = MENU[chosen_drink]["ingredients"]
    missing_ingredients = []
    for resource in ingredients:
        if resources[resource] < MENU[chosen_drink]["ingredients"][resource]:
            missing_ingredients.append(resource)
            return False, missing_ingredients
    return True, None


def process_payment(drink):
    global profit

    def process_coins():
        quarters = int(input("How many quarters?: "))
        nickles = int(input("How many nickles?: "))
        dimes = int(input("How many dimes?: "))
        pennies = int(input("How many pennies?: "))
        amount_inserted = quarters * 0.25 + nickles * 0.05 + dimes * 0.1 + pennies * 0.01
        return amount_inserted

    amount_paid = process_coins()
    if amount_paid < MENU[drink]["cost"]:
        print("Sorry that's not enough money. Money refunded.")
        return False
    elif amount_paid == MENU[drink]["cost"]:
        print("Payment processed")
        profit += amount_paid
        return True
    else:
        change = round(amount_paid - MENU[drink]["cost"], 2)
        profit += MENU[drink]["cost"]
        print(f"Here is {change}€ in change")
        return True


def make_coffee(drink):
    ingredients = MENU[drink]["ingredients"]
    for resource in ingredients:
        resources[resource] -= MENU[drink]["ingredients"][resource]
    print(f"Here's your {drink}. Enjoy!")


machine_on = True

while machine_on:
    prompt = user_prompt()
    if prompt == "report":
        print_report()
    elif prompt == "off":
        machine_on = False
    elif prompt in MENU.keys():
        is_enough, missing_ingredients = enough_resources(prompt)
        if not is_enough:
            print(f"Sorry, right now we do not have enough of {missing_ingredients} to prepare your drink.")
        else:
            if process_payment(prompt):
                make_coffee(prompt)
            else:
                pass
    else:
        print("Enter a valid drink. Try again.")






