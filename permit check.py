#! python3

import requests, re, os, sys

#make sure working directory is set the same as file directory
os.chdir(os.path.dirname(sys.argv[0]))

page = requests.get('https://portal.permit.pcta.org/availability/mexican-border.php', headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
print(page.text)

#make regex for getting only dict
#eval dict
#for loop for finding proper dict key

# bezi kontinualne
# posli email