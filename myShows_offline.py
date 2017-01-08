import wx
import os
import sys
import ntpath
from datetime import datetime
from myshows.api_client import MyShowsClient
from myshows.exceptions import *
from notifu import notify

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        credentials = self.ReadSettings()

        self.dirname = credentials['path']

        self.client = MyShowsClient(credentials['login'], credentials['password'])
        self.client.login()

        self.listOfEpisodes, self.checkedEpisodes = self.LoadEpisodes()

        wx.Frame.__init__(self, parent, title=title, size=(320,400))
        self.control = wx.CheckListBox(self, choices=self.listOfEpisodes, style=wx.LB_SINGLE)
        self.CreateStatusBar()

        filemenu= wx.Menu()
        menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        settingsmenu = wx.Menu()
        menuPath = settingsmenu.Append(wx.ID_OPEN, "&Path"," Edit the path to your episodes")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        menuBar.Append(settingsmenu,"&Settings")
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Events.
        self.Bind(wx.EVT_MENU, self.OnPath, menuPath)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        self.Show()

    def LoadEpisodes(self):
        episodes = []
        echeckedEpisodes = []
        for self.dirname, dirnames, filenames in os.walk(self.dirname):
            for filename in filenames:
                episode = self.client.find_episode(filename)
                if episode:
                    episodes.append(filename)

        '''
        for filename in os.listdir(self.dirname):
            episodes.append(filename)
        '''

        return episodes, checkedEpisodes

    def ReadSettings(self):
        path = ntpath.dirname(sys.argv[0])
        with open(ntpath.join(path, 'settings.txt'), 'r') as f:
            settings = f.readlines()
        credentials = {}
        for s in settings:
            x, y = s.split('=')
            x = x.strip()
            y = y.strip()
            credentials[x] = y
        return credentials

    def OnAbout(self,e):
        # Create a message dialog box
        dlg = wx.MessageDialog(self, " MyShows offline tool for desktop \n in wxPython", "About this app", wx.OK)
        dlg.ShowModal() # Shows it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

    def OnPath(self,e):
        """ Choose the path"""
        dlg = wx.DirDialog(self, "Choose a path", self.dirname)
        if dlg.ShowModal() == wx.ID_OK:
            self.dirname = dlg.GetPath()
            self.listOfEpisodes, self.checkedEpisodes = self.LoadEpisodes()
            self.control.Clear()
            self.control.InsertItems(self.listOfEpisodes, 0)
            # TODO
        dlg.Destroy()

app = wx.App(False)
frame = MainWindow(None, "MyShows Offline")
app.MainLoop()