from notion.client import NotionClient
from notion.block import TextBlock
from notion.block import ImageBlock
from random import randint
from pathlib import Path
import json
import requests


class Automater:
    def __init__(self):
        self.config_file = Path("config.json")
        self.setup()
        self.parsed_config_file = self.load_config()
        self.client = NotionClient(token_v2=self.parsed_config_file["cookie"])

    def setup(self):
        if not self.config_file.exists():
            self.create_files()

        return 0
    
    def create_files(self) -> int:
        if Path("config.json").exists():
            raise FileExistsError("Config file already exists!")

        with open("config.json", 'x') as file:
            print(json.dumps({"use_quotes": "True",
                                "use_memes": "True",
                                "cookie": "",
                                "quotes": [{"file_path": "quotes.txt", "block": ""}],
                                "memes": [{"meme_url": "https://www.reddit.com/r/EarthPorn", "block": ""}]}, indent=4), file=file)
        
        if Path("quotes.json").exists():
            raise FileExistsError("Quote file already exists!")

        with open("quotes.txt", 'x') as file:
            print("quote 1", "author 1\n", "quote 2", "author 2", sep="\n", file=file)

        return 0

    def load_config(self) -> dict:
        with open(self.config_file, 'r') as file:
            parsed_config_file = json.load(file)

        if parsed_config_file["cookie"] == "":
            raise ValueError("The cookie attribute is missing in the config.json file, perhaps the file was only just created?")

        return parsed_config_file

    def generate_everything(self):
        if self.parsed_config_file["use_quotes"] == "True":
            self.generate_quotes()

        if self.parsed_config_file["use_memes"] == "True":
            self.generate_memes()

    def generate_quotes(self):
        for quote_infos in self.parsed_config_file["quotes"]:
            quote_path = Path(quote_infos["file_path"])
            block = quote_infos["block"]
            if not quote_path.exists():
                raise FileNotFoundError("Could not find the quote file %s", quote_path)

            with open(quote_path) as f:
                quote_file = [line for line in f.read().splitlines() if line != ""]
                rand = randint(0, len(quote_file)/2-1)
                quote = quote_file[2*rand]
                author = quote_file[2*rand+1]
            
            page = self.client.get_block(url_or_id=block)
            for child in page.children:
                child.remove()
            
            quote_block = page.children.add_new(TextBlock)
            quote_block.title = quote
            author_block = page.children.add_new(TextBlock)
            author_block.title = "*" + author + "*"
            
    def generate_memes(self):
        for meme_info in self.parsed_config_file["memes"]:
            url = meme_info["meme_url"]
            block = meme_info["block"]
            json_url = url + ".json"
            result = requests.get(json_url, headers={'user-agent':''}).json() # The header is needed to circumvent "Too many Requests" error
            children = result["data"]["children"]
            for child in children:
                try:
                    img_link = child['data']['preview']['images'][0]['source']['url']
                except KeyError:
                    continue

            img_link = img_link.replace('amp;', '')
            page = self.client.get_block(url_or_id=block)
            for child in page.children:
                child.remove()
            
            img_block = page.children.add_new(ImageBlock)
            img_block.set_source_url(img_link)



#block = page.children.add_new(VideoBlock)
#block.set_source_url("https://www.youtube.com/watch?v=E4WlUXrJgy4")

#img = page.children.add_new(ImageBlock)
#img.set_source_url("https://wallpapercave.com/wp/wp9414303.jpg")

# for installing: pip install git+https://github.com/jamalex/notion-py.git@refs/pull/294/merge


if __name__ == "__main__":
    auto = Automater()
    auto.generate_everything()
