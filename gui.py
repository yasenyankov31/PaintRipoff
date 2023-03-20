import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter.colorchooser import askcolor
from PIL import ImageTk, Image

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



class PaintRipOff(tk.Tk):
    def __init__(self):
        super().__init__()
        self.new_color_counter=0
        self.selected_color=1
        
        self.last_x, self.last_y = None, None
        self.draw_color = "black"
        self.draw_size = 5
        self.is_drawing = False

        self.attributes('-fullscreen', False)
        self.bind("<Escape>", lambda event: self.destroy())

        self.color_select = tk.Frame(self)
        self.color_select.grid(row=0, column=5, sticky="nsew")

        #selected color 1
        self.selected_Color_widget("Color\n 1",1,"#000000","#00a2e8")
        #selected color 2
        self.selected_Color_widget("Color\n 2",2,"#FFFFFF","#FFFFFF")

        #color palete
        self.panel = tk.Frame(self)
        self.panel.grid(row=0, column=5, sticky="nsew")
        self.panel.columnconfigure(0, weight=1)

        row = 3
        column = 25

        for i, color in enumerate(colors):   
            if i%10==0:
                row += 1
                column = 25
            column += 1
            r,g,b=color
            color_hex = f'#{r:02x}{g:02x}{b:02x}'
            canvas = tk.Canvas(self.panel, width=15, height=15, background=color_hex, highlightthickness=1, highlightbackground="black")
            canvas.grid(row=row, column=column, padx=1, pady=1)
            canvas.bind("<Button-1>",self.get_background_color)


        self.img = PhotoImage(file="images/raindbow.png")
        self.color_button = tk.Button(self.panel, text="Edit \ncolors",image=self.img, compound="top",command=self.pick_color)
        self.color_button.grid(row=1, column=45, rowspan=10, sticky="nsew", padx=10, pady=10)

        

        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.grid(row=1, column=0, columnspan=len(colors)+1, sticky="nsew")

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)


        

        # Configure grid weights to expand the canvas when the window is resized
        self.rowconfigure(1, weight=1)
        for i in range(len(colors)+1):
            self.columnconfigure(i, weight=1)

    def menu_Bar_widget(self):
        # Create the menu bar
        menubar = tk.Menu(self)

        # Create the file menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.debug)
        filemenu.add_command(label="Open", command=self.debug)
        filemenu.add_command(label="Save", command=self.debug)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # Create the options menu
        optionsmenu = tk.Menu(menubar, tearoff=0)
        optionsmenu.add_command(label="Edit colors", command=self.debug)
        menubar.add_cascade(label="Options", menu=optionsmenu)

        # Create the help menu
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.debug)
        menubar.add_cascade(label="Help", menu=helpmenu)

        # Add the menu bar to the root window
        self.config(menu=menubar)

    def selected_Color_widget(self,text,column,color,bordercolor):
        # New frame for the first color canvas and label
        color_frame = tk.Frame(self.color_select, padx=10, pady=10,highlightthickness=1,highlightbackground=bordercolor)
        color_frame.bind("<Button-1>", lambda event:self.change_draw_color(self,text))
        color_frame.grid(row=3, column=column, sticky="nesw", columnspan=1, rowspan=15)

        # Duplicate of the first color canvas
        color_canvas = tk.Canvas(color_frame, width=25, height=25, background=color, highlightthickness=1, highlightbackground="black")
        color_canvas.bind("<Button-1>",lambda event:self.change_draw_color(self,text))
        color_canvas.pack()

        # Duplicate of the first color label
        color_label = tk.Label(color_frame, text=text)
        color_label.bind("<Button-1>", lambda event:self.change_draw_color(self,text))
        color_label.pack()

    def pick_color(self):
        color = askcolor()
        self.draw_color = color[1]
        
        #add to the color palete
        self.new_color_counter+=1
        name_of_widget=f".!frame.!canvas{self.new_color_counter+20}"
        new_color_box = self.nametowidget(name_of_widget)
        new_color_box.configure(background=color[1])
        if self.selected_color==1:
            selected_color = self.nametowidget(".!frame.!frame.!canvas")
            selected_color.configure(background=color[1])
        else:
            selected_color = self.nametowidget(".!frame.!frame2.!canvas")
            selected_color.configure(background=color[1])  

        if self.new_color_counter==10:
            self.new_color_counter=0

    def change_draw_color(self,event,text):
        color_box=None
        if text == "Color\n 1":
            color_box = self.nametowidget(".!frame.!frame.!canvas")
            frame1 = self.nametowidget(".!frame.!frame")
            frame2 = self.nametowidget(".!frame.!frame2")
            self.selected_color=1
        else:
            color_box = self.nametowidget(".!frame.!frame2.!canvas")
            frame1 = self.nametowidget(".!frame.!frame2")
            frame2 = self.nametowidget(".!frame.!frame")
            self.selected_color=2

        self.draw_color = color_box.cget("background")
        frame1.config(highlightthickness=1, highlightbackground="#00a2e8")
        frame2.config(highlightthickness=1, highlightbackground="#FFFFFF")


    def debug(self,event):
        print("Hello world!",event.widget)      

    def get_background_color(self, event):
        self.draw_color = event.widget.cget("background")
        if self.selected_color==1:
            selected_color = self.nametowidget(".!frame.!frame.!canvas")
            selected_color.configure(background=self.draw_color)
        else:
            selected_color = self.nametowidget(".!frame.!frame2.!canvas")
            selected_color.configure(background=self.draw_color)  

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

app = PaintRipOff()
app.mainloop()
