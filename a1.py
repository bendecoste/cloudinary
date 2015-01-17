from Tkinter import *
import tkFileDialog
import cloudinary
import cloudinary.uploader
import cloudinary.api

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

    # images
    self.image_listbox = Listbox(frame)
    self.image_listbox.grid(row=3)

    self.refresh_images()


    ## File options
    self.file_opt = {}
    self.file_opt['filetypes'] = [
        ('JPG', '.jpg'),
        ('PNG', '.png'),
        ('BMP', '.bmp')
        ];


  def upload_file(self):

      f = tkFileDialog.askopenfilename(**self.file_opt)
      print "Uploading file (" + f + ")"

      cloudinary.uploader.upload(f)

  def upload_url(self):

      ## TODO -- validate this
      url = self.url_string.get()
      cloudinary.uploader.upload(url)
      print "uploaded url image"

  def refresh_images(self):
      resources = cloudinary.api.resources()
      print resources

root = Tk()
app = App(root)
root.mainloop()
