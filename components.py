class Terminal:
    def __init__(self, label, type_, nature):
        self.label = label 
        self.type = type_      # 'male' or 'female'
        self.nature = nature   # 'pos', 'neg', or 'zero'
        self.connected_to=[]
        self.dataAnt = "None" # set 'in' for to act as receiver and 'out' for act as  transmitter
        self.passed = ""
    def connect(self, other_terminal):
        if other_terminal not in self.connected_to:
            self.connected_to.append(other_terminal)
        if self not in other_terminal.connected_to:
            other_terminal.connected_to.append(self)
    def data_settr(self,other_terminal,dataValue):
        if self.dataAnt!="None":
            if self.dataAnt=="out":
                other_terminal.passed = dataValue
                # return f"Data sent from {self.label} to {other_terminal.label}: {dataValue}"
            elif self.dataAnt=="in":
                self.passed = dataValue
                # return f"Data received at {self.label} from {other_terminal.label}: {dataValue}"
        # return f"No data sent from {self.label} to {other_terminal.label}."
    def __str__(self):
        connected_labels = [t.label for t in self.connected_to]
        return f"{self.label} ({self.type}, {self.nature}) connected terminals: {connected_labels}"
    
class LED:
    def __init__(self, name, pos_terminal, neg_terminal, color, voltage_drop=1):
        self.name = name
        self.terminals = {
            "positive": pos_terminal,
            "negative": neg_terminal
        }
        self.color = color
        self.voltage_drop = voltage_drop
        self.state = "OFF"
        # Assign terminal roles
        pos_terminal.dataAnt = "in"
        neg_terminal.dataAnt = "out"
    def evaluate(self):
        """Receive voltage at positive terminal, transmit reduced voltage from negative."""
        input_voltage = self.terminals["positive"].passed
        if isinstance(input_voltage, (int, float)) and input_voltage >= self.voltage_drop:
            self.state = "ON"
            output_voltage = input_voltage - self.voltage_drop
            results = []
            for connected_terminal in self.terminals["negative"].connected_to:
                result = self.terminals["negative"].data_settr(connected_terminal, output_voltage)
                results.append(result)
            return f"{self.color} LED '{self.name}' is ON.\n" #+ "\n".join(results)
        else:
            self.state = "OFF"
            self.terminals["negative"].data_settr(self.terminals["negative"].connected_to[0], "None")
            return f"{self.color} LED '{self.name}' is OFF. Insufficient voltage."

    def __str__(self):
        return (f"LED created !!\n name={self.name}, color={self.color}, "
                f"{self.terminals['positive']}, "
                f"{self.terminals['negative']}")

class Battery:
    def __init__(self, name, voltage, pos_terminal, neg_terminal):
        self.name = name
        self.voltage = voltage
        self.terminals = {
            "positive": pos_terminal,
            "negative": neg_terminal
        }
        pos_terminal.dataAnt="out"
        neg_terminal.dataAnt="in"
        # keep direct references for convenience
        self.pos_terminal = pos_terminal
        self.neg_terminal = neg_terminal

    def setDaata(self):
        # update stored references from terminals dict if needed
        self.pos_terminal = self.terminals["positive"]
        self.neg_terminal = self.terminals["negative"]

        for connected_terminal in self.pos_terminal.connected_to:
            self.pos_terminal.data_settr(connected_terminal, self.voltage)
    def checkClose(self):
        # Only suppress warning if return signal is exactly 0.0
        pos_terminal = self.pos_terminal
        neg_terminal = self.neg_terminal

        if not neg_terminal.connected_to or neg_terminal.passed != 0.0:
            print(f"⚠️ Circuit may be open or miswired. Battery negative terminal '{neg_terminal.label}' received: {neg_terminal.passed}")
        else:
            print(f"✅ Circuit properly closed. Return signal at '{neg_terminal.label}' is {neg_terminal.passed}V")


    def __str__(self):
        return (f"Battery created !!\n name={self.name},  voltage={self.voltage}V "
                f"{self.terminals['positive']}, "
                f"{self.terminals['negative']}")

