from mcp.server.fastmcp import FastMCP
from brain_ask import ask_brain
import os

# Inicializar servidor MCP
mcp = FastMCP("IppSec-Brain")

@mcp.tool()
def ask_ippsec(question: str) -> str:
    """
    Ask IppSec a question about CTF, hacking techniques, or machine walkthroughs.
    Returns the top relevant excerpts from his videos with high precision (Re-ranked).
    Use this tool when you need expert advice on how to solve a specific hacking problem.
    """
    try:
        results = ask_brain(question, return_results=True)
        
        if not results:
            return "No information found in IppSec's knowledge base for this query."
            
        formatted_response = f"### IppSec's Wisdom on: '{question}'\n\n"
        for i, doc in enumerate(results):
            source = doc.metadata.get('source', 'Unknown Video')
            # Extract just the filename if it's a full path
            video_name = os.path.basename(source).replace('.txt', '')
            
            formatted_response += f"#### From Video: {video_name}\n"
            formatted_response += f"> {doc.page_content}\n\n"
            
        return formatted_response
    except Exception as e:
        return f"Error querying IppSec Brain: {str(e)}"

if __name__ == "__main__":
    print("[*] IppSec Brain MCP Server running...")
    mcp.run()
