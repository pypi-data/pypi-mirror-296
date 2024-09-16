from io import StringIO
from typing import List

from .properties import EXECUTION_STATE_EVENT 
from thonny.editors import EditorCodeViewText
import os, re, ast, traceback, textwrap, tkinter as tk, base64, dill, thonny
from thonny.common import BackendEvent

def wrap(string:str, length=8, break_long_words=False):   
    """Wrap a text using the `wraptext` module.

    Args:
        string (str): the string to wrap.
        length (int, optional): the min length from which the string will be wrapped. Defaults to 8.
        break_long_words (bool, optional): if False the entire words will not be wrapped
                                        if the words lentgh is more that the given length. Defaults to False.
    Returns:
        str: the wrapped string.
    """
    return '\n'.join(textwrap.wrap(string, length, break_on_hyphens=False, break_long_words=break_long_words))

def create_node_name(node:ast.AST):
    """
    Returns the node representation. Especially, returns the prototype or the signature of the node.
    This function can only construct a string representation of the supported nodes. 
    The supported nodes are reported in ASTParser.py in the global variable SUPPORTED_TYPES.
    
    Even if unsupported node is given so just it's name is returned.
    
    Args: 
        node (ast.AST): The supported node 

    Returns:
        str: Return the string represantation of a node
    """
    arg_to_exclude = lambda arg: arg in ("self", "cls")
    if isinstance(node, ast.ClassDef):
        return "%s(%s)" % (node.name, ", ".join([base.id for base in node.bases]))
    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return "%s(%s)" % (node.name, ", ".join([a.arg for a in node.args.args if not arg_to_exclude(a.arg)]))
    else:
        return ""

def remove_url_part(error_msg:str):
    """Removes the hyperlink section from the `error_msg`. The hyperlink
    contains the filename and line number. 
    
    This function is only used by the L1TestErrorView to show the details of
    an error as a normal text.

    Args:
        error_msg (str): the error message from which the hyperlink will
                        be removed.

    Returns:
        str: The new error message without hyperlink part.
    """
    return re.sub(r'(File .*,\s*line\s*\d*)(, .*)?', "", error_msg)

def replace_error_line(error:str, line_number:int):
    """Replace the line of the error to iven `line_number`

    Args:
        error (str): The error that probably contains the error line.
        line_number (int): the new line number of the error.

    Returns:
        str: the same error with a new error line number.
    """
    return re.sub(r'(?P<match>line) (\d+)', '\g<match> %s' % line_number, error)

def replace_filename(filename, error:str):
    """Replace the filename in the given error to the specified `filename`

    Args:
        filename (str): the new filename
        error (str): the error message

    Returns:
        str: the same error but with replaced filename.
    """
    return re.sub(r'"(<.*>)?"', '"%s"' % filename, error)

def format_filename_to_hyperlink(error_message:str):
    """
    Finds the filename and line number in the given error message 
    then creates the corresponding hyperlink leading to the right place in the code editor.
    
    If no filename and line number found so an empty string is returned
    
    Args:
        text (str): the error_message supposed containing the hyperlink.

    Returns:
        str: Returns a hyperlink in RST format. 
    """
    def extract_file_and_lineno(error):
        file_line = re.search(r'File\s*(.*),\s*line\s*(\d*)(.*)', error)
        return {
                "filename": file_line.group(1).replace("\"", ""), 
                "lineno": file_line.group(2),
                "complement": file_line.group(3)
            } if file_line else None
    
    extracted = extract_file_and_lineno(error_message)
    if extracted:
        if os.path.exists(extracted["filename"]):
            filename, lineno, comp = extracted["filename"], extracted["lineno"], extracted["complement"]
            url = "thonny-editor://" + escape(filename).replace(" ", "%20")
            if lineno is not None:
                url += "#" + str(lineno)
            # return the hyperlink format following the rst specification
            return "`File \"%s\", line %s%s <%s>`__\n" % (escape(filename), lineno, comp, url)
        else: 
            return ""
    else:
        return ""

def escape(s:str):
    return (
        s.replace("\\", "\\\\")
         .replace("*", "\\*")
         .replace("`", "\\`")
         .replace("_", "\\_")
         .replace("..", "\\..")
    )

