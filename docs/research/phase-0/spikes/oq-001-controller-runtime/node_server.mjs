import { DatabaseSync } from "node:sqlite";

import { McpServer } from "@modelcontextprotocol/server";
import { serveStdio } from "@modelcontextprotocol/server/stdio";
import * as z from "zod/v4";


function checkFts5() {
  const database = new DatabaseSync(":memory:");
  database.exec("CREATE VIRTUAL TABLE notes USING fts5(body)");
  const insert = database.prepare("INSERT INTO notes(body) VALUES (?)");
  insert.run("geness controller runtime");
  const row = database.prepare("SELECT count(*) AS count FROM notes WHERE notes MATCH ?").get("controller");
  if (row.count !== 1) throw new Error(`unexpected FTS5 result: ${row.count}`);
  database.close();
}


function createServer() {
  checkFts5();
  const server = new McpServer({ name: "geness-oq001-node", version: "0.1.0" });
  server.registerTool(
    "echo",
    { description: "Return the supplied message", inputSchema: z.object({ message: z.string() }) },
    async ({ message }) => ({ content: [{ type: "text", text: message ?? "" }] }),
  );
  return server;
}


void serveStdio(createServer);
