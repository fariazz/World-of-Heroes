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
#    * Neither the name of the <ORGANIZATION> nor the names of its contributors
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
#   Project: World of Heroes
#
#   File: gui_example.py
#
#   Description: This file presents an example layout composed of the GUI
#   objects developed for World of Heroes. This elements are game
#   independent, as all the game specific widgets were put in a separate file,
#   and thus they could be use in other pygame projects.
#
################################################################################

from gui_lib import *

def main():
    """Main function of the GUI example"""
    
    pygame.display.set_caption('GUI Example')

    """Create widgets by adding them to the GUI object"""
    main_widget_id=gui.addWidget(Widget(None,1024,768,(0,0,0),0,0))

    d1_id=gui.addWidget(Dialog(main_widget_id,200,200,(100,200,120),100,150,
    'Dialog box',12,'images/desert.jpg',18))

    d3_id=gui.addWidget(Dialog(main_widget_id,400,200,(255,255,255),350,0,
    'Text input dialog',10,'images/tundra.jpg',16))

    d2_id=gui.addWidget(Dialog(main_widget_id,400,400,(160,20,40),350,250,
    'Title',10,'images/dialog_bg.jpg',16))

    button1_id=gui.addWidget(Button(d1_id,140,40,(200,120,100),20,70,'Close',
    'images/button_background.png',20,button_close_parent))

    button2_id=gui.addWidget(Button(d1_id,170,40,(100,200,120),20,130,'Show Input Dialog',
    'images/button_background.png',18,show_widget,d3_id))

    text1_id=gui.addWidget(TextWidget(d2_id,100,120,(255,255,255),45,85,
    'The GUI contained in gui_lib.py is independent from WOH and could be used in other pygame proyects.'))

    image1_id=gui.addWidget(ImageWidget(d2_id,40,40,(0,0,0),200,100,
    'images/forest.jpg')) 

    button3_id=gui.addWidget(Button(d2_id,130,35,(100,200,120),45,40,
    'Change text','images/button_background.png',16,button_change_text,(text1_id,'Today is a good day')))

    button4_id=gui.addWidget(Button(d2_id,130,35,(100,200,120),50,250,
    'Change image!','images/button_background.png',16,button_change_img,
    (image1_id,'images/mountain.jpg')))

    button5_id=gui.addWidget(Button(d3_id,120,35,(200,120,100),50,150,'Close',
    'images/button_background.png',20,button_close_parent))

    txtinput1_id=gui.addWidget(TextInput(d3_id,110,25,(255,255,255),50,85,'str',14))

    txtinput2_id=gui.addWidget(TextInput(d3_id,110,25,(255,255,255),200,85,'int',100))


    """Display widgets"""
    gui.widgets[main_widget_id].show()
    
    """Initialize clock"""
    clock = pygame.time.Clock()
    
    while 1:      

        """set frame rate"""
        clock.tick(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            """Pass key events to the widget that is in the users focus"""
            if event.type == pygame.KEYDOWN:
                gui.widgets[gui.getFocus()].handleKeyboard(event)

            """Mouse events are passed to the parent widget"""
            if pygame.mouse.get_pressed()==(1,0,0):
                gui.widgets[main_widget_id].clickOnWidget(pygame.mouse.get_pos())

        """display layout"""
        screen.fill(black)
        gui.widgets[main_widget_id].display(screen)  
        pygame.display.flip()

main()
