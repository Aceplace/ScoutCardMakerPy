from tkinter import *
from formationlibrary import FormationLibrary
from formationlibraryedtior import FormationLibraryEditor
from libraryeditorcontroller import LibraryEditorController

root = Tk()

menubar = Menu(root)

filemenu = Menu(menubar, tearoff = 0)
filemenu.add_command(label='Open Library')
filemenu.add_command(label='Save Library')
filemenu.add_command(label='Save Library As...')
filemenu.add_separator()

menubar.add_cascade(label='File', menu=filemenu)

root.config(menu=menubar)

library = FormationLibrary()
library.load_library('formations.scmfl')

libraryeditor = FormationLibraryEditor(root, LibraryEditorController(library))

libraryeditor.pack(fill=BOTH, expand=True)

root.mainloop()