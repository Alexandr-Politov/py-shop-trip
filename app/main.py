import json

from app.customer import Customer
from app.shop import Shop


with open("config.json", "r") as json_file:
    data_dict = json.load(json_file)

FUEL_PRICE = data_dict["FUEL_PRICE"]

customers = [Customer(*data_dict["customers"][i].values())
             for i in range(len(data_dict["customers"]))]

shops = [Shop(*data_dict["shops"][i].values())
         for i in range(len(data_dict["shops"]))]


def shop_trip() -> None:
    for customer in customers:
        print(f"{customer.name} has {customer.money} dollars")

        min_milk_cost = 0
        min_bread_cost = 0
        min_butter_cost = 0
        min_total_cost = float("inf")
        min_shop = None

        for shop in shops:
            distance = (((shop.location[0] - customer.location[0]) ** 2
                        + (shop.location[1] - customer.location[1]) ** 2)
                        ** 0.5)
            fuel_cost = round((distance * customer.car["fuel_consumption"]
                               / 100 * FUEL_PRICE) * 2, 2)
            milk_cost = (customer.product_cart["milk"]
                         * shop.products["milk"])
            bread_cost = (customer.product_cart["bread"]
                          * shop.products["bread"])
            butter_cost = (customer.product_cart["butter"]
                           * shop.products["butter"])
            total_cost = round(
                fuel_cost + milk_cost + bread_cost + butter_cost, 2
            )

            print(f"{customer.name}'s trip to the "
                  f"{shop.name} costs {total_cost}")

            if total_cost <= min_total_cost:
                min_total_cost = total_cost
                min_milk_cost = milk_cost
                min_bread_cost = bread_cost
                min_butter_cost = butter_cost
                min_shop = shop.name

        if customer.money < min_total_cost:
            print(f"{customer.name} doesn't have enough "
                  f"money to make a purchase in any shop")
        else:
            print(f"{customer.name} rides to {min_shop}\n")
            print("Date: 04/01/2021 12:33:41")
            print(f"Thanks, {customer.name}, for your purchase!")
            print("You have bought:")
            print(f"{customer.product_cart['milk']} "
                  f"milks for {min_milk_cost} dollars")
            print(f"{customer.product_cart['bread']} "
                  f"breads for {int(min_bread_cost)} dollars")
            print(f"{customer.product_cart['butter']} "
                  f"butters for {min_butter_cost} dollars")
            print(f"Total cost is "
                  f"{min_milk_cost + min_bread_cost
                     + min_butter_cost} dollars")
            print("See you again!\n")
            print(f"{customer.name} rides home")
            print(f"{customer.name} now has "
                  f"{customer.money - min_total_cost} dollars\n")
