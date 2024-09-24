import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

async def run():
    system_up_time_oid = ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0'))
    cisco_contact_info_oid = ObjectType(ObjectIdentity('1.3.6.1.4.1.9.2.1.61.0'))

    errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
        SnmpEngine(),
        CommunityData('public'),
        await UdpTransportTarget.create(('192.168.1.124', 161)),
        ContextData(),
        system_up_time_oid,
        cisco_contact_info_oid
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
        ))
    else:
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), str(val)))

# Run the async function
asyncio.run(run())