class Resistor:
    def __init__(self, name, terminal1, terminal2, base_resistance=1.0, multiplier=0, current_mA=1.0):
        self.name = name
        self.terminals = [terminal1, terminal2]
        self.multiplier = multiplier
        self.base_resistance = base_resistance
        self.resistance = base_resistance * (10 ** multiplier)  # Ohms
        self.current_mA = current_mA  # milliamps
        self.state = "IDLE"
        terminal1.dataAnt = "in"
        terminal2.dataAnt = "out"
    def get_resistance_str(self):
        if self.multiplier == 6:
            return f"{self.base_resistance:.2f} MΩ"
        elif self.multiplier == 3:
            return f"{self.base_resistance:.2f} kΩ"
        else:
            return f"{self.base_resistance:.2f} Ω"
    def evaluate(self):
        input_voltage = self.terminals[0].passed
        current_A = self.current_mA / 1000.0
        voltage_drop = current_A * self.resistance
        if isinstance(input_voltage, (int, float)):
            output_voltage = input_voltage - voltage_drop
            if output_voltage > 0:
                self.state = "ACTIVE"
                results = []
                for connected_terminal in self.terminals[1].connected_to:
                    result = self.terminals[1].data_settr(connected_terminal, output_voltage)
                    results.append(result)
                return (f"Resistor '{self.name}' is ACTIVE. "
                        f"Voltage drop: {voltage_drop:.2f}V at {self.current_mA}mA\n" )#+
                        #"\n".join(results))
            else:
                self.state = "BLOCKED"
                self.terminals[1].data_settr(self.terminals[1].connected_to[0], "None")
                return (f"Resistor '{self.name}' BLOCKED. Input voltage too low "
                        f"for drop of {voltage_drop:.2f}V at {self.current_mA}mA.")
        else:
            self.state = "IDLE"
            self.terminals[1].data_settr(self.terminals[1].connected_to[0], "None")
            return f"Resistor '{self.name}' is IDLE. No input voltage."
    def __str__(self):
        t1, t2 = self.terminals
        return (f"Resistor created !!\nname={self.name}, resistance={self.get_resistance_str()}, "
                f"current={self.current_mA}mA, terminals=[{t1.label} (in), {t2.label} (out)]")

class ConnectSingle:
    def __init__(self, name, source_terminal, target_terminal):
        self.name = name
        self.source = source_terminal
        self.target = target_terminal
        self._connect_terminals()  # Automatically connect on creation
    def _connect_terminals(self):
        if self.source.dataAnt == "out" and self.target.dataAnt == "in":
            self.source.connect(self.target)
        else:
            print(f"Warning: {self.name} may be connecting terminals with mismatched roles.")
    def __str__(self):
        return (f"Single Connection:\n"
            f" name={self.name}\n"
            f" source={self.source.label} ({self.source.dataAnt}) → "
            f"target={self.target.label} ({self.target.dataAnt})")


class DigPhotoSensor:
    def __init__(self, name, paired_component, output_terminal):
        self.name = name
        self.paired_to = paired_component  # e.g., an LED object
        self.output = output_terminal      # Terminal object
        self.output.dataAnt = "out"        # Sensor transmits digital signal
    def evaluate(self):
        """Emit True if paired LED is ON, else False."""
        signal = True if getattr(self.paired_to, "state", "OFF") == "ON" else False
        results = []
        for connected_terminal in self.output.connected_to:
            result = self.output.data_settr(connected_terminal, signal)
            results.append(result)
        return f"Sensor '{self.name}' evaluated.\n" #+ "\n".join(results)
    def __str__(self):
        return (f"DigPhotoSensor created !!\n name={self.name}, "
                f"paired_to={self.paired_to.name}, "
                f"output={self.output.label}")

class Printr:
    def __init__(self, name, attached_terminal, messages):
        self.name = name
        self.attached_to = attached_terminal  # Terminal object
        self.attached_to.dataAnt = "in"       # Ensure it's a receiver
        self.messages = messages              # Tuple: (on_message, off_message)
    def evaluate(self):
        """Read signal from attached terminal and print message."""
        signal = self.attached_to.passed
        # Optional debug output
        #print(f"[{self.name}] Signal received at {self.attached_to.label}: {signal}")
        if signal is True:
            print(self.messages[0])
        elif signal is False:
            print(self.messages[1])
        else:
            print(f"[{self.name}] No valid signal received. Defaulting to OFF message.")
            print(self.messages[1])
    def __str__(self):
        return (f"Printr attached !!\n"
                f" name={self.name}, attached_to={self.attached_to.label}, "
                f"messages={self.messages}")

