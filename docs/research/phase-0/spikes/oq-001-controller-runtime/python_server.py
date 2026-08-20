"""Disposable Python MCP/SQLite FTS5 server for OQ-001."""

import sqlite3

from mcp.server.mcpserver import MCPServer


def check_fts5() -> None:
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE VIRTUAL TABLE notes USING fts5(body)")
    connection.execute("INSERT INTO notes(body) VALUES (?)", ("geness controller runtime",))
    count = connection.execute(
        "SELECT count(*) FROM notes WHERE notes MATCH ?", ("controller",)
    ).fetchone()[0]
    if count != 1:
        raise RuntimeError(f"unexpected FTS5 result: {count}")
    connection.close()


server = MCPServer(name="geness-oq001-python", version="0.1.0")


@server.tool()
def echo(message: str) -> str:
    """Return the supplied message."""

    return message


if __name__ == "__main__":
    check_fts5()
    server.run(transport="stdio")
