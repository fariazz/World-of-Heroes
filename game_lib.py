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
#   File: game_lib.py
#
#   Description: This file contains the gameplay classes for World of Heroes, a
#   2D turn-based strategy game.
#
#   EngineObject is a top-level class that keeps track of general gameplay
#   variables and methods. The class Map manages the game map and its interaction with the
#   game characters and resources. The class Player manages the player's army.
#
#   Other classes in this file are: Army (superclass for all the armies in the
#   game), Terrain (represent a terrain type), Path (represent the path the
#   player is going to follow), and Polyline (draw a polyline on a surface).
#
################################################################################

from gui_lib import *
import satar_modif
from random  import *

class EngineObject:
    """This class manages gameplay variables and methods such as the default
    size of the sprites, and the turn system.    
    """

    current_turn = 1
    
    def __init__(self):
        """Initialize the EngineObject"""
        self.tile_x=32
        self.tile_y=32

        """frames per second"""
        self.fps=50

    def newTurn(self, (player, map_obj)):
        """Prepare all the game elements for a new turn"""

        player.newTurn(map_obj)
        EngineObject.current_turn+=1

    def setMapCanvas(self, widget_id):
        """Keep track of the id of the MapCanvas widget"""
        
        self._map_canvas_id=widget_id

    def getMapCanvas(self):
        """Return the id of the MapCanvas widget"""

        return self._map_canvas_id

    def setRightPanel(self, widget_id):
        """Keep track of the id of the RightPanel widget"""
        
        self._right_panel_id=widget_id

    def getRightPanel(self):
        """Return the id of the RightPanel widget"""

        return self._right_panel_id

        

class Terrain(SpriteObj):
    """Represents the terrain types and their attributes, it is a subclass
    of SpriteObj

    Constructor: Terrain(str, str, str, int, boolean)
    """

    def __init__(self, filename, terrain_id, terrain_name, move_cost,
    is_walkable):

        SpriteObj.__init__(self, filename)
        self._terrain_id=terrain_id
        self._terrain_name=terrain_name
        self._move_cost=int(move_cost)
        self._is_walkable=int(is_walkable)

    def __str__(self):
        """Represent a Terrain object as string"""

        terr_str="Terrain ID:" + str(self._terrain_id) + ", Name:"
        terr_str=terr_str+str(self._terrain_name) + ", Is_walkable:"
        terr_str=terr_str+ str(self._is_walkable)+ ", Move cost:" 
        terr_str=terr_str+str(self._move_cost)

        return terr_str  
        
    def getMoveCost(self):
        """Get the terrain type's move cost"""
        return self._move_cost

    def getIsWalkable(self):
        """Get if the terrain is walkable or not"""
        return self._is_walkable

    def getTerrainName(self):
        """Get the name of the terrain type"""
        return self._terrain_name
    
