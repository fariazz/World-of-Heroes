################################################################################
#
#   License BSD
#
#   Copyright (c) 2009, Pablo C. Farias Navarro
#   All rights reserved.
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#    * Neither the name of the creator nor the names of its contributors
#      may be used to endorse or promote products derived from this software
#      without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#   IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#   ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#   LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#   CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
#   SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#   INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
#   CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#   ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#   POSSIBILITY OF SUCH DAMAGE.
#
################################################################################################################################################################
#
#   Project: World of Heroes
#
#   File: gui_lib.py
#
#   Description: This file contains GUI classes to be used with pygame. They are
#   not directly related to World of Heroes, so that they can be used in other
#   pygame projects as well.
#
#   This GUI is based on the superclass Widget, that is common to all the GUI
#   elements such as dialog boxes, text labels, text entries, and buttons.
#
#   The class GUI creates a top level object that keeps track and manages all
#   Widgets in the program.
#
#   Other classes in this file: Dialog, Button, TextWidget, ImageWidget,
#   TextInput, SpriteObj (extended version of pygame Sprite class).
#
################################################################################

import sys, pygame
pygame.init()

size = width, height = 1024,768
screen = pygame.display.set_mode(size)
black = 0, 0, 0
yellow = 255, 255, 120

MOUSE_RIGHT=(0,0,1)
MOUSE_LEFT=(1,0,0)
MOUSE_NOT_PRESSED=(0,0,0)

class GUI:
    """A class to store and manage all the widgets in the application"""

    _next_ID=1

    def __init__(self):
        """Initialize the GUI object. The attribute widgets is a dictionary of
        Widget type and is defined as a public attribute."""
        
        self.widgets={}
        self._focus=1
        self.no_modal_dialog=True

    def addWidget(self,new_widget):
        """Add a new Widget object into the widget dictionary"""
        
        self.widgets[GUI._next_ID]=new_widget
        self.widgets[GUI._next_ID].index=GUI._next_ID

        """add the child to the parent"""
        if new_widget._parent!=None:
            self.widgets[new_widget._parent].addSubwidget(GUI._next_ID)
        
        GUI._next_ID+=1

        return GUI._next_ID-1

    def setFocus(self, widget_id):
        """Set the user focus to the specified widget. This is used to handle
        keyboard input.

        Precondition: widget_id needs to be an existing id"""

        self.widgets[self._focus].deactivate()
        self._focus=widget_id

    def getFocus(self):
        """Get the ID of the widget that is being focused"""
        return self._focus

    def updateWidgets(self, obj):
        """Update the state of all the widgets, this method is called at the
        frame rate of the game."""

        for w in self.widgets:
            self.widgets[w].update(obj)        

