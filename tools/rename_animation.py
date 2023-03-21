import os
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image


class ImageRenamer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Renommer les images")
        self.geometry("800x600")
        # Variables de classe pour stocker les images et leur ordre
        self.images = []
        self.image_order = []

        # Widgets
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Display images
        self.current_image_index = 0
        self.image_label = tk.Label(self.canvas)
        self.image_label.pack()

        # Boutons pour ajouter/supprimer des images
        add_button = tk.Button(self.canvas, text="Ajouter des images", command=self.add_images)
        add_button.pack(side=tk.LEFT, padx=10, pady=10)

        remove_button = tk.Button(self.canvas, text="Supprimer des images", command=self.remove_images)
        remove_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Liste pour afficher les images
        self.image_list = tk.Listbox(self.canvas, selectmode=tk.SINGLE)
        self.image_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Boutons pour déplacer les images
        up_button = tk.Button(self.canvas, text="Monter", command=self.move_up)
        up_button.pack(side=tk.RIGHT, padx=10, pady=10)

        down_button = tk.Button(self.canvas, text="Descendre", command=self.move_down)
        down_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Barre de saisie pour renommer les images
        label = tk.Label(self.canvas, text="Renommer les images :")
        label.pack(side=tk.LEFT, padx=10, pady=10)

        self.entity_entry = tk.Entry(self.canvas, width=10)
        self.entity_entry.pack(side=tk.LEFT, padx=5, pady=10)

        self.action_entry = tk.Entry(self.canvas, width=10)
        self.action_entry.pack(side=tk.LEFT, padx=5, pady=10)

        position_options = ["left", "lefttop", "top", "righttop", "right", "rightbottom", "bottom", "leftbottom"]
        self.position_optionmenu = tk.OptionMenu(self.canvas, tk.StringVar(self), *position_options)
        self.position_optionmenu.pack(side=tk.LEFT, padx=5, pady=10)

        self.increment_entry = tk.Entry(self.canvas, width=10, textvariable=tk.StringVar(self, value='0'))
        self.increment_entry.pack(side=tk.LEFT, padx=5, pady=10)

        # Bouton pour renommer les images
        rename_button = tk.Button(self.canvas, text="Renommer les images", command=self.rename_images)
        rename_button.pack(side=tk.LEFT, padx=10, pady=10)

        play_button = tk.Button(self.canvas, text="Play Images", command=self.start_playing)
        play_button.pack()

    def play_images(self):
        if self.current_image_index < len(self.images):
            image_path = self.images[self.current_image_index]
            image = Image.open(image_path)
            image = image.resize((400, 400), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
            self.current_image_index += 1
            self.canvas.after(100, self.play_images)
        else:
            self.current_image_index = 0
            self.canvas.after(100, self.play_images)

    def start_playing(self):
        self.play_images()

    def add_images(self):
        # Demande à l'utilisateur de sélectionner des fichiers d'image
        filetypes = (("Fichiers image", "*.jpg *.jpeg *.png *.gif"), ("Tous les fichiers", "*.*"))
        filenames = filedialog.askopenfilenames(title="Sélectionnez des images", filetypes=filetypes)

        # Ajoute les images à la liste et les affiche
        for filename in filenames:
            self.images.append(filename)
            self.image_list.insert(tk.END, os.path.basename(filename))
            self.image_order.append(len(self.images) - 1)

    def remove_images(self):
        # Supprime l'image sélectionnée de la liste et de la variable de classe
        index = self.image_list.curselection()
        if index:
            index = int(index[0])
            self.image_list.delete(index)

    def rename_images(self):
        # Récupère les valeurs de la barre de saisie
        entity = self.entity_entry.get()
        action = self.action_entry.get()
        position = self.position_entry.get()
        increment = int(self.increment_entry.get())

        # Renomme les fichiers en fonction de leur ordre et de la barre de saisie
        for i, index in enumerate(self.image_order):
            old_filename = self.images[index]
            new_filename = f"{entity}_{action}_{position}_{i + increment}.png"
            os.rename(old_filename, new_filename)
            self.images[index] = new_filename
            self.image_list.delete(i)
            self.image_list.insert(i, os.path.basename(new_filename))

    def move_up(self):
        # Déplace l'image sélectionnée vers le haut
        index = self.image_list.curselection()
        if index and index[0] > 0:
            index = int(index[0])
            self.image_order[index], self.image_order[index - 1] = self.image_order[index - 1], self.image_order[index]
            self.image_list.delete(index)
            self.image_list.insert(index - 1, os.path.basename(self.images[self.image_order[index - 1]]))
            self.image_list.selection_clear(0, tk.END)
            self.image_list.selection_set(index - 1)

    def move_down(self):
        # Déplace l'image sélectionnée vers le bas
        index = self.image_list.curselection()
        if index and index[0] < len(self.images) - 1:
            index = int(index[0])
            self.image_order[index], self.image_order[index + 1] = self.image_order[index + 1], self.image_order[index]
            self.image_list.delete(index)
            self.image_list.insert(index + 1, os.path.basename(self.images[self.image_order[index + 1]]))
            self.image_list.selection_clear(0, tk.END)
            self.image_list.selection_set(index + 1)


if __name__ == "__main__":
    app = ImageRenamer()
    app.mainloop()
