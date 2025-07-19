import requests
from bs4 import BeautifulSoup

URL = 'https://www.senetic.fr/?srsltid=AfmBOoqGYBfQQzv0UtQEgVbcE-hk444CD-8vO6C7itNOzGU6RbRytMa2'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/58.0.3029.110 Safari/537.3'
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Trouve les conteneurs produits (adapter le sélecteur CSS selon la structure de la page)
product_containers = soup.select('div.product-list > div.product-item')  # Exemple, à adapter

result = []
for product in product_containers[:20]:  # Limite à 20 produits
    try:
        # Nom du produit
        title = product.select_one('a.product-title').get_text(strip=True)

        # URL image principale
        img_tag = product.select_one('img.product-image')
        img_url = img_tag['src'] if img_tag else None

        # Prix (exemple)
        price_tag = product.select_one('span.price')
        price = price_tag.get_text(strip=True) if price_tag else None

        # Construction de l'objet produit simplifié
        prod_data = {
            'name': title,
            'image': img_url,
            'price': price,
        }
        result.append(prod_data)
    except Exception as e:
        print(f"Erreur extraction produit: {e}")

# Affichage JSON ou traitement
import json
print(json.dumps(result, indent=2, ensure_ascii=False))
