
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.carousel import Carousel
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty

import glob

from .kv_builder import MenuBuilder, SelectMultipleBuilder


__all__ = ['PicBreeder', 'Menu', 'SelectMultiple']

menu = MenuBuilder()
selection = SelectMultipleBuilder()

Builder.load_string(menu.return_string + selection.return_string)

class PicBreeder(App):

    def build(self):

        self.images_normal, self.images_pressed = self.init_images()

        self.title = 'PicBreeder Interactive Evolution'

        self.selected_parents = ListProperty([])
        self.saved_parents = ListProperty([])

        root = Carousel()

        # Menu page
        root.add_widget(Menu())

        # Selection page
        root.add_widget(SelectMultiple())

        return root

    def init_images(self):

        # These paths should be more general for the current users sys path. These folders will need to be generated each time app is run.
        normal_location = '/home/chad/Documents/research/evolearn/evolearn/applications/interactive_evolution/imgs/normal/*.jpg'
        image_normal_list = []

        for filename in glob.glob(normal_location):
            image_normal_list.append(filename)

        pressed_location = '/home/chad/Documents/research/evolearn/evolearn/applications/interactive_evolution/imgs/pressed/*.jpg'
        image_pressed_list = []

        for filename in glob.glob(pressed_location):
            image_pressed_list.append(filename)

        return image_normal_list, image_pressed_list

    def normal_define(self, id):
        return self.images_normal[id]

    def pressed_define(self, id):
        return self.images_pressed[id]

class Menu(GridLayout):
    pass

class SelectMultiple(GridLayout):

    select_breed = ListProperty([])
    select_breed_limits = [ 5, 8 ]

    select_seed = ListProperty([])
    select_seed_limits = [ 5, 8 ]

    def return_id(self, caller):

        self.check_parents(caller.label)

    def check_parents(self, selected):

        # Remove double-clicked parents
        if selected in self.select_breed:
            self.select_breed.remove(selected)

        # Add new parents
        else:
            self.select_breed.append(selected)

    def clear_selections(self):
        self.select_breed = []


# class TestApp(App):
#
#     selected = ListProperty([])
#     saved_parents = ListProperty([])
#
#     def build(self):
#         self.title = 'PicBreeder Interactive Evolution'
#         root = Carousel()
#
#         # Menu page
#         root.add_widget(Menu()) # 0
#
#         # Start from scratch page - One way to keep scratch and seeds separate would be to
#         #   have one as odd indices and the other as the even (just remember the menu is = slide[0])
#
#         # OR, alternatively, should the best solution be to launch a separate app for each, with its own numbering?
#
#         # ALTHOUGH, if it is truly functional, the only difference between a SCRATCH and SEED trajectory should be the definition of those images.
#         #   Therfore, it could instead be numbered [0]-menu, [1-x]: saved seeds, [x+1:]: interactive evolution based on selected seed (SCRATCH or SAVED)
#
#         root.add_widget(Page()) # 1
#
#         for seeds in range(3):
#
#             # Start from saved seed page
#             root.add_widget(Seeds()) # 2, 3, 4
#
#         return root
#
#     def wrap_up(self, selected, limits):
#
#         if len(selected) >= limits[0] and len(selected) <= limits[1]:
#
#             self.selected = selected
#             self.stop()
#
#     def check_app_access(self, selected, limits):
#         if len(selected) < limits[0]:
#             output = 'Add parents (min %d)' % (limits[0],)
#         elif len(selected) > limits[1]:
#             output = 'Too many (max %d)' % (limits[1], )
#         else:
#             output = 'EVOLVE >'
#         return output
#
#     def save_parents(self, selected, limits):
#
#         if len(selected) >= limits[0] and len(selected) <= limits[1]:
#
#             self.saved_parents = selected