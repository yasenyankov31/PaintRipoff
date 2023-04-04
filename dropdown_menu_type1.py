import tkinter as tk

class DropdownMenu:
    def __init__(self, master, images):
        self.master = master
        self.images = images
        self.options_window=None
        self.button_is_pressed=False
        self.index=0


        # Create the button
        self.button = tk.Button(self.master,image=self.images[0], text='Brushes',compound="top")
        self.button.bind("<ButtonPress>", self.on_press_button)
        self.button.bind("<ButtonRelease>", self.on_realease_button)
        self.button.pack(side=tk.LEFT, padx=2,ipady=15)
        
    

    def force_close(self,_):
        if self.options_window is not None and not self.button_is_pressed:
            self.options_window.destroy()

    def on_realease_button(self,_):
        self.button_is_pressed=False 
    
    def on_press_button(self,_):
        exists=False
        existing_menu=None
        for child in self.master.winfo_children():
            if ".!frame.!toplevel" in str(child).strip():         
                exists=True
                existing_menu=child
        if not exists:
            self.button_is_pressed=True
            # Create the options window 
            self.options_window = tk.Toplevel(self.master)
            self.options_window.title('Options')
            self.options_window.geometry('260x220')
            self.options_window.overrideredirect(True)
            
            
            # Calculate the position of the options window below the button
            x = self.button.winfo_rootx()
            y = self.button.winfo_rooty() + self.button.winfo_height()

            # Set the position of the options window using the place method
            self.options_window.geometry("+%d+%d" % (x, y))

            self.panel = tk.Frame(self.options_window, bd=1, relief=tk.SUNKEN)
            self.panel.pack(fill=tk.BOTH, expand=True)

            row = 0
            column = 0

            for i, image in enumerate(self.images):
                if i % 4 == 0:
                    row += 1
                    column = 0
                column += 1
                option_button = tk.Button(self.panel,image=image,compound="top", command=lambda index=i: self.select_option(index))
                option_button.grid(row=row, column=column, padx=10, pady=10)
        else:
            existing_menu.destroy()
        
    def select_option(self, index):
        self.button.configure(image=self.images[index])
        self.index=index
        self.options_window.destroy()