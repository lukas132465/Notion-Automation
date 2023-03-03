#import notion
from notion.client import NotionClient
from notion.block import TextBlock
from notion.block import ImageBlock
from random import randint

def setup():
    return 0

file_path = ""
cookie = ""
block = ""

with open(file_path) as f:
    file = f.read().splitlines()
    doubles = [i for i in file if i != ""]
    rand = randint(0, len(doubles)/2-1)
    quote = doubles[2*rand]
    author = doubles[2*rand+1]



client = NotionClient(token_v2=cookie)

page = client.get_block(block)

for child in page.children:
    child.remove()

#page2.title = "it worked"
#block = page.children.add_new(VideoBlock)
#block.set_source_url("https://www.youtube.com/watch?v=E4WlUXrJgy4")

text = page.children.add_new(TextBlock)
text.title = quote

by = page.children.add_new(TextBlock)
by.title = "*" + author + "*"

img = page.children.add_new(ImageBlock)
img.set_source_url("https://wallpapercave.com/wp/wp9414303.jpg")

#page.title = "Test"

# for installing: pip install git+https://github.com/jamalex/notion-py.git@refs/pull/294/merge
