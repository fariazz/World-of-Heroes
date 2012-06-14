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
################################################################################
#
#   Project: World of Heroes
#
#   File: woh_gui_lib.py
#
#   Description: This file contains specific to World of Heroes GUI elements
#   that inherit from the general GUI classes defined in gui_lib.py. The GUI
#   elements defined in this file interact directly with gameplay objects such
#   as the game map and the armies.
#
#   The GUI is WOH is composed by three main widgets, a side panel, represented
#   by the class RightPanel, where general information and some options are
#   shown; a bottom panel represented by the class BottomPanel, which is not
#   used at the current state of development; and the map canvas where the game
#   map, the player and the resource spots are displayed. This is represented by
#   the class MapCanvas.
#
#   Other classes in this file: GameOptionsDialog (shows common gameplay
#   options), and ResConqueredDialog (to be shown when a resource is conquered)   .
#
################################################################################

from gui_lib import *
from game_lib import *
from sys import *


class RightPanel(Widget):
    """Side panel widget. This panel shows information about the game and holds
    buttons with options"""

    def __init__(self, parent,width,height,background,pos_x,pos_y,map_obj,player,
        filename):
        """Initialize the RightPanel object
        (int,int,int,(int,int,int),int,int,str,Map)-->()

        Preconditions: same as Widget."""
        Widget.__init__(self, parent,width,height,background,pos_x,pos_y)

        if filename:
            self._image=SpriteObj(filename)
            self._image.resize(width,height,True)

        self._map_obj=map_obj
        self._player=player
        
    def initializeGameRelated(self):
        """Initialize other, game related attributes and elements of the widget"""

        """Add subwidgets"""
        self._txt_moves_id=gui.addWidget(TextWidget(self.index,70,17,
        (255,255,255),8,40,'Moves left:',12,'black',2))

        self._txt_moves_num_id=gui.addWidget(TextWidget(self.index,32,17,
        (255,255,255),80,40,'_',12,'black',2))

        self._btn_next_turn_id=gui.addWidget(Button(self.index,100,35,
        (255,255,255),8,70,'End Turn','images/button_background.png',14,
        engine.newTurn,(self._player, self._map_obj)))

        self._txt_sold_id=gui.addWidget(TextWidget(self.index,70,17,
        (255,255,255),8,140,'Soldiers:',12,'black',2))

        self._txt_sold_num_id=gui.addWidget(TextWidget(self.index,32,17,
        (255,255,255),80,140,'_',12,'black',2))

        self._txt_resources_id=gui.addWidget(TextWidget(self.index,100,20,
        (255,255,255),8,180,'RESOURCES',12,'black',2))

        self._txt_gold_id=gui.addWidget(TextWidget(self.index,70,17,
        (255,255,255),8,210,'Gold:',12,'black',2))

        self._txt_gold_num_id=gui.addWidget(TextWidget(self.index,32,17,
        (255,255,255),80,210,'_',12,'black',2))

        self._txt_food_id=gui.addWidget(TextWidget(self.index,70,17,
        (255,255,255),8,240,'Food:',12,'black',2))

        self._txt_food_num_id=gui.addWidget(TextWidget(self.index,32,17,
        (255,255,255),80,240,'_',12,'black',2))

        self._txt_ore_id=gui.addWidget(TextWidget(self.index,70,17,
        (255,255,255),8,270,'Ore:',12,'black',2))

        self._txt_ore_num_id=gui.addWidget(TextWidget(self.index,32,17,
        (255,255,255),80,270,'_',12,'black',2))

        self._txt_gems_id=gui.addWidget(TextWidget(self.index,70,17,
        (255,255,255),8,300,'Gems:',12,'black',2))

        self._txt_gems_num_id=gui.addWidget(TextWidget(self.index,32,17,
        (255,255,255),80,300,'_',12,'black',2))


        """Game options dialog"""
        self._dlg_game_opt_id=gui.addWidget(GameOptionsDialog(self._parent,250,
        450,(255,255,255),325,115,'Game Options',3,'images/dialog_bg.jpg'))

        self._btn_game_opt_id=gui.addWidget(Button(self.index,100,35,
        (255,255,255),8,650,'Game Options','images/button_background.png',
        14,show_widget,self._dlg_game_opt_id))

        """Dialog with city options. Open when player steps into a city and
        pressed the city option button"""
        self._dlg_city_opt_id=gui.addWidget(CityOptionsDialog(self._parent,350,
        350,(255,255,255),325,115,'',3,self._map_obj,self._player,
        'images/dialog_bg.jpg'))

        self._btn_city_opt_id=gui.addWidget(Button(self.index,100,35,
        (255,255,255),8,380,'City Options','images/button_background.png',
        14,gui.widgets[self._dlg_city_opt_id].show))
        
        gui.widgets[self._dlg_game_opt_id].initializeGameRelated()
        gui.widgets[self._dlg_city_opt_id].initializeGameRelated()
               
        gui.widgets[self._txt_moves_id].show()
        gui.widgets[self._txt_moves_num_id].show()
        gui.widgets[self._btn_next_turn_id].show()
        gui.widgets[self._txt_sold_id].show()
        gui.widgets[self._txt_sold_num_id].show()
        gui.widgets[self._txt_resources_id].show()
        gui.widgets[self._txt_gold_id].show()
        gui.widgets[self._txt_gold_num_id].show()
        gui.widgets[self._txt_food_id].show()
        gui.widgets[self._txt_food_num_id].show()
        gui.widgets[self._txt_ore_id].show()
        gui.widgets[self._txt_ore_num_id].show()
        gui.widgets[self._txt_gems_id].show()
        gui.widgets[self._txt_gems_num_id].show()
        gui.widgets[self._btn_game_opt_id].show()
                                                   
    def display(self,surface):
        """Display the widget on the screen. First the background image is drawn
        on the Widget's attribute _surf Then, _surf is displayed on the
        screen."""

        if self._shown:
            """the 0,0 values mean the upper left corner of the surface"""
            self._image.display(0,0,self._surf)
            surface.blit(self._surf, self._rect)
            self.displaySubwidgets(surface)

    def update(self,(player, game_map)):
        """Update the elements in the widget, this method is called at the
        frame rate of the game."""

        """update movements left"""
        moves_left = '%.1f' % (player.getMovesLeft())
        gui.widgets[self._txt_moves_num_id].changeText(moves_left)

        """update resource amounts"""
        res = player.getResources()
        gui.widgets[self._txt_gold_num_id].changeText(str(res['gold']))
        gui.widgets[self._txt_food_num_id].changeText(str(res['food']))
        gui.widgets[self._txt_ore_num_id].changeText(str(res['ore']))
        gui.widgets[self._txt_gems_num_id].changeText(str(res['gems']))

        """update the number of soldiers"""
        soldiers = player.getSoldiers()
        gui.widgets[self._txt_sold_num_id].changeText(str(soldiers))
      

    def showCityOptionsButton(self, city_obj):
        """Show the City Options Button. This is called when the player steps
        on a city. A City Object is passed"""

        gui.widgets[self._dlg_city_opt_id].setCity(city_obj)
        gui.widgets[self._btn_city_opt_id].show()

    def closeCityOptionsButton(self):
        """Close the City Options Button. This is called when the player steps
        away from a city"""

        gui.widgets[self._btn_city_opt_id].close()

        

