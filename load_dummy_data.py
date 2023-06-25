from api.models import *
import random


categories = Category.objects.all()

if not categories:
    print("Inserting Categories")
    for value in range(1, 3):
        title = f"Category {value}"
        category = Category(title=title, slug=title.lower().replace(" ", "-"))
        category.save()
    print("Categories inserted")

menu_items = MenuItem.objects.all()
categories = Category.objects.all()

if not menu_items:
    print("Inserting Menu Items")
    for _ in range(1, 50):
        menu_item = MenuItem()
        menu_item.title = "Menu Item"
        menu_item.price = float(random.randint(1, 50)) + 0.99
        menu_item.featured = random.choice([True, False])
        menu_item.category = random.choice(categories)
        menu_item.save()
    print("Menu Items inserted")
