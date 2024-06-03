import requests
from bs4 import BeautifulSoup as bs
from halo import Halo
from MahakRobot import pbot as app
from pyrogram import filters

spinner = Halo(text='Fetching Cricket Scores', color='green', spinner='hamburger')

# URLs
url_live = "https://m.cricbuzz.com/cricket-match/live-scores"
url_recent = "https://m.cricbuzz.com/cricket-match/live-scores/recent-matches"
url_upcoming = "https://m.cricbuzz.com/cricket-match/live-scores/upcoming-matches"

def fetch_matches(url):
    spinner.start()
    try:
        r = requests.get(url)
        soup = bs(r.content, 'html.parser')
        matches = soup.find_all("div", class_="cb-col cb-col-100 cb-mtch-lst")
        
        match_info = []
        for match in matches:
            title = match.find("h3", class_="cb-ltst-wgt-hdr").text.strip()
            match_data = match.find_all("div", class_="cb-col cb-col-100 cb-ltst-wgt-hdr")
            for data in match_data:
                teams = data.find("a").text.strip()
                status = data.find("div", class_="cb-text-live").text.strip() if data.find("div", class_="cb-text-live") else 'Status Not Available'
                score = data.find_all("div", class_="cb-ovr-flo")[0].text.strip() if data.find_all("div", class_="cb-ovr-flo") else 'Score Not Available'
                match_info.append(f"\n> {teams}\n> {status}\n> {score}\n")
        
        if not match_info:
            match_info.append("No matches found at the moment")

        spinner.stop()
        return "\n".join(match_info)
    
    except Exception as e:
        spinner.stop()
        return f"Error: {e}"

@app.on_message(filters.command(["live"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def send_live_scores(_, message):
    chat_id = message.chat.id
    await message.reply("Fetching live scores...")
    
    scores = fetch_matches(url_live)
    await message.reply.delete()
    await app.send_message(chat_id, scores)

@app.on_message(filters.command(["recent"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def send_recent_matches(_, message):
    chat_id = message.chat.id
    await message.reply("Fetching recent matches...")
    
    scores = fetch_matches(url_recent)
    await app.send_message(chat_id, scores)

@app.on_message(filters.command(["upcoming"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def send_upcoming_matches(_, message):
    chat_id = message.chat.id
    await message.reply("Fetching upcoming matches...")
    
    scores = fetch_matches(url_upcoming)
    await message.reply.delete()
    await app.send_message(chat_id, scores)

# Start the app (if not already running in your main file)
if __name__ == "__main__":
    app.run()