class BottomPanel(Widget):
    """Bottom panel widget. This panel shows information about the game
    Doesn't show anything at this moment but is intended to show map
    related information."""

    def __init__(self, parent,width,height,background,pos_x,pos_y,
        filename=None):
        """Initialize the BottomPanel object
        (int,int,int,(int,int,int),int,int,str)-->()

        Preconditions: same as Widget."""
        Widget.__init__(self, parent,width,height,background,pos_x,pos_y)

        if filename:
            self._image=SpriteObj(filename)
            self._image.resize(width,height,True)

    def display(self,surface):
        """Display the widget on the screen. First the background image is drawn
        on the Widget's attribute _surf Then, _surf is displayed on the
        screen."""

        if self._shown:
            """the 0,0 values mean the upper left corner of the surface"""
            self._image.display(0,0,self._surf)
            surface.blit(self._surf, self._rect)
            self.displaySubwidgets(surface)


class MapCanvas(Widget):
    """The map is displayed in this widget"""

    def __init__(self, parent,width,height,background,pos_x,pos_y):
        """Initialize the MapCanvas object
        (int,int,int,(int,int,int),int,int)-->()

        Preconditions: same as Widget."""
        Widget.__init__(self, parent,width,height,background,pos_x,pos_y)

    def initializeGameRelated(self, player, map_obj):
        """Initialize other, game related attributes and elements of the widget"""

        self._map_obj=map_obj
        
        """Subwidgets"""
        
        """Dialog to be displayed when a resource is conquered by the player"""
        self._dlg_res_conq_id=gui.addWidget(ResConqueredDialog(self._parent,250,
        450,(255,255,255),325,115,'',3,'images/dialog_bg.jpg'))

        """Resource info dialog"""
        self._dlg_res_info_id=gui.addWidget(ResourceInfoDialog(self._parent,350,
        350,(255,255,255),325,115,'',3,self._map_obj,'images/dialog_bg.jpg'))
        
        gui.widgets[self._dlg_res_conq_id].initializeGameRelated()
        gui.widgets[self._dlg_res_info_id].initializeGameRelated()        

    def handleKeyboard(self, key_event, (player,map_obj)):
        """This method is called when the widget has the focus and a key is
        pressed. Parameter obj is used to pass a tupple with the player
        object and the map object."""

        player.handleKeyboard(key_event,self._map_obj)

    def clickOnWidget(self,button,(x,y),player):
        """When the user clicks on the map Terrain information is retrieved.
        First it is checked if the user clicked inside this widget."""
                    
        if self.checkClick((x,y)) and gui.no_modal_dialog:

            """set the focus to clicked widget"""
            gui.setFocus(self.index)
            
            map_dims=self._map_obj.getDimensions()
            if x>self._rect.x and x<self._rect.x + map_dims['width']:
                if y>self._rect.y and y<self._rect.y + map_dims['height']:

                    cell_click=self._map_obj.getCellFromXY(x-self._rect.x,
                        y-self._rect.y)
                    
                    if button == MOUSE_LEFT:
                        """check if there is a path on the screen and the
                        destination circle was click. If so, the player will
                        move to that location. Otherwise, a path will be drawn
                        on the screen"""                        

                        dest_clicked=player.destinationCircleClicked((x,y),
                            self._map_obj)
                        
                        if dest_clicked and not(player.isMoving()):
                            player.setMovingPath(self._map_obj)
                                               
                        elif not(player.isMoving()):
                            player.setPath((x,y), self._map_obj)

                    if button == MOUSE_RIGHT:
                        """Check if there is a resource sport or city in the
                        clicked cell"""

                        res_on_cell, res_id = self._map_obj.resOnCellXY(x,y)
                        
                        if res_on_cell:
                            self.showResInfoDialog(self._map_obj.getResourceObj(res_id))
                        
    def showResConqueredDialog(self,title,text):
        """Show a dialog box when a resource zone is conquered"""
        
        gui.widgets[self._dlg_res_conq_id].initializeResource(title, text)
        gui.widgets[self._dlg_res_conq_id].show(title, text)

    def showResInfoDialog(self, res_obj):
        """Show information about the resource that the user right clicked. A
        Resource object is passed"""

        gui.widgets[self._dlg_res_info_id].setRes(res_obj)
        gui.widgets[self._dlg_res_info_id].show()


