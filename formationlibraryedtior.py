from tkinter import *
from formationvisualeditor import FormationVisualEditor


class FormationLibraryEditor(Frame):
    def __init__(self, root, controller):
        Frame.__init__(self, root)

        self.controller = controller

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        formation_entry_frame = Frame(self)
        Label(formation_entry_frame, text='Formation Name:').pack()
        self.formation_name_entry = Entry(formation_entry_frame)
        self.formation_name_entry.pack()
        self.save_formation_btn = Button(formation_entry_frame, text='Save Formation')
        self.save_formation_btn.pack()
        formation_entry_frame.grid(row=0, column=0)

        override_checkboxes_frame = Frame(self)
        self.is_override_cb = Checkbutton(override_checkboxes_frame, text='Override Formation')
        self.is_override_cb.pack(anchor=W)
        self.t_cb = Checkbutton(override_checkboxes_frame, text='T')
        self.t_cb.pack(anchor=W)
        self.h_cb = Checkbutton(override_checkboxes_frame, text='H')
        self.h_cb.pack(anchor=W)
        self.x_cb = Checkbutton(override_checkboxes_frame, text='X')
        self.x_cb.pack(anchor=W)
        self.y_cb = Checkbutton(override_checkboxes_frame, text='Y')
        self.y_cb.pack(anchor=W)
        self.z_cb = Checkbutton(override_checkboxes_frame, text='Z')
        self.z_cb.pack(anchor=W)
        self.q_cb = Checkbutton(override_checkboxes_frame, text='Q')
        self.q_cb.pack(anchor=W)
        override_checkboxes_frame.grid(row=0, column=1, stick=W)

        formation_library_frame = Frame(self)
        Label(formation_library_frame, text='Formations').pack()
        self.delete_selected_btn = Button(formation_library_frame, text='Delete Selected Formation')
        self.delete_selected_btn.pack()
        library_scrollbar = Scrollbar(formation_library_frame, orient=VERTICAL)
        self.library_lb = Listbox(formation_library_frame, yscrollcommand=library_scrollbar.set)
        library_scrollbar.config(command=self.library_lb.yview)
        library_scrollbar.pack(side=RIGHT, fill=Y, expand=True)
        self.library_lb.pack(side=LEFT, fill=Y, expand=True)
        formation_library_frame.grid(row=1, column=0, stick=N+S)

        formation_visual_editor_frame = FormationVisualEditor(self, self.controller)
        formation_visual_editor_frame.grid(row=1, column=1, stick=N+S+E+W)

        self.refresh_library_listbox()

        self.pack(fill=BOTH, expand=True)

    def refresh_library_listbox(self):
        formations = self.controller.formation_library.get_sorted_formation_names_right()
        self.library_lb.delete(0, END)
        for formation in formations:
            self.library_lb.insert(END, formation)




from formationlibrary import FormationLibrary
from libraryeditorcontroller import LibraryEditorController
from formation import Formation

if __name__ == '__main__':

    root = Tk()
    library = FormationLibrary()
    library.load_library('formations.scmfl')

    formations = sorted([formation_name for formation_name in library.formations.keys() ])

    libraryeditor = FormationLibraryEditor(root, LibraryEditorController(library))

    print(formations)


    root.mainloop()
