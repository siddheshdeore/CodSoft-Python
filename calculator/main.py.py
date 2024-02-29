from decimal import Decimal
from textual import events, on
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.css.query import NoMatches
from textual.reactive import var
from textual.widgets import Button, Digits


class CalculatorApp(App):
    CSS_PATH = "style.tcss"

    numbers = var("0")
    show_ac = var(True)
    left = var(Decimal("0"))
    right = var(Decimal("0"))
    result = var("")
    operator = var("plus")

    map_data = {
        "asterisk": "multiply",
        "minus": "minus",
        "slash": "di`vide",
        "plus_minus_sign": "plus-minus",
        "percent_sign": "percent",
        "full_stop": "point",
        "underscore": "plus-minus",
        "plus": "plus",
        "equals_sign": "equals",
    }

    def watch_numbers(self, value: str) -> None:
        self.query_one("#numbers", Digits).update(value)

    def compute_show_ac(self) -> bool:
        return self.result in ("", "0") and self.numbers == "0"

    def watch_show_ac(self, show_ac: bool) -> None:
        self.query_one("#c").display = not show_ac
        self.query_one("#ac").display = show_ac

    def compose(self) -> ComposeResult:
        with Container(id="calculator"):
            yield Digits(id="numbers")
            yield Button("AC", id="ac", variant="primary")
            yield Button("C", id="c", variant="primary")
            yield Button("+/-", id="plus-minus", variant="primary")
            yield Button("%", id="percent", variant="primary")
            yield Button("÷", id="divide", variant="warning")
            yield Button("7", id="number-7", classes="number")
            yield Button("8", id="number-8", classes="number")
            yield Button("9", id="number-9", classes="number")
            yield Button("*", id="multiply", variant="warning")
            yield Button("4", id="number-4", classes="number")
            yield Button("5", id="number-5", classes="number")
            yield Button("6", id="number-6", classes="number")
            yield Button("-", id="minus", variant="warning")
            yield Button("1", id="number-1", classes="number")
            yield Button("2", id="number-2", classes="number")
            yield Button("3", id="number-3", classes="number")
            yield Button("+", id="plus", variant="warning")
            yield Button("0", id="number-0", classes="number")
            yield Button(".", id="point")
            yield Button("=", id="equals", variant="warning")

    def on_key(self, event: events.Key) -> None:
        def press(button_id: str) -> None:
            try:
                self.query_one(f"#{button_id}", Button).press()
            except NoMatches:
                print("Unknow key pressed!")

        key = event.key
        if key.isdecimal():
            press(f"number-{key}")
        elif key == "c":
            press("c")
            press("ac")
        else:
            button_id = self.map_data.get(key)
            if button_id is not None:
                press(self.map_data.get(key, key))

    @on(Button.Pressed, ".number")
    def handle_number_pressed(self, event: Button.Pressed) -> None:
        if event.button.id is None:
            raise Exception("Unknow Event happend")
        number = event.button.id.partition("-")[-1]
        self.numbers = self.result = self.result.lstrip("0") + number

    @on(Button.Pressed, "#plus-minus")
    def handle_plus_minus_pressed(self) -> None:
        self.numbers = self.result = str(Decimal(self.result or "0") * -1)

    @on(Button.Pressed, "#point")
    def handle_pressed_point(self) -> None:
        if "." not in self.result:
            self.numbers = self.result = (self.result or "0") + "."

    @on(Button.Pressed, "#percent")
    def handle_percent_pressed(self) -> None:
        self.numbers = self.result = str(Decimal(self.result or "0") / Decimal(100))

    @on(Button.Pressed, "#ac")
    def handle_pressed_ac(self) -> None:
        self.result = ""
        self.left = self.right = Decimal(0)
        self.operator = "plus"
        self.numbers = "0"

    @on(Button.Pressed, "#c")
    def handle_pressed_c(self) -> None:
        self.result = ""
        self.numbers = "0"

    def calculate(self) -> None:
        try:
            match self.operator:
                case "plus":
                    self.left += self.right
                case "minus":
                    self.left -= self.right
                case "divide":
                    self.left /= self.right
                case "multiply":
                    self.left *= self.right
            self.numbers = str(self.left)
            self.result = ""
        except Exception:
            self.numbers = "Syntax Error"

    @on(Button.Pressed, "#plus,#minus,#divide,#multiply")
    def pressed_op(self, event: Button.Pressed) -> None:
        self.right = Decimal(self.result or "0")
        self.calculate()
        if event.button.id is None:
            raise Exception("Unknown Button Pressed!")
        self.operator = event.button.id

    @on(Button.Pressed, "#equals")
    def pressed_equals(self) -> None:
        if self.result:
            self.right = Decimal(self.result)
        self.calculate()


if __name__ == "__main__":
    app = CalculatorApp()
    app.run()
