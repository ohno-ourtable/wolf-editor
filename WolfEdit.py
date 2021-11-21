import PySimpleGUI as sg
import os
import sys
import codecs
import io
from os import error, listdir
from os.path import isfile, join
import traceback

versionCode = "1.6"

if os.path.exists(os.path.expanduser("~") + '/WolfEditorDocuments'):
    pass
else:
    os.mkdir(os.path.expanduser("~") + '/WolfEditorDocuments')

from PySimpleGUI.PySimpleGUI import InputText, WIN_CLOSED, WIN_CLOSE_ATTEMPTED_EVENT, WIN_X_EVENT
# Setup the main editor window
print('Attempting to setup the window...')
sg.theme('SystemDefaultForReal')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Wolf Editor Desktop')],
            [sg.Button('New'), sg.InputText(key='savePath'), sg.Button('Save'), sg.Checkbox("Save In Documents Folder", True, key='documentsFolder'),sg.InputText(key='loadPath'), sg.Button('Load'), sg.Button("Load Using Selector"), sg.Button('About'), sg.Button("Changelog"), sg.Button('Found a bug?'), sg.Button('Quit')],
            [sg.Multiline(size=(158, 42), key='MainDocument')]
]

# Function for creating error messages
def errorMessage(title, message):
    elayout = [[sg.Text(message)], # Create the main text for the error message.
    [sg.Button('Dismiss')]]
    ewindow = sg.Window(title, elayout, icon='icon.ico') # Create the error message window

    while True:
        eevent, evalues = ewindow.read()
        if eevent == sg.WIN_CLOSED or eevent == 'Dismiss': # if user closes window or clicks dismiss in the window
            break
    
    ewindow.close()


