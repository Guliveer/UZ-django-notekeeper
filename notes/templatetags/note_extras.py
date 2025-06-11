from django import template
import hashlib

register = template.Library()

@register.filter
def category_color(category_name):
    # Lista kolorów w formacie hex
    colors = [
        '#FF6B6B',  # czerwony
        '#4ECDC4',  # turkusowy
        '#45B7D1',  # niebieski
        '#96CEB4',  # zielony
        '#FFEEAD',  # żółty
        '#D4A5A5',  # różowy
        '#9B59B6',  # fioletowy
        '#3498DB',  # jasny niebieski
        '#E67E22',  # pomarańczowy
        '#2ECC71',  # jasny zielony
    ]
    
    # Używamy nazwy kategorii do wygenerowania indeksu koloru
    hash_object = hashlib.md5(category_name.encode())
    hash_value = int(hash_object.hexdigest(), 16)
    color_index = hash_value % len(colors)
    
    return colors[color_index] 