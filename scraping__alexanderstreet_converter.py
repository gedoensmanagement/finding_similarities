from bs4 import BeautifulSoup
from pathlib import Path

def convert_to_txt(filename, outfolder="."):
    """ Converts books downloaded from AlexanderStreet.com 
        with JS_downloader.js (as HTML of the whole page) 
        to pure text files. """

    with open(filename, "r", encoding="utf-8") as f:
        data = f.read()

    soup = BeautifulSoup(data, "html.parser")

    results = soup.find('span', class_="xml-text")  
    # Use find(id = "text-obj-content") if you want to 
    # include the TEI header.
    # The <span class="xml-text"> tag contains the text 
    # of the book and page numbers in brackets like [page XYZ].

    with open(f"{outfolder}/{Path(filename).stem}.txt", "w", encoding="utf-8") as o:
        o.writelines([f"{x}\n" for x in results.stripped_strings])

def main():
    filename = "test.html"
    convert_to_txt(filename)

if __name__ == "__main__":
    main()

