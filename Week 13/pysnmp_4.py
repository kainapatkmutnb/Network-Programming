import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

# Asynchronous function to perform SNMP queries
async def run():
    # SNMP command to get the system description
    g = getCmd(
        SnmpEngine(),
        CommunityData('public'),
        await UdpTransportTarget.create(('192.168.1.124', 161)),
        ContextData(),
        ObjectType(ObjectIdentity('.1.3.6.1.2.1.1.1.0'))
    )

    # Fetch the response from the generator
    errorIndication, errorStatus, errorIndex, varBinds = await g

    # Check for errors and print out results
    if errorIndication:
        print(errorIndication)  # Print the error indication
    elif errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
        ))
    else:
        for varBind in varBinds:
            print('= '.join([x.prettyPrint() for x in varBind]))  # Print OID values

# Run the asynchronous function
asyncio.run(run())