def get_last_exception(exc_info:tuple):
    """
    Formats exception information provided by ~exc_info~.
    Extracts the last exception located in the last frame.
    
    Args:
        exc_info (tuple): The tuple must contain three elements: 
                        (type, value, traceback) as returned by sys.exc_info().
        with_details (bool): Set as True and some extra informations will be considered
                        while formatting the exception informations. Defaults to True.

    Returns:
        str: Returns a string containing a traceback message for the given ~exc_info~.
    """
    # Get a traceback message.
    excout = StringIO()
    exc_type, exc_val, exc_tb = exc_info
    traceback.print_exception(exc_type, exc_val, exc_tb, file=excout)
    # la variable `content`` va contenir toute la trace liée à l'exception levée
    content = excout.getvalue()
    excout.close()

    # mais on en retire que la dernière frame qui indiquent l'exception renvoyée par l'éditeur thonny
    last_exception = __extract_last_exception(content.rstrip("\n"))
    
    # parfois Python inclut plusieurs lignes vides dans l'exception.
    last_exception = re.sub("\n+", "\n", last_exception)
    # On assure que tout ce qui procède la dernière exception est retiré
    return re.sub(r'.*(?=File.*)', "", last_exception)

def __extract_last_exception(traceback_content:str):
    """Extract the last exception from the traceback frames,

    Args:
        content (str): The returned traceback as string.

    Returns:
        str: The lines representing the compilation error 
    """
    # splitted va contenir toutes les ligne de la traceback
    splitted = traceback_content.split("\n")
    keyword = "File"
    last_frame_index = 0
    
    # On veut pas afficher les frames du backend sur thonny, c'est inutile et illisible.
    frames_to_exclude = ["cpython_backend", os.path.join("thonny", "backend")]
    
    # on filtre par le mot "File" pour récupérer la dernière Frame.
    # C'est la dernière frame qui contient l'erreur survenu du script de thonny 
    # On veut pas, évidement, afficher toute la trace contenant les exceptions levées par l1test backend.
    for i in range(len(splitted)):
        frame = splitted[i]
        if keyword in frame :    
            last_frame_index = i
            
    # last_frame contient le nom du fichier et le détail de l'erreur              
    last_frame = splitted[last_frame_index:] 
    # Le nom du fichier de la dernière frame est à la position 0
    last_frame_file = last_frame[0]
    
    # Dans le cas de l'interuption du programme par un <Control+c>, 
    # la dernière frame contiendra une exception levée par le backend thonny.
    # En l'occurrence, on doit pas afficher toute la frame, mais juste le message renvoyé.
    # En général, on évite d'afficher les frames survenue du backend thonny.
    for frame_to_exclude in frames_to_exclude: 
        if frame_to_exclude in last_frame_file:
            last_frame_index = -1    
            
    # last_frame[-1] -> contient le message de l'exception de la frame          
    return last_frame[-1] if last_frame_index < 0 else "\n".join(last_frame).strip()

def get_module_name(filename:str):
    """
    Gets the module name from the specified filename.
    This function simply gets the basename of the filename, then removes 
    the ".py" extension. 

    Args:
        filename (str): an absolute path

    Returns:
        str: the module name of the given filename.
    """
    return  get_basename(filename, "py")

def get_basename(filename:str, extension:str="*"):
    """
    Gets the module name from the specified filename.
    This function simply gets the basename of the filename, then removes 
    the given extension. 

    Args:
        filename (str): an absolute path
        extension (str): the extension to remove from the filename. 
        Extension can be a regex. Use '*' to remove all extensions.

    Returns:
        str: the basename of the given filename without the given extension.
    """
    return re.sub(r'.'+extension, "", os.path.basename(filename))

def get_focused_writable_text():
    """
    Returns the focused text

    Returns:
        Widget: A widget Object if there's a focused area in the editor
        None : if no focused area exists in the editor
    """
    from thonny.editors import EditorCodeViewText
    widget = thonny.get_workbench().focus_get()
    # In Ubuntu when moving from one menu to another, this may give None when text is actually focused
    if isinstance(widget, EditorCodeViewText) and (
        not hasattr(widget, "is_read_only") or not widget.is_read_only()
    ):
        return widget
    else:
        return None
    
