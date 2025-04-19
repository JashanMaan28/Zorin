from playsound import playsound
from backend.textToSpeech import speak
from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import requests
import subprocess
import keyboard
import asyncio
import pvporcupine
import pyaudio
import pyautogui as autogui
import struct
import time
import os

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")
ACCESS_KEY = env_vars.get("pvporcupine_ACCESS_KEY")

# Define CSS classes for parsing specific elements in HTML content.
classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YmPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
           "IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe",
           "LwkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz26b"]

# Define a user-agent for making web requests.
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

client = Groq(api_key=GroqAPIKey)

professional_responses = [
    # OG resonses
    "Your satisfaction is my priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask.",
    
    # General service closings
    "Is there anything else I can assist you with today?",
    "If you have any further questions, please don't hesitate to ask.",
    "I'm here to help if you need any additional assistance.",
    "Please let me know if you require any clarification or have other questions.",
    "I'd be happy to provide further assistance if needed.",
    
    # Satisfaction-focused closings
    "I hope this solution works well for you. Please let me know if you need anything else.",
    "Was this helpful? I'm available if you need further assistance.",
    "I trust this addresses your needs. Feel free to reach out with any other questions.",
    "I hope this information proves valuable. Please let me know if you need anything more.",
    "My goal is your complete satisfaction—please let me know if there's anything else I can do.",
    
    # Availability-focused closings
    "I'm available anytime you need further assistance with this or other matters.",
    "Feel free to return anytime with additional questions or concerns.",
    "I'll be here if you need any follow-up assistance or have other questions.",
    "Don't hesitate to reach out if you require additional support in the future.",
    "My assistance is available whenever you need it—just let me know how I can help.",
    
    # Follow-up focused closings
    "Would you like me to explain anything else about this solution?",
    "If you encounter any issues implementing this, please don't hesitate to ask for clarification.",
    "I'll be interested to know how this works for you—please feel free to provide feedback.",
    "Should you need any adjustments to this solution, I'm happy to refine it further.",
    "If you'd like to explore alternative approaches, I'm here to discuss options.",
    
    # Personalized service closings
    "I've enjoyed assisting you today. Please reach out if you need anything else.",
    "It's been a pleasure helping you resolve this. I'm here if you need further support.",
    "Thank you for the opportunity to assist you. I'm available if you have other questions.",
    "I appreciate your patience as we worked through this. Please let me know if you need anything more.",
    "I value your trust and am committed to providing continued support whenever needed.",
    
    # Problem-solving closings
    "If you encounter any difficulties with this solution, please don't hesitate to get back in touch.",
    "Should any complications arise, I'm ready to help troubleshoot further.",
    "I hope this resolves your issue completely—but if not, I'm here to explore other solutions.",
    "Please test this solution and let me know if any adjustments are needed.",
    "This approach should address your needs, but I'm available to refine it if necessary.",
    
    # Action-oriented closings
    "Is there any specific aspect of this you'd like me to elaborate on further?",
    "Would you like me to help with implementing any part of this solution?",
    "Do you anticipate needing any additional resources to move forward with this?",
    "Shall we schedule a follow-up to ensure everything is working as expected?",
    "Would you like me to document these steps for future reference?",
    
    # Confidence-building closings
    "Rest assured that your satisfaction is my highest priority.",
    "I'm confident this solution will meet your needs, but I'm here if adjustments are required.",
    "You can proceed with confidence, knowing support is available if needed.",
    "I stand behind this solution, but welcome any feedback for improvement.",
    "You're in good hands—I'll ensure your issue is fully resolved to your satisfaction."
]

messages = []

SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write a content like letters, codes, applications, essays, notes, songs, poems, etc."}]

def GoogleSearch(Topic):
    search(Topic)
    return True

# GoogleSearch("Google")

