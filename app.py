from fastapi import FastAPI
from pydantic import BaseModel
from agent.agentic_workflow import GraphBuilder
from fastapi.responses import JSONResponse
import os

# Initialize the FastAPI app (This was implied but not visible in the screenshot)
app = FastAPI()

# Define the request model
class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        print(query)
        
        # Initialize the graph builder with the Groq model provider
        graph = GraphBuilder(model_provider="groq")
        react_app = graph()  # Compiling the graph
        
        # Generate and save the graph image (Mermaid PNG)
        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)
        
        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")

        # Prepare the input for the agent
        # Note: We use query.query because the class QueryRequest defined 'query', not 'question'
        messages = {"messages": [query.query]}
        
        # Run the agent
        output = react_app.invoke(messages)

        # Process the result
        # If the output is a dictionary with messages, get the last message content
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  # Last AI response
        else:
            final_output = str(output)

        # Return the final answer
        return {"answer": final_output}

    except Exception as e:
        # Return a 500 error if something goes wrong
        return JSONResponse(status_code=500, content={"error": str(e)})