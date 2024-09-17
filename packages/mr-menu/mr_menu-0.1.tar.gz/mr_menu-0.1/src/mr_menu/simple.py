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

from typing import Callable, Dict, Any

# *Format*
# - Menu -
# identifier: "Menu 1"
# menu: {1: "Add two numbers", 2: "Subtract two numbers"}
# submenu: {2: -Menu-}

class Menu:
    """Base Node Class for Menu Tree.

    ### Parameters

    - `identifier` `_(str)_`: Unique Identifier for Menu Node.
    - `menu` `_(dict[int, str])_`: Menu in the form of dict where keys are `int` and values are the labels in `str` format.
    - `functions` `_(dict[int, callable])_`: Another dict mapped as per the `Menu` parameter where keys are `int` and exists in `Menu` and values are callable functions.
    - `submenu`: This should be set to None, if you want submenus, use `MenuBuilder`.
    - `go_back_index` `_(int | None)_`: If not using `MenuBuilder`, set it to the int key value that represents the `Go Back` option. If set to None, an extra `Go Back` option will be created auto-matically.
        
        If using `MenuBuilder`, set it to None, `Go Back` option will be created automatically.
    
    ### Usage

    ```
    >>> from menux.simple import Menu
    >>> from typing import Any

    >>> def add_two():
    ...     num1 = int(input("enter num1: "))
    ...     num2 = int(input("enter num2: "))
    ...     return num1 + num2
    ...

    >>> def sub_two():
    ...     num1 = int(input("enter num1: "))
    ...     num2 = int(input("enter num2: "))
    ...     return num1 - num2
    ...

    >>> menu = Menu("menu_0", {1: "Add Two nums", 2: "Subtract Two nums"}, {1: add_two, 2: sub_two}, None, None)

    >>> result: tuple[bool, Any] = menu.handler(prompt="Enter choice: ")

    >>> if result[0]:
    ...     pass # executed successfully.
    ... else:
    ...     pass # did not execute successfully.
    ```
    """
    def __init__(self,
                 identifier: str,
                 menu: dict[int, str],
                 functions: Dict[int, Callable | None],
                 submenu: dict[int, 'Menu'] | None = None,
                 go_back_index: int | None = None) -> None:
        """Base Node Class for Menu Tree.

        ### Parameters

        - `identifier` `_(str)_`: Unique Identifier for Menu Node.
        - `menu` `_(dict[int, str])_`: Menu in the form of dict where keys are `int` and values are the labels in `str` format.
        - `functions` `_(dict[int, callable])_`: Another dict mapped as per the `Menu` parameter where keys are `int` and exists in `Menu` and values are callable functions.
        - `submenu`: This should be set to None, if you want submenus, use `MenuBuilder`.
        - `go_back_index` `_(int | None)_`: If not using `MenuBuilder`, set it to the int key value that represents the `Go Back` option. If set to None, an extra `Go Back` option will be created auto-matically.
          
          If using `MenuBuilder`, set it to None, `Go Back` option will be created automatically.
        
        ### Usage

        ```
        >>> from menux.simple import Menu
        >>> from typing import Any

        >>> def add_two():
        ...     num1 = int(input("enter num1: "))
        ...     num2 = int(input("enter num2: "))
        ...     return num1 + num2
        ...

        >>> def sub_two():
        ...     num1 = int(input("enter num1: "))
        ...     num2 = int(input("enter num2: "))
        ...     return num1 - num2
        ...

        >>> menu = Menu("menu_0", {1: "Add Two nums", 2: "Subtract Two nums"}, {1: add_two, 2: sub_two}, None, None)

        >>> result: tuple[bool, Any] = menu.handler(prompt="Enter choice: ")

        >>> if result[0]:
        ...     pass # executed successfully.
        ... else:
        ...     pass # did not execute successfully.
        ```
        """
        self.identifier = identifier
        self.menu = menu
        self.submenu = submenu if submenu != None else {}
        self.gobackindex = go_back_index if go_back_index != None else list(dict(sorted(self.menu.items(), key=lambda x: x[0])).keys())[-1] + 1
        self.functions = functions
        self.results: Dict[int, Any] = {}
    
    def execute_function(self, key: int, store_result: bool) -> None:
        """Execute a function of the menu.

        ### Parameters

        - `key` `_(int)_`: key of the menu whose, function you need to execute.
        - `store_result` `_(bool)_`: If result needs to be stored. If True, result will be available in `self.results[key]`

        ### Usage

        ```
        >>> from menux.simple import Menu

        >>> def add_two():
        ...     num1 = int(input("enter num1: "))
        ...     num2 = int(input("enter num2: "))
        ...     return num1 + num2
        ...

        >>> def sub_two():
        ...     num1 = int(input("enter num1: "))
        ...     num2 = int(input("enter num2: "))
        ...     return num1 - num2
        ...

        >>> menu = Menu("menu_0", {1: "Add Two nums", 2: "Subtract Two nums"}, {1: add_two, 2: sub_two}, None, None)

        >>> menu.execute_function(key=1, store_result=True)

        >>> result = menu.results[1]
        ```
        """
        func = self.functions.get(key)
        if func:
            result = func()
            if store_result:
                self.results[key] = result
    
    def _display_menu(self, Title_format: str = "Menu: {identifier}", Body_format: str = "{index} - {text}") -> None:
        """displays the menu."""
        print(Title_format.replace("{identifier}", self.identifier))
        for key, value in self.menu.items():
            print(Body_format.replace("{index}", str(key)).replace("{text}", value))

        print(Body_format.replace("{index}", str(self.gobackindex)).replace("{text}", "Go back"))
        print()
    
    def _capture_selection(self, prompt: str, invalid_promt: str = "Invalid Selection. Please choose a valid option.") -> int:
        """captures the output of the menu and returns it."""
        while True:
            try:
                selection = int(input(prompt.strip() + " "))
                if selection in self.menu or selection == self.gobackindex:
                    return selection
                else:
                    print(invalid_promt.strip())
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    def handler(self,
                prompt: str,
                Invalid_Prompt: str = "Invalid Selection. Please choose a valid option.", 
                Title_Format: str = "Menu: {identifier}",
                Body_Format: str = "{index} - {text}",
                post_execution_label: str = "Menu Executed.",
                return_execution_result: bool = False) -> tuple[bool, Any]:
        """`handles the menu and runs any associated functions`
        
        ### parameters

        - `prompt` `_(str)_`: The prompt for the user after the menu is displayed.
        - `Invalid_Pompt` `_(str)_`: The message that is shown before asking for the choice again in case of invalid choice.
        - `Title_Format` `_(str)_`: The format in which the menu name will be displayed.
        - `Body_Format` `_(str)_`: The format in which the menu body will be displayed.
        - `post_execution_label` `_(str)_`: After execution of the associated menu function, what to print.
        - `return_execution_result` `_(bool)_`: If the result is to be returned after execution for the function.

        ### Usage

        ```
        >>> from menux.simple import Menu
        >>> from typing import Any

        >>> def add_two():
        ...     num1 = int(input("enter num1: "))
        ...     num2 = int(input("enter num2: "))
        ...     return num1 + num2
        ...

        >>> def sub_two():
        ...     num1 = int(input("enter num1: "))
        ...     num2 = int(input("enter num2: "))
        ...     return num1 - num2
        ...

        >>> menu = Menu("menu_0", {1: "Add Two nums", 2: "Subtract Two nums"}, {1: add_two, 2: sub_two}, None, None)

        >>> result: tuple[bool, Any] = menu.handler(prompt="select your choice: ")
        ```

        ### Returns

        > `tuple[bool, Any]` where bool is True if execution is success else False. `Any` could be `None` if no result is returned, else whatever may be the result of the menu function execution
        """
        # if 
        self._display_menu(Title_format=Title_Format, Body_format=Body_Format)
        selection = self._capture_selection(prompt, Invalid_Prompt)

        if selection == self.gobackindex:
            return (False, None)
        elif selection in self.menu and selection in self.functions:
            if self.functions[selection] is not None:
                self.execute_function(selection, return_execution_result)
                print(post_execution_label)
                if return_execution_result:
                    return (True, self.results[selection])
                else:
                    return (True, None)
            else:
                return (True, None)    