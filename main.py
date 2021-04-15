import os
import ctypes
import time as sleeptime
from datetime import datetime, time
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from avanza import Avanza
import config

# Account details
avanza = Avanza(
    {
        "username": config.avanzaUsername,
        "password": config.avanzaPassword,
        "totpSecret": config.totpSecret,
    }
)


def in_market_hours(market_open, market_close):
    current_time = datetime.now().time()
    return current_time >= market_open and current_time <= market_close


while True:
    try:
        # Only execute API calls on weekdays (to minimize load on API)
        if datetime.today().weekday() < 5 and in_market_hours(
            time(9, 00), time(22, 00)
        ):
            overview = avanza.get_account_overview(config.accountID)
            ownedCapital = str(int(overview["ownCapital"]))
            balanceText = ownedCapital + " sek"

            # Generate image
            W, H = (1920, 1080)
            img = Image.new("RGBA", (W, H), config.backgroundColor)
            draw = ImageDraw.Draw(img)
            myFont = ImageFont.truetype("font.ttf", size=75)
            w, h = draw.textsize(balanceText, font=myFont)

            # Draws centered text
            draw.text(
                ((W - w) / 2, (H - h) / 2),
                balanceText,
                font=myFont,
                fill="white",
                align="center",
            )
            img.save("balance.png", "PNG")

            # Set as wallpaper
            ctypes.windll.user32.SystemParametersInfoW(
                20,
                0,
                os.getcwd() + "\\balance.png",
                0,
            )

        # Sleeps for x seconds before looping again
        sleeptime.sleep(config.updateIntervalSeconds)
    except Exception as e:
        print("Error occurred: ", e)
