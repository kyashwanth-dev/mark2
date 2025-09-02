from components import Terminal, Battery, Resistor, LED, DigPhotoSensor, Printr, Switch, ConnectSingle

# Create terminals
bat1 = Terminal("bat1", "ntr", "pos")
bat2 = Terminal("bat2", "ntr", "neg")
switchIn = Terminal("switchIn", "male", "pos")
switchOut = Terminal("switchOut", "female", "zero")
res1 = Terminal("res1", "ntr", "zero")
res2 = Terminal("res2", "ntr", "zero")
ter1 = Terminal("ter1", "male", "pos")
ter2 = Terminal("ter2", "male", "neg")
sensorOut = Terminal("sensorOut", "male", "out")
printerIn = Terminal("printerIn", "female", "zero")

# Create components
powerA = Battery("powerA", 3, bat1, bat2)
sw = Switch("sw1", switchIn, switchOut, default_state="OFF")
r = Resistor("R1", res1, res2, base_resistance=100, multiplier=0, current_mA=10)
bulb = LED("bulb", ter1, ter2, "red", voltage_drop=2)
bulbSensor = DigPhotoSensor("bulbSensor", bulb, sensorOut)
print1 = Printr("print1", printerIn, ("LED is ON", "LED is OFF"))

# Connect terminals
ConnectSingle("con1a", bat1, switchIn)       # Battery → Switch
ConnectSingle("con1b", switchOut, res1)      # Switch → Resistor
ConnectSingle("con2", res2, ter1)            # Resistor → LED
ConnectSingle("con5", ter2, bat2)            # LED → Battery negative terminal
ConnectSingle("con4", sensorOut, printerIn)  # Sensor → Printer

# === First Run: Switch is OFF ===
print("\n--- First Run: Switch OFF ---")
print(sw.evaluate())
print(r.evaluate())
print(bulb.evaluate())
print(bulbSensor.evaluate())
print1.evaluate()
powerA.setDaata()

# === Toggle Switch ON ===
sw.toggle()

# === Second Run: Switch is ON ===
print("\n--- Second Run: Switch ON ---")
print(sw.evaluate())
print(r.evaluate())
print(bulb.evaluate())
print(bulbSensor.evaluate())
print1.evaluate()
powerA.setDaata()
