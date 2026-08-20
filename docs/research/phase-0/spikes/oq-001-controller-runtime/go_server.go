package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"

	_ "github.com/mattn/go-sqlite3"
	"github.com/modelcontextprotocol/go-sdk/mcp"
)

type echoInput struct {
	Message string `json:"message" jsonschema:"the message to echo"`
}

type echoOutput struct {
	Message string `json:"message"`
}

func checkFTS5() error {
	database, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		return err
	}
	defer database.Close()
	if _, err := database.Exec("CREATE VIRTUAL TABLE notes USING fts5(body)"); err != nil {
		return err
	}
	if _, err := database.Exec("INSERT INTO notes(body) VALUES (?)", "geness controller runtime"); err != nil {
		return err
	}
	var count int
	if err := database.QueryRow("SELECT count(*) FROM notes WHERE notes MATCH ?", "controller").Scan(&count); err != nil {
		return err
	}
	if count != 1 {
		return fmt.Errorf("unexpected FTS5 result: %d", count)
	}
	return nil
}

func echo(_ context.Context, _ *mcp.CallToolRequest, input echoInput) (*mcp.CallToolResult, echoOutput, error) {
	return nil, echoOutput{Message: input.Message}, nil
}

func main() {
	if err := checkFTS5(); err != nil {
		log.Fatal(err)
	}
	server := mcp.NewServer(&mcp.Implementation{Name: "geness-oq001-go", Version: "0.1.0"}, nil)
	mcp.AddTool(server, &mcp.Tool{Name: "echo", Description: "Return the supplied message"}, echo)
	if err := server.Run(context.Background(), &mcp.StdioTransport{}); err != nil {
		log.Fatal(err)
	}
}
