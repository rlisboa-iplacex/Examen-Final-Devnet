from ncclient import manager

# Conexión NETCONF con el router CSR1kv
m = manager.connect(
    host="10.0.0.106",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
)

# Configuración NETCONF para cambiar el hostname
netconf_hostname = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>Raimundo-Lisboa</hostname>
  </native>
</config>
"""

print("Cambiando hostname a 'Raimundo-Lisboa'...")
response = m.edit_config(target="running", config=netconf_hostname)
print(response)

# Configuración NETCONF para crear Loopback 11
netconf_loopback = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>11</name>
        <ip>
          <address>
            <primary>
              <address>11.11.11.11</address>
              <mask>255.255.255.255</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>
"""

print("Creando Loopback 11 con IP 11.11.11.11/32...")
response = m.edit_config(target="running", config=netconf_loopback)
print(response)

