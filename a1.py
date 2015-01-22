import os
import shutil

from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk

import cloudinary
import cloudinary.uploader
import cloudinary.api

import json
import wget

class App:

  def __init__(self, master):

    ## Cloudinary setup
    cloudinary.config(
        cloud_name="doe3dftxt",
        api_key="918736736476493",
        api_secret="IXmm50IApSzP14SfFbn9cFWe4-E"
    )

    ## Basic UI
    frame = Frame(master)
    frame.pack(fill=X)
    Label(frame, text="Choose File").grid(row=0, sticky=W)
    Label(frame, text="Enter URL").grid(row=1, sticky=W, pady=20)

    self.file_upload = Button(frame, text="Choose File", command=self.upload_file)
    self.file_upload.grid(row=0, column=1, sticky=E)

    self.url_string = StringVar()
    self.url_upload = Entry(frame, textvariable=self.url_string)
    self.url_upload.grid(row=1, column=1, sticky=E, pady=20)

    self.url_upload_btn = Button(frame, text="Upload URL", command=self.upload_url)
    self.url_upload_btn.grid(row=2, column=1, sticky=E)

    Label(frame, text="Enter Unique Name").grid(row=3, column=0, sticky=E, padx=30)
    self.file_name_string = StringVar()
    self.file_name_entry = Entry(frame, textvariable=self.file_name_string)
    self.file_name_entry.grid(row=3, column=1, sticky=E, padx=30)

    # images
    scrollbar = Scrollbar(frame, orient=VERTICAL)
    self.image_listbox = Listbox(frame, yscrollcommand=scrollbar.set)
    scrollbar.config(command=self.image_listbox.yview)
    # scrollbar.pack(side=RIGHT, fill=Y)
    self.image_listbox.bind('<Double-Button-1>', self.download_file)
    self.image_listbox.grid(row=4)

    self.image_map = {}

    self.refresh_images()

    ## File options
    self.file_opt = {}
    self.file_opt['filetypes'] = [
        ('JPG', '.jpg'),
        ('PNG', '.png'),
        ('BMP', '.bmp')
        ];



  def download_file(self, event):
    img = self.image_listbox.get(self.image_listbox.curselection()[0])
    dl_url = self.image_map[img]
    print "downloading: " + dl_url

    if not os.path.exists('downloads'):
      print "creating download directory"
      os.makedirs('downloads')

    wget.download(dl_url, out='downloads/')

  def upload_file(self):

      f = tkFileDialog.askopenfilename(**self.file_opt)
      print "Uploading file (" + f + ")"

      cloudinary.uploader.upload(f, public_id=self.file_name_string.get())
      self.refresh_images

  def upload_url(self):

      ## TODO -- validate this
      url = self.url_string.get()
      cloudinary.uploader.upload(url)
      print "uploaded url image"

  def __refresh_images(self, next_c):
    all_res = None
    if next_c is not None:
      all_res = cloudinary.api.resources(next_cursor=next_c)
    else:
      all_res = cloudinary.api.resources()

    for res in all_res['resources']:
      self.image_map[res['public_id']] = res['url']
      self.image_listbox.insert(END, res['public_id'])

    if 'next_cursor' in all_res:
      self.__refresh_images(all_res['next_cursor'])

  def refresh_images(self):
      self.__refresh_images(None)

      # if not os.path.exists('tmp'):
      #   print "making tmp dir"
      #   os.makedirs('tmp')

      # for res in all_res['resources']:
      #   wget.download(res['url'], out='tmp/')

      # for img in os.listdir('tmp'):
      #   # self.image_listbox.insert(END, PhotoImage(file='tmp/' + img))
      #   loaded_image = Image.open('tmp/' + img)
      #   self.image_listbox.insert(END, ImageTk.PhotoImage(file='tmp/' + img))

root = Tk()
root.geometry("%dx%d+%d+%d" % (600, 400, 100, 100))
app = App(root)
root.mainloop()
# shutil.rmtree('tmp')
