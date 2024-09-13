"""
FreeGenius AI Plugin - create maps

Create maps

[FUNCTION_CALL]
"""

from freegenius import config, print3
from freegenius.utils.python_utils import PythonUtil
import re, os

def create_map(function_args):
    code = function_args.get("code") # required
    information = PythonUtil.showAndExecutePythonCode(code)
    htmlPattern = """\.save\(["']([^\(\)]+\.html)["']\)"""
    match = re.search(htmlPattern, code)
    if match:
        htmlFile = match.group(1)
        os.system(f"{config.open} {htmlFile}")
        print3(f"Saved: {htmlFile}")
        return ""
    elif information:
        return information
    return ""

functionSignature = {
    "examples": [
        "create map",
        "pin on map",
    ],
    "name": "create_map",
    "description": f'''Create maps''',
    "parameters": {
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "Generate python code that integrates packages 'folium' and 'geopy', when needed, to resolve my request. Created maps are saved in *.html file. Tell me the file path at the end.",
            },
        },
        "required": ["code"],
    },
}

config.addFunctionCall(signature=functionSignature, method=create_map)