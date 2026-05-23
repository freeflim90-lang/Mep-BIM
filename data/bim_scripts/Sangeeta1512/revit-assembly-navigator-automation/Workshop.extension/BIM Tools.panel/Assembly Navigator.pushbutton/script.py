# -*- coding: utf-8 -*-
from pyrevit import revit
import clr
import os

clr.AddReference("System")
clr.AddReference("PresentationCore")
clr.AddReference("PresentationFramework")
clr.AddReference("WindowsBase")

from System.Collections.Generic import List
from System.Windows import Window, Thickness, HorizontalAlignment, WindowStartupLocation, Visibility
from System.Windows.Controls import StackPanel, DockPanel, ScrollViewer, CheckBox, Button, TextBox, Dock

# DLL path
base_dir = os.path.dirname(__file__)
dll_path = os.path.join(base_dir, "lib", "AssemblyHelper.dll")
clr.AddReferenceToFileAndPath(dll_path)

from RevitAssemblyTools import AssemblyService

uidoc = revit.uidoc
service = AssemblyService(uidoc)

# all assemblies
assemblies = service.GetAllAssemblies()

# selected in model
selected_names_net = service.GetSelectedAssemblyNames()
selected_names = set([x for x in selected_names_net if x])

# unique names
all_names = sorted(set([a.Name for a in assemblies if a.Name]))

# selected at top
top_names = [n for n in all_names if n in selected_names]
remaining_names = [n for n in all_names if n not in selected_names]
display_names = top_names + remaining_names


class AssemblyPicker(Window):
    def __init__(self, names, selected):
        self.Title = "Select Assemblies"
        self.Width = 350
        self.Height = 550
        self.WindowStartupLocation = WindowStartupLocation.CenterScreen
        self.selected_result = None
        self._updating_all = False

        root = DockPanel()
        root.Margin = Thickness(10)
        self.Content = root

        # top area
        top_panel = StackPanel()
        DockPanel.SetDock(top_panel, Dock.Top)
        root.Children.Add(top_panel)

        self.search_box = TextBox()
        self.search_box.Height = 28
        self.search_box.Margin = Thickness(0, 0, 0, 8)
        self.search_box.TextChanged += self.on_search_changed
        top_panel.Children.Add(self.search_box)

        self.select_all_cb = CheckBox()
        self.select_all_cb.Content = "Select All"
        self.select_all_cb.Margin = Thickness(0, 0, 0, 8)
        self.select_all_cb.IsChecked = False
        self.select_all_cb.Checked += self.on_select_all_changed
        self.select_all_cb.Unchecked += self.on_select_all_changed
        top_panel.Children.Add(self.select_all_cb)

        # bottom button
        select_btn = Button()
        select_btn.Content = "Select"
        select_btn.Width = 90
        select_btn.Height = 30
        select_btn.HorizontalAlignment = HorizontalAlignment.Right
        select_btn.Click += self.on_select
        DockPanel.SetDock(select_btn, Dock.Bottom)
        root.Children.Add(select_btn)

        # list area
        scroll = ScrollViewer()
        DockPanel.SetDock(scroll, Dock.Top)
        root.Children.Add(scroll)

        self.items_panel = StackPanel()
        scroll.Content = self.items_panel

        self.checkboxes = []
        for name in names:
            cb = CheckBox()
            cb.Content = name
            cb.Margin = Thickness(2, 2, 2, 2)
            cb.IsChecked = name in selected
            cb.Checked += self.on_item_changed
            cb.Unchecked += self.on_item_changed
            self.items_panel.Children.Add(cb)
            self.checkboxes.append(cb)

        self.update_select_all_state()

    def get_visible_checkboxes(self):
        return [cb for cb in self.checkboxes if cb.Visibility == Visibility.Visible]

    def on_search_changed(self, sender, args):
        text = (self.search_box.Text or "").strip().lower()

        for cb in self.checkboxes:
            name = str(cb.Content).lower()
            if not text or text in name:
                cb.Visibility = Visibility.Visible
            else:
                cb.Visibility = Visibility.Collapsed

        self.update_select_all_state()

    def on_select_all_changed(self, sender, args):
        if self._updating_all:
            return

        state = self.select_all_cb.IsChecked
        for cb in self.get_visible_checkboxes():
            cb.IsChecked = state

    def on_item_changed(self, sender, args):
        self.update_select_all_state()

    def update_select_all_state(self):
        self._updating_all = True

        visible_cbs = self.get_visible_checkboxes()
        if visible_cbs and all(cb.IsChecked for cb in visible_cbs):
            self.select_all_cb.IsChecked = True
        else:
            self.select_all_cb.IsChecked = False

        self._updating_all = False

    def on_select(self, sender, args):
        self.selected_result = [str(cb.Content) for cb in self.checkboxes if cb.IsChecked]
        self.DialogResult = True
        self.Close()


form = AssemblyPicker(display_names, selected_names)
result = form.ShowDialog()

if result and form.selected_result:
    net_names = List[str]()
    for name in form.selected_result:
        net_names.Add(name)
    service.SelectAssembliesByNames(net_names)