class GameOptionsDialog(Dialog):
    """Represents a dialog box with the main game options. This class inherits
    from Dialog."""

    def __init__(self, parent,width,height,background,pos_x,pos_y,title,title_y,
    filename=None,font_size=18):
        """Initialize the GameOptionsDialog with the superclass method

        (int,int,int,(int,int,int),int,int,str,int,str,int)-->()

        Preconditions: same as Dialog."""

        Dialog.__init__(self, parent,width,height,background,pos_x,pos_y,title,
        title_y,filename,font_size)


    def initializeGameRelated(self):
        """Initialize other, game related attributes and elements of the widget"""

        """Initialize subwidgets"""
        self._btn_newgame_id=gui.addWidget(Button(self.index,150,35,
        (255,255,255),50,35,'New Game','images/button_background.png',14,
        button_close_parent))

        self._btn_save_id=gui.addWidget(Button(self.index,150,35,(255,255,255),
        50,100,'Save Game','images/button_background.png',14,
        button_close_parent))

        self._btn_load_id=gui.addWidget(Button(self.index,150,35,(255,255,255),
        50,165,'Load Game','images/button_background.png',14,
        button_close_parent))

        self._btn_fullscr_id=gui.addWidget(Button(self.index,150,35,
        (255,255,255),50,230,'Toggle on/off fullscreen',
        'images/button_background.png',14,pygame.display.toggle_fullscreen))
        
        self._btn_exit_id=gui.addWidget(Button(self.index,150,35,(255,255,255),
        50,295,'Exit Game','images/button_background.png',14,sys.exit))
        
        self._btn_close_id=gui.addWidget(Button(self.index,150,35,(255,255,255),
        50,360,'Close Window','images/button_background.png',14,
        button_close_parent))

    def show(self, showsubw=True):
        """Call the same show method from its superclass, and set up the modal
        dialog flag from the gui object"""

        Dialog.show(self,showsubw)
        gui.no_modal_dialog=False

    def close(self):
        """Call the same close method from its superclass, and set up the modal
        dialog flag from the gui object"""

        Dialog.close(self)
        gui.no_modal_dialog=True

