# Programa que verifica una VLAN según su rango

vlan = int(input("Ingrese el número de la VLAN: "))

if 1 <= vlan <= 1005:
    print("La VLAN pertenece al rango NORMAL.")
elif 1006 <= vlan <= 4094:
    print("La VLAN pertenece al rango EXTENDIDO.")
else:
    print("El número ingresado NO corresponde a una VLAN válida.")