def Content(Topic):

    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model = "gemma2-9b-it",
            messages = SystemChatBot + messages,
            max_tokens = 2048,
            temperature = 0.7,
            top_p = 1,
            stream = True,
            stop = None
        )  

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        
        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer
    
    Topic: str = Topic.replace("Content", "")
    ContentByAI = ContentWriterAI(Topic)

    with open(rf"Data\{Topic.lower().replace(' ','')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()
    
    OpenNotepad(rf"Data\{Topic.lower().replace(' ','')}.txt")
    return True

# Content("Write a sick leave")

def YoutubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

# YoutubeSearch("Youtube Search AI news")

def PlayYoutbe(query):
    playonyt(query)
    return True

# PlayYoutbe("Play karan aujla 48 rhymes")

def OpenApp(app, sess=requests.session()):
    # Clean the app name by removing "Open " prefix if it exists
    clean_app_name = app
    if clean_app_name.lower().startswith("open "):
        clean_app_name = clean_app_name[5:].strip()
    
    # Dictionary of special websites that might need specific URLs
    special_websites = {
        # Social Media
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "twitter": "https://twitter.com",
        "x": "https://twitter.com",
        "linkedin": "https://www.linkedin.com",
        "pinterest": "https://www.pinterest.com",
        "reddit": "https://www.reddit.com",
        "snapchat": "https://web.snapchat.com",
        "tiktok": "https://www.tiktok.com",
        "tumblr": "https://www.tumblr.com",
        "mastodon": "https://mastodon.social",
        "threads": "https://www.threads.net",

        # Video/Streaming
        "youtube": "https://www.youtube.com",
        "twitch": "https://www.twitch.tv",
        "netflix": "https://www.netflix.com",
        "hulu": "https://www.hulu.com",
        "disney+": "https://www.disneyplus.com",
        "disneyplus": "https://www.disneyplus.com",
        "amazon prime": "https://www.amazon.com/Prime-Video",
        "prime video": "https://www.primevideo.com",
        "hbo max": "https://www.max.com",
        "max": "https://www.max.com",
        "paramount+": "https://www.paramountplus.com",
        "peacock": "https://www.peacocktv.com",
        "vimeo": "https://vimeo.com",
        "dailymotion": "https://www.dailymotion.com",

        # Shopping
        "amazon": "https://www.amazon.com",
        "ebay": "https://www.ebay.com",
        "walmart": "https://www.walmart.com",
        "target": "https://www.target.com",
        "etsy": "https://www.etsy.com",
        "best buy": "https://www.bestbuy.com",
        "alibaba": "https://www.alibaba.com",
        "aliexpress": "https://www.aliexpress.com",
        "wayfair": "https://www.wayfair.com",
        "costco": "https://www.costco.com",
        "newegg": "https://www.newegg.com",
        "zappos": "https://www.zappos.com",
        "shein": "https://www.shein.com",
        "temu": "https://www.temu.com",

        # Productivity/Work
        "gmail": "https://mail.google.com",
        "google mail": "https://mail.google.com",
        "google docs": "https://docs.google.com",
        "google sheets": "https://sheets.google.com",
        "google slides": "https://slides.google.com",
        "google drive": "https://drive.google.com",
        "google calendar": "https://calendar.google.com",
        "outlook": "https://outlook.live.com",
        "microsoft outlook": "https://outlook.office.com",
        "microsoft office": "https://www.office.com",
        "office 365": "https://www.office.com",
        "onedrive": "https://onedrive.live.com",
        "dropbox": "https://www.dropbox.com",
        "notion": "https://www.notion.so",
        "evernote": "https://www.evernote.com",
        "trello": "https://trello.com",
        "asana": "https://asana.com",
        "slack": "https://slack.com",
        "zoom": "https://zoom.us",
        "teams": "https://teams.microsoft.com",
        "microsoft teams": "https://teams.microsoft.com",
        "webex": "https://www.webex.com",
        "google meet": "https://meet.google.com",
        "airtable": "https://airtable.com",
        "monday": "https://monday.com",
        "jira": "https://www.atlassian.com/software/jira",
        "confluence": "https://www.atlassian.com/software/confluence",
        "figma": "https://www.figma.com",
        "canva": "https://www.canva.com",
        "miro": "https://miro.com",
        "obsidian": "https://obsidian.md",
        "clickup": "https://clickup.com",
        "todoist": "https://todoist.com",
        "linear": "https://linear.app",

        # AI Tools
        "chatgpt": "https://chat.openai.com",
        "bard": "https://bard.google.com",
        "gemini": "https://gemini.google.com",
        "claude": "https://claude.ai",
        "anthropic": "https://www.anthropic.com",
        "perplexity": "https://www.perplexity.ai",
        "dall-e": "https://labs.openai.com",
        "midjourney": "https://www.midjourney.com",
        "stable diffusion": "https://stability.ai",
        "hugging face": "https://huggingface.co",
        "openai": "https://openai.com",
        "replicate": "https://replicate.com",
        "jasper": "https://www.jasper.ai",
        "copy.ai": "https://www.copy.ai",
        "synthesia": "https://www.synthesia.io",
        "runway": "https://runwayml.com",
        "elevenlabs": "https://elevenlabs.io",
        "github copilot": "https://github.com/features/copilot",

        # Education
        "wikipedia": "https://www.wikipedia.org",
        "khan academy": "https://www.khanacademy.org",
        "coursera": "https://www.coursera.org", 
        "udemy": "https://www.udemy.com",
        "edx": "https://www.edx.org",
        "skillshare": "https://www.skillshare.com",
        "duolingo": "https://www.duolingo.com",
        "quizlet": "https://quizlet.com",
        "chegg": "https://www.chegg.com",
        "brilliant": "https://brilliant.org",
        "codecademy": "https://www.codecademy.com",
        "freecodecamp": "https://www.freecodecamp.org",
        "udacity": "https://www.udacity.com",
        "ted": "https://www.ted.com",
        "masterclass": "https://www.masterclass.com",

        # News/Information
        "cnn": "https://www.cnn.com",
        "bbc": "https://www.bbc.com",
        "nytimes": "https://www.nytimes.com",
        "new york times": "https://www.nytimes.com",
        "washingtonpost": "https://www.washingtonpost.com",
        "washington post": "https://www.washingtonpost.com",
        "fox news": "https://www.foxnews.com",
        "npr": "https://www.npr.org",
        "reuters": "https://www.reuters.com",
        "ap news": "https://apnews.com",
        "bloomberg": "https://www.bloomberg.com",
        "wall street journal": "https://www.wsj.com",
        "wsj": "https://www.wsj.com",
        "economist": "https://www.economist.com",
        "guardian": "https://www.theguardian.com",
        "huffpost": "https://www.huffpost.com",

        # Finance
        "paypal": "https://www.paypal.com",
        "venmo": "https://venmo.com",
        "cashapp": "https://cash.app",
        "chase": "https://www.chase.com",
        "bank of america": "https://www.bankofamerica.com",
        "wells fargo": "https://www.wellsfargo.com",
        "robinhood": "https://robinhood.com",
        "coinbase": "https://www.coinbase.com",
        "mint": "https://mint.intuit.com",
        "credit karma": "https://www.creditkarma.com",
        "binance": "https://www.binance.com",
        "fidelity": "https://www.fidelity.com",
        "vanguard": "https://www.vanguard.com",
        "schwab": "https://www.schwab.com",
        "etrade": "https://us.etrade.com",

        # Travel
        "airbnb": "https://www.airbnb.com",
        "booking": "https://www.booking.com",
        "expedia": "https://www.expedia.com",
        "tripadvisor": "https://www.tripadvisor.com",
        "kayak": "https://www.kayak.com",
        "skyscanner": "https://www.skyscanner.com",
        "hotels": "https://www.hotels.com",
        "orbitz": "https://www.orbitz.com",
        "vrbo": "https://www.vrbo.com",
        "hotwire": "https://www.hotwire.com",
        "priceline": "https://www.priceline.com",
        "trivago": "https://www.trivago.com",
        "travelocity": "https://www.travelocity.com",

        # Tech/Development
        "github": "https://github.com",
        "gitlab": "https://gitlab.com",
        "stackoverflow": "https://stackoverflow.com",
        "stack overflow": "https://stackoverflow.com",
        "bitbucket": "https://bitbucket.org",
        "codepen": "https://codepen.io",
        "vercel": "https://vercel.com",
        "netlify": "https://www.netlify.com",
        "heroku": "https://www.heroku.com",
        "aws": "https://aws.amazon.com",
        "azure": "https://azure.microsoft.com",
        "google cloud": "https://cloud.google.com",
        "digitalocean": "https://www.digitalocean.com",
        "mongodb": "https://www.mongodb.com",
        "mysql": "https://www.mysql.com",
        "w3schools": "https://www.w3schools.com",
        "mdn": "https://developer.mozilla.org",
        "codecademy": "https://www.codecademy.com",
        "replit": "https://replit.com",
        "codesandbox": "https://codesandbox.io",
        "vscode": "https://code.visualstudio.com",

        # Music
        "spotify": "https://www.spotify.com",
        "apple music": "https://music.apple.com",
        "youtube music": "https://music.youtube.com",
        "soundcloud": "https://soundcloud.com",
        "pandora": "https://www.pandora.com",
        "tidal": "https://tidal.com",
        "deezer": "https://www.deezer.com",
        "bandcamp": "https://bandcamp.com",
        "last.fm": "https://www.last.fm",
        "amazon music": "https://music.amazon.com",

        # Games
        "steam": "https://store.steampowered.com",
        "epic games": "https://www.epicgames.com",
        "playstation": "https://www.playstation.com",
        "xbox": "https://www.xbox.com",
        "nintendo": "https://www.nintendo.com",
        "twitch": "https://www.twitch.tv",
        "discord": "https://discord.com",
        "roblox": "https://www.roblox.com",
        "minecraft": "https://www.minecraft.net",
        "origin": "https://www.origin.com",
        "ea": "https://www.ea.com",
        "ubisoft": "https://www.ubisoft.com",
        "battle.net": "https://battle.net",
        "gog": "https://www.gog.com",
        "itch.io": "https://itch.io",

        # Messaging
        "whatsapp": "https://web.whatsapp.com",
        "telegram": "https://web.telegram.org",
        "signal": "https://signal.org",
        "discord": "https://discord.com/app",
        "messenger": "https://www.messenger.com",
        "skype": "https://web.skype.com",
        "viber": "https://account.viber.com/en/login",
        "line": "https://line.me",
        "wechat": "https://web.wechat.com",
        "kakaotalk": "https://accounts.kakao.com",

        # Cloud Storage
        "google drive": "https://drive.google.com",
        "dropbox": "https://www.dropbox.com",
        "onedrive": "https://onedrive.live.com",
        "box": "https://www.box.com",
        "icloud": "https://www.icloud.com",
        "mega": "https://mega.nz",
        "mediafire": "https://www.mediafire.com",

        # Health & Fitness
        "fitbit": "https://www.fitbit.com",
        "myfitnesspal": "https://www.myfitnesspal.com",
        "strava": "https://www.strava.com",
        "peloton": "https://www.onepeloton.com",
        "nike": "https://www.nike.com",
        "nike run club": "https://www.nike.com/nrc-app",
        "garmin": "https://connect.garmin.com",
        "headspace": "https://www.headspace.com",
        "calm": "https://www.calm.com",
        "webmd": "https://www.webmd.com",
        "mayo clinic": "https://www.mayoclinic.org",
        "doordash": "https://www.doordash.com",
        "ubereats": "https://www.ubereats.com",
        "grubhub": "https://www.grubhub.com",
        "instacart": "https://www.instacart.com",
        "allrecipes": "https://www.allrecipes.com",
        
        # Others
        "google": "https://www.google.com",
        "bing": "https://www.bing.com",
        "duckduckgo": "https://duckduckgo.com",
        "yahoo": "https://www.yahoo.com",
        "weather": "https://weather.gov",
        "maps": "https://maps.google.com",
        "google maps": "https://maps.google.com",
        "apple maps": "https://maps.apple.com",
        "waze": "https://www.waze.com",
        "imdb": "https://www.imdb.com",
        "goodreads": "https://www.goodreads.com",
        "glassdoor": "https://www.glassdoor.com",
        "indeed": "https://www.indeed.com",
        "linkedin jobs": "https://www.linkedin.com/jobs",
        "craigslist": "https://www.craigslist.org",
        "zillow": "https://www.zillow.com",
        "redfin": "https://www.redfin.com",
        "apartments": "https://www.apartments.com",
        "yelp": "https://www.yelp.com",
        "opentable": "https://www.opentable.com",
        "rotten tomatoes": "https://www.rottentomatoes.com",
        "metacritic": "https://www.metacritic.com",
        "medium": "https://medium.com",
        "substack": "https://substack.com",
        "patreon": "https://www.patreon.com",
        "behance": "https://www.behance.net",
        "dribbble": "https://dribbble.com",
        "shutterstock": "https://www.shutterstock.com",
        "unsplash": "https://unsplash.com",
        "pexels": "https://www.pexels.com",
        "flickr": "https://www.flickr.com"
    }
    
    try:
        # First try to open as a local app
        appopen(clean_app_name, match_closest=True, output=True, throw_error=True)
        speak(f"Opened, {clean_app_name} ")
        return True
    
    except:
        # Check if it's a special website first
        for site_name, url in special_websites.items():
            if site_name.lower() in clean_app_name.lower():
                print(f"Opening {site_name} in browser: {url}")
                webopen(url)
                return True
        
        # Rest of the search code as before
        def extract_links_from_google(html):
            # [Keep the existing extract_links_from_google function]
            if html is None:
                return []
            
            soup = BeautifulSoup(html, 'html.parser')
            all_links = []
            
            # Try multiple methods to extract links
            
            # Method 1: Find all <a> tags with href attributes
            for a_tag in soup.find_all('a', href=True):
                href = a_tag.get('href')
                
                # Filter Google's redirect links to get the actual URL
                if href.startswith('/url?q='):
                    actual_url = href.split('/url?q=')[1].split('&')[0]
                    all_links.append(actual_url)
                # Also include direct http links
                elif href.startswith('http') and 'google' not in href:
                    all_links.append(href)
            
            # Method 2: Search for metadata
            meta_tags = soup.find_all('meta', {'property': 'og:url'})
            for tag in meta_tags:
                if tag.get('content') and tag.get('content').startswith('http'):
                    all_links.append(tag.get('content'))
            
            # Filter out unwanted links
            filtered_links = []
            for link in all_links:
                if (link.startswith('http') and 
                    'google' not in link and 
                    'youtube.com/watch' not in link and
                    'accounts.google' not in link and
                    'support.google' not in link):
                    filtered_links.append(link)
            
            # Remove duplicates while preserving order
            unique_links = []
            for link in filtered_links:
                if link not in unique_links:
                    unique_links.append(link)
            
            return unique_links
        
        def search_google(query):
            # [Keep the existing search_google function]
            url = f"https://www.google.com/search?q={query}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.google.com/',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0',
            }
            try:
                response = sess.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    return response.text
                else:
                    print(f"Failed to retrieve search results for {query}. Status code: {response.status_code}")
            except Exception as e:
                print(f"Exception during search: {str(e)}")
            return None
        
        try:
            # Search for the app name
            search_query = f"{clean_app_name}"
            print(f"Searching for: {search_query}")
            html = search_google(search_query)
            
            if html:
                links = extract_links_from_google(html)
                
                print(f"Found {len(links)} potential links for {clean_app_name}")
                
                if links and len(links) > 0:
                    # Try to find the most relevant link (preference for official websites)
                    for link in links[:5]:  # Check first 5 links
                        lower_link = link.lower()
                        lower_app = clean_app_name.lower()
                        
                        # Check if link contains app name and looks like an official site
                        is_official = False
                        if lower_app in lower_link:
                            domain_parts = lower_link.split('/')[2].split('.')
                            if lower_app in domain_parts:
                                is_official = True
                        
                        if is_official:
                            print(f"Opening official site for {clean_app_name}: {link}")
                            webopen(link)
                            return True
                    
                    # If no official site found, use the first link
                    first_link = links[0]
                    speak(f"Opened first search result for {clean_app_name}: {first_link}")
                    webopen(first_link)
                    return True
                else:
                    print(f"No search results found for {clean_app_name}.")
                    # Try a more specific search
                    html = search_google(f"{clean_app_name} official website")
                    links = extract_links_from_google(html)
                    
                    if links and len(links) > 0:
                        first_link = links[0]
                        print(f"Opening search result from alternate query: {first_link}")
                        webopen(first_link)
                        return True
                    else:
                        print(f"Could not find any relevant links for {clean_app_name}.")
                        
                        # Try some common URL patterns for the app name
                        app_name_no_spaces = clean_app_name.lower().replace(' ', '')
                        
                        # Try multiple TLDs and URL patterns
                        url_patterns = [
                            f"https://www.{app_name_no_spaces}.com",
                            f"https://www.{app_name_no_spaces}.ai",
                            f"https://www.{app_name_no_spaces}.io",
                            f"https://www.{app_name_no_spaces}.app",
                            f"https://{app_name_no_spaces}.com",
                            f"https://{app_name_no_spaces}.ai", 
                            f"https://{app_name_no_spaces}.io",
                            f"https://{app_name_no_spaces}.app"
                        ]
                        
                        for url in url_patterns:
                            print(f"Attempting to open URL: {url}")
                            webopen(url)
                            return True  # Return after first attempt
                        
                        return False
            else:
                print(f"Failed to get search results for {clean_app_name}.")
                
                # Even if search fails, try common URL patterns
                app_name_no_spaces = clean_app_name.lower().replace(' ', '')
                url = f"https://www.{app_name_no_spaces}.com"
                print(f"Search failed. Attempting to open constructed URL: {url}")
                webopen(url)
                speak(f"Opened {clean_app_name}")
                return True
                
        except Exception as e:
            print(f"Error while trying to open {clean_app_name} in browser: {str(e)}")
            
            # Even if everything fails, try a simple URL construction as last resort
            try:
                app_name_no_spaces = clean_app_name.lower().replace(' ', '')
                url = f"https://www.{app_name_no_spaces}.com"
                print(f"Exception occurred. Attempting to open as last resort: {url}")
                webopen(url)
                speak(f"Opened {clean_app_name}")
                return True
            except:
                return False

