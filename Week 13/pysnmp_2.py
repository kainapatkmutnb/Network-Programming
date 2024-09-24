import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

# Asynchronous function to perform SNMP queries
async def run():
    # SNMP target host and community
    host = '192.168.1.124'
    community = 'public'
    
    # Define SNMP OIDs for system name and uptime
    system_name_oid = ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0'))
    system_uptime_oid = ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0'))

    # SNMP command to get system name and uptime
    errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
        SnmpEngine(),
        CommunityData(community),
        await UdpTransportTarget.create((host, 161)),  # Specify host and port
        ContextData(),
        system_name_oid,
        system_uptime_oid
    )

    # Check for errors and print out results
    if errorIndication:
        print(errorIndication)  # Print the error indication
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
            ))
        else:
            for name, val in varBinds:
                print('%s = %s' % (name.prettyPrint(), str(val)))  # Print OID values

# Run the async function
asyncio.run(run())