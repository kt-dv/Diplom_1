import pytest
from unittest.mock import Mock
from praktikum.burger import Burger


class TestBurger:
    """Класс с тестами для бургера"""

    # --- ТЕСТЫ ДЛЯ МЕТОДА set_buns ---
    def test_set_buns(self, burger):
        mock_bun = Mock()
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    # --- ТЕСТЫ ДЛЯ МЕТОДА add_ingredient ---
    def test_add_ingredient(self, burger):
        mock_ingredient = Mock()
        burger.add_ingredient(mock_ingredient)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ingredient

    # --- ТЕСТЫ ДЛЯ МЕТОДА remove_ingredient ---
    def test_remove_ingredient(self, burger):
        mock_ing1 = Mock()
        mock_ing2 = Mock()
        burger.ingredients = [mock_ing1, mock_ing2]
        burger.remove_ingredient(0)
        assert len(burger.ingredients) == 1
        assert burger.ingredients[0] == mock_ing2

    # --- ТЕСТЫ ДЛЯ МЕТОДА move_ingredient ---
    def test_move_ingredient(self, burger):
        mock_ing1 = Mock()
        mock_ing2 = Mock()
        mock_ing3 = Mock()
        burger.ingredients = [mock_ing1, mock_ing2, mock_ing3]
        burger.move_ingredient(0, 2)
        assert burger.ingredients == [mock_ing2, mock_ing3, mock_ing1]

    # --- ТЕСТЫ ДЛЯ МЕТОДА get_price (с параметризацией и моками) ---
    @pytest.mark.parametrize("bun_price, ing_prices, expected_price", [
        (100, [], 200),
        (100, [50], 250),
        (100, [50, 30], 280),
        (0, [10], 10),
    ])
    def test_get_price(self, burger, bun_price, ing_prices, expected_price):
        mock_bun = Mock()
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)

        for price in ing_prices:
            mock_ing = Mock()
            mock_ing.get_price.return_value = price
            burger.add_ingredient(mock_ing)

        assert burger.get_price() == expected_price

    # --- ТЕСТЫ ДЛЯ МЕТОДА get_receipt ---
    def test_get_receipt(self, burger):
        mock_bun = Mock()
        mock_bun.get_name.return_value = "Белая булочка"
        mock_bun.get_price.return_value = 100
        burger.set_buns(mock_bun)

        mock_ing1 = Mock()
        mock_ing1.get_name.return_value = "Котлета"
        mock_ing1.get_type.return_value = "FILLING"
        mock_ing1.get_price.return_value = 50
        burger.add_ingredient(mock_ing1)

        mock_ing2 = Mock()
        mock_ing2.get_name.return_value = "Кетчуп"
        mock_ing2.get_type.return_value = "SAUCE"
        mock_ing2.get_price.return_value = 20
        burger.add_ingredient(mock_ing2)

        expected_receipt = (
            "(==== Белая булочка ====)\n"
            "= filling Котлета =\n"
            "= sauce Кетчуп =\n"
            "(==== Белая булочка ====)\n\n"
            "Price: 270"
        )
        assert burger.get_receipt() == expected_receipt

    # --- ДОПОЛНИТЕЛЬНЫЙ ТЕСТ ---
    def test_get_price_empty_burger(self, burger):
        mock_bun = Mock()
        mock_bun.get_price.return_value = 0
        burger.set_buns(mock_bun)
        assert burger.get_price() == 0