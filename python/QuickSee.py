#!/usr/bin/python
# A GUI to read txt files
# TODO List:
# 1. Add more opitions in menu
# 2. Add search/replace function
#
# Ver 0.1:  Jenny, 2015/08/17
#           Initial version
#
from os import listdir, getcwd
from os.path import isfile, join, dirname, realpath

'''QuickSee.py
Can change direcotry, select file from the filelist, and
display it, you can edit and save.
It supports only text file.
'''
try:
   # Python2
    import Tix as tix
    #import Tkinter as tk  # use tix instead
    import tkFileDialog as tkfd
except ImportError:
   # Python3
    import tkinter.tix as tix
    #import tkinter as tk  # use tix instead
    import tkinter.filedialog as tkfd

class MyEditor(object):
   def __init__(self, master):
      # control panel
      conf = tix.Frame(master,bg="lightblue",  width=300, padx=1,pady=1)
      conf.grid(row=0,column=0,sticky="nw")
      conf.pack(fill="both", expand=1, side = "left")

      # file list window
      self.files = tix.FileSelectBox(conf, bg='white', width=300, height=760, command=self.dispfile)
      self.files.grid(row=1, column=1,sticky="nw")
      self.files.pack(fill='both', expand=1, side = "bottom")

      # text window
      textw = tix.Frame(master,bg="lightblue", width=900, height=960, padx=5, pady=1)
      textw.grid(row=0,column=1,columnspan=2,sticky="ne")
      textw.pack(fill='both', expand=1, side = "right")

      self.edit = tix.ScrolledText(textw,bg='lightblue', width=900, height=960)
      self.edit.pack()

      # Menu
      menu = tix.Menu(master)
      root.config(menu=menu)
      # file menu
      filemenu = tix.Menu(menu, tearoff=0)
      menu.add_cascade(label="File", menu=filemenu)
      filemenu.add_command(label="New", command=self.new_text)
      filemenu.add_command(label="Open", command=self.file_open)
      filemenu.add_command(label="SaveAs", command=self.file_saveas)
      filemenu.add_separator()
      filemenu.add_command(label="Exit", command=self.do_exit)

      # start with cursor in the editor area
      self.edit.focus()


   def dispfile(self, path):
      text = open(path).read()
      if text != None:
         # delete any old text first
          self.edit.text.delete(0.0, 'end')
          self.edit.text.insert('end', text)

   def new_text(self):
       """clear the text area so you can start new text"""
       self.edit.text.delete(0.0, 'end')

   def file_open(self):
       """open a file to read"""
       # the filetype mask (default is all files)
       mask = \
             [("Text and Python files","*.txt *.py *.pyw"),
                   ("HTML files","*.htm *.html"),
                   ("All files","*.*")]
       fin = tkfd.askopenfile(filetypes=mask, mode='r')

       text = fin.read()
       if text != None:
          # delete any old text first
           self.edit.text.delete(0.0, 'end')
           self.edit.text.insert('end', text)


   def file_saveas(self):
       """get a filename and save your text to it"""
       # default extension is optional, will add .txt if missing
       fout = tkfd.asksaveasfile(mode='w', defaultextension=".txt")
       text2save = str(self.edit.text.get(0.0, 'end'))
       print(text2save)  # test

       fout.write(text2save)
       fout.close()

   def do_exit(self):
       root.destroy()

root = tix.Tk()
# use width x height + x_offset + y_offset (no spaces!)
root.geometry("%dx%d+%d+%d" % (1200, 968, 120, 80))
root['bg']='lightblue'
#root.minsize(width=1200, height=968)
#root.resizable(width="true", height="true")
info1 = "QuickSee "
info2 = "(ctrl+c=copy ctrl+v=paste ctrl+x=cut ctrl+/=select all)"
root.title(info1+info2)
myed = MyEditor(root)
root.mainloop()


