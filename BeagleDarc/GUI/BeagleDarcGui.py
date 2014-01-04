#!/usr/bin/env python
import os
import sys
import pygtk  
pygtk.require("2.0")  
import gtk  


from BeagleDarc.Model import BeagleDarcServerM 
from BeagleDarc.Controller import Controller

class BeagleDarcGui:

    wTree = gtk.Builder()

    def __init__( self ):
        path, fil = os.path.split(os.path.abspath(__file__))
        bds = BeagleDarcServerM('beagledarc_server')
        self.controller = Controller()

        self.builder = gtk.Builder()
        self.builder.add_from_file(path+"/glade/beagledarc.glade")
        self.window = self.builder.get_object ("window1")
        self.window.set_events(self.window.get_events() | gtk.gdk.BUTTON_PRESS_MASK)

        if self.window:
            self.window.connect("destroy", gtk.main_quit)

        #Toggle button to connect to beaglebone
        self.connect_togglebutton = self.builder.get_object ("connect_togglebutton")
        self.connect_togglebutton.connect("toggled", self.callback, "Connection")

        #default entries
        self.entry1 = self.builder.get_object("entry1")
        self.entry2 = self.builder.get_object("entry2")
        self.entry3 = self.builder.get_object("entry3")
        self.entry4 = self.builder.get_object("entry4")

        self.entry1.set_text(bds.host ) 
        self.entry2.set_text(bds.user ) 
        self.entry3.set_text(bds.password) 
        self.entry4.set_text(bds.port ) 

        dic = { 
            "on_buttonQuit_clicked" : self.quit,
            "on_window1_destroy" : self.quit,
            "gtk_widget_destroy" : self.quit,
            "on_phasescreen_menuitem_activate" : self.phasescreen,
            "on_stars_menuitem_activate" : self.stars
        }
        
        self.builder.connect_signals( dic )

    def callback(self, widget, data=None):
        '''
        callback
        '''
        print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
        if widget.get_active() is True:
            widget.set_label(gtk.STOCK_DISCONNECT)
            widget.set_use_stock(True)
            self.controller.start_BBBServer()

        if widget.get_active() is False:
            widget.set_label(gtk.STOCK_CONNECT)
            widget.set_use_stock(True)
            self.controller.stop_BBBServer()

    def quit(self, widget):
        sys.exit(0)


    def phasescreen(self, widget):
        from GUI import LayersGui
        from GUI import LayerData
        LayersGui.Layers()
        LayerData.LayerData()

    def stars(self, widget):
        from GUI import StarsGui
        from GUI import StarData
        StarsGui.Main()
        StarData.StarData()

BeagleDarcGui = BeagleDarcGui()
BeagleDarcGui.window.show()
gtk.main()
