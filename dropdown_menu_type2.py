import tkinter as tk
from PIL import ImageTk, Image
import os 

class DropdownMenu:
    def __init__(self, master, images,options_text,size,button):
        self.master = master
        self.images = images
        self.labels=options_text
        self.button=button
        self.size=size
        self.button_is_pressed=False
        self.options_window=None
        
    def force_close(self,_):
        if self.options_window is not None and not self.button_is_pressed:
            self.options_window.destroy()

    def on_press_button(self,_):
        exists=False
        existing_menu=None
        for child in self.master.winfo_children():
            if ".!frame.!toplevel" in str(child).strip():         
                exists=True
                existing_menu=child 
        if not exists:
            self.button_is_pressed=True
            self.options_window = tk.Toplevel(self.master)
            self.options_window.title('Options')
            self.options_window.geometry(self.size)
            self.options_window.overrideredirect(True)
            
            # Calculate the position of the options window below the button
            x = self.button.winfo_rootx()
            y = self.button.winfo_rooty() + self.button.winfo_height()

            # Set the position of the options window using the place method
            self.options_window.geometry("+%d+%d" % (x, y))

            self.panel = tk.Frame(self.options_window, bd=1)
            self.panel.pack(side=tk.LEFT)

            row = 0

            for i, image in enumerate(self.images):
                option_button = tk.Button(self.panel,text=self.labels[i],image=image,bd=0,compound="left",border=0, command=self.select_option)
                option_button.grid(row=row, column=0, padx=10, pady=2)
                row += 1
        else:
            existing_menu.destroy() 

    def on_realease_button(self,_):
        self.button_is_pressed=False

    def select_option(self):
        self.options_window.destroy()
        
# if __name__ == '__main__':
#     root = tk.Tk()
#     root.title('Dropdown Menu Example')
#     sqaure_size=25
#     #load images
#     folder="images/rotations/"
#     shapes_icons=[]
#     labels=["Rotate right 90°",
#             "Rotate left 90°",
#             "    Rotate 180°",
#             "   Flip vertical",
#             "Flip horizontal"]
#     images = os.listdir(folder)

#     for x in range(len(images)):
#         image=folder+images[x]
#         img = Image.open(image)
#         img = img.resize((sqaure_size, sqaure_size))
#         shapes_icons.append(ImageTk.PhotoImage(img))
#     #button for dropdown menu
#     button = tk.Button(root,image=shapes_icons[0],compound="left", text='Rotate')
#     dropdown = DropdownMenu(root, shapes_icons,labels,'130x170',button)
#     # Create the button
    
#     button.bind("<ButtonPress>", dropdown.on_press_button)
#     button.bind("<ButtonRelease>", dropdown.on_realease_button)
#     root.bind("<Button-1>", dropdown.force_close)
#     button.pack()
#     root.mainloop()