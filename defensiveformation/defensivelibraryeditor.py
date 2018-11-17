from tkinter import *
from tkinter import messagebox

from defensiveformation.defensiveeditor import DefensiveEditor
from misc.scoutcardmakerexceptions import ScoutCardMakerException


class DefensiveLibraryEditor(Frame):
    def __init__(self, root, controller):
        Frame.__init__(self, root)

        self.controller = controller
        self.controller.editor = self

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        defense_name_frame = Frame(self)
        Label(defense_name_frame, text='Defense Name').pack()
        self.defense_name_entry = Entry(defense_name_frame)
        self.defense_name_entry.pack()
        self.save_defense_btn = Button(defense_name_frame, text='Save Defense', command=self.save_defense)
        self.defense_name_entry.bind('<Return>' , self.save_defense)
        self.save_defense_btn.pack()
        Label(defense_name_frame, text='Composite Defense').pack()
        self.composite_defense_entry = Entry(defense_name_frame)
        self.composite_defense_entry.pack()
        self.load_composite_btn = Button(defense_name_frame, text='Load Defense', command=self.load_composite_defense)
        self.composite_defense_entry.bind('<Return>', self.load_composite_defense)
        self.load_composite_btn.pack()
        defense_name_frame.grid(row=0, column=0, sticky=W)

        defense_library_list_frame = Frame(self)
        Label(defense_library_list_frame, text='Defenses').pack()
        self.delete_selected_btn = Button(defense_library_list_frame, text='Delete Selected Defense', command=self.delete_selected_defense)
        self.delete_selected_btn.pack()
        defense_library_scrollbar = Scrollbar(defense_library_list_frame, orient=VERTICAL)
        self.defense_library_lb = Listbox(defense_library_list_frame, yscrollcommand=defense_library_scrollbar.set)
        defense_library_scrollbar.config(command=self.defense_library_lb.yview)
        defense_library_scrollbar.pack(side=RIGHT, fill=Y, expand=True)
        self.defense_library_lb.pack(side=LEFT, fill=Y, expand=True)
        self.defense_library_lb.bind('<<ListboxSelect>>', lambda e: self.defense_library_on_select(e))
        defense_library_list_frame.grid(row=1, column=0, sticky=N+S)

        defense_editor_frame = Frame(self)
        self.defense_editor = DefensiveEditor(defense_editor_frame, self.controller)
        self.defense_editor.pack(fill=BOTH, expand=True)
        defense_editor_frame.grid(row=0, column=1, rowspan=2, sticky=N+S+E+W)

        self.refresh_library()


    def save_defense(self, *args):
        try:
            affected_defender_tags = self.defense_editor.get_affected_defenders()

            self.controller.save_defense_to_library(self.defense_name_entry.get(), affected_defender_tags)
            self.refresh_library()

        except ScoutCardMakerException as e:
            messagebox.showerror('Save Defense Error', e)

    def load_composite_defense(self, *args):
        try:
            self.controller.load_composite_defense_from_library(self.composite_defense_entry.get())
            self.defense_editor.update_view()
        except ScoutCardMakerException as e:
            messagebox.showerror('Load Composite Defense Error', e)

    def delete_selected_defense(self):
        if self.defense_library_lb.curselection():
            try:
                index = self.defense_library_lb.curselection()[0]
                self.controller.delete_defense_from_library(self.defense_library_lb.get(index))
                self.refresh_library()
            except ScoutCardMakerException as e:
                messagebox.showerror('Delete Defense Error', e)

    def refresh_library(self):
        defenses = self.controller.defense_library.get_sorted_defense_names()
        self.defense_library_lb.delete(0, END)
        for defense in defenses:
            self.defense_library_lb.insert(END, defense)

    def defense_library_on_select(self, event):
        listbox = event.widget
        if listbox.curselection():
            index = listbox.curselection()[0]
            self.defense_name_entry.delete(0,END)
            self.defense_name_entry.insert(0,listbox.get(index))
            self.controller.load_defense_from_library(listbox.get(index))
            self.defense_editor.set_affected_defender_checkboxes()
            self.defense_editor.change_defender() #this forces the editor to update the placement rule gui
            self.defense_editor.update_view()


