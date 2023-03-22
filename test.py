import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter.colorchooser import askcolor
from PIL import ImageTk, Image
import os
import dropdown_menu_type1
import dropdown_menu_type2

colors = [
    (0, 0, 0),
    (127, 127, 127),
    (136, 0, 21),
    (237, 28, 36),
    (255, 127, 39),
    (255, 242, 0),
    (34, 177, 76),
    (0, 162, 232),
    (63, 72, 204),
    (163, 73, 164),
    (255, 255, 255),
    (195, 195, 195),
    (185, 122, 87),
    (255, 174, 201),
    (255, 201, 14),
    (239, 228, 176),
    (181, 230, 29),
    (153, 217, 234),
    (112, 146, 190),
    (200, 191, 231),
    (255, 255, 255),
    (255, 255, 255),
    (255, 255, 255),
    (255, 255, 255),
    (255, 255, 255),
    (255, 255, 255),
    (255, 255, 255),
    (255, 255, 255),
    (255, 255, 255),
    (255, 255, 255),
]

class PaintApp(tk.Tk):
    def __init__(self):
        super().__init__()
        #brush settings
        self.brush_sizes=[3,7,11,15]
        self.select_color_widgets=[]
        self.brushesh_is_closed=True
        self.new_color_counter=0
        self.selected_color=1
        
        self.last_x, self.last_y = None, None
        self.draw_color = "black"
        self.draw_size = 3
        self.is_drawing = False

        #main window settings
        self.title("Paint")
        self.geometry("800x600")
        self.attributes('-fullscreen', False)
        self.bind("<Escape>", lambda event: self.destroy())

        # Create a toolbar frame and buttons
        self.toolbar = tk.Frame(self, bd=1, relief=tk.RAISED,border=1)
        self.toolbar.grid(row=0, column=0, sticky="ew")

        #Copy paste tools widget
        self.copy_paste_widget()

        #Resize tools widget    
        self.resize_widget()

        #Tools widget
        self.tools_widget()
        
        #Brushes widget
        self.brushes_widget()

        #Shapes widget
        self.shapes_widget()

        #Size of brush drop down menu
        self.brush_size_widget()

        #First color 
        self.selected_colors_widget("Color\n 1","#000000","#00a2e8")
        #Second color 
        self.selected_colors_widget("Color\n 2","#FFFFFF","#FFFFFF")
        #Color palete 
        self.color_palete_widget()
        #Edit color button
        self.edit_colors_widget()

        #White canvas
        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.grid(row=1, column=0, sticky="nsew")


        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)
        print(self.select_color_widgets[0].winfo_children()[0])

        # Configure grid weights to expand the canvas and toolbar when the window is resized
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.toolbar.rowconfigure(0, weight=1)

    def copy_paste_widget(self):
        sqaure_size=15

        #load images
        shapes_icons=[]
        labels=["Paste",
                "Paste from"]


        img_1 = Image.open("images/others/paste_from.png")
        img_1 = img_1.resize((sqaure_size, sqaure_size))
        shapes_icons.append(ImageTk.PhotoImage(img_1))

        img_2 = Image.open("images/others/paste.png")
        img_2 = img_2.resize((sqaure_size, sqaure_size))
        shapes_icons.append(ImageTk.PhotoImage(img_2))

        self.paste_img = PhotoImage(file="images/others/paste.png")
        self.select_button1 = tk.Button(self.toolbar,image=self.paste_img, compound="top", text='Select',bd=0)
        dropdown_1 =dropdown_menu_type2.DropdownMenu(self, shapes_icons,labels,'110x50',self.select_button1)

        self.select_button1.bind("<ButtonPress>",dropdown_1.on_press_button)
        self.select_button1.bind("<ButtonRelease>", dropdown_1.on_realease_button)
        self.bind("<Button-1>", dropdown_1.force_close, add="+")
        self.select_button1.pack(side=tk.LEFT, padx=2)

        self.copy_panel = tk.Frame(self.toolbar, bd=0, relief=tk.SUNKEN)
        self.copy_panel.pack(side=tk.LEFT, padx=5, pady=5)


        self.cut_image = PhotoImage(file="images/others/scissors.png")
        button_cut = tk.Button(self.copy_panel,image=self.cut_image,compound="left",text="Cut",bd=0)
        button_cut.grid(row=0, column=0, padx=5)

        self.copy_image = PhotoImage(file="images/others/copy.png")
        button_copy = tk.Button(self.copy_panel,image=self.copy_image,compound="left",text=f"Copy",bd=0)
        button_copy.grid(row=1, column=0, padx=5)

    def get_background_color(self, event):
        canvas = event.widget
        color = canvas.cget("background")
        print(color)
    
    def resize_widget(self):
        sqaure_size=15

        #load images
        folder="images/selection/"
        shapes_icons_1=[]
        labels_1=["Rectangular selection",
                "Free-form selection",
                "Select all                   ",
                "Inver selection      ",
                "Delete                     "]
        images_1 = os.listdir(folder)

        for x in range(len(images_1)):
            image=folder+images_1[x]
            img = Image.open(image)
            img = img.resize((sqaure_size, sqaure_size))
            shapes_icons_1.append(ImageTk.PhotoImage(img))

        self.select_rect_img = PhotoImage(file="images/others/rect_dots.png")
        self.select_button = tk.Button(self.toolbar,image=self.select_rect_img, compound="top", text='Select',bd=0)

        dropdown_1 =dropdown_menu_type2.DropdownMenu(self, shapes_icons_1,labels_1,'170x140',self.select_button)
        self.select_button.bind("<ButtonPress>",dropdown_1.on_press_button)
        self.select_button.bind("<ButtonRelease>", dropdown_1.on_realease_button)
        self.bind("<Button-1>", dropdown_1.force_close, add="+")
        self.select_button.pack(side=tk.LEFT, padx=2)

        self.resize_panel = tk.Frame(self.toolbar, bd=0, relief=tk.SUNKEN)
        self.resize_panel.pack(side=tk.LEFT, padx=5, pady=5)

        self.crop_image = PhotoImage(file="images/others/crop.png")
        button_crop = tk.Button(self.resize_panel,image=self.crop_image,compound="left",text="Crop",bd=0)
        button_crop.grid(row=0, column=0, padx=5)

        self.resize_image = PhotoImage(file="images/others/resize.png")
        button_resize = tk.Button(self.resize_panel,image=self.resize_image,compound="left",text="Resize",bd=0)
        button_resize.grid(row=1, column=0, padx=5)

        
        #load images
        folder="images/rotations/"
        shapes_icons=[]
        labels=["Rotate right 90°",
                "Rotate left 90°",
                "    Rotate 180°",
                "   Flip vertical",
                "Flip horizontal"]
        images = os.listdir(folder)

        for x in range(len(images)):
            image=folder+images[x]
            img = Image.open(image)
            img = img.resize((sqaure_size, sqaure_size))
            shapes_icons.append(ImageTk.PhotoImage(img))
        #button for dropdown menu
        button = tk.Button(self.resize_panel,image=shapes_icons[0],bd=0,compound="left", text='Rotate')
        dropdown =dropdown_menu_type2.DropdownMenu(self, shapes_icons,labels,'130x140',button)
        # Create the button
        
        button.bind("<ButtonPress>",dropdown.on_press_button)
        button.bind("<ButtonRelease>", dropdown.on_realease_button)
        self.bind("<Button-1>", dropdown.force_close, add="+")
        button.grid(row=2, column=0, padx=5)
        
    def brushes_widget(self):
        sqaure_size=35
        #load images
        folder="images/brushes/"
        shapes_icons=[]
        images = os.listdir(folder)
        for x in range(len(images)):
            image=folder+images[x]
            img = Image.open(image)
            img = img.resize((sqaure_size, sqaure_size))
            shapes_icons.append(ImageTk.PhotoImage(img))
        
        menu=dropdown_menu_type1.DropdownMenu(self.toolbar, shapes_icons)
        self.bind("<Button-1>", menu.force_close, add="+")

    def shapes_widget(self):
        self.shapes_panel = tk.Frame(self.toolbar, bd=1, relief=tk.SUNKEN)
        self.shapes_panel.pack(side=tk.LEFT, padx=5, pady=5)

        sqaure_size=20
        #load images
        folder="images/shapes/"
        self.shapes_icons=[]
        images = os.listdir(folder)
        for x in range(len(images)):
            image=folder+images[x]
            img = Image.open(image)
            img = img.resize((sqaure_size, sqaure_size))
            self.shapes_icons.append(ImageTk.PhotoImage(img))
            

        

        row = 0
        column = 0
        
        for i,image in enumerate(images):
            if i%7==0:
                row += 1
                column = 0
            column += 1
            button = tk.Button(self.shapes_panel,image=self.shapes_icons[i],height=sqaure_size,width=sqaure_size,bd=0)
            button.grid(row=row, column=column, padx=5, pady=5)
        label = tk.Label(self.shapes_panel, text="Shapes")
        label.grid(row=3,column=4)

    def tools_widget(self):
        self.tools_panel = tk.Frame(self.toolbar, bd=0, relief=tk.SUNKEN)
        self.tools_panel.pack(side=tk.LEFT, padx=5, pady=5)

        sqaure_size=20
        # load images
        folder="images/tools/"
        images = os.listdir(folder)
        self.tool_icons=[]
        for x in range(len(images)):
            image=folder+images[x]
            img = Image.open(image)
            img = img.resize((sqaure_size, sqaure_size))
            self.tool_icons.append(ImageTk.PhotoImage(img))

        row = 0
        column = 0
        
        for i,image in enumerate(images):
            if i%3==0:
                row += 1
                column = 0
            column += 1
            button = tk.Button(self.tools_panel,image=self.tool_icons[i],height=sqaure_size,width=sqaure_size,bd=0)
            button.grid(row=row, column=column, padx=5, pady=5)
        label = tk.Label(self.tools_panel, text="Tools")
        label.grid(row=3,column=2)
    
    def brush_size_widget(self):
        # Define a list of image filenames
        images = ["images/brush_size/size_1.png", "images/brush_size/size_2.png", "images/brush_size/size_3.png", "images/brush_size/size_4.png"]
        
        # Create a list to store the image objects
        self.image_objects = []
        # Load the images, resize them to 25 x 25 pixels, and store them in the image_objects list
        for image in images:
            img = Image.open(image)
            img = img.resize((110, 50))
            self.image_objects.append(ImageTk.PhotoImage(img))
            

        # Create a StringVar object to store the selected option
        selected_option = tk.StringVar()

        # Set the default value for the selected_option to the first option in the list
        selected_option.set("Size")

        # Create the Menubutton widget
        option_menu = tk.Menubutton(self.toolbar, textvariable=selected_option, indicatoron=False, borderwidth=1)
        option_menu.pack(side=tk.LEFT, padx=2)

        # Create a menu for the Menubutton widget
        menu = tk.Menu(option_menu, tearoff=False)

        # Add the options as buttons to the menu
        for i in range(4):
            menu.add_command(label="", image=self.image_objects[i], compound="center", command=lambda index=i: self.change_brush_size(index))
            menu.entryconfigure(i, image=self.image_objects[i], compound="center", font=("Arial", 12))

        #Icon image
        icon = Image.open("images/brush_size/size_icon.png")
        icon = icon.resize((50, 50))
        self.icon_image=ImageTk.PhotoImage(icon)

        # Configure the Menubutton widget to display the menu
        option_menu.configure(menu=menu)
        option_menu.config(image=self.icon_image, compound="top")
    
    def selected_colors_widget(self,text,color,bordercolor):
        color_frame = tk.Frame(self.toolbar, padx=10, pady=2,highlightthickness=1,highlightbackground=bordercolor)
        color_frame.bind("<Button-1>",lambda event:self.change_draw_color(self,text))
        color_frame.pack(side=tk.LEFT, padx=2)

        # Duplicate of the first color canvas
        color_canvas = tk.Canvas(color_frame, width=25, height=25,background=color, highlightthickness=1, highlightbackground="black")
        color_canvas.bind("<Button-1>",lambda event:self.change_draw_color(self,text))
        color_canvas.pack()

        # Duplicate of the first color label
        color_label = tk.Label(color_frame, text=text)
        color_label.bind("<Button-1>",lambda event:self.change_draw_color(self,text))
        color_label.pack()
        self.select_color_widgets.append(color_frame)
    
    def edit_colors_widget(self):
        self.color_palete_img = PhotoImage(file="images/others/raindbow.png")
        self.draw_button = tk.Button(self.toolbar,image=self.color_palete_img, compound="top", text='Edit\n colors',command=self.pick_color)
        self.draw_button.pack(side=tk.LEFT, padx=2)
   
    def color_palete_widget(self):
        # Create a color selection panel
        self.panel = tk.Frame(self.toolbar, bd=1, relief=tk.SUNKEN)
        self.panel.pack(side=tk.LEFT, padx=5, pady=5)

        # Add color selection canvases to the panel
        row = 0
        column = 0

        for i, color in enumerate(colors):
            if i%10==0:
                row += 1
                column = 0
            column += 1
            r,g,b=color
            color_hex = f'#{r:02x}{g:02x}{b:02x}'
            canvas = tk.Canvas(self.panel, width=15, height=15, background=color_hex, highlightthickness=1, highlightbackground="black")
            canvas.grid(row=row, column=column, padx=1, pady=1)
            canvas.bind("<Button-1>",self.get_background_color)
            canvas.bind("<Enter>", lambda event, canvas=canvas: canvas.config(highlightthickness=2))
            canvas.bind("<Leave>", lambda event, canvas=canvas: canvas.config(highlightthickness=1))
 
    def start_draw(self, event):
        self.is_drawing = True
        self.last_x, self.last_y = event.x, event.y

    def stop_draw(self, event):
        self.is_drawing = False

    def draw(self, event):
        if self.is_drawing:
            if self.last_x and self.last_y:
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                    width=self.draw_size, fill=self.draw_color, capstyle=tk.ROUND, smooth=tk.TRUE)

            self.last_x, self.last_y = event.x, event.y

    def change_brush_size(self,index):
        self.draw_size = self.brush_sizes[index]

    def pick_color(self):
        color = askcolor()
        self.draw_color = color[1]

    def change_draw_color(self,event,text):
        color_box=None
        frame1 = self.select_color_widgets[0]
        frame2 = self.select_color_widgets[1]
        if text == "Color\n 1":
            color_box = self.nametowidget(str(self.select_color_widgets[0].winfo_children()[0]))
            self.selected_color=1
            frame1.config(highlightthickness=1, highlightbackground="#00a2e8")
            frame2.config(highlightthickness=1, highlightbackground="#FFFFFF")
        else:
            color_box = self.nametowidget(str(self.select_color_widgets[1].winfo_children()[0]))
            self.selected_color=2
            frame1.config(highlightthickness=1, highlightbackground="#FFFFFF")
            frame2.config(highlightthickness=1, highlightbackground="#00a2e8")

        self.draw_color = color_box.cget("background")
        frame1.config(highlightthickness=1, highlightbackground="#00a2e8")
        frame2.config(highlightthickness=1, highlightbackground="#FFFFFF")
if __name__ == '__main__':
    app = PaintApp()
    app.mainloop()