class ResConqueredDialog(Dialog):
    """Dialog box to be shown when the player conquers a resource spot."""

    def __init__(self, parent,width,height,background,pos_x,pos_y,title,title_y,
    filename=None,font_size=18):
        """Initialize the ResConqueredDialog with the superclass method

        (int,int,int,(int,int,int),int,int,str,int,str,int)-->()

        Preconditions: same as Dialog."""

        Dialog.__init__(self, parent,width,height,background,pos_x,pos_y,title,
        title_y,filename,font_size)
        
    def initializeGameRelated(self):
        """Initialize other, game related attributes and elements of the widget"""

        self._btn_close_id=gui.addWidget(Button(self.index,150,35,(255,255,255),
        50,360,'Close Window','images/button_background.png',14,
        button_close_parent))

        self._txt_id=gui.addWidget(TextWidget(self.index,140,250,(255,255,255),
        55,100,'',13,'black',2))
        
    def initializeResource(self, title, text):
        """Initialize resource specific attributes and elements of the widget"""
        
        self.changeTitle(title)        

    def show(self, title, text):
        """Show window on the screen"""        
        
        Dialog.show(self,True)
        self.changeTitle(title)
        gui.widgets[self._txt_id].changeText(text)
        gui.no_modal_dialog=False

    def close(self):
        """Call the same close method from its superclass, and set up the modal
        dialog flag from the gui object"""

        Dialog.close(self)
        gui.no_modal_dialog=True


