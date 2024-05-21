from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.template import loader
import spotipy
import fast_colorthief
from spotipy import SpotifyOAuth
import os
import urllib.parse as parsee
from urllib.request import urlopen
import time
import colorsys
import skimage
# Create your views here.

def landing(request, id=os.getenv("SPOTIPY_CLIENT_ID"), secret=os.getenv("SPOTIPY_CLIENT_SECRET")):
    spauth = SpotifyOAuth(client_id=id, client_secret=secret, redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"), scope="playlist-read-private user-top-read user-library-read")
    destination = spauth.get_authorize_url()
    return HttpResponseRedirect(destination)

def tokenn(request):
    fullurl = request.get_full_path()
    plasentaCode = parsee.urlparse(fullurl)
    realCode = parsee.parse_qs(plasentaCode.query)['code'][0]
    spath = SpotifyOAuth()
    token = spath.get_access_token(realCode, as_dict=False, check_cache=False)
    request.session["TOKEN"] = token
    if(realCode != ""):
        return HttpResponseRedirect("/home/")

def home(request):
    sp = spotipy.Spotify(auth=request.session["TOKEN"])
    items = {}
    i = 0
    while len(items)%50 == 0:
        newshit = sp.current_user_playlists(limit=50, offset=len(items))
        if(len(newshit['items']) != 0):
            for item in newshit['items']:
                hue = colorsys.rgb_to_hls(fast_colorthief.get_dominant_color(skimage.io.imread(item["images"][0]["url"])))[0]
                items[hue] = items.get(hue, []) + [i]
                i += 1
        else:
            break
    items = dict(sorted(items.items()))
    
    context = {
    }
    
    browserr = loader.get_template("browser.html")
    return HttpResponse(browserr.render(context, request))
    