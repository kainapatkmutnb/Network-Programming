import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

# Asynchronous function to run SNMP get command
async def run():
    # Define SNMP OIDs for system name and uptime
    system_name_oid = ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0'))
    system_uptime_oid = ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0'))

    # Perform the SNMP get command asynchronously
    errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
        SnmpEngine(),
        CommunityData('public'),
        await UdpTransportTarget.create(('192.168.1.124', 161)),  # Target IP address and port
        ContextData(),
        system_name_oid,
        system_uptime_oid
    )

    # Check for errors and print the results
    if errorIndication:
        print(errorIndication)  # Print error indication if any
    elif errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),  # Print error status
            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
        ))
    else:
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), str(val)))  # Print the variable bindings

# Run the async function
asyncio.run(run())