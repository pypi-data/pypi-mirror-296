"""
SNMPv1
++++++

Send SNMP GET request using the following options:

  * with SNMPv1, community 'public'
  * over IPv4/UDP
  * to an Agent at demo.pysnmp.com:161
  * for an instance of SNMPv2-MIB::sysDescr.0 MIB object
  * Based on asyncio I/O framework

Functionally similar to:

| $ snmpgetnext -v1 -c public demo.pysnmp.com SNMPv2-MIB::sysDescr.0

"""  #
import pytest
from pysnmp.hlapi.v3arch.asyncio import *
from pysnmp.smi import builder, compiler, view
from tests.agent_context import AGENT_PORT, AgentContextManager


@pytest.mark.asyncio
async def test_v1_next():
    # Assemble MIB browser
    mibBuilder = builder.MibBuilder()
    mibViewController = view.MibViewController(mibBuilder)
    compiler.addMibCompiler(
        mibBuilder,
        sources=["file:///usr/share/snmp/mibs", "https://mibs.pysnmp.com/asn1/@mib@"],
    )

    # Pre-load MIB modules we expect to work with
    mibBuilder.loadModules("PYSNMP-MIB")

    async with AgentContextManager():
        with Slim(1) as slim:
            slim.snmpEngine.cache["mibViewController"] = mibViewController
            errorIndication, errorStatus, errorIndex, varBinds = await slim.next(
                "public",
                "localhost",
                AGENT_PORT,
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
            )

            assert errorIndication is None
            assert errorStatus == 0
            assert errorIndex == 0
            assert len(varBinds) == 1
            assert varBinds[0][0][0].prettyPrint() == "SNMPv2-MIB::sysObjectID.0"
            assert (
                varBinds[0][0][1].prettyPrint() == "PYSNMP-MIB::pysnmp"
            )  # IMPORTANT: MIB is needed to resolve this name
            # assert type(varBinds[0][0][1]).__name__ == "ObjectIdentifier"  # TODO: fix this
