#!/usr/bin/env python
'''
Stars
'''
import os
import pygtk
pygtk.require('2.0')
import gtk

from star_coord import star_coord
from BeagleDarc.Controller import Controller

class Stars:
    '''
    Stars
    '''
    def __init__(self):
        self.path, fil = os.path.split(os.path.abspath(__file__))
        self.win = gtk.Window()
        self.win.set_size_request(800, 800)
        self.win.set_title('Stars')
        self.win.set_resizable(False)
        self.win.set_events(self.win.get_events() | gtk.gdk.BUTTON_PRESS_MASK)
        self.win.connect('destroy', gtk.main_quit)
       

        self.fix = gtk.Fixed()
        self.win.add(self.fix)
        self.win.show_all()
        img = gtk.Image()
        img.set_from_file(self.path+'/img/star800.png')
        img.show()
        self.fix.put(img, 0, 0)
        #Creating controller
        self.controller = Controller()
        star_status = self.controller.get_stars_status()
        #Create all buttons here:
        for i in range(1, star_coord.__len__() +1):
            if i <= 53:
                button = gtk.ToggleButton("%d"%i)
                button.connect("toggled", self.callback, "%d"%i)
                button.show()
                self.fix.put(button, star_coord[i][0], star_coord[i][1])
                self.default_style_toogle = button.get_modifier_style()
                if star_status[i].__contains__('ON') is True:
                    button.set_active(True)
            else:
                pass
        
    def callback(self, widget, data=None):
        '''
        callback
        '''
        print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
        star = int(data)
        map   = widget.get_colormap()
        color_on  = map.alloc_color("red")

        if widget.get_active() is True:
            widget.modify_bg(gtk.STATE_ACTIVE, color_on)
            
            try:
                self.controller.star_on(star)
            except Exception, e:
                print e
        else:
            widget.modify_style(self.default_style_toogle)
            try:
                self.controller.star_off(star)
            except Exception, e:
                print e

if __name__ == '__main__':
    app = Stars()
    gtk.main()