class CityOptionsDialog(Dialog):
    """Dialog box with the city options for the player."""

    def __init__(self, parent,width,height,background,pos_x,pos_y,title,title_y,
    map_obj, player, filename=None,font_size=18):
        """Initialize the CityOptions with the superclass method

        (int,int,int,(int,int,int),int,int,str,int,str,int)-->()

        Preconditions: same as Dialog."""

        Dialog.__init__(self, parent,width,height,background,pos_x,pos_y,title,
        title_y,filename,font_size)

        self._player=player
        self._city_obj=None
        
    def initializeGameRelated(self):
        """Initialize other, game related attributes and elements of the widget"""

        self._txt_title_id=gui.addWidget(TextWidget(self.index,140,23,(255,255,255),
        25,100,'Soldiers Recruitment',16,'black',2))

        self._txt_gold_id=gui.addWidget(TextWidget(self.index,40,17,(255,255,255),
        25,135,'Gold:',13,'black',2))

        self._txt_p_gold_id=gui.addWidget(TextWidget(self.index,25,17,(255,255,255),
        75,135,'',12,'black',2))

        self._txt_ore_id=gui.addWidget(TextWidget(self.index,35,17,(255,255,255),
        130,135,'Ore:',13,'black',2))

        self._txt_p_ore_id=gui.addWidget(TextWidget(self.index,25,17,(255,255,255),
        170,135,'',12,'black',2))

        self._insertam_id=gui.addWidget(TextWidget(self.index,100,20,(255,255,255),
        25,170,'Insert Amount',14,'black',2))

        self._txtinput1_id=gui.addWidget(TextInput(self.index,30,23,(255,255,255),
        135,168,'int',999))

        self._btn_buy1_id=gui.addWidget(Button(self.index,100,25,(255,255,255),
        190,170,'Recruit','images/button_background.png',14,
        self.buySoldiers))

        self._btn_close_id=gui.addWidget(Button(self.index,150,35,(255,255,255),
        50,250,'Close Window','images/button_background.png',14,
        button_close_parent))
        
    def initializeCity(self):
        """Initialize city specific attributes and elements of the widget"""

        title=self._city_obj.getName()
        price_gold, price_ore = self._city_obj.getSoldierPrice()
        
        self.changeTitle(title)
        gui.widgets[self._txt_p_gold_id].changeText(str(price_gold))
        gui.widgets[self._txt_p_ore_id].changeText(str(price_ore))
                
       
    def show(self):
        """Show window on the screen""" 
        
        Dialog.show(self,True)
        self.initializeCity()
        gui.no_modal_dialog=False

    def close(self):
        """Call the same close method from its superclass, and set up the modal
        dialog flag from the gui object"""

        Dialog.close(self)
        gui.no_modal_dialog=True

    def buySoldiers(self):
        """Buy the soldiers in case the player has enough resources"""

        num=self.getNumSoldiers()

        if num>0:
            ans=self._player.buySoldiers(num, self._city_obj)
            print ans

    def getNumSoldiers(self):
        """Get the number of soldiers input by the user"""

        return gui.widgets[self._txtinput1_id].getInput()

    def setCity(self, city_obj):
        """Set a city object to the dialog so that the city specific info
        will be displayed"""

        self._city_obj=city_obj

        
class ResourceInfoDialog(Dialog):
    """Dialog box with resource information."""

    def __init__(self, parent,width,height,background,pos_x,pos_y,title,title_y,
    map_obj, filename=None,font_size=18):
        """Initialize the CityOptions with the superclass method

        (int,int,int,(int,int,int),int,int,str,int,str,int)-->()

        Preconditions: same as Dialog."""

        Dialog.__init__(self, parent,width,height,background,pos_x,pos_y,title,
        title_y,filename,font_size)

        self._map_obj=map_obj
        self._res_obj=None
        
    def initializeGameRelated(self):
        """Initialize other, game related attributes and elements of the widget"""

        self._txt_owner_id=gui.addWidget(TextWidget(self.index,160,40,(255,255,255),
        90,55,'Owner txt',13,'black',2))

        self._txt_res_id=gui.addWidget(TextWidget(self.index,160,50,(255,255,255),
        90,110,'',13,'black',2))        

        self._btn_close_id=gui.addWidget(Button(self.index,150,35,(255,255,255),
        95,250,'Close Window','images/button_background.png',14,
        button_close_parent))
        
    def initializeRes(self):
        """Initialize resource specific attributes and elements of the widget"""

        title=self._res_obj.getName()
        res_type = self._res_obj.getType()
        turn_amount= self._res_obj.getTurnAmount()
        _ , owner = self._res_obj.getOwner()

        n_owned_own_txt='This resource spot doesn\'t have an owner.'
        n_owned_res_txt=''

        owned_own_txt='Owned by ' + str(owner)
        owned_res_txt='This resource spot delivers ' + str(turn_amount) + \
            ' units of ' + str(res_type) + ' per week.'        
        
        self.changeTitle(title)

        if not(owner):
            gui.widgets[self._txt_owner_id].changeText(n_owned_own_txt)
            gui.widgets[self._txt_res_id].close()

        else:
            gui.widgets[self._txt_owner_id].changeText(owned_own_txt)
            gui.widgets[self._txt_res_id].changeText(owned_res_txt)
                 
       
    def show(self):
        """Show window on the screen""" 
        
        Dialog.show(self,True)
        self.initializeRes()
        gui.no_modal_dialog=False

    def close(self):
        """Call the same close method from its superclass, and set up the modal
        dialog flag from the gui object"""

        Dialog.close(self)
        gui.no_modal_dialog=True


    def setRes(self, res_obj):
        """Set a resource object to the dialog so that the resource specific info
        will be displayed"""

        self._res_obj=res_obj