#OpenApp("Open apple music")

def CloseApp(app):
    
    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False

# CloseApp("Close whatsapp")

def System(command):

    def mute():
        keyboard.press_and_release('volume mute')

    def unmute():
        keyboard.press_and_release('volume mute')
    
    def volume_up():
        keyboard.press_and_release('volume up')
    
    def volume_down():
        keyboard.press_and_release('volume down')
    
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    
    return True

# System("unmute")

async def TranslateAndExecute(commands: list[str]):

    funcs = []

    for command in commands:

        if command.startswith("open "):
            
            if "open it" in command:
                pass
            if "open file" in command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)
            
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)
        
        elif command.startswith("play "):
            fun = asyncio.to_thread(playonyt, command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("search ") or command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("search "))
            funcs.append(fun)
        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)
        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)
        else:
            print(f"No Function Found for {command}")
        
    results = await asyncio.gather(*funcs)

    for result in results:
        if isinstance(results, str):
            yield result
        else:
            yield result


async def Automation(commands: list[str]):
    
    async for result in TranslateAndExecute(commands):
        pass
    return True

# Assistant Sound Playing function
def playAssistantSound(dir):
    try:
        playsound(dir)
    except Exception as e:
        print(f"Error playing sound: {e}")

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):

    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
        
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    
    return new_query.capitalize()