class Widget:
    """Widget object represents a superclass for all the gui elements in the
    application"""

    def __init__(self, parent_id,width,height,background,pos_x,pos_y):
        """Initialize a Widget object

        (int, int, int, (int,int,int), int, int) --> ()
                
        Precondition: width, height, pos_x and pos_y > 0, parent_id
        has to be the id of an existing widget"""
        
        self._parent=parent_id

        """dictionary with sub widgets ids"""
        self.sub_widgets=[]

        """initialize superclass attributes"""
        self._width=width
        self._height=height
        self._background=background
        self._pos_x=pos_x
        self._pos_y=pos_y        
        self._rect =pygame.Rect(0,0,self._width,self._height)
        self._shown = False
        
    def show(self,show_subwidgets=True):
        """Method to show set up the widget to be displayed"""
        self._surf=pygame.Surface((self._width,self._height))        
        self.initSurface(self._background)

        """rectangle coordinates are obtain differently whether
        it is the main gui element or not"""
        
        if self._parent!=None: 
            self._rect.x=gui.widgets[self._parent]._rect.x+self._pos_x
            self._rect.y=gui.widgets[self._parent]._rect.y+self._pos_y
        else:
            self._rect.x=0
            self._rect.y=0
            
        self._shown = True

        """if this parameter is True, set all the subwidgets to shown"""
        if show_subwidgets:
            for sw in self.sub_widgets:
                gui.widgets[sw].show()
            
        
    def initSurface(self, colour):
        """Initialize Surface of the widget"""
        pygame.draw.rect(self._surf,colour,self._rect, 1)
        self._surf.fill(colour)         
        
    def addSubwidget(self,child_id):
        """Tell the widget about a new child"""
        self.sub_widgets.append(child_id)
                                
    def display(self,surface):
        """Display widget on the screen"""

        if self._shown:
            self._surf.set_colorkey((255,0,255))
            surface.blit(self._surf, self._rect)
            self.displaySubwidgets(surface)

    def displaySubwidgets(self,surface):
        """Display the subwidgets by calling their own display methods"""
        for sw in self.sub_widgets:
            gui.widgets[sw].display(surface)

    def clickOnWidget(self,button,(x,y),obj=None):
        """Check if the user has clicked in the widget. The same checking
        if performed for all the subwidgets as well. Some subwidgets may
        send an action response regarding the click, such as closing the
        parent Widget, which will be excecuted.

        Parameter obj allows subclasses to receive objects of
        different data types."""
        
        if self.checkClick((x,y)) and self._shown:
            """set the focus to clicked widget"""
            gui.setFocus(self.index)
                        
            """then check for subwidgets"""
            response={}
            for sw in self.sub_widgets:
                response[sw]=gui.widgets[sw].clickOnWidget(button,(x,y),obj)
                
            """update widgets according to their click response"""
            for k in response:
                if response[k]=='close':
                    gui.widgets[k].close()

                elif response[k]=='close_parent':
                    return 'close'

                
    def checkClick(self,(x,y)):
        """Compare the mouse click coordinates with the widget's coordinates
        too see if the widget was clicked on."""

        if self._shown:
            if x>=self._rect.x and x<=self._rect.x+self._width:
                if y>=self._rect.y and y<=self._rect.y+self._height:
                    return True
                else:
                    return False
            else:
                return False

        else:
            return False
    
    def close(self):
        """Close a widget and all of its subwidgets. A widget is closed by
        setting its Surface attribute _surf to an empty Surface"""

        self._shown = False
        
        for j in self.sub_widgets:            
            gui.widgets[j].close()

        self._surf=pygame.Surface((0,0))
        
    def __str__(self):
        """String representation of a Widget object"""
        if self._parent != None:
            return str(self._parent) + '.' + str(self._index)

        else:
            return str(self._index)

    def deactivate(self):
        """This method is called when the widget loses the user focus. This
        method is overriden in the subclasses that need to perform actions
        in this case."""
        pass

    def handleKeyboard(self, key_event, obj=None):
        """This method is called when the widget has the focus and a key is
        pressed. This method is overriden in the subclasses that need to
        perform actions in this case.

        Parameter obj allows subclasses to receive objects of
        different data types."""
        pass

    def getSurf(self):
        """Return the pygame Surface attribut of the widget"""
        return self._surf

    def update(self, obj):
        """Update the state of the widgets, this method is called at the
        frame rate of the game."""
        pass

        

