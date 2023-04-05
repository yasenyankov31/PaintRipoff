import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw,ImageGrab
import os


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


class Shape:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        self.radius = 150
        self.angle=0
        self.border_width = 23 #max value 30
        self.alpha = 255 #int(1 * 255)
        self.draw_color=[0,0,0]

    def create_arrow(self,size):
        # Define the arrow shape as a list of points relative to the center
        arrow_points = [
            (-0.5, -size/8),
            (0.5*size, -size/8),
            (0.5*size, -size/4),
            (size, size/8),
            (0.5*size, size/2),
            (0.5*size, 3*size/8),
            (-0.5, 3*size/8)
        ]


        # Translate the arrow points to the center point
        translated_points = [(x*size + self.center_x/3, y*size + self.center_y/1.2) for x, y in arrow_points]

        return translated_points
    
    def create_star(self, size):
        # Define the star points relative to center point (0, 0)
        relative_points = [
            (-25, -40),
            (-15, -15),
            (10, -15),
            (-10, 0),
            (0, 25),
            (-25, 10),
            (-50, 25),
            (-40, 0),
            (-60, -15),
            (-35, -15),
        ]
    
        # Scale the star points and translate to center point
        scaled_points = [(int(self.center_x + size*x)+120, int(self.center_y + size*y)+30) for x,y in relative_points]
    
        return scaled_points

    def create_pentagon(self, size):
        # Define the pentagon points relative to center point (0, 0)
        relative_points = [
            (0, -1),
            (0.951, -0.309),
            (0.588, 0.809),
            (-0.588, 0.809),
            (-0.951, -0.309)
        ]
    
        # Scale the pentagon points and translate to center point
        scaled_points = [(int(self.center_x + size*x), int(self.center_y + size*y)) for x,y in relative_points]
    
        return scaled_points    

    def create_triangle(self, size):
        # Define the triangle points relative to center point (0, 0)
        relative_points = [
            (0, -1),
            (0.866, 0.5),
            (-0.866, 0.5)
        ]

        # Scale the triangle points and translate to center point
        scaled_points = [(int(self.center_x + size*x), int(self.center_y + size*y)) for x,y in relative_points]

        return scaled_points

    def reset_image(self):
        self.image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)
    
    def draw_star(self):
        self.reset_image()
        # Define the points that make up the star
        outer_points = self.create_star(5)
        # Draw the outer star
        self.draw.polygon(outer_points, outline='black', fill=(self.draw_color[0], self.draw_color[1], self.draw_color[2], self.alpha))

        # Define the points that make up the inner star
        inner_points = self.create_star(self.border_width/6)
        # Calculate the centroid of the outer polygon
        cx = sum(x for x, y in outer_points) / len(outer_points)
        cy = sum(y for x, y in outer_points) / len(outer_points)
        # Calculate the offset to move the star to the centroid of the outer polygon
        dx = cx - sum(x for x, y in inner_points) / len(inner_points)
        dy = cy - sum(y for x, y in inner_points) / len(inner_points)
        # Translate the inner polygon to the centroid of the outer polygon
        inner_points = [(x + dx, y + dy) for x, y in inner_points]
        # Draw the inner star
        self.draw.polygon(inner_points, outline='black', fill=(0, 0, 0,0))

    def draw_rectangle(self):
        self.reset_image()
        x0, y0 = 50, 120
        x1, y1 = 350, 270
        offset=75-self.border_width*2.5
        # draw the rectangle with a black border
        self.draw.rectangle((x0, y0, x1, y1), outline='black', fill=(self.draw_color[0], self.draw_color[1], self.draw_color[2], self.alpha))
        if x0+offset!=125:
            self.draw.rectangle((x0+offset, y0+offset, x1-offset, y1-offset), outline="black", fill=(0, 0, 0, 0))
        
    def draw_circle(self):
        self.reset_image()
        # Draw the outer circle
        self.draw.ellipse((self.center_x - self.radius, self.center_y - self.radius, self.center_x + self.radius, self.center_y + self.radius ),
                          outline="black", fill=(self.draw_color[0], self.draw_color[1], self.draw_color[2], self.alpha))

        # Draw the inner circle
        inner_radius = self.radius - 5*(30-self.border_width)
        self.draw.ellipse((self.center_x - inner_radius, self.center_y - inner_radius, self.center_x + inner_radius, self.center_y + inner_radius),
                          outline="black", fill=(0, 0, 0, 0))

    def draw_pentagon(self):
        self.reset_image()
        outer_points = self.create_pentagon(150)
        self.draw.polygon(outer_points, outline='black', fill=(self.draw_color[0], self.draw_color[1], self.draw_color[2], self.alpha))
        inner_points = self.create_pentagon(int(self.border_width/3)*16)
        # Calculate the centroid of the outer polygon
        cx = sum(x for x, y in outer_points) / len(outer_points)
        cy = sum(y for x, y in outer_points) / len(outer_points)
        # Calculate the offset to move the star to the centroid of the outer polygon
        dx = cx - sum(x for x, y in inner_points) / len(inner_points)
        dy = cy - sum(y for x, y in inner_points) / len(inner_points)
        # Translate the inner polygon to the centroid of the outer polygon
        inner_points = [(x + dx, y + dy) for x, y in inner_points]

        # draw the pentagon with a blue outline and filled with white color
        self.draw.polygon(inner_points, outline='black', fill=(0, 0, 0, 0))

    def draw_triangle(self):
        self.reset_image()
        inner_vertices = self.create_triangle(150)
        self.draw.polygon(inner_vertices, outline='black',fill=(self.draw_color[0], self.draw_color[1], self.draw_color[2], self.alpha))
        outter_vertices = self.create_triangle(int(self.border_width/3)*16)
        # Draw the triangle using the polygon function
        self.draw.polygon(outter_vertices, outline='black',fill=(0, 0, 0, 0))

    def map_range(self,value, in_min, in_max, out_min, out_max):
    # Map the value from the input range to the output range
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def draw_arrow(self):
        self.reset_image()
        outer_points = self.create_arrow(17)
        self.draw.polygon(outer_points, outline='black', fill=(self.draw_color[0], self.draw_color[1], self.draw_color[2], self.alpha))
        width=self.map_range(self.border_width,0,30,1,16)
        inner_points = self.create_arrow(width)
        # Calculate the centroid of the outer polygon
        cx = sum(x for x, y in outer_points) / len(outer_points)
        cy = sum(y for x, y in outer_points) / len(outer_points)
        # Calculate the offset to move the star to the centroid of the outer polygon
        dx = cx - sum(x for x, y in inner_points) / len(inner_points)
        dy = cy - sum(y for x, y in inner_points) / len(inner_points)
        # Translate the inner polygon to the centroid of the outer polygon
        inner_points = [(x + dx+dx/3, y + dy) for x, y in inner_points]

        # draw the pentagon with a blue outline and filled with white color
        self.draw.polygon(inner_points, outline='black', fill=(0, 0, 0, 0))

        #self.image.paste(self.image.rotate(90))

    def get_resized_image(self, x, y):
        invert_x = 0
        invert_y = 0

        image_resize_algorithm=Image.BILINEAR
        if x == 0:
            x = 1
        if y == 0:
            y = 1

        if x < 0 and y < 0:
            x = abs(x)
            y = abs(y)
            resized_image = self.image.transpose(method=Image.FLIP_TOP_BOTTOM).resize((x, y),image_resize_algorithm)
            resized_image = resized_image.transpose(method=Image.FLIP_LEFT_RIGHT)
            invert_x = -x
            invert_y = -y
        elif x < 0:
            x = abs(x)
            resized_image = self.image.transpose(method=Image.FLIP_LEFT_RIGHT).resize((x, y), image_resize_algorithm)
            invert_x = -x
        elif y < 0:
            y = abs(y)
            resized_image = self.image.transpose(method=Image.FLIP_TOP_BOTTOM).resize((x, y), image_resize_algorithm)
            invert_y = -y
        else:
            resized_image = self.image.resize((x, y), image_resize_algorithm)

        return resized_image, invert_x, invert_y
    
    def change_draw_color(self,new_color):
        self.draw_color.clear()
        for color in new_color:
            self.draw_color.append(color)