class Switch:
    def __init__(self, name, input_terminal, output_terminal, default_state="OFF"):
        self.name = name
        self.input = input_terminal
        self.output = output_terminal
        self.default_state = default_state.upper()
        self.current_state = self.default_state
        # Assign terminal roles
        self.input.dataAnt = "in"
        self.output.dataAnt = "out"
    def toggle(self):
        # Flip the current state
        self.current_state = "OFF" if self.current_state == "ON" else "ON"
    def is_closed(self):
        # Return True only if current state is ON
        return self.current_state == "ON"
    def reset(self):
        # Restore to default state
        self.current_state = self.default_state
    def evaluate(self):
        input_voltage = self.input.passed
        if self.is_closed():
            results = []
            for connected_terminal in self.output.connected_to:
                result = self.output.data_settr(connected_terminal, input_voltage)
                results.append(result)
            return f"Switch '{self.name}' is ON. Voltage passed: {input_voltage}V\n" #+ "\n".join(results)
        else:
            self.output.data_settr(self.output.connected_to[0], "None")
            return f"Switch '{self.name}' is OFF. No voltage passed."
    def __str__(self):
        return (f"Switch created !!\n name={self.name}, default={self.default_state}, "
                f"current={self.current_state}, in={self.input}, out={self.output}")


class Diode:
    def __init__(self, name, anode_terminal, cathode_terminal, forward_voltage=0.3):
        self.name = name
        self.terminals = {
            "anode": anode_terminal,
            "cathode": cathode_terminal
        }
        self.forward_voltage = forward_voltage
        self.state = "OFF"
        # Assign terminal roles: anode receives, cathode transmits
        anode_terminal.dataAnt = "in"
        cathode_terminal.dataAnt = "out"

    def evaluate(self):
        """Allow conduction only if anode voltage ≥ forward_voltage (simple model)."""
        input_voltage = self.terminals["anode"].passed
        # Try to coerce the passed value to a numeric voltage. Treat non-numeric values as no voltage.
        try:
            numeric_voltage = float(input_voltage)
        except (TypeError, ValueError):
            numeric_voltage = None

        if numeric_voltage is not None and numeric_voltage >= self.forward_voltage:
            self.state = "ON"
            output_voltage = numeric_voltage - self.forward_voltage
            for connected_terminal in self.terminals["cathode"].connected_to:
                self.terminals["cathode"].data_settr(connected_terminal, output_voltage)
            return f"Diode '{self.name}' is ON. Forward drop: {self.forward_voltage}V"
        else:
            self.state = "OFF"
            # If no conduction, ensure downstream sees "None" if possible
            if self.terminals["cathode"].connected_to:
                self.terminals["cathode"].data_settr(self.terminals["cathode"].connected_to[0], "None")
            return f"Diode '{self.name}' is OFF. Blocked or insufficient forward voltage."

    def __str__(self):
        return (f"Diode created !!\n name={self.name}, forward_voltage={self.forward_voltage}V, "
                f"anode={self.terminals['anode']}, cathode={self.terminals['cathode']}")



class ANDGate:
    def __init__(self, name, input_terminals, output_terminal):
                """
                input_terminals: iterable of Terminal objects
                output_terminal: Terminal object
                """
                self.name = name
                # normalize inputs to a list
                self.inputs = list(input_terminals)
                self.output = output_terminal
                self.state = "OFF"
                # assign terminal roles
                for t in self.inputs:
                    t.dataAnt = "in"
                self.output.dataAnt = "out"

    def _to_bool(self, v):
                """Coerce various passed values into a boolean signal."""
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
                """Evaluate digital AND: output True only if all inputs are True."""
                # Gather input signals
                input_values = [t.passed for t in self.inputs]
                bools = [self._to_bool(val) for val in input_values]

                # Determine gate output
                output_signal = all(bools)
                self.state = "ON" if output_signal else "OFF"

                # Propagate to connected terminals (if any)
                for connected_terminal in self.output.connected_to:
                    self.output.data_settr(connected_terminal, output_signal)

                return f"ANDGate '{self.name}' evaluated: {self.state}."
        
    def __str__(self):
                input_labels = [t.label for t in self.inputs]
                return (f"ANDGate created !!\n name={self.name}, inputs={input_labels}, "
                        f"output={self.output.label}, current_state={self.state}")


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