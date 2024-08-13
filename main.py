import customtkinter
import PIL
import requests
from customtkinter import *
from PIL import Image, ImageTk
from io import BytesIO



#Setting up base url's
base_url = "https://pokeapi.co/api/v2/"
base_image_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self._set_appearance_mode("light")
        self.title("Pokédex ")
        self.geometry("800x400")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.resizable(0, 0) # Don't allow for resizing in the x or y direction. Why?... Because I am lazy.
        self.iconbitmap('icon.ico')
        
        # Entry Frame
        self.entry_frame = customtkinter.CTkEntry(self, placeholder_text="Enter the Pokémon you wish to search for!",fg_color="#be9b7b", 
                                                  placeholder_text_color="#4b3832" ,text_color="#4b3832",
                                                  border_color="#3c2f2f", border_width=2, width=800)
        self.entry_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsw")
        
        # Search Button
        self.button = customtkinter.CTkButton(self, text="Search!", 
                                              command=self.clicked_handler, 
                                              fg_color="#be9b7b", border_color="#3c2f2f", border_width=2, text_color="#4b3832")
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # Labels to display Pokemon data
        self.lblname = CTkLabel(self, bg_color="#EBEBEB", text_color="#4b3832", text=f"Name: ") # type: ignore
        self.lblname.grid(row=4, column=0, padx=10, pady=(10, 0), sticky="w")

        self.lblid = CTkLabel(self, bg_color="#EBEBEB", text_color="#4b3832", text=f"ID: ") # type: ignore
        self.lblid.grid(row=5, column=0, padx=10, pady=(10, 0), sticky="w")

        self.lblheight = CTkLabel(self, bg_color="#EBEBEB", text_color="#4b3832", text=f"Height: m") # type: ignore
        self.lblheight.grid(row=6, column=0, padx=10, pady=(10, 0), sticky="w")

        self.lblweight = CTkLabel(self, bg_color="#EBEBEB", text_color="#4b3832", text=f"Weight: kg") # type: ignore
        self.lblweight.grid(row=7, column=0, padx=10, pady=(10, 0), sticky="w")

        self.image_label = CTkLabel(self, text="", bg_color="#EBEBEB")
        self.image_label.grid(row=4, column=1, padx=10, pady=(10, 0), sticky="w")


    # Event for button clicked
    def clicked_handler(self):
        url = f"{base_url}/pokemon/{self.entry_frame.get().lower()}" #Gets the text from entry and converts it to lower case
        response = requests.get(url)


        # Ensure the request was successful
        if response.status_code == 200:
            
            pokemon_data = response.json()
            pokemon_id = pokemon_data['id']
            height_in_m = pokemon_data['height'] / 10
            weight_in_kg = pokemon_data['weight'] / 10
            self.lblname.configure(text=f"Name: {pokemon_data['name'].capitalize()}")
            self.lblid.configure(text=f"ID: {pokemon_data['id']}")
            self.lblheight.configure(text=f"Height: {height_in_m}m")
            self.lblweight.configure(text=f"Weight: {weight_in_kg}kg")

        else:
            print(f"Failed to retrieve data {response.status_code}")   


        # Creating link for pokemon image
        image_url=f"{base_image_url}{pokemon_id}.png"
        response_image = requests.get(image_url)


        # Ensure the request was successful
        if response_image.status_code == 200 and 'image' in response_image.headers['Content-Type']:
            
            # Load the image data into Pillow
            image_data = BytesIO(response_image.content)
            img = Image.open(image_data)

            tk_image = ImageTk.PhotoImage(img)

            self.image_label.configure(image=tk_image)
            self.image_label.image = tk_image
            
        else:
            print(f"Failed to retrieve data {response_image.status_code}")
            print(f"Content-Type: {response_image.headers['Content-Type']}")
    

app = App()
app.mainloop()