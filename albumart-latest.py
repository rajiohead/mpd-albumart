#!/usr/bin/python
# Rajiohead's MPD Album Art
# Writes current album art to /tmp/cover
# Original author: Unknown
# Code was 'cleaned up' by sloth, who posted the version I based this on.
# Updated to python3, fixes for albumart.org's cloudflare blocking, and additional cleanup/messmaking done by me
# Original code belongs to whoever wrote it.
import os
import shutil
import cfscrape
import subprocess
import urllib.request
# Cloudflare is annoying, big thanks to cfscrape.

# TODO: fix needless str() calls, clean up, add ability to change res of cover.
#       add image display if user doesn't want to use conky?




scraper = cfscrape.create_scraper()
def copycover(currentalbum, src, dest, defaultfile):
    searchstring = currentalbum
    if not os.path.exists(src):
        search = str(searchstring)
        url = "http://www.albumart.org/index.php?searchk=" + search[:-1] +"&itempage=1&newsearch=1&searchindex=Music" # search[:-1] to get rid of the \n is kind of messy
        cover = str(scraper.get(url).content)
        image = ""
        shig = cover.split('\\n')
        for line in shig:
            if "amazon.com" in line:
                image = line.partition('src="')[2].partition('"')[0]
                image = image.replace("._SL160_", '._SL1000') # Change the number to increase the size!
                print(image)
                break
        if image:
            urllib.request.urlretrieve(image, src)
    if os.path.exists(src):
        shutil.copy(src, dest)
    elif os.path.exists(defaultfile):
        shutil.copy(defaultfile, dest)
    else:
        print("Image not found")

# Path where the images are saved
imgpath = os.getenv("HOME") + "/.covers/"

# image displayed when no image found
noimg = imgpath + "nocover.png"

# Cover displayed by conky/feh/whateveryoulike
cover = "/tmp/cover"

# Name of current album
album = subprocess.check_output("mpc --format %artist%+%album% | head -n 1", shell=True).decode()

# If tags are empty, use noimg.
if album == "":
    if os.path.exists(conkycover):
        os.remove(conkycover)
    if os.path.exists(noimg):
        shutil.copy(noimg, conkycover)
    else:
        print("Image not found!")
else:

    filename = str(imgpath) + str(album) + ".jpg"
    if os.path.exists("/tmp/nowplaying") and os.path.exists("/tmp/cover"):
        nowplaying = open("/tmp/nowplaying").read()
        if nowplaying == album:
            pass
        else:
            copycover(album, filename, cover, noimg)
            open("/tmp/nowplaying", "w").write(album)
    else:
        copycover(album, filename, cover, noimg)
        open("/tmp/nowplaying", "w").write(album)