print('Creating the window.')
window = sg.Window('Wolf Editor Desktop', layout, icon='icon.ico')
# Event Loop to process 'events' and get the 'values' of the inputs

        
while True:    
    event, values = window.read()
    
    if event == WIN_CLOSED:
        break
    
    if event == 'About': # of user clicks about:
        alayout = [  [sg.Image("/wedit/WolfEditor.gif")],
            [sg.Text('Wolf Editor Desktop is the offline, self-contained version of Wolf Editor.\nWolf editor is a simple text editor creted by Barry Piel (a.k.a Focal Fossa).\nYou are running version ' + versionCode + ' Check the changelog.txt file for a list of all new changes.')],
            [sg.Button('Dismiss')]
        ] # Create our about window layout

        awindow = sg.Window('Wolf Editor About', alayout, icon='icon.ico') # Create the window

        while True:
            aevent, avalues = awindow.read()
            if aevent == sg.WIN_CLOSED or aevent == 'Dismiss': # if user closes window or clicks dismiss in the about window
                break
        
        awindow.close() # Close the about window
    
    if event == 'Quit': # of user clicks quit:
        qlayout = [  [sg.Text('Are you sure you want to quit? Any unsaved changes will be lost!')],
                [sg.Button('No'), sg.Button('Yes')]
            ] # Setup the layout for the new quit conformation window

        qwindow = sg.Window('Really Quit?', qlayout, icon='icon.ico') # Create the quit conformation window
        
        while True:
            qevent, qvalues = qwindow.read()

            if qevent == 'Yes': # When the user says yes to quitting
                sys.exit(0)
                #exit()
            if qevent == sg.WIN_CLOSED or qevent == 'No': # When the user says no to quitting
                break
        qwindow.close() # Close the window after it is needed

    if event == 'New': # of user clicks New:
        nlayout = [  [sg.Text('Are you sure you want to create a new file? Any unsaved changes will be lost!')],
            [sg.Button('No'), sg.Button('Yes')]
        ] # Setup the layout for the new new file conformation window

        nwindow = sg.Window('Make a new file?', nlayout, icon='icon.ico') # Create the new file conformation window

        while True:
            
            nevent, nvalues = nwindow.read()

            if nevent == 'Yes': # When the user says yes to making a new file
                window.FindElement('MainDocument').Update('')
                window.FindElement('savePath').Update('')
                window.FindElement('loadPath').Update('')
                break
            if nevent == sg.WIN_CLOSED or nevent == 'No': # When the user says no to making a new file
                break
        nwindow.close()

    if event == 'Found a bug?':
        errorMessage('Found a bug?', 'Report it on the `issues` part Wolf Editor`s github page.')
    
    if event == 'Save':
        # Check if the user wanted to save the file in the WolfEditorDocuments folder
        if values['documentsFolder'] == True:
            filePathToSave = os.path.expanduser("~") + "/WolfEditorDocuments/" + values['savePath'] # There needs to be two \ characters, because python will freak out if only one \ is used.
            
            if filePathToSave == os.path.expanduser("~") + '/WolfEditorDocuments':
                errorMessage('Warning', 'You cannot save a file without specifying a file path.')
            else:
                if os.path.exists(filePathToSave):
                    ovlayout = [  [sg.Text('The file you are trying to save already exists. Do you want to replace it?')],
                [sg.Button('No'), sg.Button('Yes')]
            ] # Setup the layout for the iverwrite file conformation window

                    ovwindow = sg.Window('Make a new file?', ovlayout, icon='icon.ico') # Create the overwrite file conformation window

                    while True:
                        
                        ovevent, ovvalues = ovwindow.read()

                        if ovevent == 'Yes': # When the user says yes to overwriting
                            loaded_file = open(filePathToSave, 'w', encoding="utf8")
                            loaded_file.write(values['MainDocument'])
                            loaded_file.close()
                            ovwindow.close()
                            errorMessage('Wolf Editor', 'Successfully saved file')
                            break
                        if ovevent == sg.WIN_CLOSED or ovevent == 'No': # When the user says no to making a new file
                            break
                    ovwindow.close() 
                
                else:
                    print('The file does not exist, create new file before continue')
                    os.system('echo "" > ' + filePathToSave)
                    try:
                    	loaded_file = io.open(filePathToSave, 'w', encoding="utf8")
                    	loaded_file.write(values['MainDocument'])
                    	loaded_file.close()
                    	errorMessage('Wolf Editor', 'Successfully saved file')
                    except:
                    	errorMessage("Error saving file", traceback.format_exc())
        else:
            filePathToSave = values['savePath'] # There needs to be two \ characters, because python will freak out if only one \ is used.
            
            if filePathToSave == '':
                errorMessage('Warning', 'You cannot save a file without specifying a file path.')
            else:
                if os.path.exists(filePathToSave):
                    ovlayout = [  [sg.Text('The file you are trying to save already exists. Do you want to replace it?')],
                [sg.Button('No'), sg.Button('Yes')]
            ] # Setup the layout for the iverwrite file conformation window

                    ovwindow = sg.Window('Make a new file?', ovlayout, icon='icon.ico') # Create the overwrite file conformation window

                    while True:
                        
                        ovevent, ovvalues = ovwindow.read()

                        if ovevent == 'Yes': # When the user says yes to overwriting
                            loaded_file = open(filePathToSave, 'w', encoding="utf8")
                            loaded_file.write(values['MainDocument'])
                            loaded_file.close()
                            ovwindow.close()
                            errorMessage('Wolf Editor', 'Successfully saved file')
                            break
                        if ovevent == sg.WIN_CLOSED or ovevent == 'No': # When the user says no to making a new file
                            break
                    ovwindow.close() 
                
                else:
                    print('The file does not exist, create new file before continue')
                    os.system('echo "" > ' + filePathToSave)
                    try:
                    	loaded_file = io.open(filePathToSave, 'w', encoding="utf8")
                    	loaded_file.write(values['MainDocument'])
                    	loaded_file.close()
                    	errorMessage('Wolf Editor', 'Successfully saved file')
                    except:
                    	errorMessage("Error saving file", traceback.format_exc())

    if event == 'Load':
        filePathToLoad = os.path.expanduser("~") + '/WolfEditorDocuments' + values['loadPath']
        
        if filePathToLoad == os.path.expanduser("~") + '/WolfEditorDocuments':
            errorMessage('Warning', 'You cannot load a file without specifying a file path.')
        else:
            if os.path.exists(filePathToLoad):
                try:
                	loaded_file = io.open(filePathToLoad, 'r', encoding="utf8")
                	loaded_file_data = loaded_file.read()
                	window.FindElement('MainDocument').Update(loaded_file_data)
                	#window.FindElement('savePath').Update(filePathToLoad)
                	loaded_file.close()
                	errorMessage('Wolf Editor', 'Successfully loaded file')
                except:
                	errorMessage("Error loading file", traceback.format_exc())
            
            else:
                errorMessage('Warning', 'The file you`re trying to load does not exist.')

    if event == 'Changelog':
        filePathToLoad = "/wedit/Allchanges/Changelog.txt"

        if os.path.exists(filePathToLoad):
            loaded_file = io.open(filePathToLoad, 'r', encoding="utf8")
            loaded_file_data = loaded_file.read()
            window.FindElement('MainDocument').Update(loaded_file_data)
            #window.FindElement('savePath').Update(filePathToLoad)
            loaded_file.close()
            errorMessage('Wolf Editor', 'Successfully loaded file')
        
        else:
            errorMessage('Warning', 'The changelog file does not exist.')

    if event == 'Load Using Selector':
        files = [f for f in listdir(os.path.expanduser("~") + '/WolfEditorDocuments') if isfile(join(os.path.expanduser("~") + '/WolfEditorDocuments', f))]
        lfusLayout = [
            [sg.Listbox(files, key='_selectedFile_', size=(50, 15))],
            [sg.Button("Load"), sg.Button("Cancel"), sg.Button("Refresh")]
        ]
        lfusWin = sg.Window('Load File', lfusLayout, icon='icon.ico') # Create the window

        while True:
            lfusEvent, lfusValues = lfusWin.read()
            if lfusEvent == sg.WIN_CLOSED or lfusEvent == 'Cancel': # if user closes window or clicks dismiss in the about window
                break
            
            if lfusEvent == 'Refresh': # if user closes window or clicks dismiss in the about window
                files = [f for f in listdir(os.path.expanduser("~") + '/WolfEditorDocuments') if isfile(join(os.path.expanduser("~") + '/WolfEditorDocuments', f))]
                lfusWin.FindElement('_selectedFile_').Update(values=files)
            
            if lfusEvent == 'Load': # if user closes window or clicks dismiss in the about windows
                filePathToLoad = lfusWin.FindElement('_selectedFile_').get()
                if len(filePathToLoad) == 0:
                    errorMessage("Warning", "You cannot load a file without selecting one...")
                else:
                    filePathToLoad = filePathToLoad[0]
                    print(filePathToLoad)
                    filePathToLoad = os.path.expanduser("~") + '/WolfEditorDocuments/' + filePathToLoad
                
                    if filePathToLoad == os.path.expanduser("~") + '/WolfEditorDocuments':
                        errorMessage('Warning', 'You cannot load a file without selecting one...')
                    else:
                        if os.path.exists(filePathToLoad):
                            loaded_file = io.open(filePathToLoad, 'r', encoding="utf8")
                            loaded_file_data = loaded_file.read()
                            window.FindElement('MainDocument').Update(loaded_file_data)
                            #window.FindElement('savePath').Update(filePathToLoad)
                            loaded_file.close()
                            errorMessage('Wolf Editor', 'Successfully loaded file') 
                            break       
                        else:
                            errorMessage('Warning', 'The file you`re trying to load does not exist.')        
        lfusWin.close() # Close the about window
        

window.close()
