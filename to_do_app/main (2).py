import sys

import pytermgui as ptg

tasks = []


class TaskButton(ptg.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def get_task_widgets(manager: ptg.WindowManager) -> list[ptg.Label, TaskButton]:
    task_widgets = []

    for task_dict in tasks:
        for task_name, task_status in task_dict.items():
            label = ptg.Label(task_name, parent_align=0, position=1)
            button = TaskButton(
                "done" if task_status else "pending",
                lambda btn: handle_task_update(manager, btn),
                id=f"{task_name}",
            )
            task_widgets.append((label, button))

    return task_widgets


def parse_and_add_task(manager: ptg.WindowManager, modal: ptg.Window) -> None:
    global tasks

    for widget in modal:
        if isinstance(widget, ptg.InputField):
            new_task = widget.value
            tasks.append({new_task: False})

    show_tasks_and_status(manager)
    modal.close()


def show_add_task_modal(manager: ptg.WindowManager) -> None:
    modal = ptg.Window(
        "Add Task",
        "",
        ptg.InputField("Eat food...", prompt="Task: ", id="task_input"),
        "",
        ptg.Container(
            ptg.Splitter(
                ptg.Button("Enter", lambda *_: parse_and_add_task(manager, modal)),
                ptg.Button("Close", lambda *_: modal.close()),
            )
        ),
    ).center()
    manager.add(modal)


def handle_task_update(manager: ptg.WindowManager, button: TaskButton) -> None:
    global tasks

    def mark_task_as_done(task_name: str) -> None:
        for task in tasks:
            if task_name in task.keys():
                task[task_name] = True
        modal.close()
        show_tasks_and_status(manager)

    modal = ptg.Window(
        "Mark Task as Done?",
        "",
        ptg.Container(
            ptg.Splitter(
                ptg.Button("Yes", lambda *_: mark_task_as_done(button.id)),
                ptg.Button("Close", lambda *_: modal.close()),
            )
        ),
    ).center()

    manager.add(modal)


def confirm_quit(manager: ptg.WindowManager) -> None:
    modal = ptg.Window(
        "Confirm Quit?",
        "",
        ptg.Container(
            ptg.Splitter(
                ptg.Button("Yes", lambda *_: manager.stop()),
                ptg.Button("No", lambda *_: modal.close()),
            ),
        ),
    ).center()

    modal.select(1)
    manager.add(modal)


def show_tasks_and_status(manager: ptg.WindowManager) -> None:
    task_widgets = get_task_widgets(manager)

    tasks_column = ptg.Window(
        *[task[0] for task in task_widgets], id="tasks_col"
    ).set_title("Tasks")

    status_column = ptg.Window(
        *[task[1] for task in task_widgets], id="tasks_status_col"
    ).set_title("Tasks Status")
    for window in manager._windows:
        if window.id in ["tasks_col", "tasks_status_col"]:
            manager.remove(window)

    manager.add(status_column, assign="body_right")
    manager.add(tasks_column, assign="body")


def define_layout() -> ptg.Layout:
    layout = ptg.Layout()

    layout.add_slot("Header", height=2)
    layout.add_break()

    layout.add_slot("Body")
    layout.add_slot("Body right", width=0.2)
    layout.add_break()

    layout.add_slot("Footer", height=1)

    return layout


def main() -> None:
    with ptg.WindowManager() as manager:
        manager.layout = define_layout()

        header = ptg.Window("TO-DO-APP", box="EMPTY")
        manager.add(header, assign="header")

        show_tasks_and_status(manager)

        footer = ptg.Window(
            ptg.Splitter(
                ptg.Button("Add Task", lambda *_: show_add_task_modal(manager)),
                ptg.Button("Quit", lambda *_: confirm_quit(manager)),
            ),
            box="EMPTY",
        )
        manager.add(footer, assign="footer")
        manager.run()


if __name__ == "__main__":
    sys.exit(main())