class Button(Widget):
    """This class represents a button in the GUI. Buttons have callback
    functions defined when initialized"""
    
    def __init__(self, parent,width,height,background,pos_x,pos_y,text,
    filename=None,font_size=18,onclick_actions=None,callback_param=None):
        """Initialize a Button object. The user needs to enter its geometry,
        background colour or image, an a callback funcion with its parameters

        (int,int,int,(int,int,int),int,int,str,str,int,funcion,tupple)-->()

        Preconditions: same as Widget. the callback parameters are passed
        in a tupple, there is no restriction on the datatypes and size
        of this tupple."""

        Widget.__init__(self, parent,width,height,background,pos_x,pos_y)
        self._text=text
        self._onclick_actions=onclick_actions
        self._callback_param=callback_param
        
        if filename:
            self._image=SpriteObj(filename)
            self._image.resize(width,height,True)

        self._font = pygame.font.SysFont('arial', font_size)
        self._textsurf = self._font.render(self._text, True, pygame.Color(
        'gray20'))
        
        (w,h)=(self._textsurf.get_width(),self._textsurf.get_height())
        text_x=int((self._width-w)*0.5)
        text_y=int((self._height-h)*0.5)
        self._textrect = pygame.Rect(text_x,text_y,w,h)
        
    def clickOnWidget(self,button,(x,y),obj=None):
        """first check if the user clicked in this widget. If so
        execute callback funciton."""        
        
        if self.checkClick((x,y)) and button==MOUSE_LEFT:
            gui.setFocus(self._parent)
            if self._callback_param:
                result=self._onclick_actions(self._callback_param)
            else:
                result=self._onclick_actions()
            return result

    def display(self,surface):
        """Display the Widget on the screen

        First the background image is drawn on the Widget's attribute _surf
        Then, the title text is drawn on top of the image, and finally _surf is
        displayed on the screen."""

        if self._shown:
            """the 0,0 values mean the upper left corner of the surface"""
            self._image.display(0,0,self._surf)
            self._surf.blit(self._textsurf, self._textrect)
            surface.blit(self._surf, self._rect)
     

class Dialog(Widget):
    """This class represents a generic dialog box, which can contain other
    widgets as well such as buttons, text labels, etc."""
    
    def __init__(self, parent,width,height,background,pos_x,pos_y,title,title_y,
    filename=None,font_size=18):
        """Initialize a Dialog object, representing a dialog box

        (int,int,int,(int,int,int),int,int,str,int,str,int)-->()

        Preconditions: same as Widget."""
        
        Widget.__init__(self, parent,width,height,background,pos_x,pos_y)
        self._title=title
        self._title_y=title_y

        if filename:
            self._image=SpriteObj(filename)
            self._image.resize(width,height,True)

        self._font = pygame.font.SysFont('arial', font_size)
        self._textsurf = self._font.render(self._title, True, pygame.Color(
        'gray20'))

        (w,h)=(self._textsurf.get_width(),self._textsurf.get_height())
        text_x=int((self._width-w)*0.5)
        text_y=int(self._title_y)
        self._textrect = pygame.Rect(text_x,text_y,w,h)
        
    def display(self,surface):
        """Display the widget on the screen

        First the background image is drawn on the Widget's attribute _surf
        Then, the title text is drawn on top of the image, and finally _surf is
        displayed on the screen."""

        if self._shown:
            """the 0,0 values mean the upper left corner of the surface"""
            self._image.display(0,0,self._surf)
            self._surf.blit(self._textsurf, self._textrect)
            surface.blit(self._surf, self._rect)
            self.displaySubwidgets(surface)


    def changeTitle(self,text):
        """Change the title of the Dialog object"""

        self._title=text
        self._textsurf = self._font.render(self._title, True, pygame.Color(
        'gray20'))
        
        (w,h)=(self._textsurf.get_width(),self._textsurf.get_height())
        text_x=int((self._width-w)*0.5)
        text_y=int(self._title_y)
        self._textrect = pygame.Rect(text_x,text_y,w,h)
        

