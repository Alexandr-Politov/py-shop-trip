from decimal import Decimal, ROUND_HALF_UP
import json

from app.customer import Customer
from app.shop import Shop


with open("app/config.json", "r") as json_file:
    data_dict = json.load(json_file)

FUEL_PRICE = Decimal(data_dict["FUEL_PRICE"])

customers = [Customer(*data_dict["customers"][i].values())
             for i in range(len(data_dict["customers"]))]

shops = [Shop(*data_dict["shops"][i].values())
         for i in range(len(data_dict["shops"]))]


def shop_trip() -> None:
    for customer in customers:
        print(f"{customer.name} has {customer.money} dollars")

        min_milk_cost = Decimal("0")
        min_bread_cost = Decimal("0")
        min_butter_cost = Decimal("0")
        min_total_cost = Decimal("Infinity")
        min_shop = None

        for shop in shops:
            distance = Decimal((((shop.location[0] - customer.location[0]) ** 2
                                 + (shop.location[1]
                                    - customer.location[1]) ** 2) ** 0.5))
            fuel_cost = (distance * Decimal(customer.car["fuel_consumption"])
                         / Decimal("100") * FUEL_PRICE) * 2
            milk_cost = (Decimal(str(customer.product_cart["milk"]))
                         * Decimal(str(shop.products["milk"])))
            bread_cost = (Decimal(str(customer.product_cart["bread"]))
                          * Decimal(str(shop.products["bread"])))
            butter_cost = (Decimal(str(customer.product_cart["butter"]))
                           * Decimal(str(shop.products["butter"])))
            total_cost = fuel_cost + milk_cost + bread_cost + butter_cost
            total_cost = total_cost.quantize(Decimal("0.01"),
                                             rounding=ROUND_HALF_UP)

            print(f"{customer.name}'s trip to "
                  f"the {shop.name} costs {total_cost}")

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
            print(f"""{customer.name} rides to {min_shop}\n
Date: 04/01/2021 12:33:41
Thanks, {customer.name}, for your purchase!
You have bought:
{customer.product_cart["milk"]} milks for {min_milk_cost} dollars
{customer.product_cart["bread"]} breads for {int(min_bread_cost)} dollars
{customer.product_cart["butter"]} butters for {min_butter_cost} dollars
Total cost is {min_milk_cost + min_bread_cost + min_butter_cost} dollars
See you again!\n\n{customer.name} rides home
{customer.name} now has {customer.money - min_total_cost} dollars\n""")
