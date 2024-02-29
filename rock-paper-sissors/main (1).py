from random import choice
import sys

import pytermgui as ptg


def define_layout() -> ptg.Layout:
    layout = ptg.Layout()

    layout.add_slot("header", height=1)
    layout.add_break()

    layout.add_slot("body")
    layout.add_break()

    layout.add_slot("footer", height=1)

    return layout


def close_modal(manager: ptg.WindowManager, modal: ptg.Window) -> None:
    for window in manager._windows:
        if modal in window:
            window.remove(modal)


def remove_widget_by_id(manager: ptg.WindowManager, widget_id: str) -> ptg.Window:
    for window in manager._windows:
        for widget in window._widgets:
            if widget.id == widget_id:
                close_modal(manager, widget)
                return window


def remove_all_windows(manager: ptg.WindowManager) -> None:
    for window in manager._windows:
        manager.remove(window)


def play_again_callback(manager: ptg.WindowManager, modal: ptg.Container) -> None:
    close_modal(manager, modal)
    remove_all_windows(manager)
    initialize_screen(manager)


def game_callback(button: ptg.Button, manager: ptg.WindowManager) -> None:
    computer_choice = choice(["🗻", "📃", "✂"])
    result = "[bold #00FF00]WIN"
    if computer_choice == button.label:
        result = "TIE"
    elif computer_choice == "🗻" and button.label == "✂":
        result = "[bold #FF0000]LOOSE"
    elif computer_choice == "📃" and button.label == "🗻":
        result = "[bold #FF0000]LOOSE"

    modal = ptg.Container(
        ptg.Label(f"👨 have selected: {button.label}"),
        "",
        ptg.Label(f"💻 Has selected: {computer_choice}"),
        "",
        ptg.Label(f"You {result}"),
        ptg.Splitter(
            ptg.Button("Play Again", lambda *_: play_again_callback(manager, modal)),
            ptg.Button("Quit", lambda *_: manager.stop()),
        ),
    ).center()

    window = remove_widget_by_id(manager, "game_window_container")
    window._add_widget(modal)


def get_game_window(manager: ptg.WindowManager) -> ptg.Window:
    return ptg.Window(
        ptg.Container(
            ptg.Splitter(
                ptg.Button("🗻", lambda button: game_callback(button, manager)),
                ptg.Button("📃", lambda button: game_callback(button, manager)),
                ptg.Button("✂", lambda button: game_callback(button, manager)),
            ),
            id="game_window_container",
        ),
        id="game_window",
    )


def initialize_screen(manager: ptg.WindowManager) -> None:
    header = ptg.Window("Rock-Paper-Scissors", box="EMPTY")
    manager.add(header, assign="header")

    game_window = get_game_window(manager)
    manager.add(game_window, assign="body")

    footer_buttons = ptg.Splitter(
        ptg.Button("Quit", lambda *_: manager.stop()),
    )
    footer = ptg.Window(footer_buttons, box="EMPTY")
    manager.add(footer, assign="footer")


def main():
    with ptg.WindowManager() as manager:
        manager.layout = define_layout()
        initialize_screen(manager)
        manager.run()


if __name__ == "__main__":
    sys.exit(main())