class Map:
    """This class represents the game map, which is a 2D grill where each
    cell represents a certain terrain type. From this class the map is loaded
    from differente text files containing cell and terrain information, and it
    is drawn in a pygame Surface object, which is drawn into the MapCanvas gui
    element.

    This class also manages gameplay related map operations and elements, such
    as resource spots, cities, and part of the path finding and armies updating.
    """

    def __init__(self, tileset_file, terrains_file, resource_type_file,
    resource_pos_file,cities_file,cities_pos_file):
        """Initialize the game map"""
        
        self._tileset_file=tileset_file
        self._terrains_file=terrains_file
        self._resource_type_file=resource_type_file
        self._resource_pos_file = resource_pos_file
        self._cities_file=cities_file
        self._cities_pos_file=cities_pos_file

        """Terrain information is in two files, terrains_file contains the
        description of every terrain type. tileset contains the terrain
        type of every cell in the map"""
        self._terrain_types={}
        self._terrain_types={}
        self.loadTerrainTypes()
        self.loadTileset()

        """resource information is stored in two different files,
        resource_types_file contains the description of every
        different kind of resource spot in the game, two resource spots can
        deliver the same resource, for example a small farm and a big
        farm will both deliver food. resource_spots_file contains the position
        of every resource spot in the game map"""
        self._resource_spots={}
        self._resource_types={}
        self.loadResourceTypes()
        self.loadResourcePos()

        """cities info stored in two files, just like for the resources, there
        is a file to store the cities attributes and a file to store their
        positions"""
        self.loadCities()
        self.loadCitiesPos()

        self._map_surf=pygame.Surface((self._tiles_x*engine.tile_x,
        self._tiles_y*engine.tile_y))
        
        self._map_rect=self._map_surf.get_rect()
        
        self.setMoveCost1D()
        

    def loadTerrainTypes(self):
        """Load text file with terrain types information. The file's format is:

        terrain_id, terrain_name, move_cost, is_walkable, image_filename
          (int)       (str)         (int)       (int)        (str)

        """
        
        f = open(self._terrains_file, 'U')
        
        for line in f:

            """read and process each line that has data, and save the info in
            the dictionary"""
            if line.rfind(',') != -1:

                """splits each line into a list"""
                sline=line.split(',')
                
                """the info is stored in the dictorionary. Whitespaces, tabs and
                new lines are removed"""
                self._terrain_types[sline[0].strip()]=Terrain(sline[4].strip(),
                sline[0].strip(),sline[1].strip(),sline[2].strip(),
                sline[3].strip())
       
        """close the file"""
        f.close()        

    def loadTileset(self):
        """Load the map grid from a text file. This file is organized
        as a nxm matrix where n is the number of rows of the map, and m the
        number of columns. Each value representes a terrain id. Values are
        separated by commas, and rows by new lines

        Precondition: the values in the file must exist in the file where
        the terrain types are defined, terrains_file."""

        """list to store the tileset"""        
        self._tiles=[]
        
        f = open(self._tileset_file, 'U')

        i=0
        for line in f:

            """read and process each line that has data"""
            if line.rfind(',') != -1:

                """splits each line into a list"""
                splitted_line=line.split(',')

                j=0

                self._tiles.append([])

                for t in splitted_line:
                    self._tiles[i].append(t.strip())
                    j+=1
                i+=1
                
                
        """close the file"""
        f.close()

        """save dimensions of the map"""
        self._tiles_x=j+1
        self._tiles_y=i+1
    
    def display(self, dest_surf, player):
        """Draw the map in the destination surface. Only the cells that are
        visible to the player will be displayed."""

        cell_visib=player.getCellVisibility()

        dest_surf.fill((0,0,0))

        """display visible terrains"""
        if cell_visib:     
            for i in range(0,self._tiles_y-1):
                for j in range(0,self._tiles_x-1):
                    if cell_visib[i][j]:
                        self._terrain_types[self._tiles[i][j]].display(
                        j*engine.tile_y,i*engine.tile_x,dest_surf)

        """display resource spots and cities"""
        for i in self._resource_spots:
            x,y=self._resource_spots[i].getPos()
            res_cell=self.getCellFromXY(x,y)
            
            if cell_visib[res_cell['row']][res_cell['col']]:            
                self._resource_spots[i].display(dest_surf)     
         
    def getIsWalkable(self,x,y):
        """Return the _is_walkable attribute of the terrain located at
        coordinates x,y. This coordinates are in pixels"""
        
        target_cell=self.getCellFromXY(x,y)

        left_border=x<self._map_rect.left
        top_border=y<self._map_rect.top
        right_border=x>=self._map_rect.right
        bot_border=y>=self._map_rect.bottom
        
        if (left_border or top_border) or (right_border or bot_border):
            return False
        
        target_terrain=self._tiles[target_cell['row']][target_cell['col']]
        return self._terrain_types[target_terrain].getIsWalkable()

    def getCellFromXY(self,x,y):
        """Return the row and column of the cell located in some X, Y pixel
        coordinates.getMoveCost1D

        Precondition: the origin (0,0) is located on the upper left corner of
        the map."""
        
        col=int((x - x%engine.tile_x)/engine.tile_x)
        row=int((y - y%engine.tile_y)/engine.tile_y)
        cell={'row':row, 'col':col}        
        return cell

    def getCellCoordFromXY(self,x,y):
        """Return the coordinates of the upper left corner of the cell where
        the point x,y is located. x,y in Pixel coordinates.

        Precondition: the origin (0,0) is located on the upper left corner of
        the map."""

        current_cell = self.getCellFromXY(x,y)
        x_left = current_cell['col']*engine.tile_x
        y_left = current_cell['row']*engine.tile_y
        return (x_left, y_left)
        

    def showTerrainInfo(self,cell):
        """Returns data on the terrain located in cell "cell".
        Parameter cell is a dictionary with the format:

        dict{'row':row number, 'col':column number}"""
        
        terr_id=self._tiles[cell['row']][cell['col']]
        return self._terrain_types[terr_id]

    def setMoveCost1D(self):
        """Generate a list with the move cost of every cell in the map"""

        self._1d_move_cost=[]
        
        for j in range(0,self._tiles_y-1):
            for i in range(0,self._tiles_x-1):
                self._1d_move_cost.append(
                self._terrain_types[self._tiles[j][i]].getMoveCost())   

    def getMoveCost1D(self):
        """Returns a list with the move cost of every cell in the map"""

        return self._1d_move_cost

    def getDimensions(self):
        """Return the dimensions of the map, in number of cells and in pixels"""

        dim_dict={}
        dim_dict['num_rows']=self._tiles_y
        dim_dict['num_cols']=self._tiles_x
        dim_dict['width']=self._map_rect.width
        dim_dict['height']=self._map_rect.height
                    
        return dim_dict

    def getCostBetween2Points(self,(x0,y0),(x1,y1)):
        """Estimate the movement cost between two points in the map. Coodinates
        in pixels.

        Precondition: both points are either the same corner of two adjacent
        cells, or the center of two adjacent cells."""

        cell0=self.getCellFromXY(x0,y0)
        cell1=self.getCellFromXY(x1,y1)

        terrain_id0=self._tiles[cell0['row']][cell0['col']]
        terrain_id1=self._tiles[cell1['row']][cell1['col']]
        
        move_cost0=self._terrain_types[terrain_id0].getMoveCost()
        move_cost1=self._terrain_types[terrain_id1].getMoveCost()

        """Normalize the coordinates"""
        x0=x0/engine.tile_x
        x1=x1/engine.tile_x
        y0=y0/engine.tile_y
        y1=y1/engine.tile_y

        xm = (x0 + x1)/2
        ym = (y0 + y1)/2
        
        mc0 = (((x0-xm))**2+((y0-ym))**2)**(0.5)*move_cost0
        mc1 = (((xm-x1))**2+((ym-y1))**2)**(0.5)*move_cost1
        
        return mc0 + mc1

    def loadResourceTypes(self):
            """Load text file with resource types information in format:

            type_id,, type,, name,, amount_per_turn,, instant_amount,, 
             (int)    (str)  (str)        (int)           (int)          

             img_filename,, text_when_conquered, text_first_time
                (str)              (str)               (str)

            Precondition: type_id values must be unique, considering the
            cities as well.

            """
            
            f = open(self._resource_type_file, 'U')
            
            for line in f:

                """read and process each line that has data, and save the info
                in the dictionary"""
                if line.rfind(',') != -1:

                    """splits each line into a list"""
                    sline=line.split(',,')
                    
                    """the info is stored in the dictorionary. Whitespaces,
                    tabs and new lines are removed"""
                    
                    self._resource_types[sline[0].strip()]={'type': sline[1].strip(),
                    'name': sline[2].strip(),'amount_per_turn': int(sline[3].strip()),
                    'instant_amount': int(sline[4].strip()),
                    'filename': sline[5].strip(), 'conquered_text': sline[6].strip(),
                    'first_time_text': sline[7].strip()}

            """close the file"""
            f.close()

    def loadResourcePos(self):
            """Load text file with the location of the resource spots, the file
            is in the format:

            type_id, column_number, row_number
            (int)         (int)       (int)             

            After loading the file, Resource objects are created to represent
            these resource spots. The resource spots are an attribute of the
            Map object.
            """            
  
            f = open(self._resource_pos_file, 'U')
            
            for line in f:

                """read and process each line that has data, and save the info
                in the dictionary"""
                if line.rfind(',') != -1:

                    """splits each line into a list"""
                    splitted_line=line.split(',')
                    
                    """the info is used to create Resource objects. Whitespaces,
                    tabs and new lines are removed"""
                    type_id=splitted_line[0].strip()
                    col=int(splitted_line[1].strip())
                    row=int(splitted_line[2].strip())

                    x=col*engine.tile_x
                    y=row*engine.tile_y
                    
                    self._resource_spots[Resource._nextID-1]=Resource(type_id,
                    self._resource_types[type_id]['filename'],
                    self._resource_types[type_id]['type'],
                    self._resource_types[type_id]['name'],
                    self._resource_types[type_id]['amount_per_turn'],
                    self._resource_types[type_id]['instant_amount'],
                    self._resource_types[type_id]['conquered_text'],
                    self._resource_types[type_id]['first_time_text'],x, y)
                    
            """close the file"""
            f.close()

    def resOnCellXY(self,x,y):
        """Checks if there is a resource in the map coordinates x,y"""

        army_cell=self.getCellFromXY(x,y)

        for r in self._resource_spots:
            res_x, res_y = self._resource_spots[r].getPos()
            res_cell=self.getCellFromXY(res_x,res_y)

            if army_cell == res_cell:
                return True, self._resource_spots[r].getID()

        return False, None

    def setResourceOwner(self, army_id, army_name, res_id, colour):
        """Set an owner army to a certain resource spot"""

        self._resource_spots[res_id].setOwner(army_id, army_name, colour)       

    def getResourceOwner(self, res_id):
        """Get the owner of a resource spot"""

        return self._resource_spots[res_id].getOwner()       

    def getResConqueredText(self, res_id):
        """Get the text for a dialog box when a resource is conquered"""

        return self._resource_spots[res_id].getConqueredText()

    def payTurnResources(self, army_obj):
        """Pay the army the end of turn resource amounts according to its owned
        resource spots"""

        army_id=army_obj.getID()
        
        for r in self._resource_spots:
            owner=self._resource_spots[r].getOwner()        

            if owner==army_id:
                res_type=self._resource_spots[r].getType()
                amount=self._resource_spots[r].getTurnAmount()
                army_obj.updateResource(res_type, amount)

    def getResourceType(self, res_id):
        """Get the resource type of the specified resource id"""

        return self._resource_spots[res_id].getType()

    def payFirstTimeRes(self, army_obj, res_id):
        """Pay the army the amount of resources available when conquering
        a resource. If the resource spot has been conquered before, the
        resource object will return zero for the resource amount."""

        army_id=army_obj.getID()
        res_type=self._resource_spots[res_id].getType()
        amount=self._resource_spots[res_id].payFirstAmount()
        army_obj.updateResource(res_type, amount)

    def armyOnResource(self,army_obj,res_id):
        """Method to be called when an army is on a resource spot"""

        owner=self.getResourceOwner(res_id)
        self.setResourceOwner(army_obj.getID(), army_obj.getName(), res_id,
            army_obj.getColour())
        dialog_title, dialog_text=self.getResConqueredText(res_id)
                    
        """if the resource was not owned by the army, check for first
        time reward and show a dialog"""
        if owner != army_obj.getID():
            self.payFirstTimeRes(army_obj, res_id)
            gui.widgets[engine.getMapCanvas()].showResConqueredDialog(
            dialog_title,dialog_text)
        
        if self._resource_spots[res_id].isCity():
            """if its a city show city options button in the right panel"""
            gui.widgets[engine.getRightPanel()].showCityOptionsButton(
                self._resource_spots[res_id])
        

    def loadCities(self):
            """Load text file with cities attributes in format:

            type_id,, type,, name,, amount_per_turn,, instant_amount,, 
             (int)    (str)  (str)        (int)           (int)          

            img_filename,, text_when_conquered,, text_first_time,,
                (str)              (str)               (str)

            soldier_cost_gold,, soldier_cost_ore
                (int)               (int)

            Precondition: type_id values must be unique, considering the
            cities as well.
            """
            
            f = open(self._cities_file, 'U')
            
            for line in f:

                """read and process each line that has data, and save the info
                in the dictionary"""
                if line.rfind(',') != -1:

                    """splits each line into a list"""
                    sline=line.split(',,')
                    
                    """the info is stored in the dictorionary. Whitespaces,
                    tabs and new lines are removed"""
                    
                    self._resource_types[sline[0].strip()]={'type': sline[1].strip(),
                    'name': sline[2].strip(),'amount_per_turn': int(sline[3].strip()),
                    'instant_amount': int(sline[4].strip()),
                    'filename': sline[5].strip(), 'conquered_text': sline[6].strip(),
                    'first_time_text': sline[7].strip(),'sld_cost_gold': int(sline[8].strip()),
                    'sld_cost_ore': int(sline[9].strip())}

            """close the file"""
            f.close()

    def loadCitiesPos(self):
            """Load text file with the location of the cities, the file
            is in the format:

            type_id, column_number, row_number
            (int)         (int)       (int)             

            After loading the file, City objects are created.
            Cities are an attribute of the Map object.
            """            
  
            f = open(self._cities_pos_file, 'U')
            
            for line in f:

                """read and process each line that has data, and save the info
                in the dictionary"""
                if line.rfind(',') != -1:

                    """splits each line into a list"""
                    splitted_line=line.split(',')
                    
                    """the info is used to create City objects. Whitespaces,
                    tabs and new lines are removed"""
                    type_id=splitted_line[0].strip()
                    col=int(splitted_line[1].strip())
                    row=int(splitted_line[2].strip())

                    x=col*engine.tile_x
                    y=row*engine.tile_y

                    self._resource_spots[Resource._nextID-1]=City(type_id,
                    self._resource_types[type_id]['filename'],
                    self._resource_types[type_id]['type'],
                    self._resource_types[type_id]['name'],
                    self._resource_types[type_id]['amount_per_turn'],
                    self._resource_types[type_id]['instant_amount'],
                    self._resource_types[type_id]['conquered_text'],
                    self._resource_types[type_id]['first_time_text'],x, y,
                    self._resource_types[type_id]['sld_cost_gold'],
                    self._resource_types[type_id]['sld_cost_ore'])
                    
            """close the file"""
            f.close()

    def getResourceObj(self, res_id):
        """Get the resource object with id "res_id". Precondition: the id refers
        to an existing resource object in the map"""

        return self._resource_spots[res_id]

        
