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
#   File: game.py
#
#   Description: This file contains the main loop and the game loop for World of
#   Heroes, a 2D turn-based strategy game.
#
#   In this function the main gameplay elements are initialized and displayed on
#   the screen. This function features the game loop as well, which is executed
#   at the frame rate specified in the EngineObj element, in the file game_lib.
#
################################################################################

from gui_lib import *
from woh_gui_lib import *
from game_lib import *


def main():
    """Main function of the game. In this function the main gameplay elements
    are initialized and displayed on the screen. This function features the
    game loop as well, which is executed at the frame rate specified in the
    EngineObj element, in the file game_lib."""
    
    """Initialize pygame parameters"""
    pygame.display.set_caption('World of Heroes')
    pygame.key.set_repeat(500, 30)    
        
    """Initialize clock"""
    clock = pygame.time.Clock()
    time = pygame.time.get_ticks()

    """Create main game objects and load the current scenario"""
    game_map=Map('map.txt','terrtypes.txt','resource_types.txt','resource_pos.txt',
    'cities.txt','cities_pos.txt')

    red=(220,20,60)
    heroe=Player('images/heroe.png','heroe',0,0, time, red, game_map)
    
    """Create main GUI objects"""
    right_panel_w=128
    right_panel_h=768
    right_panel_pos_x=896
    right_panel_pos_y=0

    bottom_panel_w=896
    bottom_panel_h=32
    bottom_panel_pos_x=0
    bottom_panel_pos_y=736

    map_canv_w=896
    map_canv_h=736
    map_canv_pos_x=0
    map_canv_pos_y=0
    
    main_widget_id=gui.addWidget(Widget(None,1024,768,(0,0,0),0,0))

    right_panel_id=gui.addWidget(RightPanel(main_widget_id,right_panel_w,
    right_panel_h,(255,0,0),right_panel_pos_x,right_panel_pos_y,game_map,
    heroe,'images/right_panel.jpg'))

    bottom_panel_id=gui.addWidget(BottomPanel(main_widget_id,bottom_panel_w,
    bottom_panel_h,(0,150,0),bottom_panel_pos_x,bottom_panel_pos_y,
    'images/bottom_panel.jpg'))

    map_canv_id=gui.addWidget(MapCanvas(main_widget_id,map_canv_w,map_canv_h,
    (0,0,0),map_canv_pos_x,map_canv_pos_y))

    engine.setMapCanvas(map_canv_id)
    engine.setRightPanel(right_panel_id)
        
    """show widgets"""
    gui.widgets[main_widget_id].show(False)
    gui.widgets[map_canv_id].show(True)
    gui.widgets[right_panel_id].show(False)
    gui.widgets[bottom_panel_id].show(True)

    """initialize gameplay related widgets"""
    gui.widgets[right_panel_id].initializeGameRelated()
    gui.widgets[map_canv_id].initializeGameRelated(heroe, game_map)

    key_pressed=False
    mouse_pressed=False

    """Game loop"""
    while 1:

        """Frame rate per second specified in the EngineObj object"""
        clock.tick(engine.fps)
        time = pygame.time.get_ticks() 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            """When there is keyboard, send the event to the widget that has the
            user focus"""
            if event.type == pygame.KEYDOWN:
                gui.widgets[gui.getFocus()].handleKeyboard(event, (heroe,
                game_map))

                key_pressed=True
                
            elif event.type == pygame.KEYDOWN and key_pressed==True:
                key_pressed=False

            """Mouse events are sent to the main widget"""
            if pygame.mouse.get_pressed() in (MOUSE_LEFT, MOUSE_RIGHT) and not(mouse_pressed):
                mouse_pressed=True
                gui.widgets[main_widget_id].clickOnWidget(pygame.mouse.get_pressed(),pygame.mouse.get_pos(),
                (heroe))
                
            if pygame.mouse.get_pressed()==MOUSE_NOT_PRESSED and mouse_pressed==True:
                mouse_pressed=False
            
            
        """update game elements"""
        heroe.update(time, game_map)
        gui.updateWidgets((heroe,game_map))
        
        """display elements on the screen"""
        #screen.fill(black)
        gui.widgets[main_widget_id].display(screen)
        game_map.display(gui.widgets[map_canv_id].getSurf(), heroe)    
        heroe.display(gui.widgets[map_canv_id].getSurf())       
        pygame.display.flip()
        
main()
