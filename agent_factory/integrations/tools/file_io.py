"""File I/O tools for reading and writing files."""

from pathlib import Path
from agent_factory.core.tool import function_tool


@function_tool(
    name="read_file",
    description="Read contents of a file"
)
def read_file(file_path: str) -> str:
    """
    Read a file and return its contents.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File contents as string
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    return path.read_text()


@function_tool(
    name="write_file",
    description="Write content to a file"
)
def write_file(file_path: str, content: str) -> str:
    """
    Write content to a file.
    
    Args:
        file_path: Path to the file
        content: Content to write
        
    Returns:
        Success message
    """
    path = Path(file_path)
    
    # Create parent directories if needed
    path.parent.mkdir(parents=True, exist_ok=True)
    
    path.write_text(content)
    
    return f"Successfully wrote {len(content)} characters to {file_path}"


# Create tool instances
read_file_tool = read_file.tool if hasattr(read_file, 'tool') else None
write_file_tool = write_file.tool if hasattr(write_file, 'tool') else None
