from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
from formationlibrary import FormationLibrary
from formationlibraryedtior import FormationLibraryEditor
from libraryeditorcontroller import LibraryEditorController
from scoutcardmakerexceptions import ScoutCardMakerException

class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        #menu setup
        menubar = Menu(self)
        filemenu = Menu(menubar, tearoff = 0)

        filemenu.add_command(label='Open Library', command=self.open_library)
        filemenu.add_command(label='Save Library', command=self.save_library)
        filemenu.add_command(label='Save Library As...', command=self.save_library_as)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.destroy)

        menubar.add_cascade(label='File', menu=filemenu)
        self.config(menu=menubar)

        #frame set ups
        mainframe = Frame(self)
        mainframe.pack(side=TOP, fill=BOTH, expand=True)
        mainframe.grid_rowconfigure(0, weight=1)
        mainframe.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.library_editor_controller = LibraryEditorController(FormationLibrary())
        self.frames[FormationLibraryEditor] = FormationLibraryEditor(mainframe, self.library_editor_controller)
        self.frames[FormationLibraryEditor].grid(row = 0, column = 0, stick=N+S+E+W)

        self.current_library_filename = None


    def open_library(self):
        try:
            library_filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select library", filetypes=(("Scout Card Maker Library", "*.scmfl"),))
            if library_filename:
                self.library_editor_controller.load_library(library_filename)
                self.current_library_filename = library_filename
        except ScoutCardMakerException as e:
                messagebox.showerror('Open Library Error', e)

    def save_library(self):
        try:
            library_filename = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save library", filetypes=(("Scout Card Maker Library", "*.scmfl"),))
            if library_filename:
                self.library_editor_controller.save_library(library_filename)
                self.current_library_filename = library_filename
        except ScoutCardMakerException as e:
                messagebox.showerror('Save Library Error', e)

    def save_library_as(self):
        try:
            library_filename = filedialog.asksaveasfilename(initialdir=os.getcwd(),
                                                            title='Save library',
                                                            filetypes=(('Scout Card Maker Library', '*.scmfl'),),
                                                            defaultextension='.scmfl')
            if library_filename:
                self.library_editor_controller.save_library(library_filename)
                self.current_library_filename = library_filename
        except ScoutCardMakerException as e:
                messagebox.showerror('Save Library Error', e)



root = App()
root.state('zoomed')
root.mainloop()