engine=EngineObject()    

class Army(SpriteObj):
    """Superclass for the armies in the game. An army is represented bu a
    SpriteObj object displayed in the map, which has several attributes
    that define its current state and behaviour.    
    """

    _next_ID=1
    
    def __init__(self, filename, army_name, x0, y0, start_time, colour, map_obj,
    food=100,gold=50,ore=50,gems=50,soldiers=10):
        """Initialize the common attributes to all Army subclasses"""
        
        SpriteObj.__init__(self, filename)
        self._id=Army._next_ID
        Army._next_ID+=1
        self._name=army_name
        self._x=x0
        self._y=y0
        self._w=engine.tile_x
        self._h=engine.tile_y
        self._colour=colour
        self._map_obj=map_obj
        
        self._moves_per_turn=float(10)
        self._moves_left=self._moves_per_turn

        self._current_time=start_time
        self._speed = 2
        
        self._resources={'food':food,'gold':gold,'ore':ore, 'gems':gems}
                
        self._soldiers=soldiers

        """Initialize map visibility"""
        self.initializeVisibility(self._map_obj)
        
    def walk(self,dx,dy,map_obj):
        """Evaluate if it is possible to move the army a vector distance (dx,dy)
        in pixels from its current position. dx, dy go in the same direction as
        the coordinates of the map surface, which are positive going down and
        right"""
        
        if map_obj.getIsWalkable(self.rect.right-1+dx,self.rect.top+dy):            
            if map_obj.getIsWalkable(self.rect.right-1+dx,self.rect.bottom-1+dy):
                if map_obj.getIsWalkable(self.rect.left+dx,self.rect.top+dy):
                    if map_obj.getIsWalkable(self.rect.left+dx,
                    self.rect.bottom-1+dy):
                        
                        self.move(self._x+dx,self._y+dy)

    def move(self,x1,y1):
        """Move the army to the position (x1,y1). This coordinates are pixel
        coordinates of the MapCanvas gui element."""
        
        self._x=x1
        self._y=y1
    
    def display(self,surface):
        """Draw the Army in the destination surface"""
        
        self.rect.x=self._x
        self.rect.y=self._y
        surface.set_colorkey((255,0,255))
        surface.blit(self.image, self.rect)

    def getMovesLeft(self):
        """Get the number of moves the army has left for the turn"""
        
        return self._moves_left

    def getID(self):
        """Get the army's ID"""
        
        return self._id

    def updateResource(self, res_type, amount):
        """Update the specified resource type in 'amount' units"""

        self._resources[res_type]+=amount

    def getResources(self):
        """Get the resource amounts"""

        return self._resources

    def getSoldiers(self):
        """Get the amount of soldiers"""

        return self._soldiers

    def initializeVisibility(self, map_obj):
        """Initialize the army's visibility of the game map"""

        self._cell_visibility=[]
        map_dims = map_obj.getDimensions()

        for i in range(0,map_dims['num_rows']):
            self._cell_visibility.append([])
            for j in range(0,map_dims['num_cols']):
                self._cell_visibility[i].append(0)

        self.updateVisibility(map_obj)

    def update(self, clock, map_obj):
        """Updates Army's attributes. Called in every game loop."""

        delta_t = clock - self._current_time
        self._current_time = clock        

    def updateVisibility(self, map_obj):
        """Update the army's visibility according to its current location"""

        current_cell=map_obj.getCellFromXY(self._x,self._y)

        self._cell_visibility[current_cell['row']][current_cell['col']]=1

        first_row=current_cell['row']==0
        last_row=current_cell['row']==len(self._cell_visibility)-1
        first_col=current_cell['col']==0
        last_col=current_cell['col']==len(self._cell_visibility[0])-1
        
        if not(first_row):
            self._cell_visibility[current_cell['row']-1][current_cell['col']]=1

        if not(last_row):
            self._cell_visibility[current_cell['row']+1][current_cell['col']]=1

        if not(first_col):
            self._cell_visibility[current_cell['row']][current_cell['col']-1]=1

        if not(last_col):
            self._cell_visibility[current_cell['row']][current_cell['col']+1]=1

        if not(first_row) and not(first_col):
            self._cell_visibility[current_cell['row']-1][current_cell['col']-1]=1

        if not(first_row) and not(last_col):
            self._cell_visibility[current_cell['row']-1][current_cell['col']+1]=1

        if not(last_row) and not(first_col):
            self._cell_visibility[current_cell['row']+1][current_cell['col']-1]=1

        if not(last_row) and not(last_col):
            self._cell_visibility[current_cell['row']+1][current_cell['col']+1]=1

    def getCellVisibility(self):
        """Return the cell visibility matrix"""
        return self._cell_visibility

    def getColour(self):
        """Return the army's colour"""
        return self._colour

    def updateSoldiers(self,amount):
        """Update the amount of soldiers"""

        self._soldiers += amount

    def getName(self):
        """Get the name of the army"""
        return self._name
       
       

