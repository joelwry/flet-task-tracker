import os
import json
import datetime
import flet as ft

TODO_FILE_PATH = "./todo_data2.json"

class Task:
    def __init__(self, title, description, expiration_date=None, completed=False):
        self.title = title
        self.description = description
        self.expiration_date = expiration_date
        self.completed = completed

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "expiration_date": self.expiration_date,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["title"],
            data["description"],
            data["expiration_date"],
            data["completed"],
        )


def save_todo_list(todo_list):
    with open(TODO_FILE_PATH, "w") as file:
        json.dump([task.to_dict() for task in todo_list], file)


def load_todo_list():
    if os.path.exists(TODO_FILE_PATH):
        with open(TODO_FILE_PATH, "r") as file:
            data = json.load(file)
            return [Task.from_dict(task_data) for task_data in data]
    return []

# this function creates a Column layout component that has controls of input field for editing the todo Task the user wants to re-edit
def responsiveInputContents(title_value:str,description_value:str,task_value_state:bool,expiration_value:str) -> ft.Column:
    INPUTS_BORDER_COLOR = "#683ee9"
    _title_input = ft.TextField(hint_text="Enter the title of the task...", col={"sm": 6, "md": 4, "xl": 4}, border='UNDERLINE',focused_border_color="#16cb99",border_color=INPUTS_BORDER_COLOR, value=title_value,label="Title of Task")
    _description_input = ft.TextField(
        hint_text="Enter the description of the task...",  col={"sm": 12, "md": 12, "xl": 8},border='underline',content_padding=30,focused_border_color="#16cb99",multiline=True,border_color=INPUTS_BORDER_COLOR,value=description_value,label="Description of task"
    )
    _state = ft.RadioGroup(content=ft.Column(
            alignment="CENTER",spacing=20,
            controls=[
                ft.Radio(value=True, label='Task Completed',fill_color='#16cb99'),
                ft.Radio(value=False, label="Not Completed", fill_color='red')
            ]
        ), value=task_value_state
    )
    
    _expiration_input = ft.TextField(
        hint_text="Enter the expiration date (YYYY-MM-DD)...", col={"sm": 6, "md": 4, "xl": 4}, border='underline',focused_border_color="#16cb99",keyboard_type="DATETIME",value=expiration_value,label="Expiration Date of Task"
    )

    return ft.Column(spacing=20,run_spacing=20, alignment='CENTER',scroll="AUTO",
            controls=[
                _title_input,
                _expiration_input,
                _description_input,
                _state
            ]
        )


# this function views a task in a pop up modal
def viewTaskDetails(title: str, description: str, start_date: str, completion_state: bool):
    view_component = ft.Column(
        spacing=20,
        controls=[
            ft.Text(f"Title: {title}", size=20),
            ft.Text(f"Description: {description}"),
            ft.Text(f"Start Date: {start_date}"),
            ft.Text("Completion State: Completed" if completion_state else "Completion State: Not Completed")
        ]
    )

    view_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Task Details"),
        content=view_component,
        actions=[
            ft.TextButton("Close", on_click=close_dlg)
        ],
        shape=ft.RoundedRectangleBorder(radius=ft.BorderRadius(20, 30, 30, 20))
    )

    page.dialog = view_dialog
    view_dialog.open = True
    page.update()

# create dialog pop up modal for showing element to edit
def editElementComponent(task_header:str,_component:ft.Column,actions_button = None) -> ft.AlertDialog :
    if actions_button != None:
        actions_button = [
            ft.TextButton("Cancel", on_click=close_dlg),
            ft.TextButton("Save", on_click=save_task),
            ft.TextButton("Delete", on_click=delete_task)
        ]
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text(task_header),
        content=_component,
        actions=actions_button,
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
        shape=ft.RoundedRectangleBorder(radius=ft.BorderRadius(20,30,30,20))
    )
    return dlg_modal

# closes the dialog attached to the page
def close_dlg(e):
    page = e.page
    page.dialog.open = False
    page.update()

def delete_task(e):
    if not isinstance(e.control, ft.TextButton):
        print('cannot delete task')
        return
    hash_id = e.control.data
    print(hash_id)
    for task in todo_list:
        if task.__hash__() == hash_id:
            todo_list.remove(task)
            save_todo_list(todo_list)
            render_todo_list()
            close_dlg(e)  # Close the dialog after deletion
            break

