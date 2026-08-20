use rmcp::{
    ServiceExt, handler::server::wrapper::Parameters, schemars, tool, tool_router, transport::stdio,
};
use rusqlite::Connection;
use serde::Deserialize;

#[derive(Debug, Deserialize, schemars::JsonSchema)]
struct EchoParams {
    message: String,
}

#[derive(Clone)]
struct Probe;

#[tool_router(server_handler)]
impl Probe {
    #[tool(description = "Return the supplied message")]
    fn echo(&self, Parameters(EchoParams { message }): Parameters<EchoParams>) -> String {
        message
    }
}

fn check_fts5() -> Result<(), Box<dyn std::error::Error>> {
    let connection = Connection::open_in_memory()?;
    connection.execute_batch("CREATE VIRTUAL TABLE notes USING fts5(body);")?;
    connection.execute(
        "INSERT INTO notes(body) VALUES (?1)",
        ["geness controller runtime"],
    )?;
    let count: i64 = connection.query_row(
        "SELECT count(*) FROM notes WHERE notes MATCH ?1",
        ["controller"],
        |row| row.get(0),
    )?;
    if count != 1 {
        return Err(format!("unexpected FTS5 result: {count}").into());
    }
    Ok(())
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    check_fts5()?;
    let service = Probe.serve(stdio()).await?;
    service.waiting().await?;
    Ok(())
}
