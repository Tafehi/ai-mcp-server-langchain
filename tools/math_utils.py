# ## local math calculations

import mcp
import math


class MathTool:
    """
    A tool for performing basic math calculations.
    """

    def __init__(self, a: float, b: float):
        """Initialize the MathTool."""
        self.a = a
        self.b = b

    @mcp.Tool()
    def add(self) -> float:
        """Returns the sum of two numbers."""
        print(f"Server received add request: {self.a}, {self.b}")
        return self.a + self.b

    @mcp.Tool()
    def subtract(self) -> float:
        """Returns the difference of two numbers."""
        print(f"Server received subtract request: {self.a}, {self.b}")
        return self.a - self.b

    @mcp.Tool()
    def multiply(self) -> float:
        """Returns the product of two numbers."""
        print(f"Server received multiply request: {self.a}, {self.b}")
        return self.a * self.b

    @mcp.Tool()
    def divide(self) -> float:
        """Returns the quotient of two numbers."""
        print(f"Server received divide request: {self.a}, {self.b}")
        if self.b != 0:
            return self.a / self.b
        return math.nan

    @mcp.Tool()
    def sine(self) -> float:
        print(f"Server received sine request: {self.a}")
        return math.sin(self.a)
