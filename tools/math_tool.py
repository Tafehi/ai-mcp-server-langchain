# ## local math calculations

import mcp
import math
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("math")
# class MathTool:
#     """
#     A tool for performing basic math calculations.
#     """

#     def __init__(self, a: float, b: float):
#         """Initialize the MathTool."""
#         self.a = a
#         self.b = b


@mcp.tool()
def add(a: float, b: float) -> float:
    """Returns the sum of two numbers."""
    print(f"Server received add request: {a}, {b}")
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Returns the difference of two numbers."""
    print(f"Server received subtract request: {a}, {b}")
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Returns the multiply of two numbers."""
    print(f"Server received multiply request: {a}, {b}")
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Returns the dividing of two numbers."""
    print(f"Server received divide request: {a}, {b}")
    if b != 0:
        return a / b
    return math.nan


@mcp.tool()
def sine(a: float) -> float:
    """Returns the sine of a number."""
    print(f"Server received sine request: {a}")
    return math.sin(a)


if __name__ == "__main__":
    mcp.run(transport="stdio")
