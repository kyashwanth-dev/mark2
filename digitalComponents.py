class DigitalPower:
    """
    Simple digital rail that provides a constant HIGH or LOW boolean level.
    Call `drive()` to push the level onto all connected terminals.
    """
    def __init__(self, name, output_terminal, high_level=True):
        self.name = name
        self.output = output_terminal
        self.high_level = bool(high_level)
        self.state = "HIGH" if self.high_level else "LOW"
        self.output.dataAnt = "out"

    def set_level(self, high_level):
        self.high_level = bool(high_level)
        self.state = "HIGH" if self.high_level else "LOW"

    def drive(self):
        for terminal in self.output.connected_to:
            self.output.data_settr(terminal, self.high_level)
        return f"DigitalPower '{self.name}' drove {self.state}."

    def __str__(self):
        return f"DigitalPower(name={self.name}, state={self.state})"


class ORGate:
    def __init__(self, name, input_terminals, output_terminal):
        self.name = name
        self.inputs = list(input_terminals)
        self.output = output_terminal
        self.state = "OFF"
        for t in self.inputs:
            t.dataAnt = "in"
        self.output.dataAnt = "out"

    def _to_bool(self, v):
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return v != 0
        if isinstance(v, str):
            s = v.strip().lower()
            if s in ("true", "1", "on"):
                return True
            return False
        return False

    def evaluate(self):
        input_values = [t.passed for t in self.inputs]
        bools = [self._to_bool(val) for val in input_values]
        output_signal = any(bools)
        self.state = "ON" if output_signal else "OFF"
        for connected_terminal in self.output.connected_to:
            self.output.data_settr(connected_terminal, output_signal)
        return f"ORGate '{self.name}' evaluated: {self.state}."


class NOTGate:
    def __init__(self, name, input_terminal, output_terminal):
        self.name = name
        self.input = input_terminal
        self.output = output_terminal
        self.state = "OFF"
        self.input.dataAnt = "in"
        self.output.dataAnt = "out"

    def _to_bool(self, v):
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return v != 0
        if isinstance(v, str):
            s = v.strip().lower()
            if s in ("true", "1", "on"):
                return True
            return False
        return False

    def evaluate(self):
        signal = self._to_bool(self.input.passed)
        output_signal = not signal
        self.state = "ON" if output_signal else "OFF"
        for connected_terminal in self.output.connected_to:
            self.output.data_settr(connected_terminal, output_signal)
        return f"NOTGate '{self.name}' evaluated: {self.state}."


class XORGate:
    def __init__(self, name, input_terminals, output_terminal):
        self.name = name
        self.inputs = list(input_terminals)
        if len(self.inputs) != 2:
            raise ValueError("XORGate requires exactly two input terminals.")
        self.output = output_terminal
        self.state = "OFF"
        for t in self.inputs:
            t.dataAnt = "in"
        self.output.dataAnt = "out"

    def _to_bool(self, v):
        if isinstance(v, bool):
            return v
        if isinstance(v, (int, float)):
            return v != 0
        if isinstance(v, str):
            s = v.strip().lower()
            if s in ("true", "1", "on"):
                return True
            return False
        return False

    def evaluate(self):
        bools = [self._to_bool(t.passed) for t in self.inputs]
        output_signal = bools[0] ^ bools[1]
        self.state = "ON" if output_signal else "OFF"
        for connected_terminal in self.output.connected_to:
            self.output.data_settr(connected_terminal, output_signal)
        return f"XORGate '{self.name}' evaluated: {self.state}."