class TextWidget(Widget):
    """Represents a text box to be displayed inside other widget objects"""    
    
    def __init__(self, parent,width,height,background,pos_x,pos_y,paragraph,
    font_size=10,font_colour='black',ipad=5):
        """Initialize a TextWidget object.

        (int,int,int,(int,int,int),int,int,str,int,str,int)-->()

        Preconditions: same as Widget. ipad represents the space between the
        text and the borders of the TextWidget and needs to be >0, smaller
        than the widget's width and size plus the font size.

        Another precondition, is that it is up to the user to estimate a
        proper size for the text box so that the text will fit properly"""
    
        Widget.__init__(self, parent,width,height,background,pos_x,pos_y)
        self._font_size=font_size
        self._font = pygame.font.SysFont('arial', self._font_size)
        self._paragraph=paragraph
        self._ipad=ipad
        self._font_colour=font_colour        
        self._current_colour = self._background

    def show(self):
        """Method to show set up the widget to be displayed"""
        
        Widget.show(self)
        self.splitLines()
        
    def changeText(self,new_text):
        """Change the text in the widget"""
        
        self.initSurface(self._current_colour)
        self._paragraph=new_text
        self.splitLines()

    def splitLines(self):
        """The text is splitted to fit in the TextWidget and drawn in the surf"""
        
        line=0
        pixel=0
        dest_rect = pygame.Rect(self._rect.x,self._rect.y,self._width,
        self._font_size)

        splitted_parag=self._paragraph.split()
        
        for w in splitted_parag:
            current_word=self._font.render(w, True, pygame.Color(
            self._font_colour))

            current_size=current_word.get_width()+5
            
            """if there is no room for the word in the current line, a new line
            is created"""
            if (pixel + current_size)>(self._width-self._ipad):
                line+=1
                pixel=0
                

            dest_x=self._ipad+pixel
            dest_y=self._ipad+line*self._font_size

            dest_rect.x=dest_x
            dest_rect.y=dest_y
            dest_rect.width=current_size
            
            self._surf.blit(current_word, dest_rect)
            pixel+=current_size

        def getText(self):
            return self._paragraph

        
class ImageWidget(Widget):
    """This class, which inherits from Widget, displays an image inside of a
    dialog box or a panel."""
    
    def __init__(self, parent,width,height,background,pos_x,pos_y,filename):
        """Initialize the ImageWidget object. First the super class attributes
        are initialized"""
        Widget.__init__(self, parent,width,height,background,pos_x,pos_y)
                
        if filename:
            self._image=SpriteObj(filename)
            self._image.resize(self._width,self._height,True)

    def changeImage(self, filename):
        """Change the image displayed"""
        self._image=SpriteObj(filename)
        self._image.resize(self._width,self._height,True)
    
    def display(self,surface):
        """Display the image on the screen. This is done by drawing the
        SpriteObj attribute into the upper left corner of the _surf attribute
        ( 0,0 mean upper left corner)"""

        if self._shown:
            self._image.display(0,0,self._surf)
            surface.blit(self._surf, self._rect)