def save_task(e):
    print('save event called')
    if isinstance(e.control, ft.TextButton):  # 
        hash_id = e.control.data  # Get the hash_id

        input_controls = e.page.dialog.content.controls 
        for task in todo_list:
            print(f'{hash_id} <==> {task.__hash__()}')
            if hash_id == task.__hash__():
                # Check if any changes were made to the task
                if task.title != input_controls[0].value or \
                   task.description != input_controls[2].value or \
                   task.expiration_date != input_controls[1].value or \
                   task.completed != input_controls[3].value:
                    # Update the task with the new values
                    task.title = input_controls[0].value
                    task.description = input_controls[2].value
                    task.expiration_date = input_controls[1].value
                    task.completed = input_controls[3].value
                    save_todo_list(todo_list)
                    render_todo_list()
                    print('changes made to todo item')
                close_dlg(e)  # Close the dialog after saving
                break
            print("Nothing to update")




# this function open a dialog component on the page for editing user todo task
def openEditTaskDialog(e,hash_id:int,title_value:str,description_value:str,task_value_state:bool,expiration_value:str):
    """ 
        This function performs three task
        - it will first create the Column component containing input fields that have values of the passed in argument
        - it will then pass this component down to the created Dialog in the editElementComponent
        - the dialog created will then be attached to the page and set to open state so as to display over all other components on the page
    """
    component = responsiveInputContents(title_value,description_value,task_value_state,expiration_value)
    dlg = editElementComponent("Editing Task",component,True)

    # add a data attribute to each action buttons in the dialog control that will be a reference value to the hash value of a Task object instance
    for action_button in dlg.actions:
        action_button.data = hash_id

    e.page.dialog = dlg 
    dlg.open = True
    e.page.update()

# this function returns a Data Table of a Todo Task
def table(todos):
    cell_data = []
    for index,todo in enumerate(todos):
        cell_data.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(content=ft.Text(todo.title), on_double_tap=lambda e : print(f'todo title {e.control.content}')),
                    ft.DataCell(content =ft.Text(todo.completed)),
                    ft.DataCell(content = ft.Text(todo.expiration_date)),
                    ft.DataCell(content=ft.Row([ft.ElevatedButton(text="Edit",on_click=lambda e, index=index,hash_id=todo.__hash__(): openEditTaskDialog(e,hash_id,todos[index].title,todos[index].description, todos[index].completed, todos[index].expiration_date)),ft.ElevatedButton("View", on_click=lambda e, title=todo.title, description=todo.description, start_date=todo.expiration_date, completion_state=todo.completed: viewTaskDetails(title, description, start_date, completion_state))]))
                ],
            )
        )

    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Title")),
            ft.DataColumn(ft.Text("Completed")),
            ft.DataColumn(ft.Text("Date"), numeric=False),
            ft.DataColumn(ft.Text("Action"), numeric=False),
        ],
        rows=cell_data
    )


# an event handler for when a user resize the window size of the app 
def pageOnResize(e):
    print('resizing')
    controller = e.control
    print(controller.width)
    if controller.width < 450:
        controller.theme = ft.theme.Theme(color_scheme_seed="green")
        controller.update()
    else:
        controller.theme = ft.theme.Theme(color_scheme_seed="black")
        controller.update()


