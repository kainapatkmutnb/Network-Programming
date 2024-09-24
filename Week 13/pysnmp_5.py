import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

communityName = 'public'
ipAddress = '192.168.1.124'
OID = '1.3.6.1.2.1.1.1.0'

async def snmp_get():
    # SNMP GET command using asyncio
    errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
        SnmpEngine(),
        CommunityData(communityName),
        UdpTransportTarget((ipAddress, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(OID))
    )

    # Check for errors and print out results
    if errorIndication:
        print(errorIndication)  # Print error indication if exists
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            print(' = '.join([x.prettyPrint() for x in varBind]))  # Print variable bindings

# Run the async function
asyncio.run(snmp_get())