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
                return f"Data sent from {self.label} to {other_terminal.label}: {dataValue}"
            elif self.dataAnt=="in":
                self.passed = dataValue
                return f"Data received at {self.label} from {other_terminal.label}: {dataValue}"
        return f"No data sent from {self.label} to {other_terminal.label}."

    def __str__(self):
        connected_labels = [t.label for t in self.connected_to]
        return f"{self.label} ({self.type}, {self.nature}) connected terminals: {connected_labels}"
    
class LED:
    def __init__(self, name, pos_terminal, neg_terminal):
        self.name = name
        self.terminals = {
            "positive": pos_terminal,
            "negative": neg_terminal
        }
    def __str__(self):
        return (f"LED created !!\n name={self.name}, "
                f"{self.terminals['positive']}, "
                f"{self.terminals['negative']}")
ter1 = Terminal("ter1", "male", "pos")
ter2 = Terminal("ter2", "male", "neg")

bulb = LED("bulb", ter1, ter2)
# print(bulb)

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
    def setDaata(self):
        pos_terminal = self.terminals["positive"]
        for connected_terminal in pos_terminal.connected_to:
            result = pos_terminal.data_settr(connected_terminal, self.voltage)
            print(result)


    def __str__(self):
        return (f"Battery created !!\n name={self.name},  voltage={self.voltage}V "
                f"{self.terminals['positive']}, "
                f"{self.terminals['negative']}")
bat1 = Terminal("bat1", "ntr", "pos")
bat2 = Terminal("bat2", "ntr", "neg")

powerA = Battery("powerA",5, bat1, bat2)
print(powerA)

class Resistor:
    def __init__(self, name, terminal1, terminal2):
        self.name = name
        self.terminals = [terminal1, terminal2]

    def __str__(self):
        t1, t2 = self.terminals
        return f"Resistor created !!\nname={self.name}, terminals=[{t1}, {t2}]"

res1 = Terminal("res1", "ntr", "zero")
res2 = Terminal("res2", "ntr", "zero")
r = Resistor("r", res1, res2)
print(r)

class ConnectSingle:
    def __init__(self, name, source_terminal, target_terminal):
        self.name = name
        self.source = source_terminal
        self.target = target_terminal
        self._connect_terminals()  # Automatically connect on creation

    def _connect_terminals(self):
        self.source.connect(self.target)

    def __str__(self):
        return f"Single Connection: \n name={self.name}, {self.source} → {self.target})"

con1 = ConnectSingle("con1", ter1, res1)
con2 = ConnectSingle("con2", res2, bat1)
con3 = ConnectSingle("con3", bat2, ter2)
print(con1)
print(con2)
print(con3)

class DigPhotoSensor:
    def __init__(self, name, paired_component, output_terminal):
        self.name = name
        self.paired_to = paired_component
        self.output = output_terminal

    def __str__(self):
        return (f"DigPhotoSensor created !!\n name={self.name}, "
                f"paired_to={self.paired_to}, "
                f"output={self.output}")
sensorOut = Terminal("sensorOut", "male", "out")
bulbSensor = DigPhotoSensor("bulbSensor", "bulb", sensorOut)
# print(bulbSensor)

class Printr:
    def __init__(self, name, attached_to, messages):
        self.name = name
        self.attached_to = attached_to  # e.g., "sensorOut"
        self.messages = messages        # Tuple: (on_message, off_message)

    def evaluate(self, signal):
        """Simulate printing based on digital signal (True/False)."""
        if signal:
            print(self.messages[0])
        else:
            print(self.messages[1])

    def __str__(self):
        return (f"Printr attached !! \n name={self.name}, attached_to={self.attached_to}, "
                f"messages={self.messages}")
    
print1 = Printr("print1", "sensorOut", ("LED is ON", "LED is OFF"))

# print(print1)

# Simulate signal from sensor
# print1.evaluate(True)   # Output: LED is ON

# print1.evaluate(False)  # Output: LED is OFF

class Switch:
    def __init__(self, name, input_terminal, output_terminal, default_state="OFF"):
        self.name = name
        self.input = input_terminal
        self.output = output_terminal
        self.default_state = default_state.upper()
        self.current_state = self.default_state  # Initial state matches default

    def toggle(self):
        # Flip the current state
        self.current_state = "OFF" if self.current_state == "ON" else "ON"

    def is_closed(self):
        # Return True only if current state is ON
        return self.current_state == "ON"

    def reset(self):
        # Restore to default state
        self.current_state = self.default_state

    def __str__(self):
        return (f"Switch created !!\n name={self.name}, default={self.default_state}, "
                f"current={self.current_state}, in={self.input}, out={self.output}")
sw = Switch("sw1", "switchIn", "switchOut", "OFF")
# print(sw)
# print(sw.is_closed())  # False (starts OFF)

# sw.toggle()
# print(sw.is_closed())  # True (now ON)

# sw.toggle()
# print(sw.is_closed())  # False (back to OFF)

# sw.reset()
# print(sw.is_closed())  # False (restored to default OFF)
powerA.setDaata()