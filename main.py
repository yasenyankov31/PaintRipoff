import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import os
import copy

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
        self.draw_color_string=""
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
        self.draw_color=list(new_color)

#shape_type,bd_width,bd_color
class ImageSpecs:
    def __init__(self,shape_type,color,border_width,opacity,tk_image):
        self.shape_type=shape_type
        self.color=color
        self.border_width=border_width
        self.opacity=opacity
        self.tk_image=tk_image
        self.angle=0

class CopiedImage:
    def __init__(self,img_spec,pos_x,pos_y):
        self.img_spec=img_spec
        self.pos_x=pos_x
        self.pos_y=pos_y 

class Action:
    def __init__(self,action_name,selected_shapes=[],tk_images=[],x_y=[]):
        self.action_name=action_name
        self.shapes=copy.copy(selected_shapes)
        self.tk_images=copy.copy(tk_images)
        self.x_y=copy.copy(x_y)

    def get_info(self):
        print(self.action_name,self.shapes,self.shapes_size)


class EditShapes:
    def __init__(self,canvas):
        #history list
        self.history =[]
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

        #selection variables
        self.drag_selection=False
        self.shape_dragged=False
        self.selected_x_y=[]
        self.selected_shapes_tag=[]
        self.selected_shapes_init_size=[]
        self.copied_image_specs=[]
        self.click_shape_x,self.click_shape_y=0,0
        self.paste_shape_x,self.paste_shape_y=0,0
        self.selected_border_width,self.selected_border_height=0,0

        #file 
        self.file_name=""
        self.tk_background_image=None

        #move/drag variables
        self.selected_rect=None

        self.shape = Shape(400, 400)
        self.image_tk = ImageTk.PhotoImage(self.shape.image)
    #draw
    def start_draw(self,event):
        self.drag_selection=self.is_clicked_inside_selection(event)
        if not self.drag_selection:
            if len(self.canvas.find_withtag(tk.CURRENT))==0:
                self.selected_shapes_tag.clear()
                self.shape_dragged=False
                self.canvas.delete("border","bottom_btn","top_btn","left_btn","right_btn")
            
            

        if not self.selection_tool:
            self.first_x, self.first_y =int(self.canvas.canvasx(event.x)),int(self.canvas.canvasy(event.y))
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
            self.selection_rectangle = (int(self.canvas.canvasx(event.x)), int(self.canvas.canvasy(event.y)), int(self.canvas.canvasx(event.x)), int(self.canvas.canvasy(event.y)))

    def stop_draw(self, event):
        if self.drag_selection and len(self.selected_shapes_tag)>1:
            self.stop_drag_shape("")
        if self.is_dragging:
            self.shape_counter+=1
            self.is_dragging = False
            self.canvas.delete("shape")
            tag=f"{self.shape_type}_shape_{self.shape_counter}"
            colors=list(self.shape.draw_color)

            specs=ImageSpecs(self.shape_type,colors,self.shape.border_width,self.shape.alpha,self.image_tk)

            self.image_specs[tag]=specs
            image_object=self.canvas.create_image(self.last_x, self.last_y, image=self.image_specs[tag].tk_image, anchor=tk.NW,tag=tag)
            self.canvas.tag_bind(image_object, "<ButtonPress-1>",lambda event,tag=tag: self.selected_shape(event,tag))
            self.canvas.tag_bind(image_object, "<B1-Motion>",self.drag_shape)
            self.canvas.tag_bind(image_object, "<ButtonRelease-1>",self.stop_drag_shape)
            self.selected_shape(event,tag)
            self.shape_dragged=False
            create_action=Action("create",self.selected_shapes_tag)
            self.history.append(create_action)
            
        #delete selection rectangle
        if self.selection_tool and not self.is_stretching:
            self.selected_x_y.clear()
            x0, y0, x1, y1 = self.selection_rectangle
            item_id=self.canvas.create_rectangle(x0, y0, x1, y1,tags="sel_rect")
            overlapping_items = self.canvas.find_overlapping(*self.canvas.bbox(item_id))
            overlapping_items = [tag for tag in overlapping_items if tag != item_id and self.canvas.type(tag) == "image" and self.canvas.gettags(tag)[0]!="background_image"]
            if len(overlapping_items)>0:
                for item in overlapping_items:
                    tag = self.canvas.gettags(item)[0]
                    self.selected_x_y.append(self.canvas.coords(tag))
                    if tag not in self.selected_shapes_tag:
                        self.selected_shapes_tag.append(tag)
                    if self.canvas.bbox(item) not in self.selected_shapes_init_size:
                        self.selected_shapes_init_size.append(self.canvas.bbox(item))

                if  not self.drag_selection:
                    bbox_coords = [self.canvas.bbox(item) for item in overlapping_items]
                    x1, y1 = min(coord[0] for coord in bbox_coords), min(coord[1] for coord in bbox_coords)
                    x2, y2 = max(coord[2] for coord in bbox_coords), max(coord[3] for coord in bbox_coords)
                    width = x2 - x1
                    height = y2 - y1
                    #self.selected_border_width,self.selected_border_height=width/2,height/2
                    
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


                
                else:
                    self.selected_shapes_init_size.clear()
                    for tag in self.selected_shapes_tag:
                        item_id = self.canvas.find_withtag(tag)[0]
                        self.selected_shapes_init_size.append(self.canvas.bbox(item_id))

        self.canvas.delete("sel_rect")

    def drag_draw(self, event):
        #draw selection rectangle
        if self.drag_selection and len(self.selected_shapes_tag)>1:
            self.drag_shape(event)

        if not self.shape_dragged and not self.is_stretching:
            if self.selection_tool:
                self.canvas.delete("sel_rect")
                self.selection_rectangle = (self.selection_rectangle[0], self.selection_rectangle[1], int(self.canvas.canvasx(event.x)), int(self.canvas.canvasy(event.y)))
                x0, y0, x1, y1 = self.selection_rectangle
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags="sel_rect", width=2,dash=(10,10))

            else:
                self.is_dragging=True
                x, y = int(self.canvas.canvasx(event.x)) - self.first_x, int(self.canvas.canvasy(event.y)) - self.first_y
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
            self.first_stretch_x=int(self.canvas.canvasx(event.x))
            self.first_stretch_y=int(self.canvas.canvasy(event.y))
            self.is_stretching=True

            images=[]
            x_y=[]
            for tag in self.selected_shapes_tag:
                image_widget=self.canvas.find_withtag(tag)[0]
                img_specs=self.image_specs[tag]
                images.append(img_specs.tk_image)
                x_y.append(self.canvas.coords(image_widget))


            stretch_action=Action("stretch",self.selected_shapes_tag,images,x_y=x_y)
            self.history.append(stretch_action)

    def calculate_stretch(self,event,new_width,new_height,button_tag):
        prev_color=list(self.shape.draw_color)
        prev_opcity=self.shape.alpha
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
                self.shape.draw_color.clear()
                self.shape.draw_color=list(self.image_specs[tag].color)
                self.shape.alpha=self.image_specs[tag].opacity

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
        
        self.shape.draw_color=list(prev_color)
        self.shape.alpha=prev_opcity
        x1,y1,x2,y2=self.canvas.coords(button_tag)
        if button_tag=="right_btn" or  button_tag=="left_btn":
            self.canvas.coords(button_tag, int(self.canvas.canvasx(event.x)),y1,int(self.canvas.canvasx(event.x))+10,y2)
        else:
            self.canvas.coords(button_tag, x1,int(self.canvas.canvasy(event.y)),x2,int(self.canvas.canvasy(event.y))+10)                        

    def stretch_image(self,event,tag):
        if self.is_stretching:
            new_height=self.first_stretch_y-int(self.canvas.canvasy(event.y))
            new_width=self.first_stretch_x-int(self.canvas.canvasx(event.x))

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
                    new_height = int(self.canvas.canvasy(event.y)) - self.first_stretch_y
                    self.calculate_stretch(event,0,new_height,tag)
                                                   
    def stop_stretch(self,event):
        self.selected_shapes_init_size.clear()
        for tag in self.selected_shapes_tag:
            item_id = self.canvas.find_withtag(tag)[0]
            self.selected_shapes_init_size.append(self.canvas.bbox(item_id))

        self.canvas.delete("resize","top_btn","left_btn","right_btn","bottom_btn")
        if len(self.selected_shapes_tag)==1:
            self.selected_shape(event,self.selected_shapes_tag[0])
        else:
            bbox_coords = [self.canvas.bbox(item) for item in self.selected_shapes_tag]
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

        
        self.is_stretching=False
    
    #select 
    def deselect_shape(self,event):
        if not self.is_clicked_inside_selection(event):
            self.selected_shapes_tag.clear()
            self.shape_dragged=False
            self.canvas.delete("border","bottom_btn","top_btn","left_btn","right_btn")

    def selected_shape(self,event,tag):
        self.selected_x_y.clear()
        self.selected_shapes_tag.clear()
        self.selected_shapes_init_size.clear()
        image_id=self.canvas.find_withtag(tag)[0]
        self.selected_x_y.append(self.canvas.coords(image_id))
        bbox=self.canvas.bbox(image_id)
        if tag not in self.selected_shapes_tag:
            self.selected_shapes_tag.append(tag)

        if bbox not in self.selected_shapes_init_size:
            self.selected_shapes_init_size.append(bbox)

        self.canvas.delete("border","bottom_btn","top_btn","left_btn","right_btn")
        # Get the rectangle's coordinates and size
        x1, y1, x2, y2 = bbox
        width = x2 - x1
        height = y2 - y1
        
        #self.selected_border_width,self.selected_border_height=width/2,height/2
        self.click_shape_x=int(self.canvas.canvasx(event.x))
        self.click_shape_y=int(self.canvas.canvasy(event.y))
        
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

    def get_hover_mouse_pos(self,event):
        self.paste_shape_x,self.paste_shape_y=int(self.canvas.canvasx(event.x)),int(self.canvas.canvasy(event.y))
        #print(self.paste_shape_x)
        
    def copy_shapes(self,_):
        self.copied_image_specs.clear()
        item_id = self.canvas.find_withtag("border")[0]
        x1,y1,x2,y2=self.canvas.coords(item_id)
        width = x2 - x1
        height = y2 - y1

        self.selected_border_width,self.selected_border_height= width/2,height/2
        

        smallest_x=0
        smallest_index=0
        for index,tag in enumerate(self.selected_shapes_tag):
            item_id = self.canvas.find_withtag(tag)[0]
            x,y=self.canvas.coords(item_id)
            if smallest_x==0 or smallest_x>x:
                smallest_x=x
                smallest_index=index


        first_item_id = self.canvas.find_withtag(self.selected_shapes_tag[smallest_index])[0]
        first_x,first_y=self.canvas.coords(first_item_id)

        for tag in self.selected_shapes_tag:
            item_id = self.canvas.find_withtag(tag)[0]
            x,y=self.canvas.coords(item_id)
            image_specs=self.image_specs[tag]
            copied_img=CopiedImage(image_specs,x-first_x,y-first_y)

            self.copied_image_specs.append(copied_img)

    def paste_shapes(self,_):
        pasted_shapes_tags=[]
        for img_copy in self.copied_image_specs:
            self.shape_counter+=1
            tag=f"{img_copy.img_spec.shape_type}_shape_{self.shape_counter}"
            pasted_shapes_tags.append(tag)
            
            copied_img_specs=copy.copy(img_copy.img_spec)
            self.image_specs[tag]=copied_img_specs
            
            image_object=self.canvas.create_image(self.paste_shape_x+img_copy.pos_x-self.selected_border_width,self.paste_shape_y+img_copy.pos_y-self.selected_border_height, 
                                                  image=self.image_specs[tag].tk_image, anchor=tk.NW,tag=tag)
            self.canvas.tag_bind(image_object, "<ButtonPress-1>",lambda event,tag=tag: self.selected_shape(event,tag))
            self.canvas.tag_bind(image_object, "<B1-Motion>",self.drag_shape)
            self.canvas.tag_bind(image_object, "<ButtonRelease-1>",self.stop_drag_shape)

        create_action=Action("create",pasted_shapes_tags)
        self.history.append(create_action)

    def is_clicked_inside_selection(self,event):
         # get the item that was clicked
        rect_items = self.canvas.find_withtag("border") # get all the rectangles with the "border" tag
        for rect in rect_items:
            rect_coords = self.canvas.coords(rect) # get the coordinates of the clicked rectangle
            x1, y1, x2, y2 = rect_coords
            if x1 < int(self.canvas.canvasx(event.x)) < x2 and y1 < int(self.canvas.canvasy(event.y)) < y2:
                self.click_shape_y=int(self.canvas.canvasy(event.y))
                self.click_shape_x=int(self.canvas.canvasx(event.x))
                return True
        return False

    #move/drag
    def drag_shape(self,event):
        self.shape_dragged=True
        dx=int(self.canvas.canvasx(event.x))-self.click_shape_x
        dy=int(self.canvas.canvasy(event.y))-self.click_shape_y
        self.selected_shapes_init_size.clear()
        for tag in self.selected_shapes_tag:
            item_id = self.canvas.find_withtag(tag)[0]
            self.canvas.move(item_id,dx, dy)
            self.selected_shapes_init_size.append(self.canvas.bbox(item_id))

        self.canvas.move(self.bottom_resize,dx, dy)
        self.canvas.move(self.top_resize,dx, dy)
        self.canvas.move(self.left_resize,dx, dy)
        self.canvas.move(self.right_resize,dx, dy)
        self.canvas.after(5, lambda dx=dx, dy=dy:self.draw_border(dx, dy))

        self.click_shape_x=int(self.canvas.canvasx(event.x))
        self.click_shape_y=int(self.canvas.canvasy(event.y)) 
            
    def stop_drag_shape(self,_):
        drag_action=Action("drag",self.selected_shapes_tag,x_y=self.selected_x_y)
        self.selected_x_y.clear()
        self.history.append(drag_action)

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
            self.shape.change_draw_color(self.image_specs[tag].color)
            self.shape.border_width=self.image_specs[tag].border_width
            self.update_shape(tag)
            self.image_specs[tag].opacity=self.shape.alpha
   
    def change_border_width(self,val):
        for tag in self.selected_shapes_tag:
            self.shape.border_width=30-int(val)
            self.shape.change_draw_color(self.image_specs[tag].color)
            self.shape.alpha=self.image_specs[tag].opacity
            self.update_shape(tag)
            self.image_specs[tag].border_width=self.shape.border_width
        
    def change_shape_color(self, color):
        if not self.selected_shapes_tag:
            self.shape.change_draw_color([int(color[i:i+2], 16) for i in (1, 3, 5)])
            return
        
        images=[]
        for tag in self.selected_shapes_tag:
            shape_specs = self.image_specs[tag]
            shape_specs.color = [int(color[i:i+2], 16) for i in (1, 3, 5)]
            images.append(self.image_specs[tag].tk_image)
            self.shape.change_draw_color(shape_specs.color)
            self.shape.border_width = shape_specs.border_width
            self.shape.alpha = shape_specs.opacity
            self.update_shape(tag)

        create_action=Action("change",self.selected_shapes_tag,tk_images=images)
        self.history.append(create_action)

    def rotate_shape(self,angle):
        images=[]
        for tag in self.selected_shapes_tag:
            # Convert the PhotoImage to a PIL Image
            self.image_specs[tag].angle+=angle
            images.append(self.image_specs[tag].tk_image)
            self.shape.change_draw_color(self.image_specs[tag].color)
            self.shape.alpha=self.image_specs[tag].opacity
            self.shape.border_width=self.image_specs[tag].border_width
            self.update_shape(tag)

        create_action=Action("change",self.selected_shapes_tag,tk_images=images)
        self.history.append(create_action)

    def save_state_of_shapes(self,_):
        images=[]
        for tag in self.selected_shapes_tag:
            images.append(self.image_specs[tag].tk_image)


        create_action=Action("change",self.selected_shapes_tag,tk_images=images)
        self.history.append(create_action)

    #select actions
    def select_all_shapes(self):
        self.selected_x_y.clear()
        self.canvas.delete("border","bottom_btn","top_btn","left_btn","right_btn")
        selected_shapes=[]
        for item in self.canvas.find_all():
            item = self.canvas.gettags(item)
            if "shape" in item[0]:
                #remove current
                if len(item)>1:
                    item=(item[0],)
                selected_shapes.append(item)

        
        for item in selected_shapes:
            if len(self.canvas.gettags(item))>0:
                tag = self.canvas.gettags(item)[0]
                self.selected_x_y.append(self.canvas.coords(tag))
                if tag not in self.selected_shapes_tag:
                    self.selected_shapes_tag.append(tag)
                if self.canvas.bbox(item) not in self.selected_shapes_init_size:
                    self.selected_shapes_init_size.append(self.canvas.bbox(item))
        
        if len(selected_shapes)>0:
            bbox_coords = [self.canvas.bbox(item) for item in selected_shapes]
            x1, y1 = min(coord[0] for coord in bbox_coords), min(coord[1] for coord in bbox_coords)
            x2, y2 = max(coord[2] for coord in bbox_coords), max(coord[3] for coord in bbox_coords)
            width = x2 - x1
            height = y2 - y1
            
            #self.selected_border_width,self.selected_border_height= (x1 + x2) / 2,(y1 + y2) / 2

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

    def delete_shapes(self):
        for tag in self.selected_shapes_tag:
            self.canvas.delete(tag,"border","bottom_btn","top_btn","left_btn","right_btn") 
            del self.image_specs[tag]
        self.selected_shapes_tag.clear()
        
    def cut_shape(self):
        self.copy_shapes("")
        self.delete_shapes()

    def undo(self):
        if self.history:
            prev_action=self.history[len(self.history)-1]
            self.canvas.delete("border","bottom_btn","top_btn","left_btn","right_btn")
            match prev_action.action_name:
                case "create":
                    for tag in prev_action.shapes:                    
                        self.canvas.delete(tag)
                case "stretch":
                    for index,tag in enumerate(prev_action.shapes):
                        self.image_widget=self.canvas.find_withtag(tag)[0]                                     
                        self.image_specs[tag].tk_image=prev_action.tk_images[index]
                        self.canvas.coords(self.image_widget, prev_action.x_y[index][0], prev_action.x_y[index][1])
                        self.canvas.itemconfig(self.image_widget, image=self.image_specs[tag].tk_image)
                case "change":
                    for index,tag in enumerate(prev_action.shapes):
                        self.image_widget=self.canvas.find_withtag(tag)[0]                                     
                        self.image_specs[tag].tk_image=prev_action.tk_images[index]
                        self.canvas.itemconfig(self.image_widget, image=self.image_specs[tag].tk_image)

                case "drag":
                    for index,tag in enumerate(prev_action.shapes):
                        self.image_widget=self.canvas.find_withtag(tag)[0]                                     
                        self.canvas.coords(self.image_widget, prev_action.x_y[index][0], prev_action.x_y[index][1])                    

           #print(prev_action.action_name)
            self.history.pop()
            

    def short_cuts(self,event):
        if event.keysym =='Delete':
            self.delete_shapes()

        if event.state==4 or event.state==12:
            if event.keysym == 's' :  # Check for Control+S
                self.quick_save()

            if event.keysym == 'a':
                self.select_all_shapes()

            if event.keysym == 'x':
                self.cut_shape()

            if event.keysym == 'c':
                self.copy_shapes(event)

            if event.keysym == 'v' :
                self.paste_shapes(event)

            if event.keysym == 'z' :
                self.undo()

    def save_as(self):
        self.file_name=filedialog.asksaveasfilename(initialdir=os.getcwd(),filetypes=(('png File','.png'),('jpg File','.jpg')))
        if self.file_name != "":
            self.file_name+='.png'

            background=None
            if self.tk_background_image==None:
                # Create a new image with a white background
                background = Image.new("RGBA",(1920, 1080), (255, 255, 255, 255))
            else:
                background=ImageTk.getimage(self.tk_background_image)

            self.canvas.delete("border","bottom_btn","top_btn","left_btn","right_btn")
            for item in self.canvas.find_all():
                obj_tags = self.canvas.gettags(item)
                if "shape" in obj_tags[0]:
                    obj_coords = self.canvas.coords(item)
                    pil_image=ImageTk.getimage(self.image_specs[obj_tags[0]].tk_image)
                    background.paste(pil_image.convert("RGB"),(int(obj_coords[0]),int(obj_coords[1])), mask=pil_image.getchannel("A"))
                


            # Save the resulting image
            background.save(self.file_name)

    def quick_save(self):
        if self.file_name == "":
            self.save_as()
        else:
            background=None
            if self.tk_background_image==None:
                # Create a new image with a white background
                background = Image.new("RGBA",(1920, 1080), (255, 255, 255, 255))
            else:
                background=ImageTk.getimage(self.tk_background_image)

            self.canvas.delete("border","bottom_btn","top_btn","left_btn","right_btn")
            for item in self.canvas.find_all():
                obj_tags = self.canvas.gettags(item)
                if "shape" in obj_tags[0]:
                    obj_coords = self.canvas.coords(item)
                    pil_image=ImageTk.getimage(self.image_specs[obj_tags[0]].tk_image)
                    background.paste(pil_image.convert("RGB"),(int(obj_coords[0]),int(obj_coords[1])), mask=pil_image.getchannel("A"))
                


            # Save the resulting image
            background.save(self.file_name)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.tk_background_image=None
        self.selected_shapes_tag.clear()

    def open_image(self):
        self.clear_canvas()
        file_name_to_open=filedialog.askopenfile(initialdir=os.getcwd(),filetypes=(('PNG File','.PNG'),('JPG File','.JPG')))
        self.canvas_background_image=Image.open(file_name_to_open.name).resize((1920,1080),Image.BILINEAR)
        self.tk_background_image=ImageTk.PhotoImage(self.canvas_background_image)
        bg_object=self.canvas.create_image(0, 0, image=self.tk_background_image, anchor="nw",tag="background_image")
        self.canvas.tag_bind(bg_object, "<ButtonPress-1>",self.deselect_shape)

class DrawApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.title("Figures art")
        self.iconbitmap("images/others/main.ico")
        self.geometry("1200x600")
        self.attributes('-fullscreen', False)
        self.bind("<Escape>", lambda event: self.destroy())
        

        
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


        self.canvas_frame=tk.Frame(self)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)        
        # Create the canvas on the right

        self.canvas = tk.Canvas(self.canvas_frame, bg='white', width=600,scrollregion=(0,0,1920,1080))
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        x_scroll = tk.Scrollbar(self.canvas_frame, orient='horizontal', command=self.canvas.xview)
        x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

        y_scroll = tk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        y_scroll.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas.config(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)
        
        

        self.edit_shape=EditShapes(self.canvas)


        #selection part 
        self.selection_frame=tk.Frame(self.tools_panel)
        self.selection_frame.pack(side=tk.TOP, fill=tk.X, pady=1) 

        self.selection_img = tk.PhotoImage(file="images/others/rect_dots.png")
        self.selection_button = tk.Button(self.selection_frame,image=self.selection_img, compound="top", text='Select',command=self.edit_shape.enable_selection_tool)
        self.selection_button.pack(side=tk.LEFT, fill=tk.Y, padx=5)

        
        self.delete_img = tk.PhotoImage(file="images/others/delete.png")
        self.deletion_button = tk.Button(self.selection_frame,image=self.delete_img, compound="top", text='Delete',command=self.edit_shape.delete_shapes)
        self.deletion_button.pack(side=tk.LEFT, fill=tk.Y, padx=5)

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
        self.canvas.bind('<Motion>', self.edit_shape.get_hover_mouse_pos)
        self.canvas.bind("<ButtonPress-1>", self.edit_shape.start_draw)
        self.canvas.bind("<ButtonRelease-1>", self.edit_shape.stop_draw)
        self.bind("<KeyPress>", self.edit_shape.short_cuts)
        
        # Set the ratio of the panel to the canvas to 1:3
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

        #option menu
        self.settings_menu()
        self.deiconify() 
    
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
        start_var = tk.DoubleVar(value=1)
        self.opacity_slider = tk.Scale(sliders_frame, from_=1, to=0, resolution=0.1,variable=start_var, orient='horizontal',command=self.edit_shape.change_opacity)
        self.opacity_slider.pack(side=tk.BOTTOM, fill=tk.Y,padx=10)
        self.opacity_slider.bind("<ButtonPress-1>", self.edit_shape.save_state_of_shapes)
        
        start_var = tk.DoubleVar(value=9)
        self.border_slider = tk.Scale(sliders_frame, from_=30, to=0, orient='horizontal',variable=start_var,command=self.edit_shape.change_border_width)
        self.border_slider.pack(side=tk.BOTTOM, fill=tk.Y,padx=10)
        self.border_slider.bind("<ButtonPress-1>", self.edit_shape.save_state_of_shapes)


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

    def settings_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.edit_shape.clear_canvas)
        filemenu.add_command(label="Open", command=self.edit_shape.open_image)
        filemenu.add_command(label="Save", command=self.edit_shape.quick_save)
        filemenu.add_command(label="Save as...", command=self.edit_shape.save_as)
        filemenu.add_command(label="Close", command=self.donothing)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu =  tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.edit_shape.undo)

        editmenu.add_separator()

        editmenu.add_command(label="Cut", command=self.edit_shape.cut_shape)
        editmenu.add_command(label="Copy", command=lambda:self.edit_shape.copy_shapes(""))
        editmenu.add_command(label="Delete", command=self.edit_shape.delete_shapes)
        editmenu.add_command(label="Select All", command=self.edit_shape.select_all_shapes)

        menubar.add_cascade(label="Edit", menu=editmenu)
        helpmenu =  tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=self.donothing)
        helpmenu.add_command(label="About...", command=self.donothing)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.config(menu=menubar)


if __name__ == "__main__":
    app = DrawApp()
    app.mainloop()