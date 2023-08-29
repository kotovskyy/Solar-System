import pytest
import math
import os
from  solarSystemRemake import SolarSystem

@pytest.fixture(autouse=True)
def app():
    app = SolarSystem(None)

def test_cart_to_pygame(app):
    cart_coords = (150, 200)
    expected = (600, 650)
    assert app.cartesian_to_pygame(cart_coords) == expected

def test_pygame_to_cart(app):
    pass