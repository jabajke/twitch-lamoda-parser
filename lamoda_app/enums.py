from enum import Enum


class GenderEnum(str, Enum):
    all = "all"
    men = "men"
    women = "women"
    girls = "girls"
    boys = "boys"
    kids = "kids"
    prism = "prism"


class SectionEnum(str, Enum):
    main = "main"
    kids = "kids"
    premium = "premium"
    beauty = "beauty"
    sport = "sport"
    _404 = "404"
    orders = "orders"
    wishlist = "wishlist"
    cart = "cart"
    empty = "empty"
