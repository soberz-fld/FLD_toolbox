import inspect
import os
import time
from datetime import datetime as __datetime
import re
import threading

__log_write_to_file_thread_object = None  # Initialized at the file ending
__log_stack = []

# _debug_print lets you print out the statements, so you do not need a separate print statement while debugging.
_debug_print = False
# _debug_write lets you write logs of type debug to file.
_debug_write = False

__logfile_name = 'logs'  # Filename without extension
__logfile_number = 0  # Counter of logfile when splitting after maximum filesize is reached
__logfile_path = ''  # path of logfile is dynamically created
__log_values_delimiter = ' | '  # If changed, you need to change regex pattern in header too
__logfile = None  # Here the logfilehandler is stored later
__log_temp_counter = 0  # If a specific number of logs are written, size of logfile has to be checked. I don't want to check it every time. It may slow down.
__project_path = ''  # path of project if python file is part of a project that has a main.py in root folder
__project_subfolder = ''  # Name of subfolder in project where logfiles are stored
__log_path_of_module_length = 120
__initialized = False
__file_lock = threading.Lock()


def set_debug_print(value: bool):
    global _debug_print
    _debug_print = value


def set_debug_write(value: bool):
    global _debug_write
    _debug_write = value


def __initialize_logfile_if_necessary() -> None:
    global __logfile
    with __file_lock:
        try:
            with open(__logfile_path, mode='r', encoding='utf-8') as logfile:
                content = logfile.read()
                if content != '':
                    return
        except FileNotFoundError:
            content = ''

        text_to_logfile = 'FLD-ToolBox logging\nThis is Logfile number ' + str(__logfile_number).zfill(4) + '\n\nThis file can be analysed by RegEx:\n\\n([^\\|\\n]+) \\| ([^\\|\\n]+) \\| ([^\\|\\n]+) \\| ([^\\|\\n]+) \\| ([^\\|\\n]+) \\| ([^\\|\\n]+)\n\n'
        # Delimiter line
        text_to_logfile += ''.ljust(26, '-')[0:26]
        text_to_logfile += '+'.center(len(__log_values_delimiter), '-')
        text_to_logfile += ''.ljust(10, '-')[0:10]
        text_to_logfile += '+'.center(len(__log_values_delimiter), '-')
        text_to_logfile += ''.ljust(__log_path_of_module_length, '-')[0:__log_path_of_module_length]
        text_to_logfile += '+'.center(len(__log_values_delimiter), '-')
        text_to_logfile += ''.ljust(11, '-')[0:11]
        text_to_logfile += '+'.center(len(__log_values_delimiter), '-')
        text_to_logfile += ''.ljust(40, '-')[0:40]
        text_to_logfile += '+'.center(len(__log_values_delimiter), '-')
        text_to_logfile += ''.ljust(100, '-')[0:100]
        text_to_logfile += '\n'
        # Header line of table
        text_to_logfile += 'Timestamp'.ljust(26, ' ')[0:26]
        text_to_logfile += __log_values_delimiter
        text_to_logfile += 'type'.ljust(10, ' ')[0:10]
        text_to_logfile += __log_values_delimiter
        text_to_logfile += 'From Module / Python File'.ljust(__log_path_of_module_length, ' ')[0:__log_path_of_module_length]
        text_to_logfile += __log_values_delimiter
        text_to_logfile += 'From line'.ljust(11, ' ')[0:11]
        text_to_logfile += __log_values_delimiter
        text_to_logfile += 'From function'.ljust(40, ' ')[0:40]
        text_to_logfile += __log_values_delimiter
        text_to_logfile += 'text\n'
        # Delimiter line
        text_to_logfile += ''.ljust(26, '-')[0:26]
        text_to_logfile += '+'.center(len(__log_values_delimiter), '-')
        text_to_logfile += ''.ljust(10, '-')[0:10]
        text_to_logfile += '+'.center(len(__log_values_delimiter), '-')
        text_to_logfile += ''.ljust(__log_path_of_module_length, '-')[0:__log_path_of_module_length]
        text_to_logfile += '+'.center(len(__log_values_delimiter), '-')
        text_to_logfile += ''.ljust(11, '-')[0:11]
        text_to_logfile += '+'.center(len(__log_values_delimiter), '-')
        text_to_logfile += ''.ljust(40, '-')[0:40]
        text_to_logfile += '+'.center(len(__log_values_delimiter), '-')
        text_to_logfile += ''.ljust(100, '-')[0:100]
        # Write everything to file
        with open(__logfile_path, mode='w', encoding='utf-8') as logfile:
            logfile.write(text_to_logfile)


def __update_logfile_path_and_check_maximum_size() -> None:
    """
    Creating the logfile path out of variables. After that checking if it does not reach 1 MB so the Windows Editor can still read it easily.
    If size of 1 MB is reached, a new logfile is created with ascending suffix.
    """
    global __logfile_path
    global __logfile_number
    global __log_temp_counter
    __log_temp_counter = 0
    if __project_path == '':
        __logfile_path = os.getenv('appdata') + '\\FLD-VT\\' + __logfile_name + '_' + str(__logfile_number).zfill(4) + '.log'
    else:
        __logfile_path = __project_path + __project_subfolder + '\\' + __logfile_name + '_' + str(__logfile_number).zfill(4) + '.log'
    try:
        while os.path.getsize(__logfile_path) > 100000:# 1000000:  # If 10MB, create a new logfile
            __logfile_number += 1
            __update_logfile_path_and_check_maximum_size()
    except FileNotFoundError:
        # if the logfile not exist
        if not os.path.isdir(os.path.dirname(__logfile_path)):
            os.mkdir(os.path.dirname(__logfile_path))
        open(__logfile_path, "a").close()
        __initialize_logfile_if_necessary()


