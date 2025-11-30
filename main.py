from components import Terminal, Battery, Resistor, LED, DigPhotoSensor, Printr, Switch, ConnectSingle,Diode
import digitalComponents

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
d1=Terminal("d1", "ntr", "zero")
d2=Terminal("d2", "ntr", "zero")
ip1=Terminal("ip1", "ntr", "in")
ip2=Terminal("ip2", "ntr", "in")
op1=Terminal("op1", "ntr", "out")
dgpower=Terminal("dgpower", "ntr", "pos")
dggnd=Terminal("dggnd", "ntr", "neg")

# Create components
powerA = Battery("powerA", 3.3, bat1, bat2)
sw = Switch("sw1", switchIn, switchOut,default_state="ON")
r = Resistor("R1", res1, res2, base_resistance=100, multiplier=0, current_mA=10)
bulb = LED("bulb", ter1, ter2, "red", voltage_drop=2)
bulbSensor = DigPhotoSensor("bulbSensor", bulb, sensorOut)
print1 = Printr("print1", printerIn, ("Output HIGH", "Output LOW"))
diode1 = Diode("diode1", d1, d2)
digitalPower = digitalComponents.DigitalPower("digitalPower", dgpower, high_level=True)
digitalGnd = digitalComponents.DigitalPower("digitalGnd", dggnd, high_level=False)
xor_gate = digitalComponents.XORGate("xor1", [ip1, ip2], op1)



# Additional connections for AND gate test
ConnectSingle("con6", dggnd, ip1)  # Battery positive to AND gate
ConnectSingle("con7", dgpower, ip2)  # Battery positive to AND gate
ConnectSingle("con8", op1, printerIn) 
# AND gate output to Printer

digitalPower.drive()
digitalGnd.drive()

print("\n--- XOR Gate running test ---")
xor_gate.evaluate()
print1.evaluate()