class Player(Army):
    """This class represents the army controlled by the player. It inherits the
    attributes of its super class Army, but handles the user input."""
    
    def __init__(self, filename, army_name, x0, y0, start_time, colour, map_obj,
    food=100,gold=50,ore=50,gems=10,soldiers=10):    
        """Initialize the Player object"""

        Army.__init__(self, filename, army_name, x0, y0, start_time, colour,
        map_obj, food,gold,ore,gems,soldiers)
        
        self._path = Path()
        self._is_moving=False
        self._dir_x=0
        self._dir_y=0
        self._dest_x=None
        self._dest_y=None
        self._pathpoints=[]        
        
    def __str__(self):
        """Return a string with information of the object"""
        return army_name

    def handleKeyboard(self,key_event,map_obj):
        """Handle user keyboard input"""
        pass


    def setPath(self,(x,y),map_obj):
        """Obtain the path from the player's current position to a destination
        point (x,y), in pixel coordinates of the map surface, using the A*
        algorithm from the satar_modif file."""
        
        """prepare parameters for the satar_modif object"""
        map_cost_1d = map_obj.getMoveCost1D()
        dest_cell = map_obj.getCellFromXY(x,y)
        current_cell = map_obj.getCellFromXY(self._x,self._y)                    
        map_dims=map_obj.getDimensions()

        if dest_cell != current_cell:
            """setup the satar_modif object"""
            astar = satar_modif.AStar(satar_modif.SQ_MapHandler(map_cost_1d,
            map_dims['num_cols']-1,map_dims['num_rows']-1))
            
            start = satar_modif.SQ_Location(current_cell['col'],
            current_cell['row'])

            end = satar_modif.SQ_Location(dest_cell['col'],dest_cell['row'])

            """find the path and convert the resulting nodes to pixels"""
            p = astar.findPath(start,end)

            if not p:
                self._path.reset()
                
            else:
                self._pathpoints = []
                self._pathpoints.append((start.x*engine.tile_x+self._w/2,
                start.y*engine.tile_y+self._h/2))

                for n in p.nodes:
                    self._pathpoints.append((
                    n.location.x*engine.tile_x+self._w/2,
                    n.location.y*engine.tile_y+self._h/2))
                
                """update the Path attribute"""                
                self._path.update(self._pathpoints,self._moves_left,map_obj)

        else:
            self._path.reset()
    
    def display(self,surface):
        """Draw the Player in the destination surface, path lines will be
        displayed if available."""
        
        self.rect.x=self._x
        self.rect.y=self._y
        surface.blit(self.image, self.rect)
        self._path.draw(surface, self)

    def update(self, clock, map_obj):
        """Updates Player's attributes. Called in every game loop."""

        Army.update(self,clock,map_obj)      

        if self._is_moving:
            """update position"""
            self._x +=self._speed * self._dir_x
            self._y +=self._speed * self._dir_y

            """update temporary gui elements"""
            """if its a city show city options button in the right panel"""
            gui.widgets[engine.getRightPanel()].closeCityOptionsButton()

            """when the next cell is reached, the path is updated and a
            checking is performed to see if the final cell of the path has
            been reached"""
            if self._x == self._dest_x and self._y == self._dest_y:

                self._moves_left-=self._current_move_cost
                
                self._x = self._dest_x
                self._y = self._dest_y
                self._dir_x=0
                self._dir_y=0

                current_cell=map_obj.getCellFromXY(self._x,self._y)
                final_destination=self._path.getFinalPoint()
                final_cell=map_obj.getCellFromXY(final_destination[0],
                final_destination[1])

                """update visibility"""
                self.updateVisibility(map_obj)

                """collition detection with resource spots is performed"""
                result, resource_id = map_obj.resOnCellXY(self._x,
                self._y)

                if result:
                    
                    """call the armyOnResource method of the resource"""
                    map_obj.armyOnResource(self,resource_id)
                    
                """if the army reached its final destination, stop moving"""
                if current_cell == final_cell:
                    self._is_moving=False
                    self._path.reset()

                else:
                    self.setPath((final_destination[0],final_destination[1]),
                    map_obj)

                    self.setMovingPath(map_obj)          
   

    def destinationCircleClicked(self,(x,y), map_obj):
        """Test if the destination circle of the path was clicked, in case
        there is a path displayed on the screen"""

        if self._path.pathDisplayed():
            dest_circle_xy=self._path.getDestCircleCoordinates()

            clicked_cell = map_obj.getCellFromXY(x,y)
            circle_cell = map_obj.getCellFromXY(dest_circle_xy[0],
            dest_circle_xy[1])

            if clicked_cell == circle_cell:
                return True

            else:
                return False
        else:
            return False

    def setMovingPath(self, map_obj):
        """Set the Army to follow the current path if there are moves left
        on the current turn."""
        
        next_point=self._path.getNextPoint()
        destination=map_obj.getCellCoordFromXY(next_point[0],next_point[1])
             
        """check if the user can move in the present turn"""
        move_cost=map_obj.getCostBetween2Points((self._x,self._y),
        (destination[0],destination[1]))

        if self._moves_left - move_cost >= 0:

            self._current_move_cost=move_cost
            self._is_moving=True
            
            self._dest_x=destination[0]
            self._dest_y=destination[1]
            
            current_cell = map_obj.getCellFromXY(self._x,self._y)
            dest_cell = map_obj.getCellFromXY(self._dest_x,self._dest_y)
            
            if dest_cell['col']-current_cell['col'] < 0:
                self._dir_x=-1
                
            elif dest_cell['col']-current_cell['col'] == 0:
                self._dir_x=0

            elif dest_cell['col']-current_cell['col'] > 0:
                self._dir_x=1

            if dest_cell['row']-current_cell['row'] < 0:
                self._dir_y=-1
                
            elif dest_cell['row']-current_cell['row'] == 0:
                self._dir_y=0

            elif dest_cell['row']-current_cell['row'] > 0:
                self._dir_y=1

        else:
            self._is_moving=False

    def isMoving(self):
        """Return if the player is currently moving"""

        return self._is_moving

    def newTurn(self,map_obj):
        """Actions to be performed when the turn is over"""

        self._moves_left = self._moves_per_turn
        self.update(pygame.time.get_ticks(),map_obj)

        if self._path.pathDisplayed():
            self.setPath(self._path.getFinalPoint(),map_obj)
        map_obj.payTurnResources(self)
        gui.setFocus(engine.getMapCanvas())

    def buySoldiers(self, num_sold, city_obj):
        """Try to buy soldiers depending on the cost of the soldiers,
        the quantity, and the available resources"""

        cost_gold, cost_ore = city_obj.getSoldierPrice()

        tot_cost_gold=cost_gold*num_sold
        tot_cost_ore=cost_ore*num_sold

        res=self.getResources()
        
        if tot_cost_gold > res['gold'] or tot_cost_ore > res['ore']:
            return False

        else:
            self.updateSoldiers(num_sold)
            self.updateResource('gold',-tot_cost_gold)
            self.updateResource('ore',-tot_cost_ore)
            return True
        

