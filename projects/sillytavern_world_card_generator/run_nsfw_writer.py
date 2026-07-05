
import asyncio
from langchain_core.messages import HumanMessage
from src.factory.workflows.nsfw_writing import create_nsfw_writing_workflow

async def main():
    """
    Main function to run the NSFW writing workflow.
    """
    app = create_nsfw_writing_workflow()

    # The initial user prompt that starts the story
    initial_prompt = "A lonely nun in a desolate, forgotten monastery."

    inputs = {"messages": [HumanMessage(content=initial_prompt)]}
    
    # The workflow will now run, with each agent building on the last.
    # The final output will be from the 'director' node.
    async for output in app.astream(inputs):
        # astream() yields intermediate outputs. We just want the final one.
        for key, value in output.items():
            print(f"Output from node '{key}':")
            print("---")
            print(value["messages"][-1])
        print("\n---\n")

if __name__ == "__main__":
    asyncio.run(main())
