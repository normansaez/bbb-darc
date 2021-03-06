#!/usr/bin/env python
import os
import sys
import pygtk  
pygtk.require("2.0")  
import gtk  


from BeagleDarc.Model import BeagleDarcServerM 
from BeagleDarc.Controller import Controller
from GUI import LayersGui
from GUI import LayerData
from GUI import StarsGui
from GUI import StarData

class BeagleDarcGui:

    wTree = gtk.Builder()

    def __init__( self ):
        path, fil = os.path.split(os.path.abspath(__file__))
        self.bds = BeagleDarcServerM('beagledarc_server')
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
        self.image4 = self.builder.get_object("image4")

        self.entry1.set_text(self.bds.host ) 
        self.entry2.set_text(self.bds.user ) 
        self.entry3.set_text(self.bds.ior) 

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
        print "%s: %s" % (data, ("disconnecting", "connecting")[widget.get_active()])
        #CONN
        if widget.get_active() is True:
            widget.set_label(gtk.STOCK_DISCONNECT)
            widget.set_use_stock(True)
            self.image4.set_from_stock(gtk.STOCK_CONNECT, gtk.ICON_SIZE_MENU)
            self.bds.ior = self.entry3.get_text()
            #Layers
            #LayersGui.Layers()
            #LayerData.LayerData()
            #StarsGui.Main()
            #StarData.StarData()

        if widget.get_active() is False:
            widget.set_label(gtk.STOCK_CONNECT)
            widget.set_use_stock(True)
            self.image4.set_from_stock(gtk.STOCK_DISCONNECT, gtk.ICON_SIZE_MENU)

    def quit(self, widget):
        sys.exit(0)


    def phasescreen(self, widget):
        LayersGui.Layers()
        LayerData.LayerData()

    def stars(self, widget):
        StarsGui.Main()
        StarData.StarData()

BeagleDarcGui = BeagleDarcGui()
BeagleDarcGui.window.show()
gtk.main()