class Polyline():
    """Represents a sequence of lines to be displayed on a surface"""

    def __init__(self,points,colour):
        """Initialize a Polyline object.

        ([(int,int)],(int,int,int)) --> ()

        Precondition: the points are in pixel coordinates, in a list of
        tuppes in the format (x value,y value} they need to be
        contained in that surface"""

        self._points=points
        self._colour=colour
   
    def update(self,points):
        """Update the attributes of the Polyline object"""

        self._points=points
             
    def draw(self,surf):
        """Draw the polyline in the destination surface using
        python.draw.aalines"""
        
        if len(self._points)>1:
            pygame.draw.lines(surf, self._colour, False, self._points, 3)

    def reset(self):
        """Resets the Polyline so it wont be displayed"""
        
        self._points=[]

    def getNumPoints(self):
        """Get the number of points of the polyline"""
        
        return len(self._points)

    def changeSinglePoint(self,pos,x_new,y_new):
        """Change a single point withing the line, located in the position
        pos"""

        if len(self._points)>0:
            self._points[pos]=(x_new, y_new)

class Path():
    """Represents the visual path from the player's current position to a
    destination cell. It is composed of a green polyline representing the
    part of the path that can be completed in the current turn, a red
    polyline representing the part of the path that can't be completed
    in the current turn, and a circle on the final destination"""

    def __init__(self):
        """Initialize the Path objects"""

        self._blue=(0,102,204)
        self._red=(237,0,0)
        self._blueline = Polyline([],self._blue)
        self._redline = Polyline([],self._red)
        self._circle_drawn=False
        self._circle_pos=[]
        self._points=[]
        self._drawing_points=[]
                
    def update(self, points, moves_left, map_obj):
        """Update the path to a new destination. This is done by obtaining
        the sections of the path that can be done in the current turn."""

        self.reset()
        
        self._points=points
        self._bluepoints=[points[0]]
        self._redpoints=[]
                
        accum_cost = 0
        i=0

        while (accum_cost <= moves_left) and (i<len(points)-1):
            next_move=map_obj.getCostBetween2Points(points[i],points[i+1])

            if (moves_left - next_move - accum_cost) >= 0:                
                self._bluepoints.append(points[i+1])
                accum_cost += map_obj.getCostBetween2Points(points[i],
                points[i+1])
                
            else:
                break
            i+=1

        if i<(len(points)-1):
            self._redpoints=[points[i]]
            while i<(len(points)-1):
                self._redpoints.append(points[i+1])
                i+=1
        
        self._blueline.update(self._bluepoints)
        self._redline.update(self._redpoints)        
        
    def draw(self,surf,army_obj):
        """Draw the polylines and destination circle in the surface using
        pygame draw methods. The first point of the blue line is updated
        at the game frame rate so to that the path is always drawn from
        the army's current position."""         

        if self._blueline.getNumPoints()>1:

            self._blueline.changeSinglePoint(0,army_obj._x+engine.tile_x/2,
            army_obj._y+engine.tile_y/2)

            self._blueline.draw(surf)            
                
        if self._redline.getNumPoints()>1:                
            self._redline.draw(surf)       
            pygame.draw.circle(surf, self._red, self._points[len(
            self._points)-1], engine.tile_x/4)

            self._circle_drawn=True
            self._circle_pos=self._points[len(self._points)-1]
                
        elif self._redline.getNumPoints()<1 and self._blueline.getNumPoints()>1:

            pygame.draw.circle(surf, self._blue, self._points[len(
            self._points)-1], engine.tile_x/4)

            self._circle_drawn=True
            self._circle_pos=self._points[len(self._points)-1]                
                
    def reset(self):
        """Resets the Polyline so it wont be displayed"""
        self._bluepoints=[]
        self._blueline.reset()
        self._redpoints=[]
        self._redline.reset()
        self._circle_drawn=False
        self._circle_pos=[]
        self._drawing_points=[]

    def pathDisplayed(self):
        """Return if there is a path displayed on the screen"""
        
        return self._circle_drawn

    def getDestCircleCoordinates(self):
        """Get the coordinates of the destination circle"""

        return self._circle_pos

    def getNextPoint(self):
        """Get the coordinates of the closest point to the current positon
        of the Army"""

        return self._points[1]

    def getFinalPoint(self):
        """Get the last point of the path"""

        return self._points[len(self._points)-1]