def get_selected_line(text_widget: EditorCodeViewText, only_lineno=True) -> int | tuple[int, int]:
    """
    Get the number of the selected line in the text editor. If only_lineno is True, 
    get only the line number.
    
    Note: Before using this method you should check if several lines are selected
    by invoking the method `assert_one_line_is_selected()` located in this file.
    
    Args:
        text_widget (Widget): The text selected in the text editor. 
                    The value of this parameter must be the result 
                    of invoking the get_focused_writable_text() method. 
        only_lineno (bool): If True, only the number of the selected line is returned.
    Returns:
        int | tuple[int, int]: Returns (lineno, column). If `only_lineno` is True, 
        returns only lineno.
    """
    # A text is selected in the editor => can't tell the exact line of the test to run
    lineno, column = map(int, text_widget.index(tk.INSERT).split("."))
    return lineno if only_lineno else (lineno, column)

def assert_one_line_is_selected() -> bool:
    """
    Returns True if only one line is selected, otherwise an exception is raised.
    """
    text = get_focused_writable_text()
    if text :
        return len(text.tag_ranges("sel")) == 0
    return False
        
def add_random_suffix(word):
    """Add a random suffix to the given word.
     
    The suffix is added in the following format 'word_suffix'. An underscore separates the two words.
    The suffix is assumed to be long(more than 9 caracters).
    
    Args:
        word (str): A word.

    Returns:
        str: Returns the given word with a random suffix appended after an underscore.
    """
    import string
    from random import shuffle, randint
    divider = "_"
    alphabet = list(string.ascii_lowercase + string.ascii_uppercase)
    
    # Divide by three to avoid the first index being so close to the last index.
    # The first index should be smaller than the last index, so we can have a long suffix.
    first_index = randint(0, len(alphabet)//3) 
    last_index = randint(len(alphabet)//2, len(alphabet)-1)
    
    shuffle(alphabet) 
    suffix = "".join(alphabet[first_index: last_index])
    return word + divider + suffix

def get_font_family_option(option="editor_font_family") -> str:
    """Retrieves the value of the "font family" option from the "options" menu.

    Returns:
        str: The value of the setted font family.
    """
    option = option if option else "editor_font_family"
    return thonny.get_workbench().get_option("view.%s" % option)

def get_font_size_option():
    """Retrieves the value of the "font size" option from the "options" menu.

    Returns:
        int: The value of the setted font size.
    """
    workbench = thonny.get_workbench()
    return workbench._guard_font_size(workbench.get_option("view.editor_font_size"))

def get_image_path(basename:str):
    """Get the absolute path to the image in the /img directory

    Args:
        basename (str): just the name of the file inluding it's extension. 
        For example: "icon.png"

    Returns:
        str: the absolute path to the image located in the /img directory
    """
    return get_absolute_path("img", basename)

def get_template_path(basename:str, dir="l1test_config"):
    return get_absolute_path(dir, "templates", basename)

def get_ini_config_path(dir="l1test_config", basename:str='conf.ini'):
    return get_absolute_path(dir, basename)

def get_absolute_path(*paths):
    """Get the absolute path of a file under the /thonnycontrib directory."""
    parent = os.path.dirname(__file__) 
    return os.path.join(os.path.abspath(parent), *paths)

class ImageStore: pass
__IMAGE_STORE = ImageStore()
    
def get_photoImage(image_name:str):
    """Returns a PhotoImage object from the given image path.

    Args:
        image_name (str): The basename of the image with its extension. 
        The image must be located in the "/img" directory.   
    
    Returns:
        PhotoImage: A PhotoImage object.
    """
    icon_path = get_image_path(image_name)
    photo_image = tk.PhotoImage(name=get_basename(icon_path), file=icon_path)
    
    stored_image = getattr(__IMAGE_STORE, image_name, None)
    if not stored_image:
        # on stocke l'image dans l'objet __IMAGE_STORE pour éviter que l'image soit détruite par le garbage collector
        # sinon l'image ne sera pas affichée.
        setattr(__IMAGE_STORE, image_name, photo_image) 
        return photo_image
    return stored_image

def build_event_msg(state, command_name=EXECUTION_STATE_EVENT, **options):
    """
    Sends the given state with given arg to the front(L1TestRunner).

    Args:
        state (ExecutionStateEnum): The current state to send.
        command_name (str, optional): The name of the command. Default is BACKEND_COMMAND.
        **options: Other options to include in the message.

    Raises:
        AssertionError: If the backend is not initialized.
    """
    from thonnycontrib.backend.models import ExecutionStateEnum
    assert isinstance(state, ExecutionStateEnum)
    state = state.value
    return BackendEvent(event_type=command_name, state=state, **options)

def clear_env_vars(vars: List[str]):
    """
    Clears the environnement variables.
    
    Args:
        vars (List[str]): The names of the environnement variables to clear.
    """
    assert isinstance(vars, list)
    assert all(isinstance(var, str) for var in vars)
    for var in vars:
        os.environ.pop(var, None) 

def measure_time(func=None, round_to=4, show_args=False):
    """
    Decorator used to measure the execution time (in seconds) of a function.
    
    Note: 
        - All the logs of the backend package are shown in the `backend.log` file (generated 
        by Thonny).
        - All the logs of the frontend package are shown directly in the console (also available 
        in `frontend.log` file generated by Thonny).
    
    Args:
        round_to (int): The number of decimal places to round the execution time.
        show_args (bool): If True, the arguments of the function will be shown in the log message.
    """
    if func is None:
        return lambda f: measure_time(f, round_to, show_args)

    import time
    from logging import getLogger
    logger = getLogger(__name__ + "#measure_time")

    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter() - start
        args_str = f"({', '.join([str(arg) for arg in args])})" if show_args else "()"
        # get the module of the function
        module = func.__module__.split(".")[-1]
        logger.info("Execution time of %s.%s%s is %ss", module, func.__qualname__, args_str, round(end, round_to))
        return result
    return wrapper

def tostring(cls):
    """
    Decorator used to add the __str__ method to a class. The generated string follows the 
    following format: `ClassName(attr1=value1, attr2=value2, ...)`. 
    
    Note : All the attributes will be shown (regardless of their visibility) in the string
    representation of the class.
    
    Use it like this:
    ```py
    @tostring
    class MyClass:
        pass
    ```
    """
    def new_str(self):
        attributes = ', '.join(["%s=%s" % (attr, str(getattr(self, attr))) for attr in vars(self)])
        return "%s(%s)" % (cls.__name__, attributes)

    cls.__str__ = new_str
    return cls

def add_env_vars(**kw) -> object:
    """
    Adds the given key arguments as environment variables. The value of the environment
    variable will be serialized.

    Args:
        **kw: The key arguments to add as environment variables.

    Returns:
        List[object]: The list of the values of the environment variables.
    """
    if os.supports_bytes_environ:
        return [os.environb.setdefault(key.encode(), serialize(value)) for key, value in kw.items()]
    else:
        return [os.environ.setdefault(key, serialize(value, True)) for key, value in kw.items()]

def get_env_var(key: str) -> object:
    """
    Retrieves the value of the environment variable with the given key.
    The value of the environment variable will be deserialized.

    Args:
        key (str): The name of the environment variable.

    Returns:
        object: The value of the environment variable.
    """
    if os.supports_bytes_environ:
        return deserialize(os.environb.get(key.encode(), serialize(None)))
    else:
        return deserialize(os.environ.get(key, serialize(None, True)))

def serialize(data: object, to_str:bool=False) -> bytes | str:
    """
    Serialize the given data to a string using Base64 encoding.

    Args:
        data (object): the data to serialize.

        to_str (bool, optional): If True, the serialized data will be returned as a string. Defaults to False.
        Use this option if you want to serialize the data to a string instead of bytes. This is useful when
        you use the operating system like Windows that doesn't support bytes in the environment variables.

    Returns:
        bytes | str: the serialized data.
    """
    encoded = base64.b64encode(dill.dumps(data))
    return encoded if not to_str else encoded.decode()

def deserialize(data: bytes | str) -> object:
    """
    Deserialize data and return the original data.

    Args:
        data (bytes | str): the data to deserialize.

    Returns:
        object: the original data.
    """
    assert isinstance(data, (bytes, str))
    decoded_data = base64.b64decode(data)
    return dill.loads(decoded_data)

def add_newline(string:str, how_much:int=1, force:bool=False) -> str:
    """
    Adds a newline character at the end of the given string if it doesn't end with a newline character.

    Args:
        s (str): The string to which the newline character will be added.
        how_much (int, optional): The number of newline characters to add. Defaults to 1.
        force (bool, optional): If True, the newline character will be added regardless of the
                                presence of a newline character at the end of the string. Defaults to False.

    Returns:
        str: The string with a newline character at the end.
    """
    how_much = max(1, how_much)
    newline = ("\n" * how_much)
    return string if string.endswith("\n") or not force else string + newline