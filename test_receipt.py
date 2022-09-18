from unittest import mock, TestCase

from receipt import Receipt


class TestReceipt(TestCase):
    """Simple unit test for receipt class methods."""

    receipt_obj = Receipt()

    def test_product_is_imported(self):
        data_val = "1 book at 12.49"
        assert self.receipt_obj.is_imported(data_val) is False

        data_val = "1 music CD at 14.99"
        assert self.receipt_obj.is_imported(data_val) is False

        data_val = "1 chocolate bar at 0.85"
        assert self.receipt_obj.is_imported(data_val) is False

        data_val = "1 imported box of chocolates at 10.00"
        assert self.receipt_obj.is_imported(data_val) is True

        data_val = "1 imported bottle of perfume at 47.50"
        assert self.receipt_obj.is_imported(data_val) is True

        data_val = "1 imported bottle of perfume at 27.99"
        assert self.receipt_obj.is_imported(data_val) is True

        data_val = "1 bottle of perfume at 18.99"
        assert self.receipt_obj.is_imported(data_val) is False

        data_val = "1 packet of headache pills at 9.75"
        assert self.receipt_obj.is_imported(data_val) is False

        data_val = "1 box of imported chocolates at 11.25"
        assert self.receipt_obj.is_imported(data_val) is True

    def test_product_is_exempt_from_basic_tax(self):
        data_val = "1 book at 12.49"
        assert self.receipt_obj.is_tax_exempt_product(data_val) is True

        data_val = "1 music CD at 14.99"
        assert self.receipt_obj.is_tax_exempt_product(data_val) is False

        data_val = "1 chocolate bar at 0.85"
        assert self.receipt_obj.is_tax_exempt_product(data_val) is True

        data_val = "1 imported box of chocolates at 10.00"
        assert self.receipt_obj.is_tax_exempt_product(data_val) is True

        data_val = "1 imported bottle of perfume at 47.50"
        assert self.receipt_obj.is_tax_exempt_product(data_val) is False

        data_val = "1 imported bottle of perfume at 27.99"
        assert self.receipt_obj.is_tax_exempt_product(data_val) is False

        data_val = "1 bottle of perfume at 18.99"
        assert self.receipt_obj.is_tax_exempt_product(data_val) is False

        data_val = "1 packet of headache pills at 9.75"
        assert self.receipt_obj.is_tax_exempt_product(data_val) is True

        data_val = "1 box of imported chocolates at 11.25"
        assert self.receipt_obj.is_tax_exempt_product(data_val) is True

    def test_rounding_to_nearest_005(self):
        assert self.receipt_obj.round_up(10.99, 0.05) == 11.0

    def test_get_product_name_and_cost(self):
        data_val = "1 book at 12.49"
        resp = self.receipt_obj.get_product_name_and_cost(data_val)
        assert resp == ("1 book", float(12.49))

        data_val = "1 music CD at 14.99"
        resp = self.receipt_obj.get_product_name_and_cost(data_val)
        assert resp == ("1 music CD", float(14.99))

        data_val = "1 chocolate bar at 0.85"
        resp = self.receipt_obj.get_product_name_and_cost(data_val)
        assert resp == ("1 chocolate bar", float(0.85))

    @mock.patch("receipt.logger")
    @mock.patch("receipt.Receipt.print_receipt", mock.MagicMock)  # Avoid printing out while running tests
    def test_the_receipt_print_out_is_accurate(self, mock_logger):
        data_val = [
            "1 book at 12.49",
            "1 music CD at 14.99",
            "1 chocolate bar at 0.85"
        ]
        self.receipt_obj.calculate_product_cost(data_val)
        mock_logger.info.assert_called_with('Total: 29.83\n')

        data_val = [
            "1 imported box of chocolates at 10.00",
            "1 imported bottle of perfume at 47.50"
        ]
        self.receipt_obj.calculate_product_cost(data_val)
        mock_logger.info.assert_called_with('Total: 65.15\n')

        data_val = [
            "1 imported bottle of perfume at 27.99",
            "1 bottle of perfume at 18.99",
            "1 packet of headache pills at 9.75",
            "1 box of imported chocolates at 11.25"
        ]
        self.receipt_obj.calculate_product_cost(data_val)
        mock_logger.info.assert_called_with('Total: 74.68\n')
