import requests
import re

addresses = [
    "http://www.mlat.uzh.ch/download_pl/?lang=0&dir=/var/www/Corpus0_Biblia/&file=Vulgata_Clementina.xml&xml=1",
    "http://www.mlat.uzh.ch/download_pl?lang=0&dir=/var/www/Corpus2_PL/&file=034_Augustinus-Hipponensis_De-Genesi-ad-litteram.xml&xml=1",
    "http://www.mlat.uzh.ch/download_pl?lang=0&dir=/var/www/Corpus2_PL/&file=032_Augustinus-Hipponensis_De-libero-arbitrio.xml&xml=1",
    "http://www.mlat.uzh.ch/download_pl?lang=0&dir=/var/www/Corpus2_PL/&file=031_Augustinus-Hipponensis_Confessiones.xml&xml=1",

]

for file in addresses:
    response = requests.get(file)
    stem = re.search(r".*file\=(\d{3}_)?(.*?)\.xml&", file).group(2)
    filename = f"{stem}.html"
    open(filename, "wb").write(response.content)
    print(f"{filename} written.")