#shape_type,bd_width,bd_color
class ImageSpecs:
    def __init__(self,shape_type,border_color,border_width,opacity,tk_image):
        self.shape_type=shape_type
        self.border_color=border_color
        self.border_width=border_width
        self.opacity=opacity
        self.tk_image=tk_image
        self.angle=0

class EditShapes:
    def __init__(self,canvas):
        #draw variables         
        self.first_x,self.first_y= None, None
        self.last_x, self.last_y = None, None
        self.is_dragging=False
        self.is_stretching=False
        self.image_specs={}
        self.shape_counter=0
        self.canvas=canvas
        self.selection_tool=False
        self.shape_type="star"
        self.selection_rectangle = None
        
        #stretch variables
        self.first_stretch_x,self.first_stretch_y= None, None
        self.last_stretch_x, self.last_stretch_y = None, None
        self.delete_origin=False

        #selection variables
        self.shape_dragged=False
        self.selected_shapes_tag=[]
        self.selected_shapes_init_size=[]
        self.click_shape_x,self.click_shape_y=0,0
        
        #move/drag variables
        self.selected_rect=None

        self.shape = Shape(400, 400)
        self.image_tk = ImageTk.PhotoImage(self.shape.image)
    #draw
    def start_draw(self,event):
        if len(self.canvas.find_withtag(tk.CURRENT))==0:
            self.selected_shapes_tag.clear()
            self.selected_shapes_init_size.clear()
            self.shape_dragged=False
            self.canvas.delete("border","bottom_btn","top_btn","left_btn","right_btn")
            
        if not self.selection_tool:
            self.first_x, self.first_y = event.x, event.y            
            self.shape_dragged=False
            match self.shape_type:
                case "star":
                    self.shape.draw_star()
                case "rectangle":
                    self.shape.draw_rectangle()
                case "circle":
                    self.shape.draw_circle()
                case "pentagon":
                    self.shape.draw_pentagon()
                case "arrow":
                    self.shape.draw_arrow()
                case "triangle":
                    self.shape.draw_triangle()
        else:
            self.selection_rectangle = (event.x, event.y, event.x, event.y)

    def stop_draw(self, event):
        if self.is_dragging:
            self.is_dragging = False
            self.canvas.delete("shape")
            tag=f"{self.shape_type}_shape_{self.shape_counter}"
            colors=[]
            for x in self.shape.draw_color:
                colors.append(x)

            specs=ImageSpecs(self.shape_type,colors,self.shape.border_width,self.shape.alpha,self.image_tk)

            self.image_specs[tag]=specs
            image_object=self.canvas.create_image(self.last_x, self.last_y, image=self.image_specs[tag].tk_image, anchor=tk.NW,tag=tag)
            self.canvas.tag_bind(image_object, "<ButtonPress-1>",lambda event,tag=tag: self.selected_shape(event,tag))
            self.canvas.tag_bind(image_object, "<B1-Motion>",lambda event,tag=tag: self.drag_shape(event,tag))
            self.selected_shape(event,tag)
            self.shape_dragged=False
            self.shape_counter+=1
        #delete selection rectangle
        if self.selection_tool and not self.is_stretching:
            x0, y0, x1, y1 = self.selection_rectangle
            item_id=self.canvas.create_rectangle(x0, y0, x1, y1,tags="sel_rect")
            overlapping_items = self.canvas.find_overlapping(*self.canvas.bbox(item_id))
            overlapping_items = [tag for tag in overlapping_items if tag != item_id and self.canvas.type(tag) == "image"]
            for item in overlapping_items:
                tag = self.canvas.gettags(item)[0]
                if tag not in self.selected_shapes_tag:
                    self.selected_shapes_tag.append(tag)
                if self.canvas.bbox(item) not in self.selected_shapes_init_size:
                    self.selected_shapes_init_size.append(self.canvas.bbox(item))
            if len(overlapping_items) > 1:
                bbox_coords = [self.canvas.bbox(item) for item in overlapping_items]
                x1, y1 = min(coord[0] for coord in bbox_coords), min(coord[1] for coord in bbox_coords)
                x2, y2 = max(coord[2] for coord in bbox_coords), max(coord[3] for coord in bbox_coords)
                width = x2 - x1
                height = y2 - y1
                
                self.selected_rect=self.canvas.create_rectangle(x1, y1, x1+width, y1+height, outline='red', width=2,tag="border",dash=(10,10))

                stretch_btn_offset=10
                x1_ = x1+(width/2)
                y1_ = y1+height

                self.bottom_resize=self.canvas.create_rectangle(x1_,y1_, x1_+stretch_btn_offset, y1_+stretch_btn_offset,fill='white',tag="bottom_btn", outline='black', width=2)
                self.canvas.tag_bind(self.bottom_resize, "<ButtonPress-1>",lambda  event:self.enable_stretch(event))
                self.canvas.tag_bind(self.bottom_resize, "<B1-Motion>",lambda event:self.stretch_image(event,"bottom_btn"))
                self.canvas.tag_bind(self.bottom_resize, "<ButtonRelease-1>",lambda event:self.stop_stretch(event))
                

                self.top_resize=self.canvas.create_rectangle(x1_-5,y1, x1_+5, y1-stretch_btn_offset,fill='white',tag="top_btn", outline='black', width=2)
                self.canvas.tag_bind(self.top_resize, "<ButtonPress-1>",lambda  event:self.enable_stretch(event))
                self.canvas.tag_bind(self.top_resize, "<B1-Motion>",lambda event:self.stretch_image(event,"top_btn"))
                self.canvas.tag_bind(self.top_resize, "<ButtonRelease-1>",lambda event:self.stop_stretch(event))

                y1_ = y1+(height/2)
                x1_ = x1+width

                self.left_resize=self.canvas.create_rectangle(x1,y1_, x1-stretch_btn_offset, y1_+stretch_btn_offset,fill='white',tag="left_btn", outline='black', width=2)
                self.canvas.tag_bind(self.left_resize, "<ButtonPress-1>",lambda  event:self.enable_stretch(event))
                self.canvas.tag_bind(self.left_resize, "<B1-Motion>",lambda event:self.stretch_image(event,"left_btn"))
                self.canvas.tag_bind(self.left_resize, "<ButtonRelease-1>",lambda event:self.stop_stretch(event))
                
                

                self.right_resize=self.canvas.create_rectangle(x1_,y1_, x1_+stretch_btn_offset, y1_+stretch_btn_offset,fill='white',tag="right_btn", outline='black', width=2)
                self.canvas.tag_bind(self.right_resize, "<ButtonPress-1>",lambda  event:self.enable_stretch(event))
                self.canvas.tag_bind(self.right_resize, "<B1-Motion>",lambda event:self.stretch_image(event,"right_btn"))
                self.canvas.tag_bind(self.right_resize, "<ButtonRelease-1>",lambda event:self.stop_stretch(event))

            elif len(overlapping_items) == 1 and len(self.selected_shapes_tag)==1:
                self.selected_shape(event, self.selected_shapes_tag[0])

            self.canvas.delete("sel_rect")

    def drag_draw(self, event):
        #draw selection rectangle
        if not self.shape_dragged and not self.is_stretching:
            if self.selection_tool:
                self.canvas.delete("sel_rect")
                self.selection_rectangle = (self.selection_rectangle[0], self.selection_rectangle[1], event.x, event.y)
                x0, y0, x1, y1 = self.selection_rectangle
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags="sel_rect", width=2,dash=(10,10))

            else:
                self.is_dragging=True
                x, y = event.x - self.first_x, event.y - self.first_y
                resized_image, invert_x, invert_y = self.shape.get_resized_image(x, y)
                self.last_x=self.first_x + invert_x
                self.last_y=self.first_y + invert_y
                self.image_tk = ImageTk.PhotoImage(resized_image)
                self.canvas.delete("shape")

                self.canvas.create_image(self.last_x, self.last_y, image=self.image_tk, anchor=tk.NW,tag="shape")

    #stretch after draw
    def enable_stretch(self,event):
        if not self.is_dragging:
            self.canvas.delete("border")
            self.first_stretch_x=event.x
            self.first_stretch_y=event.y
            self.is_stretching=True

    def calculate_stretch(self,event,new_width,new_height,button_tag):
        for index, tag in enumerate(self.selected_shapes_tag):
            img_specs=self.image_specs[tag]
            self.image_widget=self.canvas.find_withtag(tag)[0]
            x1, y1, x2, y2 = self.selected_shapes_init_size[index]
            if button_tag=="right_btn":
                width = x2 - x1 - new_width
            else:
                width = x2 - x1 + new_width

            height = y2 - y1 - new_height
            

            if height>1 and width>1:
                match img_specs.shape_type:
                    case "star":
                        self.shape.draw_star()
                    case "rectangle":
                        self.shape.draw_rectangle()
                    case "circle":
                        self.shape.draw_circle()
                    case "pentagon":
                        self.shape.draw_pentagon()
                    case "arrow":
                        self.shape.draw_arrow()
                    case "triangle":
                        self.shape.draw_triangle()

                self.rotated_image = self.shape.image.rotate(self.image_specs[tag].angle,expand=False).resize((width, height), Image.BILINEAR)
                self.image_specs[tag].tk_image=ImageTk.PhotoImage(self.rotated_image)
                self.canvas.itemconfig(self.image_widget, image=self.image_specs[tag].tk_image)
                if button_tag=="left_btn":
                    self.canvas.coords(self.image_widget,x1-new_width,y1)
                if button_tag=="top_btn":
                    self.canvas.coords(self.image_widget,x1,y1+new_height)
        
        x1,y1,x2,y2=self.canvas.coords(button_tag)
        if button_tag=="right_btn" or  button_tag=="left_btn":
            self.canvas.coords(button_tag, event.x,y1,event.x+10,y2)
        else:
            self.canvas.coords(button_tag, x1,event.y,x2,event.y+10)                        
            
    def stretch_image(self,event,tag):
        if self.is_stretching:
            new_height=self.first_stretch_y-event.y
            new_width=self.first_stretch_x-event.x

            match tag:
                case "bottom_btn":
                    self.canvas.delete("resize","top_btn","left_btn","right_btn")
                    self.calculate_stretch(event,0,new_height,tag)
                     
                case "right_btn":
                    self.canvas.delete("resize","top_btn","left_btn","bottom_btn")
                    self.calculate_stretch(event,new_width,0,tag)

                case "left_btn":
                    self.canvas.delete("resize","top_btn","right_btn","bottom_btn")
                    self.calculate_stretch(event,new_width,0,tag)

                case "top_btn":
                    self.canvas.delete("resize","bottom_btn","left_btn","right_btn")
                    new_height = event.y - self.first_stretch_y
                    self.calculate_stretch(event,0,new_height,tag)
                                                   
    def stop_stretch(self,event):
        self.selected_shapes_init_size.clear()
        self.canvas.delete("resize","top_btn","left_btn","right_btn","bottom_btn")
        if len(self.selected_shapes_tag)==1:
            self.selected_shape(event,self.selected_shapes_tag[0])
        
        self.is_stretching=False
        self.delete_origin=False
    
    def check_overlapp(self,item_id):
        overlapping_items = self.canvas.find_overlapping(*self.canvas.bbox(item_id))
        overlapping_items = [tag for tag in overlapping_items if tag != item_id and self.canvas.type(tag) == "image"]

        if overlapping_items:
            # There is an image behind the current image
            # do something here
            print(len(overlapping_items))
    #select 
    def selected_shape(self,event,tag):
        self.selected_shapes_tag.clear()
        self.selected_shapes_init_size.clear()
        image_id=self.canvas.find_withtag(tag)[0]
        bbox=self.canvas.bbox(image_id)
        self.check_overlapp(image_id)
        if tag not in self.selected_shapes_tag:
            self.selected_shapes_tag.append(tag)

        if bbox not in self.selected_shapes_init_size:
            self.selected_shapes_init_size.append(bbox)

        self.canvas.delete("border","bottom_btn","top_btn","left_btn","right_btn")
        # Get the rectangle's coordinates and size
        x1, y1, x2, y2 = bbox
        width = x2 - x1
        height = y2 - y1
        
        self.click_shape_x=event.x
        self.click_shape_y=event.y
        
        self.selected_rect=self.canvas.create_rectangle(x1, y1, x1+width, y1+height, outline='red', width=2,tag="border",dash=(10,10))

        stretch_btn_offset=10
        x1_ = x1+(width/2)
        y1_ = y1+height

        self.bottom_resize=self.canvas.create_rectangle(x1_,y1_, x1_+stretch_btn_offset, y1_+stretch_btn_offset,fill='white',tag="bottom_btn", outline='black', width=2)
        self.canvas.tag_bind(self.bottom_resize, "<ButtonPress-1>",lambda  event:self.enable_stretch(event))
        self.canvas.tag_bind(self.bottom_resize, "<B1-Motion>",lambda event:self.stretch_image(event,"bottom_btn"))
        self.canvas.tag_bind(self.bottom_resize, "<ButtonRelease-1>",lambda event:self.stop_stretch(event))
        

        self.top_resize=self.canvas.create_rectangle(x1_-5,y1, x1_+5, y1-stretch_btn_offset,fill='white',tag="top_btn", outline='black', width=2)
        self.canvas.tag_bind(self.top_resize, "<ButtonPress-1>",lambda  event:self.enable_stretch(event))
        self.canvas.tag_bind(self.top_resize, "<B1-Motion>",lambda event:self.stretch_image(event,"top_btn"))
        self.canvas.tag_bind(self.top_resize, "<ButtonRelease-1>",lambda event:self.stop_stretch(event))

        y1_ = y1+(height/2)
        x1_ = x1+width

        self.left_resize=self.canvas.create_rectangle(x1,y1_, x1-stretch_btn_offset, y1_+stretch_btn_offset,fill='white',tag="left_btn", outline='black', width=2)
        self.canvas.tag_bind(self.left_resize, "<ButtonPress-1>",lambda  event:self.enable_stretch(event))
        self.canvas.tag_bind(self.left_resize, "<B1-Motion>",lambda event:self.stretch_image(event,"left_btn"))
        self.canvas.tag_bind(self.left_resize, "<ButtonRelease-1>",lambda event:self.stop_stretch(event))
        
        

        self.right_resize=self.canvas.create_rectangle(x1_,y1_, x1_+stretch_btn_offset, y1_+stretch_btn_offset,fill='white',tag="right_btn", outline='black', width=2)
        self.canvas.tag_bind(self.right_resize, "<ButtonPress-1>",lambda  event:self.enable_stretch(event))
        self.canvas.tag_bind(self.right_resize, "<B1-Motion>",lambda event:self.stretch_image(event,"right_btn"))
        self.canvas.tag_bind(self.right_resize, "<ButtonRelease-1>",lambda event:self.stop_stretch(event))

    def draw_border(self,dx, dy):
        self.canvas.move(self.selected_rect, dx, dy)
    
    def enable_selection_tool(self):
        self.selection_tool=True

    #move/drag
    def drag_shape(self,event,tag):
        self.shape_dragged=True
        item_id = self.canvas.find_withtag(tag)[0]
        # Set the new coordinates based on the mouse position

        dx=event.x-self.click_shape_x
        dy=event.y-self.click_shape_y

        self.canvas.move(item_id,dx, dy)
        self.canvas.move(self.bottom_resize,dx, dy)
        self.canvas.move(self.top_resize,dx, dy)
        self.canvas.move(self.left_resize,dx, dy)
        self.canvas.move(self.right_resize,dx, dy)
        self.click_shape_x=event.x
        self.click_shape_y=event.y 
        
        self.canvas.after(5, lambda dx=dx, dy=dy:self.draw_border(dx, dy))

    def update_shape(self,tag):
        image_id=self.canvas.find_withtag(tag)[0]
        self.img_specs=self.image_specs[tag]
        x1, y1, x2, y2 = self.canvas.bbox(image_id)
        width = x2 - x1
        height = y2 - y1
        match self.img_specs.shape_type:
            case "star":
                self.shape.draw_star()
            case "rectangle":
                self.shape.draw_rectangle()
            case "circle":
                self.shape.draw_circle()
            case "pentagon":
                self.shape.draw_pentagon()
            case "arrow":
                self.shape.draw_arrow()
            case "triangle":
                self.shape.draw_triangle()


        self.img_specs.angle%=360
        self.shape.angle=self.img_specs.angle
        self.img_specs.tk_image=ImageTk.PhotoImage(self.shape.image.rotate(self.shape.angle,expand=False).resize((width, height), Image.BILINEAR))

        self.canvas.itemconfig(image_id, image=self.img_specs.tk_image)
        self.shape.angle=0

    def change_opacity(self,val):
        for tag in self.selected_shapes_tag:
            self.shape.alpha=int(float(val)*255)
            self.shape.change_draw_color(self.image_specs[tag].border_color)
            self.shape.border_width=self.image_specs[tag].border_width
            self.update_shape(tag)
            self.image_specs[tag].opacity=self.shape.alpha

    def change_border_width(self,val):
        for tag in self.selected_shapes_tag:
            self.shape.border_width=30-int(val)
            self.shape.change_draw_color(self.image_specs[tag].border_color)
            self.shape.alpha=self.image_specs[tag].opacity
            self.update_shape(tag)
            self.image_specs[tag].border_width=self.shape.border_width

    def change_shape_color(self, color):
        if not self.selected_shapes_tag:
            self.shape.change_draw_color([int(color[i:i+2], 16) for i in (1, 3, 5)])
            return
        
        for tag in self.selected_shapes_tag:
            shape_specs = self.image_specs[tag]
            shape_specs.border_color = [int(color[i:i+2], 16) for i in (1, 3, 5)]
            self.shape.change_draw_color(shape_specs.border_color)
            self.shape.border_width = shape_specs.border_width
            self.shape.alpha = shape_specs.opacity
            self.update_shape(tag)

    def rotate_shape(self,angle):
        for tag in self.selected_shapes_tag:
            # Convert the PhotoImage to a PIL Image
            self.image_specs[tag].angle+=angle
            self.shape.change_draw_color(self.image_specs[tag].border_color)
            self.shape.alpha=self.image_specs[tag].opacity
            self.shape.border_width=self.image_specs[tag].border_width
            self.update_shape(tag)

    def delete_shape(self,event):
        if event.keysym =='Delete':
            for tag in self.selected_shapes_tag:
                self.canvas.delete(tag,"border","bottom_btn","top_btn","left_btn","right_btn") 
                del self.image_specs[tag]
            self.selected_shapes_tag.clear()

class DrawApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Paint")
        self.geometry("1200x600")
        self.attributes('-fullscreen', False)
        self.bind("<Escape>", lambda event: self.destroy())
        self.settings_menu()

        self.file_name=""
        self.selected_color_index=0
        self.color_palete_index=0
        self.previous_shape_border=None
        
        # Create the panel on the left
        self.tools_panel = tk.Frame(self, width=200, bg='#D3D3D3',  highlightthickness = 1,highlightbackground="black")
        self.tools_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        self.color_btns = tk.Frame(self.tools_panel, width=200, bg='#D3D3D3')
        self.color_btns.pack(side=tk.TOP, fill=tk.Y)

        self.color_palete = tk.Frame(self.tools_panel, width=200)
        self.color_palete.pack(side=tk.TOP, fill=tk.Y)
        
        self.shapes_panel = tk.Frame(self.tools_panel, bd=1, relief=tk.SUNKEN,  highlightthickness = 1,highlightbackground="black")
        self.shapes_panel.pack(side=tk.TOP, fill=tk.Y)

        self.rotate_panel = tk.Frame(self.tools_panel, bd=1, relief=tk.SUNKEN,  highlightthickness = 1,highlightbackground="black")
        self.rotate_panel.pack(side=tk.TOP, fill=tk.Y, pady=5)

                
        # Create the canvas on the right
        self.canvas = tk.Canvas(self, bg='white', width=600)
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        

        self.edit_shape=EditShapes(self.canvas)

        self.selection_img = tk.PhotoImage(file="images/others/rect_dots.png")
        self.selection_button = tk.Button(self.tools_panel,image=self.selection_img, compound="top", text='Select',command=self.edit_shape.enable_selection_tool)
        self.selection_button.pack(side=tk.TOP, fill=tk.Y, pady=1)

        row = 0
        column = 0
        
        # Create a color selection panel
        self.color_palete_panel = tk.Frame(self.color_palete, highlightthickness = 1,highlightbackground="black", bg='#D3D3D3')
        self.color_palete_panel.pack(side=tk.TOP, padx=5, pady=5)


        for i, color in enumerate(COLORS):
            if i%10==0:
                row += 1
                column = 0
            column += 1
            r,g,b=color
            color_hex = f'#{r:02x}{g:02x}{b:02x}'
            canvas = tk.Canvas(self.color_palete_panel, width=15, height=15, background=color_hex, highlightthickness=1, highlightbackground="black")
            canvas.grid(row=row, column=column, padx=1, pady=1)
            canvas.bind("<Button-1>",self.change_color)




        self.select_color_widget(1,"#000000")
        self.select_color_widget(2,"#FFFFFF")
        self.shapes_widget()
        self.rotate_options_widget()
        
        self.color_btns.winfo_children()[self.selected_color_index].winfo_children()[0].create_rectangle(0, 0, 27, 27,outline='#00a2e8', width=10)

        self.color_palete_img = tk.PhotoImage(file="images/others/raindbow.png")
        self.button3 = tk.Button(self.color_btns,image=self.color_palete_img, compound="top", text='Edit\n colors',command=self.pick_color)
        self.button3.grid(row=0, column=2, sticky="ew", padx=10, pady=10)

        self.canvas.bind("<B1-Motion>", self.edit_shape.drag_draw)
        self.canvas.bind("<ButtonPress-1>", self.edit_shape.start_draw)
        self.canvas.bind("<ButtonRelease-1>", self.edit_shape.stop_draw)
        self.bind("<KeyPress>", self.edit_shape.delete_shape)
        
        # Set the ratio of the panel to the canvas to 1:3
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
    
    def pick_color(self):
        color = askcolor()
        self.color_palete_panel.winfo_children()[self.color_palete_index+20].configure(background=color[1])
        self.color_btns.winfo_children()[self.selected_color_index].winfo_children()[0].configure(background=color[1])
        self.color_palete_index+=1
        if self.color_palete_index==10:
            self.color_palete_index=0
        self.edit_shape.change_shape_color(color[1])

    def change_color(self,event):
        color=event.widget.cget("background")
        self.edit_shape.change_shape_color(color)
        self.color_btns.winfo_children()[self.selected_color_index].winfo_children()[0].configure(background=color)

    def change_selected_color(self,event,index):
        self.color_btns.winfo_children()[self.selected_color_index].winfo_children()[0].delete("all")
        self.color_btns.winfo_children()[self.selected_color_index].winfo_children()[0].create_rectangle(0, 0, 27, 27,outline='white', width=10)
        self.selected_color_index=index
        
        color=self.color_btns.winfo_children()[self.selected_color_index].winfo_children()[0].cget("background")
        self.edit_shape.change_shape_color(color)
        self.color_btns.winfo_children()[self.selected_color_index].winfo_children()[0].delete("all")
        self.color_btns.winfo_children()[self.selected_color_index].winfo_children()[0].create_rectangle(0, 0, 27, 27,outline='#00a2e8', width=10)

    def select_shape(self,shape_type,border):
        if self.previous_shape_border is not None:
            self.previous_shape_border.config(highlightbackground="gray")
        self.edit_shape.shape_type=shape_type
        border.config(highlightbackground="#363636")
        self.previous_shape_border=border
        self.edit_shape.selection_tool=False

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
            buttonborder = tk.Frame(shapes_frame, highlightbackground="gray",highlightthickness=3, bd=0)
            button = tk.Button(buttonborder,image=self.shapes_icons[i],height=sqaure_size,width=sqaure_size,command=lambda img=image,
                               border=buttonborder:self.select_shape(img,border))
            button.pack()
            buttonborder.grid(row=row, column=column, padx=5, pady=5)

        #opacity slider
        opacity_slider = tk.Scale(sliders_frame, from_=1, to=0, resolution=0.1, orient='horizontal',command=self.edit_shape.change_opacity)
        opacity_slider.set(1)
        opacity_slider.pack(side=tk.BOTTOM, fill=tk.Y,padx=10)
        
        border_slider = tk.Scale(sliders_frame, from_=30, to=0, orient='horizontal',command=self.edit_shape.change_border_width)
        border_slider.pack(side=tk.BOTTOM, fill=tk.Y,padx=10)
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

        label = tk.Label(input_panel, text="Enter angle to rotate \n the shapes:",font=font)
        label.pack(side=tk.LEFT, padx=5, pady=5)

        self.input_field = tk.Entry(input_panel,width=5)
        self.input_field.insert(0, "0")
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
    
    def rotate_buttons(self,side):
        self.edit_shape.rotate_shape(side*int(self.input_field.get()))

    def donothing(self):
        print("nothing")

    def save_as(self):
        self.file_name=filedialog.asksaveasfilename(initialdir=os.getcwd(),filetypes=(('PNG File','.PNG'),('JPG File','.JPG')))
        if self.file_name != "":
            self.file_name+='.PNG'
            transperant_image=Image.new("RGBA", (1920, 1080), (0, 0, 0,0))
            self.canvas.delete("border","bottom_btn","top_btn","left_btn","right_btn")
            for item in self.canvas.find_all():
                obj_coords = self.canvas.coords(item)
                obj_tags = self.canvas.gettags(item)
                pil_image=ImageTk.getimage(self.edit_shape.image_specs[obj_tags[0]].tk_image)
                transperant_image.paste(pil_image,(int(obj_coords[0]),int(obj_coords[1])))
            

            # Create a new image with a white background
            background = Image.new("RGBA", transperant_image.size, (255, 255, 255, 255))

            # Paste the transparent image onto the white background
            background.paste(transperant_image, mask=transperant_image)

            # Save the resulting image
            background.save(self.file_name)

    def quick_save(self):
        if self.file_name == "":
            self.save_canvas_as()
        else:
            transperant_image=Image.new("RGBA", (1920, 1080), (0, 0, 0,0))
            self.canvas.delete("border","bottom_btn","top_btn","left_btn","right_btn")
            for item in self.canvas.find_all():
                obj_coords = self.canvas.coords(item)
                obj_tags = self.canvas.gettags(item)
                pil_image=ImageTk.getimage(self.edit_shape.image_specs[obj_tags[0]].tk_image)
                transperant_image.paste(pil_image,(int(obj_coords[0]),int(obj_coords[1])))
            

            # Create a new image with a white background
            background = Image.new("RGBA", transperant_image.size, (255, 255, 255, 255))

            # Paste the transparent image onto the white background
            background.paste(transperant_image, mask=transperant_image)

            # Save the resulting image
            background.save(self.file_name)

    def clear_canvas(self):
        self.canvas.delete("all")

    def settings_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.clear_canvas)
        filemenu.add_command(label="Open", command=self.donothing)
        filemenu.add_command(label="Save", command=self.quick_save)
        filemenu.add_command(label="Save as...", command=self.save_as)
        filemenu.add_command(label="Close", command=self.donothing)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu =  tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.donothing)

        editmenu.add_separator()

        editmenu.add_command(label="Cut", command=self.donothing)
        editmenu.add_command(label="Copy", command=self.donothing)
        editmenu.add_command(label="Paste", command=self.donothing)
        editmenu.add_command(label="Delete", command=self.donothing)
        editmenu.add_command(label="Select All", command=self.donothing)

        menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu =  tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.config(menu=menubar)

if __name__ == "__main__":
    app = DrawApp()
    app.mainloop()