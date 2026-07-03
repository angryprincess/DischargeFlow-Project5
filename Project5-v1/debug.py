import asyncio
import sys
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession

async def debug_agent():
    python_exe = sys.executable
    ehr_params = StdioServerParameters(command=python_exe, args=["ehr_server.py"])
    
    async with stdio_client(ehr_params) as (ehr_read, ehr_write):
        async with ClientSession(ehr_read, ehr_write) as ehr_session:
            await ehr_session.initialize()
            
            meds_result = await ehr_session.call_tool("get_medication_list", arguments={"patient_id": "P-1007", "context_role": "discharge"})
            raw_text = meds_result.content[0].text
            print("RAW_TEXT TYPE:", type(raw_text))
            print("RAW_TEXT:", repr(raw_text))

if __name__ == "__main__":
    asyncio.run(debug_agent())
