import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
import datetime

# Asynchronous function to run SNMP queries
async def run():
    host = '192.168.1.124'
    community = 'public'

    # Define SNMP OIDs for system name and interface statistics
    system_name_oid = ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0'))
    gig0_0_in_oct_oid = ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.10.1'))
    gig0_0_in_uPackets_oid = ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.11.1'))
    gig0_0_out_oct_oid = ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.16.1'))
    gig0_0_out_uPackets_oid = ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.17.1'))

    # Function to perform SNMP query
    async def snmp_query(host, community, oid):
        errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
            SnmpEngine(),
            CommunityData(community),
            await UdpTransportTarget.create((host, 161)),  # Target IP address and port
            ContextData(),
            oid
        )

        # Check for errors and print out results
        if errorIndication:
            print(errorIndication)  # Print error indication if any
            return None
        elif errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),  # Print error status
                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
            ))
            return None
        else:
            for name, val in varBinds:
                return str(val)  # Return the value of the OID

    # Store results in a dictionary
    result = {}
    result['Time'] = datetime.datetime.utcnow().isoformat()
    result['hostname'] = await snmp_query(host, community, system_name_oid)
    result['Gig0-0_In_Octet'] = await snmp_query(host, community, gig0_0_in_oct_oid)
    result['Gig0-0_In_uPackets'] = await snmp_query(host, community, gig0_0_in_uPackets_oid)
    result['Gig0-0_Out_Octet'] = await snmp_query(host, community, gig0_0_out_oct_oid)
    result['Gig0-0_Out_uPackets'] = await snmp_query(host, community, gig0_0_out_uPackets_oid)

    # Write results to a file
    with open(r'C:\Users\Kainapxt\Desktop\Network-Programming\Week 13\result1.txt', 'a') as f:
        f.write(str(result))
        f.write('\n')

# Run the async function
asyncio.run(run())