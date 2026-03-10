from playwright.sync_api import sync_playwright
from geopy.geocoders import Nominatim
import pandas as pd
import time

# ------------------------------
# FUNCION PARA OBTENER COORDENADAS
# ------------------------------

def get_coords(city):

    geolocator = Nominatim(user_agent="maps_scraper")
    location = geolocator.geocode(city)

    if location:
        return location.latitude, location.longitude
    else:
        return None, None


# ------------------------------
# INPUT DEL USUARIO
# ------------------------------

search_query = input("¿Qué negocio quieres buscar?: ")
city = input("¿En qué ciudad?: ")
max_results = int(input("¿Cuántos resultados quieres obtener?: "))

lat, lng = get_coords(city)

if lat is None:
    print("No se pudo encontrar la ciudad.")
    exit()

print("Coordenadas:", lat, lng)

# URL centrada en la ciudad
maps_url = f"https://www.google.com/maps/@{lat},{lng},15z/search/{search_query}"

data = []

# ------------------------------
# SCRAPER
# ------------------------------

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(maps_url)

    print("Cargando resultados...")

    page.wait_for_timeout(5000)

    feed = page.locator('div[role="feed"]')

    previous_count = 0
    same_count = 0

    # SCROLL PARA CARGAR RESULTADOS
    while True:

        feed.evaluate("el => el.scrollTop = el.scrollHeight")
        page.wait_for_timeout(1500)

        listings = page.locator('div[role="article"]').all()
        current_count = len(listings)

        print("Negocios cargados:", current_count)

        if current_count >= max_results:
            break

        if current_count == previous_count:
            same_count += 1
        else:
            same_count = 0

        if same_count >= 5:
            print("No hay más resultados disponibles.")
            break

        previous_count = current_count

    print("Extrayendo datos...")

    listings = page.locator('div[role="article"]').all()

    for i, listing in enumerate(listings[:max_results]):

        try:
            listing.click()
            page.wait_for_timeout(1200)
        except:
            continue

        try:
            name = page.locator("h1.DUwDvf").inner_text()
        except:
            name = ""

        try:
            address = page.locator('button[data-item-id="address"]').inner_text()
        except:
            address = ""

        try:
            phone = page.locator('button[data-item-id^="phone"]').inner_text()
        except:
            phone = ""

        try:
            rating = page.locator('span.MW4etd').first.inner_text()
        except:
            rating = ""

        try:
            reviews = page.locator('span.UY7F9').first.inner_text()
        except:
            reviews = ""

        try:
            website = page.locator('a[data-item-id="authority"]').get_attribute("href")
        except:
            website = ""

        data.append({
            "name": name,
            "address": address,
            "phone": phone,
            "rating": rating,
            "reviews": reviews,
            "website": website
        })

        print(f"{i+1} guardado")

    browser.close()

# ------------------------------
# GUARDAR EXCEL
# ------------------------------

df = pd.DataFrame(data)

filename = f"{search_query}_{city}.xlsx".replace(" ", "_")

df.to_excel(filename, index=False)

print("Archivo guardado:", filename)