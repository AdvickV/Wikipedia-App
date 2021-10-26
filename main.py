from tkinter import *
from PIL import Image, ImageTk
import PIL
import wikipedia
import re
from functools import partial
import urllib.request
import webbrowser

IMAGES = []
TITLE = ""
IMG_INDEX = 0

def set_default_image(start=False):
	img = Image.open("logo.png")
	img = img.resize((300, 300))
	img = ImageTk.PhotoImage(img)

	if start is False:
		image_b.config(image=img)
		image_b.photo = img
	else:
		return img

def get_pil_image(image_path):
	img = Image.open(image_path)
	width, height = img.size 
	new_height = 300
	new_width  = new_height * width / height
	img = img.resize((int(new_width), new_height), Image.ANTIALIAS)
	img = ImageTk.PhotoImage(img)
	return img

def change_image():
	global IMG_INDEX
	if IMAGES and TITLE:
		IMG_INDEX += 1

		if IMG_INDEX > len(IMAGES) - 1:
			IMG_INDEX = (IMG_INDEX % len(IMAGES))

		image_path = f"output-images/{TITLE.lower()}{IMG_INDEX}.png"
		urllib.request.urlretrieve(IMAGES[IMG_INDEX], image_path)

		image = get_pil_image(image_path)	
		image_b.config(image=image)
		image_b.photo = image	

def random_article():
	random_title = wikipedia.random(pages=1)
	update_data(random_title)

def open_link():
	if TITLE:
		webbrowser.open(f"https:www.wikipedia.org/wiki/{TITLE}")

def update_data(title, article_window=None):
	global IMAGES, IMG_INDEX, TITLE

	try:
		if article_window:
			article_window.destroy()
		page = wikipedia.page(title, auto_suggest=False)

		IMAGES = [image for image in page.images[1:] if "png" in image or "jpg" in image]
		TITLE = title
		IMG_INDEX = 0

		# Set Title
		summary_title.config(text=title)

		# Set Summary
		summary_text = ''.join(sentence+'.' for sentence in re.split('\.(?=\s*(?:[A-Z]|$))', page.summary, maxsplit=3)[:-1])
		summary.config(text=summary_text)

		# Set Image

		if not IMAGES:
			set_default_image()
		else:		
			# for image in IMAGES:
			image_path = f"output-images/{title.lower()}{IMG_INDEX}.png"
			urllib.request.urlretrieve(IMAGES[0], image_path)

			image = get_pil_image(image_path)	
			image_b.config(image=image)
			image_b.photo = image

				# IMG_INDEX += 1

	except wikipedia.exceptions.DisambiguationError as results:
		article_window2 = Toplevel(window)
		article_window2.title("Choose Article")
		article_window2.config(pady=25, padx=75)

		for title in results.options[:10]:
			if not "(disambiguation)" in title:
				title_b = Button(article_window2, text=title, command=partial(update_data, title, article_window2))
				title_b.pack()
		

def search():
	query = search_ent.get()
	if query and not query.isspace():
		results = wikipedia.search(query, results=10)

		article_window = Toplevel(window)
		article_window.title("Choose Article")
		article_window.config(pady=15, padx=75)

		for title in results:
			if not "(disambiguation)" in title:
				title_b = Button(article_window, text=title, command=partial(update_data, title, article_window))
				title_b.pack()

window = Tk()
window.title("Wikipedia")
icon = PhotoImage(file="logo.png")
window.iconphoto(False, icon)
window.geometry("+0+0")
window.config(padx=30, pady=30)

head_l = Label(window, text="Search Wikipedia", font=("Times New Roman", 20, "bold"))
head_l.grid(column=0, row=0, columnspan=2)

search_ent = Entry(window, width=20)
search_ent.focus() 
search_ent.grid(column=0, row=1, padx=(0, 15), pady=(15, 15))

search_b = Button(window, text="Search", width=20, command=search)
search_b.grid(column=1, row=1, pady=(15, 15))

img = set_default_image(start=True)
image_b = Button(image=img, bd=0, command=change_image)
image_b.grid(column=0, row=2, columnspan=2, pady=(0, 15))

summary_title = Label(window, text="Title", font=("Times New Roman", 20, "bold"))
summary_title.grid(column=0, row=3, columnspan=2)

summary = Label(window, text="This is where the summary is shown.", font=("Times New Roman", 15, "bold"), wraplength=600)
summary.grid(column=0, row=4, columnspan=2, pady=(0, 10))

random_b = Button(window, text="Random Article", width=15, command=random_article)
random_b.grid(column=0, row=5)

open_article_link_b = Button(window, text="Open Article Link", width=15, command=open_link)
open_article_link_b.grid(column=1, row=5)

window.mainloop()
