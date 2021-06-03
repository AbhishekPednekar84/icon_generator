import os
import asyncio
import time
import json
from PIL import Image
from constants import (
    FAVICON_SIZE,
    APPLE_ICON_SIZES,
    ANDROID_ICON_SIZES,
    ANDROID_BG,
    FAVICON_SIZES,
    ANDROID_BG_HEX,
    OUTPUT_FOLDER,
)
from webmanifest import manifest_data


async def create_main_favicon(file):
    """
    Function to generate the favicon.ico file. The default size is 32x32. The default can be changed in constants.py

    Parameters
    ----------
    file : .PNG

          A png file present in the project root folder
    """
    new_file = file.resize(FAVICON_SIZE)
    new_file.save(f"./{OUTPUT_FOLDER}/favicon.ico", optimize=True)


async def create_apple_icons(file):
    """
    Function to generate the Apple icons. The file dimensions are specified in constants.py in the
    APPLE_ICON_SIZES list

    Parameters
    ----------
    file : .PNG

          A png file present in the project root folder
    """
    for size in APPLE_ICON_SIZES:
        new_file = file.resize(size)
        new_file.save(
            f"./{OUTPUT_FOLDER}/apple-touch-icon-{size[0]}x{size[1]}.png", optimize=True
        )


async def create_android_icons(file):
    """
    Function to generate the Android icons. The file dimensions are specified in constants.py in the ANDROID_ICON_SIZES list. Android icons require a background color. The name and hex code of the color need to be specified in the ANDROID_BG and ANDROID_HEX variables respectively. Defaults to WHITE (#FFFFFF).

    Example: ANDROID_BG="LIME", ANDROID_BG_HEX="#00FF00"

    Parameters
    ----------
    file : .PNG

          A png file present in the project root folder
    """
    for size in ANDROID_ICON_SIZES:
        image_bg = Image.new("RGBA", file.size, f"{ANDROID_BG}")
        file = file.convert("RGBA")
        x, y = file.size
        image_bg.paste(file, (0, 0, x, y), mask=file)

        new_file = image_bg.resize(size)

        new_file.save(
            f"./{OUTPUT_FOLDER}/android-chrome-{size[0]}x{size[1]}.png", optimize=True
        )
        await create_manifest_for_android()


async def create_manifest_for_android():
    """
    Function to generate the site.webmanifest file required for android. The default file contents have been specified in webmanifest.py
    """
    manifest_dict = json.loads(manifest_data)
    manifest_dict["theme_color"] = ANDROID_BG_HEX
    manifest_dict["background_color"] = ANDROID_BG_HEX

    with open(f"./{OUTPUT_FOLDER}/site.webmanifest", "w") as f:
        f.write(json.dumps(manifest_dict, indent=4))


async def create_favicons(file):
    """
    Function to generate the favicons. The file dimensions of all the favicons are specified in constants.py in the FAVICON_SIZES list.

    Parameters
    ----------
    file : .PNG

          A png file present in the project root folder
    """
    for size in FAVICON_SIZES:
        new_file = file.resize(size)
        new_file.save(
            f"./{OUTPUT_FOLDER}/favicon-{size[0]}x{size[1]}.png", optimize=True
        )


async def main():
    if not os.path.exists(f"./{OUTPUT_FOLDER}"):
        os.mkdir(f"./{OUTPUT_FOLDER}")

    location = f"./{OUTPUT_FOLDER}"

    for file in os.listdir(location):
        if file.startswith("android-chrome"):
            path = os.path.join(location, file)
            os.remove(path)

    for file in os.listdir():
        if file.endswith(".png"):
            image = Image.open(file)
            file_name = os.path.splitext(file)
            await create_main_favicon(image)
            await create_apple_icons(image)
            await create_android_icons(image)
            await create_favicons(image)


if __name__ == "__main__":
    asyncio.run(main())
