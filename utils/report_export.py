import json
import datetime
from typing import Any, Union, Optional, Dict


def export_report(
    data: Union[Dict[str, Any], Any],
    filename: str = "report.txt",
    title: Optional[str] = None,
    include_timestamp: bool = True,
    encoding: str = "utf-8"
) -> str:
    """
    Export a plain text report with optional title and timestamp.

    Args:
        data: The report data (dict or any serializable object).
        filename: Output file name.
        title: Optional report title.
        include_timestamp: Whether to include timestamp in header.
        encoding: File encoding.

    Returns:
        Status message.
    """
    header = []
    if title:
        header.append(title)
    else:
        header.append("FortiShell Pro Report")
    if include_timestamp:
        header.append(str(datetime.datetime.now()))
    try:
        with open(filename, "w", encoding=encoding) as f:
            f.write(" - ".join(header) + "\n\n")
            if isinstance(data, dict):
                for key, value in data.items():
                    f.write(f"{key}:\n")
                    if isinstance(value, list):
                        for item in value:
                            f.write(f"  - {item}\n")
                    elif isinstance(value, dict):
                        for subkey, subval in value.items():
                            f.write(f"    {subkey}: {subval}\n")
                    else:
                        f.write(f"  {value}\n")
                    f.write("\n")
            else:
                f.write(str(data))
        return f"Exported TXT to {filename} ✅"
    except Exception as e:
        return f"Failed to export TXT: {e}"


def export_json(
    data: Any,
    filename: str = "report.json",
    encoding: str = "utf-8",
    sort_keys: bool = True,
    ensure_ascii: bool = False
) -> str:
    """
    Export data as JSON with advanced options.

    Args:
        data: The data to export.
        filename: Output file name.
        encoding: File encoding.
        sort_keys: Sort keys in output.
        ensure_ascii: Escape non-ASCII chars.

    Returns:
        Status message.
    """
    try:
        with open(filename, "w", encoding=encoding) as f:
            json.dump(data, f, indent=2, sort_keys=sort_keys, ensure_ascii=ensure_ascii)
        return f"Exported JSON to {filename} ✅"
    except Exception as e:
        return f"Failed to export JSON: {e}"
