# MIT License

# Copyright (c) 2024 Soumyo Deep Gupta

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .exceptions import *
from .simple import Menu

from typing import Callable, Dict, Any

class MenuBuilder:
    """`Menu Builder class is responsible for handling a Tree of Menus.`
        
        ### Usage

        ```
        >>> from menux.generator import MenuBuilder

        >>> builder = MenuBuilder()
        ```
        """
    def __init__(self) -> None:
        """`Menu Builder class is responsible for handling a Tree of Menus.`
        
        ### Usage

        ```
        >>> from menux.generator import MenuBuilder

        >>> builder = MenuBuilder()
        ```
        """
        # create a menu pool
        self.menus: list[Menu] = []
    
    def add(self, identifier: str, menu: dict[int, str], functions: Dict[int, Callable | None], go_back_index: int | None = None):
        """`Add a menu to the menu pool.`
        
        ### Parameters

        - `identifier` `_(str)_`: Unique identifier to identify a menu.
        - `menu` `_(dict[int, str])_`: The menu in the form of dict. Key values are `int` and texts are `str`. Example: {1: "Add two nums", 2: "Subtract two nums"}
        - `functions` `_(dict[int, callable])_`: Functions that each menu index will perform in the form of dict. keys are same as in `menu` and values are functions. Put None, if the key has a submenu.
        - `go_back_index` `_(int | None)_`: set it to None, it will be handled automatically.

        ### Usage

        ```
        from menux.generator import MenuBuilder
        from typing import Any

        builder = MenuBuilder()

        # Now I want to create a menu that has a submenu.
        # like one option would be to add two nums and another option will be "more options" which will expand to subtract two nums.

        def add_two():
            num1 = int(input("enter num1: "))
            num2 = int(input("enter num2: "))
            return num1 + num2
        
        def sub_two():
            num1 = int(input("enter num1: "))
            num2 = int(input("enter num2: "))
            return num1 - num2
        
        builder.add(
            identifier = "main_menu",
            menu = {1: "Add two nums", 2: "more options"},
            functions = {1: add_two, 2: None},
        )

        # the above line will add a main_menu with the function of "2" to None. As it will have a sub menu.
        # now add the submenu. (refer add_submenu docstring for info)

        builder.add_submenu(
            parent_identifier = "main_menu",
            parent_menu_index = 2,
            submenu_identifier = "sub_menu_of_index_2",
            submenu = {1: "Subtract two nums"},
            submenu_functions = {1: sub_two},
        )

        # now that all is set, use handler (refer docstring of handler) to begin the menu.

        result: tuple[bool, Any] = builder.handler(prompt="Enter your choice:")
        
        if result[0]:
            print(f"Execution succesfull. Result: {result[1]}")
        else:
            print(f"Failed to execute.")
        ```
        """
        # Append to the menu pool in Menu Form.
        self.menus.append(Menu(identifier, menu, functions, None, go_back_index))
    
    def _find_menu(self, identifier: str, menus: list[Menu]) -> Menu | None:
        """Find and return a menu based on identifier in a given list. Recursively."""
        # for all menus,
        for menu in menus:
            # if identifier matches, return the menu
            if menu.identifier == identifier:
                return menu
            
            # if it doesnt match and there's a submenu, check the submenu.
            if menu.submenu:
                result = self._find_menu(identifier, list(menu.submenu.values()))
                if result:
                    return result
        
        # if not found then return None.
        return None

    def add_submenu(self, parent_identifier: str, parent_menu_index: int,
                    submenu_identifier: str, submenu: dict[int, str], submenu_functions: Dict[int, Callable | None],
                    go_back_index: int | None = None, replace_if_exist: bool = False):
        """`Add a sub-menu to the menu pool.`

        ### Parameters

        - `parent_identifier` `_(str)_`: Unique identifier of the parent menu where this submenu will be inserted.
        - `parent_menu_index` `_(int)_`: Index of the parent menu, whose submenu you are inserting.
        - `submenu_identifier` `_(str)_`: Unique identifier of the sub-menu.
        - `submenu` `_(dict[int, str])_`: The sub-menu in dict form, just like the parent menu.
        - `submenu_functions` `_(dict[int, callable])_`: The functions of the sub-menu in dict form.
        - `go_back_index` `_(int | None)_`: set it to none, will be handled automatically.
        - `replace_if_exist` `_(bool)_`: Replace sub-menu if it already exists.

        ### Usage

        ```
        from menux.generator import MenuBuilder
        from typing import Any

        builder = MenuBuilder()

        # Now I want to create a menu that has a submenu.
        # like one option would be to add two nums and another option will be "more options" which will expand to subtract two nums.

        def add_two():
            num1 = int(input("enter num1: "))
            num2 = int(input("enter num2: "))
            return num1 + num2
        
        def sub_two():
            num1 = int(input("enter num1: "))
            num2 = int(input("enter num2: "))
            return num1 - num2
        
        builder.add( # check docstring of add for more info
            identifier = "main_menu",
            menu = {1: "Add two nums", 2: "more options"},
            functions = {1: add_two, 2: None},
        )

        # the above line will add a main_menu with the function of "2" to None. As it will have a sub menu.
        # now add the submenu.

        builder.add_submenu(
            parent_identifier = "main_menu",
            parent_menu_index = 2,
            submenu_identifier = "sub_menu_of_index_2",
            submenu = {1: "Subtract two nums"},
            submenu_functions = {1: sub_two},
        )

        # now that all is set, use handler (refer docstring of handler) to begin the menu.

        result: tuple[bool, Any] = builder.handler(prompt="Enter your choice:")
        
        if result[0]:
            print(f"Execution succesfull. Result: {result[1]}")
        else:
            print(f"Failed to execute.")
        ```
        """
        # search for the parent using identifier
        parent = self._find_menu(parent_identifier, self.menus)

        # if parent is not in menu pool, raise exception
        if not parent:
            raise ParentMenuNotFound(f"parent_identifier[\'{parent_identifier}\'] not found in the menu pool.")
        
        # if given index is not present in the parent menu, raise exception
        if parent_menu_index not in parent.menu:
            raise ParentIndexNotFound(f"parent_menu_index[\'{parent_menu_index}\'] not found in the parent_menu[\'{parent_identifier}\'].")
        
        # if index is present but replace is set to False, raise exception
        if parent_menu_index in parent.submenu and not replace_if_exist:
            raise SubMenuAlreadyExists(f"Sub menu for parent_menu_index[\'{parent_menu_index}\'] of parent_menu[\'{parent_identifier}\'] already exists. To replace, set \'replace_if_exists\' parameter to True.")
        
        # add the sub-menu to the parent menu.
        parent.submenu[parent_menu_index] = Menu(submenu_identifier, submenu, submenu_functions, go_back_index=go_back_index)

        # if a menu function is defined for the given index, set it to None as it will never run.
        if parent.functions[parent_menu_index] is not None:
            parent.functions[parent_menu_index] = None
    
    def _display_menu(self, menu: Menu, Title_format: str = "Menu: {identifier}", Body_format: str = "{index} - {text}") -> None:
        """Display the menu in given format."""
        # print title
        print(Title_format.replace("{identifier}", menu.identifier))
        # print body
        for key, value in menu.menu.items():
            print(Body_format.replace("{index}", str(key)).replace("{text}", value))

        # add the extra `Go_back` option.
        print(Body_format.replace("{index}", str(menu.gobackindex)).replace("{text}", "Go back"))
        print()
    
    def _capture_selection(self, menu: Menu, prompt: str, invalid_promt: str = "Invalid Selection. Please choose a valid option.") -> int:
        """capture the selection by user and return it."""
        # Run until selection is valid.
        while True:
            try:
                # try to capture selection and typecast it.
                selection = int(input(prompt.strip() + " "))
                # check if selection is valid.
                if selection in menu.menu or selection == menu.gobackindex:
                    return selection
                else:
                    print(invalid_promt.strip())
                # if typecast fails:
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def handler(self,
                prompt: str,
                identifier_to_start_from: str | None = None,
                Invalid_Prompt: str = "Invalid Selection. Please choose a valid option.", 
                Title_Format: str = "Menu: {identifier}",
                Body_Format: str = "{index} - {text}",
                post_execution_label: str = "Menu Executed.",
                return_execution_result: bool = False) -> tuple[bool, Any]:
        """`Handler for all the added Menus` - Executer

        ### Parameters

        - `prompt` `_(str)_`: What to prompt the user when asking to choose an option.
        - `identifier_to_start_from` `_(str | None)_`: If `None`, then starts from first (recommended) else starts from the given identifier of the menu pool.
        - `Invalid_Prompt` `_(str)_`: The message to show if the user chooses something outside the scope of the menu.
        - `Title_Format` `_(str)_`: Format in which the menu title will be displayed.
        - `Body_Format` `_(str)_`: Format in which the menu body will be displayed.
        - `post_execution_label` `_(str)_`: The message to show after the user desired menu function is executed.
        - `return_execution_result` `_(bool)_`: If the handler should return the result of execution of the menu function.

        ### Usage

        ```
        from menux.generator import MenuBuilder
        from typing import Any

        builder = MenuBuilder()

        # Now I want to create a menu that has a submenu.
        # like one option would be to add two nums and another option will be "more options" which will expand to subtract two nums.

        def add_two():
            num1 = int(input("enter num1: "))
            num2 = int(input("enter num2: "))
            return num1 + num2
        
        def sub_two():
            num1 = int(input("enter num1: "))
            num2 = int(input("enter num2: "))
            return num1 - num2
        
        builder.add( # refer docstring of add for more info.
            identifier = "main_menu",
            menu = {1: "Add two nums", 2: "more options"},
            functions = {1: add_two, 2: None},
        )

        # the above line will add a main_menu with the function of "2" to None. As it will have a sub menu.
        # now add the submenu. (refer add_submenu docstring for info)

        builder.add_submenu(
            parent_identifier = "main_menu",
            parent_menu_index = 2,
            submenu_identifier = "sub_menu_of_index_2",
            submenu = {1: "Subtract two nums"},
            submenu_functions = {1: sub_two},
        )

        # now that all is set, use handler to begin the menu.

        result: tuple[bool, Any] = builder.handler(prompt="Enter your choice:")
        
        if result[0]:
            print(f"Execution succesfull. Result: {result[1]}")
        else:
            print(f"Failed to execute.")
        ```

        ### Returns

        > `Tuple[bool, Any]`: the bool is for execution status (True for success, False if the user chose to exit the root menu). Any is the result of the execution if return_execution_result is False, Then None.
        """
        # create a menu stack for handling back operations
        menu_stack: list[Menu] = []

        # if identifier is not provided check for validity of menu_pool
        if identifier_to_start_from is None:
            # if menu pool is empty, raise exception
            if not self.menus:
                raise NoMenuFound("Add Menus to work with them.")
            # else set it to the root menu.
            menu = self.menus[0]
        else:
            # if identifier is provided, find the identifier
            menu = self._find_menu(identifier_to_start_from, self.menus)

            # if no menu exists for the given identifier then raise exception
            if not menu:
                raise StartIdentifierNotFound(f"identifier_to_start_from[\'{identifier_to_start_from}\'] not found in the menu pool.")
        
        # Follow all menus and sub-menus until the end of menu, and execute the function associated with it.
        while True:
            # display the menu
            self._display_menu(menu, Title_Format, Body_Format)
            # capture the output.
            selection = self._capture_selection(menu, prompt, Invalid_Prompt)

            # if it is the goback index, 
            if menu.gobackindex == selection:
                # if it is not the root menu, 
                if menu_stack:
                    # go back up and run again
                    menu = menu_stack.pop()
                else:
                    # if it is the root menu, return False, None
                    return (False, None)
                # if the selection has a submenu.
            elif selection in menu.submenu:
                # append the current menu in the stack
                menu_stack.append(menu)
                # update the menu to sub - menu and run again.
                menu = menu.submenu[selection]
                # if none of it, that means it is the end:
            else:
                # if there is a function for the end point,
                if selection in menu.functions and menu.functions[selection] is not None:
                    # execute it
                    menu.execute_function(selection, return_execution_result)
                    # print post execution label
                    print(post_execution_label.strip())
                    # if the result is to be returned, return it. else return None for the result.
                    if return_execution_result:
                        return (True, menu.results[selection])
                    else:
                        return (True, None)
                    # if there is no function, raise an exception
                else:
                    raise EndReachedNoFunctionFound("End of the menu is reached but no function is found for this option. Maybe it will come soon.")