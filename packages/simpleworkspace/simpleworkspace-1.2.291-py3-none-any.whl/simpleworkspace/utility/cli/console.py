import os as _os
from simpleworkspace.utility import strings as _strings
import abc as _abc
from simpleworkspace.settingsproviders import SettingsManager_BasicConfig as _SettingsManager_BasicConfig


def LevelPrint(level:int, msg="", flush=False, end='\n'):
    print(_strings.IndentText(msg, level, indentStyle='    '), flush=flush, end=end)

def LevelInput(level:int, msg="", flush=False, end=''):
    LevelPrint(level,msg=msg,flush=flush,end=end)
    return input()

def AnyKeyDialog(msg=""):
    if msg != "":
        msg += " - "
    msg += "Press enter to continue..."
    input(msg)

def Clear():
    _os.system("cls" if _os.name == "nt" else "clear")
    return

def Prompt_YesOrNo(question:str) -> bool:
    '''
    prompts user indefinitely until one of the choices are picked

    output style: "<question> [Y/N]:"
    @return: boolean yes=True, no=False
    '''
    
    while(True):
        answer = input(question + " [Y/N]:").upper()
        if(answer == "Y"):
            return True
        elif(answer == "N"):
            return False

def Print_SelectFileDialog(message="Enter File Paths", indentLevel=0) -> list[str]|None:
    import shlex
    LevelPrint(indentLevel, f"-{message}")
    filepathString = LevelInput(indentLevel, "-")
    filepaths = shlex.split(filepathString)
    if(len(filepaths) == 0):
        return None
    return filepaths

class ConsoleApp:
    class View(_abc.ABC):
        def __init__(self, parent:'ConsoleApp.View'=None):
            self.title:str = self.__class__.__name__
            '''The title displayed in parent menus'''
            self.views:list['ConsoleApp.View'] = []
            '''Child views that will be shown as selectable options'''

            self.viewHeader:str = None
            '''Adds a message right below the namespace of the view'''
            self.tempViewMessage:str = None
            '''Adds a temporary message that is shown once, mainly for child views to give feedback'''
            self.level = 0
            self.parent = parent
            self.namespace = [self.__class__.__name__]
            if(self.parent):
                self.namespace = [*parent.namespace, *self.namespace]

        def InitView(self):
            """Sets up the ui with current namespace view and child views as options if specified 

            :return: False as long as there are choices to make and user does request to go exit
            """
            Clear()
            namespaceString = '/' + '/'.join(self.namespace)
            if(len(namespaceString) > 100):
                namespaceString = '/...' + namespaceString[-96:]
            LevelPrint(0, namespaceString)
            self.level = 1
            if(self.viewHeader):
                LevelPrint(self.level, self.viewHeader, end='\n\n')
            if(self.tempViewMessage):
                LevelPrint(self.level, f'[{self.tempViewMessage}]')
                self.tempViewMessage = None
            choices:dict[str, ConsoleApp.View] = {}
            if not self.views:
                return True
            i = 1
            for view in self.views:
                choices[str(i)] = view
                LevelPrint(self.level, f'{i}. {view.title}')
                i += 1

            if(self.parent is None):
                LevelPrint(self.level, f'0. Quit')
            else:
                LevelPrint(self.level, f'0. Go Back')

            answer = LevelInput(self.level, "- Input: ")
            if(answer == '0'):
                return True
            elif(answer in choices):
                view = choices[answer]
                view.level = self.level + 1
                view.Start()
                view.Close()
            else:
                LevelInput(self.level + 1, "* Invalid input...")
            
            return False

        def Start(self):
            '''Start hook, can perform an action and return to parent view right away or call initview to make it interactive'''
            while not self.InitView(): ...

        def Close(self): ...
    
    class SettingsView(View):
        def __init__(self, parent:'ConsoleApp.View', settingsManager: _SettingsManager_BasicConfig):
            class AddNewSettingView(ConsoleApp.View):
                def __init__(self, parent: ConsoleApp.View = None):
                    super().__init__(parent)
                    self.title = "Add New Setting"

                def Start(self):
                    while not self.InitView():...
                    key = LevelInput(self.level, "Setting Name: ")
                    value = LevelInput(self.level, "Setting Value: ")
                    settingsManager.Settings[key] = value

                    self.parent.tempViewMessage = f"Added setting: {key}={value}"

            class RemoveASettingView(ConsoleApp.View):
                def __init__(self, parent: ConsoleApp.View = None):
                    super().__init__(parent)
                    self.title = "Delete Setting"

                def Start(self):
                    while not self.InitView():...
                    key = LevelInput(self.level, "Setting Name: ")
                    if(key in settingsManager.Settings):
                        del settingsManager.Settings[key] 
                        self.parent.tempViewMessage = f"Removed setting: {key}"
                    else:
                        self.parent.tempViewMessage = f"Setting not found: {key}"


            class ChangeASettingView(ConsoleApp.View):
                def __init__(self, parent: ConsoleApp.View = None, settingName=None):
                    super().__init__(parent)
                    if(settingName is None):
                        raise Exception("SettingName not supplied to view")
                    self.title = f'{settingName} = {settingsManager.Settings[settingName]}'
                    self.viewHeader = f'Current: {self.title}'
                    self.settingName = settingName
                
                def Start(self):
                    while not self.InitView():...
                    newValue = LevelInput(self.level, "- New Value: ")
                    settingsManager.Settings[self.settingName] = newValue
                    self.parent.tempViewMessage = f"Changed setting: {self.settingName}={newValue}"


            class ChangeView(ConsoleApp.View):
                def __init__(self, parent: ConsoleApp.View = None):
                    super().__init__(parent)
                    self.title = "Change"
                    self.RefreshViews()

                def RefreshViews(self):
                    self.views = [
                        AddNewSettingView(self),
                        RemoveASettingView(self),
                        *[ChangeASettingView(self, key) for key in settingsManager.Settings]
                    ]
                
                def Start(self):
                    self.RefreshViews()
                    while not self.InitView():
                        self.RefreshViews()

            class ResetSettingsAction(ConsoleApp.View):
                def Start(self):
                    settingsManager.ClearSettings()
                    self.parent.tempViewMessage = "* Settings resetted, save settings to persist this change"

            class SaveSettingsAction(ConsoleApp.View):
                def __init__(self, parent: ConsoleApp.View = None):
                    super().__init__(parent)
                    self.title = 'Save'

                def Start(self):
                    settingsManager.SaveSettings()
                    self.parent.tempViewMessage = "* Settings Saved"
            
            super().__init__(parent)
            self.settingsManager = settingsManager
            self.viewHeader = settingsManager._settingsPath
            self.views = [
                ChangeView(self),
                ResetSettingsAction(self),
                SaveSettingsAction(self)
            ]

                
        def Close(self):
            self.settingsManager.LoadSettings()
