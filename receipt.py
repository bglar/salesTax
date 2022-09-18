import json
import logging
from decimal import Decimal
from math import ceil


logger = logging.getLogger(__name__)

BASIC_TAX_RATE = float(10 / 100)
IMPORT_TAX_RATE = float(5 / 100)

# A non-exhaustive set of products to exempt from basic tax based on test data.
# NOTE: ASSUMPTION MADE:
# I could only work with the data given thus I made the following assumptions
# a) Non-Taxable products have atleast one of the following words `
#           book`, `chocolate`, `food`, `medicine`, `drug`, `pill`
# b) Imported goods have the word `import` in the product description.

BASIC_TAX_EXEMPTION_SET = {
    # Books
    "book",
    # Food
    "chocolate",
    "food",
    # medical products
    "medicine",
    "drug",
    "pill"
}

IMPORTED_GOODS_KEY_WORD = "import"


class Receipt:
    """Class takes a list of item lines and output a receipt print out

    Usage
    -----

    receipt_obj = Receipt()
    data = [
        "1 book at 12.49",
        "1 music CD at 14.99",
        "1 chocolate bar at 0.85"
    ]
    receipt_obj.calculate_product_cost(data)

    """

    def __init__(
        self,
        basic_tax_rate: float = BASIC_TAX_RATE,
        import_tax_rate: float = IMPORT_TAX_RATE
    ):
        self.BASIC_TAX_RATE = basic_tax_rate
        self.IMPORT_TAX_RATE = import_tax_rate

    def round_up(self, value: float, to_nearest: float) -> float:
        value = Decimal(value)
        to_nearest = Decimal(to_nearest)
        rounded_val = round(float(ceil(value / to_nearest) * to_nearest), 2)
        return rounded_val

    def get_basic_sales_tax(self, price: float) -> float:
        tax_amount = price * self.BASIC_TAX_RATE
        return tax_amount

    def get_importation_tax(self, price: float) -> float:
        importation_tax = price * self.IMPORT_TAX_RATE
        return importation_tax

    def get_product_name_and_cost(self, product_desc: str) -> tuple[str, float]:
        product_parts = product_desc.split(" ")
        price = float(product_parts[-1])
        name = " ".join(product_parts[:-2])
        return name, price

    def is_tax_exempt_product(self, product_name: str) -> bool:
        for exempt_key_word in BASIC_TAX_EXEMPTION_SET:
            if exempt_key_word in product_name:
                return True
        return False

    def is_imported(self, product_name: str) -> bool:
        if IMPORTED_GOODS_KEY_WORD in product_name:
            return True
        return False

    def print_receipt(self, receipt_lines: list) -> None:
        """This is split out so that in the future if we need to format the receipt, only this function is changed."""
        print(*receipt_lines, sep="\n")

    def calculate_product_cost(self, products: list):
        """ Calculates product tax adds it to the original price."""
        total_price = 0.0
        total_tax = 0.0
        print_lines = []

        # Iterate over all products in a basket
        for product in products:
            base_tax = 0.0
            import_tax = 0.0
            name, price = self.get_product_name_and_cost(product)

            # Check if product is tax exempted, and apply basic sales tax if not.
            if not self.is_tax_exempt_product(product_name=name):
                base_tax = self.get_basic_sales_tax(price=price)

            # Check if product is imported and apply import duty tax
            if self.is_imported(product_name=name):
                import_tax = self.get_importation_tax(price=price)

            # Round to the nearest 0.05 and sum up original price and tax
            product_final_tax = self.round_up(base_tax + import_tax, 0.05)
            product_final_price = price + product_final_tax

            # Increment the final_total_price and final_total_tax as we iterate over each product.
            total_price += product_final_price
            total_tax += product_final_tax

            product_out = ("{}: {:.2f}".format(name, product_final_price))
            print_lines.append(product_out)
            logger.info(product_out)

        total_tax_out = ("Sales Taxes: {:.2f}".format(total_tax))
        logger.info(total_tax_out)
        print_lines.append(total_tax_out)

        total_price_out = ("Total: {:.2f}\n".format(total_price))
        logger.info(total_price_out)
        print_lines.append(total_price_out)

        self.print_receipt(print_lines)


def supplied_data() -> dict:
    """Gets data from data.json file."""
    with open("data.json", "r") as data_file:
        data = json.load(data_file)
    return data


if __name__ == "__main__":
    receipt_obj = Receipt()
    baskets = supplied_data()
    for basket in baskets.values():
        # Example basket value is a list of strings
        # [
        #     "1 book at 12.49",
        #     "1 music CD at 14.99",
        #     "1 chocolate bar at 0.85"
        # ]
        receipt_obj.calculate_product_cost(basket)
