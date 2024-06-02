import requests
from bs4 import BeautifulSoup as bs
from halo import Halo
from MahakRobot import pbot as app
from pyrogram import filters

spinner = Halo(text='Fetching IPL Score', color='green', spinner='hamburger')
url_data = "https://www.cricbuzz.com/cricket-match/live-scores"
recent_data = "https://www.cricbuzz.com/cricket-match/live-scores/recent-matches"

# Function to fetch and parse live scores
def fetch_scores():
    spinner.start()
    try:
        r = requests.get(url_data)
        soup = bs(r.content, 'html.parser')
        div = soup.find("div", attrs={"ng-show": "active_match_type == 'league-tab'"})
        matches = div.find_all(class_="cb-mtch-lst cb-col cb-col-100 cb-tms-itm")
        
        match_info = []
        for match in matches:
            team_names = match.find("h3").text.strip().replace(",", "")
            status = match.find("div", attrs={"class": "cb-text-live"}).text.strip() if match.find("div", attrs={"class": "cb-text-live"}) else 'Status Not Available'
            score = match.find_all("div", attrs={"style": "display:inline-block; width:140px"})[0].text.strip() if match.find_all("div", attrs={"style": "display:inline-block; width:140px"}) else 'Not yet Started'
            score_two = match.find_all("div", attrs={"style": "display:inline-block; width:140px"})[1].text.strip() if match.find_all("div", attrs={"style": "display:inline-block; width:140px"}) else 'Not yet Started'
            team_one = match.find_all("div", attrs={"class": "cb-ovr-flo cb-hmscg-tm-nm"})[0].text.strip()
            team_two = match.find_all("div", attrs={"class": "cb-ovr-flo cb-hmscg-tm-nm"})[1].text.strip()

            match_info.append(f"\n> {team_names} - {status}\n> {team_one} - {score}\n> {team_two} - {score_two}\n")
        
        if not match_info:
            match_info.append("No IPL Live Match at the Moment")

        spinner.stop()
        return "\n".join(match_info)
    
    except Exception as e:
        spinner.stop()
        return f"Error: {e}"

# Telegram bot command to fetch IPL scores
@app.on_message(filters.command(["ipl"], prefixes=["/", "!", "%", ",", ".", "@", "#"]))
async def send_ipl_scores(_, message):
    chat_id = message.chat.id
    await message.reply("Fetching IPL scores...")
    
    scores = fetch_scores()
    await app.send_message(chat_id, scores)

# Start the app (if not already running in your main file)
if __name__ == "__main__":
    app.run()