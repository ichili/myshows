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
        self.control.SetCheckedStrings(self.checkedEpisodes)

        self.CreateStatusBar()

        filemenu= wx.Menu()
        menuAbout= filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        settingsmenu = wx.Menu()
        menuPath = settingsmenu.Append(wx.ID_OPEN, "&Path"," Edit the path to your episodes")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        menuBar.Append(settingsmenu,"&Settings")
        self.SetMenuBar(menuBar)

        # Events.
        self.Bind(wx.EVT_MENU, self.OnPath, menuPath)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_CHECKLISTBOX, self.OnCheck, self.control)

        self.Show()

    def LoadEpisodes(self):
        episodes = []
        checkedEpisodes = []

        for self.dirname, dirnames, filenames in os.walk(self.dirname):
            for filename in filenames:
                episode = self.client.find_episode(filename)
                if episode:
                    episodes.append(filename)
                    sid = self.client.get_show_id(filename)
                    viewedEpisodes = self.client.checked_episodes(sid).keys()
                    if episode in viewedEpisodes:
                        checkedEpisodes.append(filename)
                    
        '''
        for filename in os.listdir(self.dirname):  <-- looks only at files in dirname,
            episodes.append(filename)                  not subdirs
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

    def OnCheck(self,e):
        #changed = self.control.IsChecked(0)
        newCheckedEpisodes = list(self.control.GetCheckedStrings())

        #print(self.checkedEpisodes)

        for episode in self.listOfEpisodes:
            sid = self.client.get_show_id(episode)
            viewedEpisodes = self.client.checked_episodes(sid).keys()
            if episode in newCheckedEpisodes and episode not in self.checkedEpisodes:
                if episode not in viewedEpisodes:
                    self.client.check_episode(episode)
                # Check this episode
            elif episode not in newCheckedEpisodes and episode in self.checkedEpisodes:
                if episode in viewedEpisodes:
                    self.client.uncheck_episode(episode)
                # Uncheck this episode

        self.checkedEpisodes = newCheckedEpisodes

        #print(newCheckedEpisodes)

    def OnAbout(self,e):
        dlg = wx.MessageDialog(self, " MyShows offline tool for desktop \n in wxPython", "About this app", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self,e):
        self.Close(True)

    def OnPath(self,e):
        dlg = wx.DirDialog(self, "Choose a path", self.dirname)
        if dlg.ShowModal() == wx.ID_OK:
            self.dirname = dlg.GetPath()
            self.listOfEpisodes, self.checkedEpisodes = self.LoadEpisodes()
            self.control.Clear()
            self.control.InsertItems(self.listOfEpisodes, 0)
            self.control.SetCheckedItems(self.checkedEpisodes)
            # TODO
        dlg.Destroy()

app = wx.App(False)
frame = MainWindow(None, "MyShows Offline")
app.MainLoop()