def main(pg: ft.Page):
    global page
    page = pg
    # making todo_list global so that it can be accessible everywhere in this file
    global todo_list
    todo_list = load_todo_list()

    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_min_height = 740
    page.window_min_width = 360
    page.scroll = "AUTO"
    page.on_resize = pageOnResize

    # variable tasks to keep track of 
    incompleted_tasks = []
    completed_tasks = []
    expired_tasks = []
    all_tasks = []
    
    # defining some input control widget for recieving user inputs
    INPUTS_BORDER_COLOR = "#683ee9"
    new_title_input = ft.TextField(hint_text="Enter the title of the task...", col={"sm": 6, "md": 4, "xl": 4}, border='UNDERLINE',focused_border_color="#16cb99",border_color=INPUTS_BORDER_COLOR)
    new_description_input = ft.TextField(
        hint_text="Enter the description of the task...",  col={"sm": 12, "md": 12, "xl": 8},border='underline',content_padding=30,focused_border_color="#16cb99",multiline=True,icon=ft.icons.DESCRIPTION_SHARP,border_color=INPUTS_BORDER_COLOR
    )
    task_state = ft.RadioGroup(content=ft.Row(
            alignment="CENTER",
            controls=[
                ft.Radio(value=True, label='Task Completed',fill_color='#16cb99'),
                ft.Radio(value=False, label="Not Completed", fill_color='red')
            ]
        ), value=False
    )
    
    new_expiration_input = ft.TextField(
        hint_text="Enter the expiration date (YYYY-MM-DD)...", col={"sm": 6, "md": 4, "xl": 4}, border='underline',icon=ft.icons.CALENDAR_VIEW_MONTH_ROUNDED,focused_border_color="#16cb99",keyboard_type="DATETIME"
    )
    
    # adding a new task from the input fields to the json db 
    def add_task(e):
        expiration_date_str = new_expiration_input.value.strip()
        try:
            todo_date = datetime.datetime.strptime(expiration_date_str,"%Y-%m-%d").date()
        except Exception as e:
            dlg = ft.AlertDialog(title=ft.Text(e), on_dismiss=lambda e: print("Dialog dismissed!"))
            page.dialog = dlg
            dlg.open = True
            page.update()
            return

        title = new_title_input.value.strip()
        description = new_description_input.value.strip()
        if title and description:
            expiration_date = datetime.datetime.strptime(
                expiration_date_str, "%Y-%m-%d"
            ).date().__str__() if expiration_date_str else None
            todo_list.append(Task(title, description, expiration_date,task_state.value))
            print(f'Task state is {task_state.value}')
            save_todo_list(todo_list)
            render_todo_list()
            new_title_input.value = ""
            new_description_input.value = ""
            new_expiration_input.value = ""
            task_state.value = False
            new_title_input.focus()
            page.update()

   
    # this reset the various category task of completed, incomplete, expired,all task
    def resetTaskListVariables():
        incompleted_tasks.clear()
        completed_tasks.clear()
        expired_tasks.clear()
        all_tasks.clear()

    # setting this function to be global
    global render_todo_list
    def render_todo_list():
        resetTaskListVariables()

        for task in todo_list:
            task_text = task.title
            if task.completed:
                completed_tasks.append(task) 
            else:
                incompleted_tasks.append(task)

            if task.expiration_date and datetime.datetime.strptime(task.expiration_date,"%Y-%m-%d").date() < datetime.date.today():
                    expired_tasks.append(task)
            all_tasks.append(task)

        # inserting this DataTable into row layout allows the table to be autoscrollable when the table content width is too large to fit the user screen 
        scrollable_row = ft.Row(controls=[table(all_tasks)],scroll="AUTO")

        #render all tasks
        container.content = scrollable_row

        page.update()

    # an event handler for when the pop menu button are clicked hence this will enable the relevant task to be shown in the data table
    def poppedMenuItemClicked(e, pop_btn:ft.PopupMenuButton)->None:
        pop_btn.content = ft.Text("showing "+e.control.text)
        task_type_to_show = e.control.data
        if task_type_to_show == "all":
            container.content = table(all_tasks)
        elif task_type_to_show =="complete":
            container.content = table(completed_tasks)
        elif task_type_to_show == "incomplete":
            container.content = table(incompleted_tasks)
        elif task_type_to_show == "expire":
            container.content = table(expired_tasks)
        page.update()

    # this function creates a pop up menu buttons for user to select the type of todo to view
    def taskMenuPopupButtons():
        _popped_buttons = ft.PopupMenuButton(
            content= ft.Text("Active Task -> All"),
            icon = ft.Icon(ft.icons.HOURGLASS_TOP_OUTLINED),
            items=[
                ft.PopupMenuItem(icon=ft.icons.POWER_INPUT, text="All Task",data="all", on_click=lambda e :poppedMenuItemClicked(e, _popped_buttons)),
                ft.PopupMenuItem(icon=ft.icons.POWER_INPUT, text="Completed Tasks",data="complete", on_click=lambda e :poppedMenuItemClicked(e, _popped_buttons)),
                ft.PopupMenuItem(icon=ft.icons.POWER_INPUT, text="Incomplete Tasks",data="incomplete", on_click=lambda e :poppedMenuItemClicked(e, _popped_buttons)),
                ft.PopupMenuItem(),  # divider
                ft.PopupMenuItem(
                    text="Expired Tasks", on_click=lambda e :poppedMenuItemClicked(e, _popped_buttons), data="expire"
                ),
            ]
        )
        return _popped_buttons

    container = ft.Container()

    title_holder =ft.Text("TODO CHECKER",size=50,color=ft.colors.WHITE,bgcolor=ft.colors.GREEN_700,weight=ft.FontWeight.BOLD,italic=True,selectable=True,text_align='CENTER')

    # adding all the control widget to the page
    page.add(
        ft.ResponsiveRow(spacing=40,run_spacing=40, alignment='CENTER',
            controls=[
                title_holder,
                new_title_input,
                new_expiration_input,
                new_description_input,
                task_state,
                ft.ElevatedButton("Add", on_click=add_task,col={"sm": 12, "md": 6, "xl": 6}, height=60),
            ]
        ),
        taskMenuPopupButtons(),
        container
    )
    
    

    render_todo_list()


ft.app(target=main)
