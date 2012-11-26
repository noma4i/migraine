import sublime, sublime_plugin
import os
import re

class MigraineCommand(sublime_plugin.WindowCommand):
  def run(self):
    try:
      cur_path = self.window.active_view().file_name()
    except AttributeError:
      if self.window.folders():
        cur_path = self.window.folders()[0]
    if cur_path:
      if os.path.isfile(cur_path):
        cur_path = os.path.dirname(cur_path)
      root = self.find_ror_root(cur_path)
    else:
      raise NothingOpen("Open folder or file")
    if root:
      self.migrations_dir = os.path.join(root, 'db', 'migrate')
      migrations = os.listdir(self.migrations_dir)

      pattern = re.compile('^\d+_\w+.rb$')
      migrations = sorted([m for m in migrations if pattern.match(m)])
      latest_migration = os.path.join(self.migrations_dir, migrations[-1])

      self.panel_items = migrations
      self.window.show_quick_panel(self.panel_items, self.open_selected)

  def open_selected(self,selected_file_index):
    if selected_file_index != -1:
      full_path = os.path.join(self.migrations_dir, self.panel_items[selected_file_index])
      sublime.active_window().open_file(full_path)

  def find_ror_root(self, path):
    expected_items = ['Gemfile', 'app', 'config', 'db']
    files = os.listdir(path)

    if path == '/':
      raise NotRailsApp("Can't find Rails project")
    if len([x for x in expected_items if x in files]) == len(expected_items):
      return path
    else:
      return self.find_ror_root(self.parent_path(path))

  def parent_path(self, path):
    return os.path.abspath(os.path.join(path, '..'))

  def on_done(self,list):
    return path

class Error(Exception):
  def __init__(self, msg):
    self.msg = msg
    sublime.error_message(self.msg)

class NotRailsApp(Error):
  pass
class NothingOpen(Error):
  pass