from tkinter import *
from formation import Formation
from formationvisualeditorcontroller import FormationVisualEditorController
from formationvisualeditor import FormationVisualEditor
from formationlibrary import FormationLibrary

# if __name__=='__main__':
#     root = Tk()
#
#     formation_library = FormationLibrary()
#     formation_library.load_library('formations.scmfl')
#
#     controller = FormationEditorController(Formation())
#     controller.current_formation.copy_formation_from_formation(formation_library.formations['TWIN RT'])
#     FormationEditor(root, controller)
#     root.mainloop()


if __name__=='__main__':
    root = Tk()

    formation_library = FormationLibrary()
    formation_library.load_library('formations.scmfl')

    formation = formation_library.get_composite_formation('Twin RT King Gun')

    controller = FormationVisualEditorController(formation)
    FormationVisualEditor(root, controller)
    root.mainloop()
