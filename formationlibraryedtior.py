from tkinter import *
from formationlibrary import FormationLibrary


if __name__ == '__main__':

    root = Tk()
    library = FormationLibrary()
    library.load_library('formations.scmfl')

    formations = sorted([formation_name for formation_name in library.formations.keys() ])

    listbox = Listbox(root)

    print(formations)


    root.mainloop()