def __init__(debug_print: bool = True, debug_write: bool = True, project_name: str = '', project_subfolder: str = '') -> None:
    """
    Initialising when imported - check if file exists and if not: Create and prepare it. The file is created in project root if possible. If no main.py is found, __project_path stays empty
    :param debug_print: lets you print out the statements, so you do not need a separate print statement while debugging.
    :param debug_write: lets you write logs of type debug to file.
    :param project_name: Name of project
    :param project_subfolder: Name of subfolder in which the logfile sould be stored
    :return: None
    """
    global __project_path
    path_temp = os.path.realpath(os.path.dirname(__file__))
    while __project_path == '':  # Try to find out where project root is
        if os.path.exists(path_temp + '\\main.py'):  # If main exists in that folder ...
            __project_path = path_temp  # ... set this path as root ...
        else:  # ... otherwise ...
            re_match = re.match('^(.*)\\\\[^\\\\]+$', path_temp)  # ... move one folder up.
            if re_match is not None:  # if parent folder found
                path_temp = re_match.group(1)
            else:
                break  # No project root found

    # Setting values of _debug_print and _debug_write
    global _debug_print
    _debug_print = debug_print
    global _debug_write
    _debug_write = debug_write

    # Setting project name (optional)
    if project_name != '':
        global __logfile_name
        __logfile_name = ''.join([i if ord(i) < 128 else '#' for i in project_name]).replace('/', '#').replace('\\', '#').replace('.', '#').replace(' ', '#') + '_logs'

    if project_subfolder != '':
        global __project_subfolder
        while project_subfolder.startswith("/") or project_subfolder.startswith("\\") or project_subfolder.endswith("/") or project_subfolder.endswith("\\"):
            project_subfolder = project_subfolder.strip("/\\")
        __project_subfolder = '\\' + project_subfolder

    __update_logfile_path_and_check_maximum_size()
    __initialize_logfile_if_necessary()  # If only empty logfile exists, it needs the head
    global __initialized
    __initialized = True


def log(text: str = '', debug: str = '', action: str = '', alert='', error: str = '', critical: str = '') -> None:
    """
    This function logs information in logfile.
    I suggest importing it like 'from fld_toolbox.fldlogging import log' so a sample input is
       log(error='TextToLog')
    :param text: is just text.
    :param debug: for debugging purposes. Prints and writes to file depending on _debug_print and _debug_write variables
    :param action: is confirmation, that an action is done. It's marked as confirmation.
    :param alert: for something strange to notice
    :param error: is a normal error message
    :param critical: is a critical error message and is marked as such
    :return: Does not return anything
    """
    if not __initialized:
        __init__()

    curframe = inspect.currentframe()
    global __logfile

    # Each parameter to dict
    __log_types = {
        'text':     text,
        'debug':    debug,
        'action':   action,
        'alert':    alert,
        'error':    error,
        'critical': critical
    }

    try:
        for log_type in __log_types:
            if __log_types[log_type] != '':
                try:
                    text_to_logfile = '\n'
                    text_to_logfile += str(__datetime.now())[0:26]
                    text_to_logfile += __log_values_delimiter
                    text_to_logfile += log_type.ljust(10, ' ')[0:10]
                    text_to_logfile += __log_values_delimiter
                    text_to_logfile += inspect.getouterframes(curframe, 2)[1][1].ljust(__log_path_of_module_length, ' ')[0:__log_path_of_module_length]
                    text_to_logfile += __log_values_delimiter
                    text_to_logfile += 'line ' + str(inspect.getouterframes(curframe, 2)[1][2]).ljust(6, ' ')[0:6]
                    text_to_logfile += __log_values_delimiter
                    text_to_logfile += inspect.getouterframes(curframe, 2)[1][3].ljust(40, ' ')[0:40]
                    text_to_logfile += __log_values_delimiter
                    text_to_logfile += str(__log_types[log_type]).replace('\n', '\\n').replace('\t', '\\t').replace('|', '/')
                    if log_type != 'debug' or _debug_write:
                        # Does not write debugs to database if _debug_write is false
                        global __log_stack
                        __log_stack.append(text_to_logfile)
                    if _debug_print:
                        print("\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(255, 128, 0, text_to_logfile[30:]))
                except KeyError:
                    pass
    except Exception as e:
        print(f'ERROR in fld_toolbox.fldlogging: {e.message}, {e.args}')


def __log_write_to_file_thread():
    global __log_temp_counter
    counter = 0
    run = True
    buffer = ''
    while run:
        if counter > 10000:
            if not threading.main_thread().is_alive():
                run = False
                __log_temp_counter = 1000
            counter = 0
        counter += 1
        try:
            if __log_stack:
                # logfile should not exceed limit of 1 MB but checking at every logging may slow programm down, so it does only check every 50 times
                buffer += __log_stack.pop()
                __log_temp_counter += 1
                if __log_temp_counter > 20:  # Only write every xth entry
                    with __file_lock:
                        with open(__logfile_path, mode='a', encoding='utf-8') as logfile:
                            logfile.write(buffer)
                    buffer = ''
                    __update_logfile_path_and_check_maximum_size()
        except Exception as e:
            print(f'ERROR in fld_toolbox.fldlogging: {e.message}, {e.args}')


if __log_write_to_file_thread_object is None:
    __log_write_to_file_thread_object = threading.Thread(target=__log_write_to_file_thread, name='fld_toolbox.fldlogging write_to_file_thread')
    __log_write_to_file_thread_object.start()
