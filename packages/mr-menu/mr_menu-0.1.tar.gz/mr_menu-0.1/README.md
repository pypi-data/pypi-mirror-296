[![Unit Tests](https://github.com/d33p0st/mr-menu/actions/workflows/test.yml/badge.svg)](https://github.com/d33p0st/mr-menu/actions/workflows/test.yml)
[![codecov](https://codecov.io/github/d33p0st/mr-menu/graph/badge.svg?token=NF0LC6QWPX)](https://codecov.io/github/d33p0st/mr-menu)
[![CD(PYPI)](https://github.com/d33p0st/mr-menu/actions/workflows/pypi.yml/badge.svg)](https://github.com/d33p0st/mr-menu/actions/workflows/pypi.yml)
# Overview

`mr-menu` helps create Menus and sub-Menus all at once and helps managing them easily. `mr-menu` can easily execute menu and sub-menus and their conditional functions all-together.

Using `mr-menu`, you can create a `Tree` of Menus and add functionalities for each menu item. `mr-menu` can execute those functionalities and return results gracefully.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Issues](#issues)
- [Pull Requests](#pull-requests)

## Features

- **_Nested Tree of Menu and Sub-Menus_**: Single Menu can have multiple sub-menus and further sub-sub-menus and so on.

- **_In-built Execution of defined functions_**: You can define functions for each menu item and `mr-menu` will execute them based on which option the user chooses.

## Installation

Execute in Terminal:

```bash
pip install mr-menu
```

## Usage

> Example Test Case: Suppose you want to create a simple menu which will contain two items - Add two nums and Sub two nums.

- **`Simple Menu`**

  - import the `Menu` class.

    ```python
    from mr-menu.simple import Menu
    ```

  - create functions/class methods for Add and Sub

    ```python
    def add_two():
        num1 = int(input("Enter num 1: "))
        num2 = int(input("Enter num 2: "))
        return num1 + num2
    
    def sub_two():
        num1 = int(input("Enter num 1: "))
        num2 = int(input("Enter num 2: "))
        return num1 - num2
    ```

  - Create `Menu` class object

    ```python
    menu = Menu(
        identifier="main", # unique menu identifier.
        menu={1: "Add two nums", 2: "Sub two nums"}, # menu in dict form
        functions={1: add_two, 2: sub_two}, # function dict with callable functions mapped to menu
    )
    ```

  - Handle the menu and it's functions.

    ```python
    result = menu.handler(
        prompt="Enter choice: ", # to be shown to the user.
        return_execution_result=True,
        *args, # see docstring
        **kwargs, # see docstring
    )

    # the above code will ask the user for input with the 
    # prompt and if it is "1", it will ask for two nums and 
    # return (True, output).
    # Similarly, if "2" is selected, it will return (True, output) again.
    # if execution fails, it will return (False, None)
    ```

> Now, Let us take an example where the first menu has two options -> Add, Sub and one extra option -> `More options` which expands into another menu, say, `Multiply` and `divide`.

- **`Tree of Menus and submenus`**

  - import `MenuBuilder` classs

    ```python
    from mr-menu.generator import MenuBuilder
    ```

  - create functions for `Add`, `Sub`, `Multiply` and `divide`

    ```python
    def add():
        num1 = int(input("enter num 1: "))
        num2 = int(input("enter num 2: "))
        return num1 + num2
    
    def sub():
        num1 = int(input("enter num 1: "))
        num2 = int(input("enter num 2: "))
        return num1 - num2
    
    def mult():
        num1 = int(input("enter num 1: "))
        num2 = int(input("enter num 2: "))
        return num1*num2
    
    def div():
        num1 = int(input("enter num 1: "))
        num2 = int(input("enter num 2: "))
        return num1/num2 if num2 != 0 else 0
    ```

  - create `MenuBuilder` class object

    ```python
    builder = MenuBuilder()
    ```

  - Add the first menu (main menu)

    ```python
    builder.add(
        identifier="main", # Unique identifier for this particular menu
        menu={1: "Add two nums", 2: "Sub two nums", 3: "More Options"}, # menu in dict form
        functions={1: add, 2: sub, 3: None}, # functions for all the options except the one that expands a new menu (3rd)
        go_back_index=None, # It is recommended to keep this
        # None, as a new (4th) option will be automatically
        # created and handled that facilitates going back to the main menu.
    )
    ```

  - Add the sub-menu

    ```python
    builder.add_submenu(
        parent_identifier="main", # parent menu is "main",
        parent_menu_index=3, # the index key where the menu is supposed to expand. i.e., 3 (More options)
        submenu_identifier="main-submenu-1", # the unique identifier for this sub-menu,
        submenu={1: "Multiply two nums", 2: "Divide two nums"}, # submenu in dict form.
        go_back_index=None, # again, keep this None, here a 3rd
        # option will be automatically created that helps to
        # go back to the main menu.
        replace_if_exist=True, # this means if the submenu already exists, replace the old one with this current one.
    )
    ```

  - Handle the menu and submenu

    If the user chooses option 1 (Add two nums), the `handler` will ask for two inputs and return the sum of the numbers. But when the user chooses 3rd option in the main menu, The new sub-menu will be displayed. The user can then choose `Multiply` and `Divide`.

    ```python
    result = builder.handler(
        prompt="Enter your choice:", # the prompt that asks to choose an option.
        post_execution_label="The Task executed Successfully", # after a task finishes, this will be printed.
        return_execution_result=True, # returns the result in tuple form with two values - tuple[bool, Any],,
        # where bool represents execute status and Any is the result.
    )
    ```

## Issues

Please submit any issues found [here](https://github.com/d33p0st/mr-menu/issues).

## Pull Requests

Pull Requests are welcome and encouraged. Find it [here](https://github.com/d33p0st/mr-menu/pulls)