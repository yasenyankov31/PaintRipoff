import tkinter as tk
import pygame
import os
import random
from PIL import Image, ImageTk

class DrawApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Paint")
        #ui panel
        self.tools_panel = tk.Frame(self.root, width=200, bg='#D3D3D3',  highlightthickness = 1,highlightbackground="black")
        self.tools_panel.pack(side=tk.LEFT, fill=tk.Y)
        self.ui()

        #pygame canvas
        self.embed_pygame = tk.Frame(self.root, width=500, height=500)
        self.embed_pygame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        os.environ['SDL_WINDOWID'] = str(self.embed_pygame.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        pygame.display.init()
        self.screen = pygame.display.set_mode((500, 500))
        
        self.circle_color = pygame.Color(0)
        self.random_color()
        
        self.color_button = tk.Button(self.tools_panel, text='Random Color', command=self.random_color)
        self.color_button.pack(side=tk.LEFT)

        self.embed_pygame.bind('<Button-1>', self.draw_circle_)
        self.draw_circle = False

        self.mainloop()

    def draw_circle_(self, event):
        self.mouse_pos = event.x,event.y
        self.draw_circle = True   

    def random_color(self):
        self.circle_color.hsla = (random.randrange(360), 100, 50, 100)
    
    def pygame_loop(self):
        self.screen.fill((255, 255, 255))
        if self.draw_circle:
            pygame.draw.circle(self.screen, self.circle_color, self.mouse_pos,250, 10)
        pygame.display.flip()
        self.root.update()  
        self.root.after(100, self.pygame_loop)
        
    def mainloop(self):
        self.pygame_loop()
        self.root.mainloop()

    def ui(self):
        self.color_btns = tk.Frame(self.tools_panel, width=200, bg='#D3D3D3')
        self.color_btns.pack(side=tk.TOP, fill=tk.Y)

        self.color_palete = tk.Frame(self.tools_panel, width=200)
        self.color_palete.pack(side=tk.TOP, fill=tk.Y)
        
        self.shapes_panel = tk.Frame(self.tools_panel, bd=1, relief=tk.SUNKEN,  highlightthickness = 1,highlightbackground="black")
        self.shapes_panel.pack(side=tk.TOP, fill=tk.Y)

        self.rotate_panel = tk.Frame(self.tools_panel, bd=1, relief=tk.SUNKEN,  highlightthickness = 1,highlightbackground="black")
        self.rotate_panel.pack(side=tk.TOP, fill=tk.Y, pady=5)
        self.color_palete_panel = tk.Frame(self.color_palete, highlightthickness = 1,highlightbackground="black", bg='#D3D3D3')
        self.color_palete_panel.pack(side=tk.TOP, padx=5, pady=5)

        row = 0
        column = 0
        COLORS = [
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

        for i, color in enumerate(COLORS):
            if i%10==0:
                row += 1
                column = 0
            column += 1
            r,g,b=color
            color_hex = f'#{r:02x}{g:02x}{b:02x}'
            canvas = tk.Canvas(self.color_palete_panel, width=15, height=15, background=color_hex, highlightthickness=1, highlightbackground="black")
            canvas.grid(row=row, column=column, padx=1, pady=1)




        self.select_color_widget(1,"#000000")
        self.select_color_widget(2,"#FFFFFF")
        self.shapes_widget()
        self.rotate_options_widget()
        

        self.color_palete_img = tk.PhotoImage(file="images/others/raindbow.png")
        self.button3 = tk.Button(self.color_btns,image=self.color_palete_img, compound="top", text='Edit\n colors')
        self.button3.grid(row=0, column=2, sticky="ew", padx=10, pady=10)

        
        # Set the ratio of the panel to the canvas to 1:3
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=3)

    def shapes_widget(self):
        big_frame = tk.Frame(self.shapes_panel, width=200)
        big_frame.pack(side=tk.LEFT, fill=tk.Y)

        shapes_frame = tk.Frame(big_frame, width=200,  highlightthickness = 1,highlightbackground="black")
        shapes_frame.pack(side=tk.BOTTOM, fill=tk.Y)

        sliders_frame = tk.Frame(big_frame, width=200,  highlightthickness = 1,highlightbackground="black")
        sliders_frame.pack(side=tk.BOTTOM, fill=tk.Y)

        label_frame = tk.Frame(self.shapes_panel, width=200)
        label_frame.pack(side=tk.RIGHT, fill=tk.X)

        sqaure_size=20
        #load images
        folder="images/shapes/"
        self.shapes_icons=[]
        images = os.listdir(folder)
        for x in range(len(images)):
            image=folder+images[x]
            images[x]=os.path.splitext(images[x])[0]
            img = Image.open(image)
            img = img.resize((sqaure_size, sqaure_size))
            self.shapes_icons.append(ImageTk.PhotoImage(img))
            

        

        row = 0
        column = 0
        
        for i,image in enumerate(images):
            if i%3==0:
                row += 1
                column = 0
            column += 1
            button = tk.Button(shapes_frame,image=self.shapes_icons[i],height=sqaure_size,width=sqaure_size,  highlightthickness = 1,highlightbackground="black",command=lambda img=image:self.select_shape(img))
            button.grid(row=row, column=column, padx=5, pady=5)

        #opacity slider
        opacity_slider = tk.Scale(sliders_frame, from_=1, to=0, resolution=0.1, orient='horizontal')
        opacity_slider.set(1)
        opacity_slider.pack(side=tk.BOTTOM, fill=tk.Y)
        
        border_slider = tk.Scale(sliders_frame, from_=30, to=0, orient='horizontal')
        border_slider.pack(side=tk.BOTTOM, fill=tk.Y)
        border_slider.set(23)

        custom_font = ("Helvetica", 9,"bold")
        
        label1 = tk.Label(label_frame,text="Border width", font=custom_font)
        label2 = tk.Label(label_frame, text="Opacity", font=custom_font)
        label3 = tk.Label(label_frame, text="Shapes", font=custom_font)

        # use grid to place the labels in a single line
        label1.grid(row=0, column=0, padx=5, pady=15)
        label2.grid(row=1, column=0, padx=5, pady=15)
        label3.grid(row=2, column=0, padx=5, pady=20)

    def select_color_widget(self,index,color):
        # Add buttons to the tools panel
        frame = tk.Frame(self.color_btns,  highlightthickness = 1,highlightbackground="black", bg='white', width=30,height=40)
        frame.bind("<Button-1>",lambda event, idx=index-1: self.change_selected_color(event, idx))
        # Duplicate of the first color canvas
        color_canvas = tk.Canvas(frame, width=25, height=25,background=color, highlightthickness=1, highlightbackground="black")
        color_canvas.bind("<Button-1>",lambda event, idx=index-1: self.change_selected_color(event, idx))
        color_canvas.pack(pady=5)

        # Duplicate of the first color label
        color_label = tk.Label(frame , text="Color "+str(index),bg='white')
        color_label.bind("<Button-1>",lambda event, idx=index-1: self.change_selected_color(event, idx))
        color_label.pack() 

        frame.grid(row=0, column=index-1, sticky="ew", padx=10, pady=10)

    def rotate_options_widget(self):
        font=("Helvetica", 9,"bold")

        input_panel=tk.Frame(self.rotate_panel, width=200)
        input_panel.pack(side=tk.TOP, padx=5, pady=5,anchor="nw")

        label = tk.Label(input_panel, text="Enter angle to  rotate \n the image:",font=font)
        label.pack(side=tk.LEFT, padx=5, pady=5)

        self.input_field = tk.Entry(input_panel,width=5)
        self.input_field.pack(side=tk.LEFT, padx=5, pady=5)

        btn_panel=tk.Frame(self.rotate_panel, width=200)
        btn_panel.pack(side=tk.BOTTOM, padx=5, pady=5)

        self.button_rotate_left_img = tk.PhotoImage(file="images/rotations/rotate_arrow_left.png").subsample(3,3)
        button_rotate_left = tk.Button(btn_panel,image=self.button_rotate_left_img,compound="left", text='Rotate \n right',font=font,
        command=lambda:self.rotate_buttons(1))
        button_rotate_left.pack(side=tk.LEFT, padx=5, pady=5)

        self.button_rotate_right_img = tk.PhotoImage(file="images/rotations/rotate_arrow_right.png").subsample(3,3)
        button_rotate_right = tk.Button(btn_panel,image=self.button_rotate_right_img,compound="right", text='Rotate \n left',font=font,
        command=lambda:self.rotate_buttons(-1))
        button_rotate_right.pack(side=tk.LEFT, padx=5, pady=5)
    
if __name__ == "__main__":
    game = DrawApp()