class Resource(SpriteObj):
    """Represents a resource spot. A resource spot can be owned by an army. If
    owned, it will give the army a certain amount of the resource at the end of
    every turn."""

    _nextID=1

    def __init__(self, type_id, filename, resource_type, resource_name,
    amount_per_turn, instant_amount, conquered_text, first_time_txt,x, y):
        """Initialize the Resource object. This is done from the Map object"""

        SpriteObj.__init__(self, filename)
        self._type_id = type_id
        self._type = resource_type
        self._name = resource_name
        self._turn_amount = randint(int(0.6*amount_per_turn),
        int(1.4*amount_per_turn))

        self._instant_amount = randint(int(0.5*instant_amount),
        int(1.5*instant_amount))

        self._conquered_text=conquered_text
        self._first_time_txt=first_time_txt
        
        self._x=x
        self._y=y
        self.rect.x=x
        self.rect.y=y
        self._owner = None
        self._owner_name = None
        self._id = Resource._nextID
        Resource._nextID += 1

        self._is_city=False

        """Owners flagpole properties. the flag is composed of a rectangle
        for the flag itself, and a rectangle for the pole. The coordinates
        of both rectangles are the upper left corners"""
        self._xflag=self._x+2
        self._yflag=self._y+engine.tile_y/8
        self._wflag=engine.tile_x/3
        self._hflag=engine.tile_y/4

        self._xpole=self._xflag+self._wflag
        self._ypole=self._yflag
        self._wpole=2
        self._hpole=engine.tile_y*2/3
        self._pole_colour=(90,90,90)

        self._flag_rect=pygame.Rect(self._xflag,self._yflag,self._wflag,
        self._hflag)

        self._pole_rect=pygame.Rect(self._xpole,self._ypole,self._wpole,
        self._hpole)
        
    def setOwner(self, army_id, army_name, colour):
        """Set the owner of the resource"""

        self._owner = army_id
        self._owner_name = army_name
        self._owner_colour = colour

    def getOwner(self):
        """Get the owner of the resource"""

        return self._owner, self._owner_name

    def display(self, surf):
        """Draw the image on the specified surface. If the resource is owned,
        display a small flag on it"""

        SpriteObj.display(self,self._x,self._y,surf)

        if self._owner:
            pygame.draw.rect(surf, self._owner_colour, self._flag_rect, 0)
            pygame.draw.rect(surf, self._pole_colour, self._pole_rect, 0)
                        

    def getPos(self):
        """Get the pixel coordinates of the Resource"""
        return self._x, self._y

    def getID(self):
        """Return the id attribute"""
        return self._id

    def getConqueredText(self):
        """Return a string to be displayed when the Resource is conquered"""

        text=self._conquered_text

        if not(self._owner):
            text=text + ' ' + self._first_time_txt

        """replace keywords by attribute values"""
        text=text.replace('_TURN_AMOUNT',str(self._turn_amount))
        text=text.replace('_RESOURCE',str(self._type))
        text=text.replace('_INSTANT_AMOUNT',str(self._instant_amount))
                     
        return self._name, text

    def getType(self):
        """Get the resource type"""

        return self._type

    def getTurnAmount(self):
        """Get the amount of resource to be paid at the end of every turn"""

        return self._turn_amount

    def payFirstAmount(self):
        """Get the amount of resource to be paid to the first army that owns
        the resource spot."""

        first_payment = self._instant_amount
        self._instant_amount = 0  
        return first_payment

    def isCity(self):
        """Check if the resource is a city or not"""

        return self._is_city

    def getName(self):
        """Get the name of the resource"""

        return self._name

class City(Resource):
    """Represents a city. Cities have the same behaviour as resource spots,
    but they also offer the option to buy soldiers."""

    _nextID=1

    def __init__(self, type_id, filename, resource_type, name,
    amount_per_turn, instant_amount, conquered_text, first_time_txt,x, y,
    price_gold, price_ore):
        
        """Initialize the City object."""

        Resource.__init__(self, type_id, filename, resource_type, name,
        amount_per_turn, instant_amount, conquered_text, first_time_txt,x, y)

        self._is_city=True
        
        self._price_gold=price_gold
        self._price_ore=price_ore

    def getSoldierPrice(self):
        """Get the price of one soldier"""

        return self._price_gold, self._price_ore        