class TextInput(TextWidget):
    """A text entry widget"""
    
    def __init__(self, parent,width,height,background,pos_x,pos_y,input_type,
        max_size,paragraph='',font_size=10,font_colour='black',ipad=5,
        focus_colour=yellow):
        """Initialize a TextInput object

        (int,int,int,(int,int,int),int,int,str,int,str,int,str,int,
        (int,int,int) --> None
        
        Precondition: same as TextWidget. input type can be either 'str'
        or 'int', if its 'str' max_size is the maximum length of the string,
        if its 'int', max_size is the maximum value."""

        TextWidget.__init__(self, parent,width,height,background,pos_x,pos_y,
        paragraph,font_size=10,font_colour='black',ipad=5)

        self._focus_colour=focus_colour
        self._input_type=input_type
        self._max_size=max_size
        
    def clickOnWidget(self,button, (x,y),obj=None):
        """First check if the user clicked in this widget. If so, activate.

        Parameter obj allows subclasses to receive objects of
        different data types."""
        
        if self.checkClick((x,y))  and button==MOUSE_LEFT:
            gui.setFocus(self.index)
            self.activate()
            return None

    def activate(self):
        """Actions to be perfomed when the user clicks on the text input
        widget"""
        self._current_colour =self._focus_colour
        self.initSurface(self._current_colour)
        self.splitLines()

    def deactivate(self):
        """This method is called when the widget loses the user focus"""
        self._current_colour =self._background
        self.initSurface(self._current_colour)
        self.splitLines()

    def handleKeyboard(self, key_event, obj=None):
        """This method is called when the widget has the focus and a key is
        pressed.
        
        Parameter obj allows subclasses to receive objects of
        different data types.
        """

        k_backspace=8

        if self._input_type=='str':
        
            """only read input if the inserted character is alpha numeric or
            space"""
            if key_event.key not in [13,271,k_backspace,266,127]:
                if len(self._paragraph)+1 <= self._max_size:
                    self._paragraph+=key_event.unicode
                    self.changeText(self._paragraph)

            elif key_event.key == k_backspace:
                if len(self._paragraph) > 0:
                    self._paragraph=self._paragraph[0:len(self._paragraph)-1]
                    self.changeText(self._paragraph)

        elif self._input_type=='int':
        
            """only read input if the inserted character is a number"""
            if key_event.key not in [13,271,k_backspace,266,127]:
                try:
                    amount_str=self._paragraph+key_event.unicode

                    if int(amount_str) <= self._max_size:
                        self._paragraph=str(int(amount_str))
                        self.changeText(self._paragraph)

                except:
                    pass

            elif key_event.key == k_backspace:
                if len(self._paragraph) > 0:
                    self._paragraph=self._paragraph[0:len(self._paragraph)-1]
                    self.changeText(self._paragraph)

    def close(self):
        """Calls the superclass Widget close method, and resets the text in the
        input field"""

        Widget.close(self)

        self._paragraph=''

    def getInput(self):
        """Get the text or integer from the input field"""

        if self._input_type == 'str':
            return self._paragraph

        elif self._input_type == 'int':
            if self._paragraph == '':
                return 0

            else:
                return int(self._paragraph)
        
                    
class SpriteObj(pygame.sprite.Sprite):
    """An extension of the pygame.Sprite class, to include more attributes and
    methods such as transparency, cutting a larger image into a smaller surface
    and displaying as a mosaic (both done by the resize method).
    """

    def __init__(self, filename):
        """Initialize a SpriteObj by loading the image file and setting up
        the parameters

        (str) --> ()

        Precondition: filename needs to be a valid filename in one of the
        image formats defined in:
        http://www.pygame.org/docs/ref/image.html"""

        pygame.sprite.Sprite.__init__(self)
        self._filename = filename
        self.image = pygame.image.load(self._filename).convert()
        self.image.set_colorkey((255,0,255))
        self.rect = self.image.get_rect()
               
    def display(self,x,y,surface):
        """Draw the image on the specified surface. surface could
        be the screen or another python.Surface object"""
        
        self.rect.x=x
        self.rect.y=y        
        surface.blit(self.image, self.rect)

    def resize(self,w,h,mosaic=False):
        """Check if the image is smaller than the new dimesions
        if it is smaller, it can be displayed as a mosaic,
        if the image is bigger, it is cut"""
        
        if self.rect.width<w or self.rect.height<h:
            new_surf=pygame.Surface((w, h))
            if mosaic:
                for i in range(0,w,self.rect.width):
                    for j in range(0,h,self.rect.height):
                        new_surf.blit(self.image,pygame.Rect(i,j,w,h))
            else:
                new_surf.blit(self.image,pygame.Rect(0,0,w,h))
            self.image=new_surf        
        else:
            self.rect.width=w
            self.rect.height=h
            self.image=self.image.subsurface(self.rect)

def button_close():
    """Close the current widget"""
    return 'close'

def button_close_parent():
    """Close the parent widget (eg a dialog box)"""
    return 'close_parent'

def button_change_text((widget_id, text)):
    """Change the text of a TextWidget object identified by widget_id"""
    gui.widgets[widget_id].changeText(text)
    return None

def button_change_img((widget_id,img)):
    """Change the image of an ImageWidget object identified by widget_id"""
    gui.widgets[widget_id].changeImage(img)
    return None

def show_widget(widget_id):
    """Sets a widget to be displayed on the screen"""
    gui.widgets[widget_id].show(True)

gui=GUI()
