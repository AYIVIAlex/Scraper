import asyncio
from playwright.async_api import async_playwright
import requests
from time import sleep
import random
import os
import re
import pandas as pd
import pyktok as pyk


url_regex = r'(?<=\.com/)(.+?)(?=\?|$)'

proxies = [
    "http://192.168.137.21:8080",
    "http://192.168.137.250:8080"
]

async def init_browser():
    proxy = random.choice(proxies)
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=True,proxy={"server": proxy})
    return browser,playwright

async def get_video_data(browser, query, count=10):
    print("Fetching videos...")
    page = await browser.new_page()
    await page.goto(f'https://www.tiktok.com/search?q={query}',timeout=60000)
    await asyncio.sleep(random.uniform(2, 5))  # Pour éviter la détection
    
    items=[]
    videos =[]
    while len(items) < count:
        await page.evaluate("window.scrollBy(0, document.body.scrollHeight);")
        await asyncio.sleep(random.uniform(2, 5))
        # user_post_item = await page.query_selector_all('div[data-e2e="user-post-item"]')
        search_top_item = await page.query_selector_all('div[data-e2e="search_top-item"]')
        items = search_top_item

    for item in items[:count]:
        ouverture = await ouverture_lien(item,browser)
        metadata= await extract_metadata(ouverture["page"],ouverture["views"],ouverture["video_url"])
        videos.append(metadata)
    await page.close()
    return videos

async def recuperation_lien(conteneur,browser):
    a_tag = await conteneur.query_selector('a') 
    href = await a_tag.get_attribute('href')  
    return href

async def recuperation_vues(conteneurview):
    following_div = await conteneurview.query_selector('xpath=following-sibling::div[@data-e2e="search-card-desc"]')
    last_strong_selector = 'div[data-e2e="search-card-like-container"] strong:last-child'
    views_element = await following_div.query_selector(last_strong_selector)
    views = await views_element.text_content() if following_div else "No views"
    return views

async def ouverture_lien(conteneur, browser):
    lien = await recuperation_lien(conteneur, browser)
    views= await recuperation_vues(conteneur)
    page = await browser.new_page()
    await page.goto(lien,timeout=60000)
    await asyncio.sleep(random.uniform(2, 5))  # Pour éviter la détection
    return {
        "page":page,
        "views": views,
        "video_url":lien
    }
    

async def extract_metadata(page, views, video_url):
    description_element = await page.query_selector('h1[data-e2e="browse-video-desc"]')
    description = await description_element.text_content() if description_element else "No description"

    author_element = await page.query_selector('span[data-e2e="browse-username"]')
    author = await author_element.text_content() if author_element else "Unknown"

    last_span_selector = 'span[data-e2e="browser-nickname"] span:last-child'
    timestamp_element = await page.query_selector(last_span_selector)
    timestamp = await timestamp_element.text_content() if timestamp_element else "Unknown"

    title_element = await page.query_selector('title')
    title = await title_element.text_content() if title_element else "Unknown"

    resume_element = await page.query_selector('meta[name="description"]')
    resume = await resume_element.get_attribute('content') if resume_element else "No description"

    like_count_element = await page.query_selector('strong[data-e2e="like-count"]')
    like_count = await like_count_element.text_content() if like_count_element else "0"

    view_count = views if views else "0"
    video_url = video_url if video_url else ""

    location_match = re.search(url_regex, video_url)

    # Si une correspondance est trouvée, obtenir la chaîne correspondante
    if location_match:
        location_str = location_match.group(0).replace('/', '_') + '.mp4'
    else:
        location_str = "unknown.mp4"
    # Obtenir le répertoire courant et remplacer les antislashs par des slashs
    current_directory = os.getcwd().replace('\\', '/')
    current_directory=current_directory+"/videos/"
    # Construire le chemin complet
    location = os.path.join(current_directory, location_str)

    data = {
        'title': title,
        'author': author,
        'timestamp': timestamp,
        'description': description,
        'like_count': like_count,
        'view_count': view_count,
        'video_url': video_url,
        'location':location
    }
    return data


def save_metadata(data, filename):
    # Convertir les données en DataFrame Pandas
    new_data = pd.DataFrame([data])

    if os.path.exists(filename):
        # Lire les données existantes
        existing_data = pd.read_csv(filename)

        # Vérifier si l'enregistrement existe déjà
        if not new_data.isin(existing_data.to_dict('list')).all(axis=None):
            # Ajouter les nouvelles données s'il n'y a pas de doublon
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
            updated_data.to_csv(filename, index=False)
        else:
            print("Les données existent déjà.")
    else:
        # Si le fichier n'existe pas, créer un nouveau fichier CSV avec les nouvelles données
        new_data.to_csv(filename, index=False)


def download_video(url, output_path):
    try:
        pyk.save_tiktok(url, True,output_dir=output_path)
    except Exception as e:
        print(url)
        print(f"Error downloading video from {url}: {e}")
        print("Vous ne pouvez malheuresement pas télécharger cette vidéo")

    

# Assurez-vous que le dossier 'videos' existe
if not os.path.exists('videos'):
    os.makedirs('videos')

async def main():
    browser,playwright = await init_browser()
    recherche = input("Enter your search: ")
    number = int(input("Enter quantity : "))
    if browser:
        videos = await get_video_data(browser, recherche, count=number)
        for video in videos:
            if 'video_url' in video and video['video_url']:
                try:
                    print(f"Downloading video: {video['title']}")
                    download_video(video['video_url'], f"videos/")
                    save_metadata(video, 'metadata.csv')
                except:
                    print("Vous ne pouvez malheuresement pas télécharger cette vidéo")
            else:
                print(f"Skipped video {video['title']} due to missing URL")

        await browser.close()
        await playwright.stop()

# Exécution du code asynchrone
asyncio.run(main())

