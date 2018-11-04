from tkinter import *
from formationvisualeditorcontroller import FormationVisualEditorController
from offense.formationvisualeditor import FormationVisualEditor
from offense.formationlibrary import FormationLibrary

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
