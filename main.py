from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import ctypes
import time
from avanza import Avanza
import datetime
import hashlib
import pyotp
import config
import os

# Account details
avanza = Avanza(
    {
        "username": config.avanzaUsername,
        "password": config.avanzaPassword,
        "totpSecret": config.totpSecret,
    }
)

while True:
    try:
        overview = avanza.get_account_overview(config.totpSecret)
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
        time.sleep(config.updateIntervalSeconds)
    except Exception as e:
        print("Error occurred: ", e)
