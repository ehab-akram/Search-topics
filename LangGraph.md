# Introduction

## Why we use it 

Building applications with large language models (LLMs) offers exciting opportunities to create sophisticated, interactive systems. But as these applications grow in complexity, especially those involving **multiple LLMs** working in concert, new challenges arise. **How do we manage the flow of information between these agents?**

**LangGraph** a powerful library within the LangChain ecosystem, provides an elegant solution for **building and managing multi-agent** LLM applications. It ensures **smooth communication** and **efficient execution** of complex tasks.

## Graph Structures

This graph comprises two primary elements:

- **Nodes** (**The Building Blocks of Work**): represents a distinct unit of work or action within the application. (e.g. Direct communication with an LLM **text generation**, etc.)

- **Edges** (**Guiding the Flow of Information and Control**): connective tissue within a LangGraph, establishing pathways for information flow and dictating the sequence of operations.

LangGraph supports multiple edge types:

- **Simple Edges**: These denote a **direct** and **unconditional** flow from one node to another. The output of the first node is fed as input to the subsequent node, creating a linear progression.

- **Conditional Edges**: Introducing a layer of **dynamism**, **conditional** edges enable the workflow to branch based on the outcome of a specific node's operation.

## State Management

- A crucial aspect of managing multi-agent systems is ensuring that all agents operate with a **shared understanding of the current state of the task**.

- This state object acts as a **repository** for critical information that needs to be accessible across different points in the workflow. This might include:
  - **Conversation History**
  - **Contextual Data**
  - **Internal Variables**

# Basic LangGraph 

1. **Define the State Structure**

```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class State(TypedDict):
    # 'messages' will store the chatbot conversation history.
    # The 'add_messages' function ensures new messages are appended to the list.
    messages: Annotated[list, add_messages]


# Create an instance of the StateGraph, passing in the State class
graph_builder = StateGraph(State)
```

- **TypedDict**: used to define dictionaries with specific key-value types in Python's type hinting system.
- **Annotated**: is used to add metadata to type hints.
- **START**: A predefined constant representing the entry point of the graph.
- **END**: A predefined constant representing the exit point of the graph.
- **StateGraph**: is a class from the langgraph library, which is used to define **stateful, multi-step workflows** for AI agents.

2. **Create the Chatbot Node**

```python
def chatbot(state: State):
    # Use the LLM to generate a response based on the current conversation history.
    response = llm.invoke(state["messages"])
    
    # Return the updated state with the new message appended
    return {"messages": [response]}

# Add the 'chatbot' node to the graph,
graph_builder.add_node("chatbot", chatbot)
```

3. **Define Entry and Finish Points**

```python
# For this basic chatbot, the 'chatbot' node is both the entry and finish point
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
```

4. **Compile the Graph**

```python
graph = graph_builder.compile()
```

5. **Visualize the Graph**

```python
from IPython.display import Image, display

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass
```

6. **Run the Chatbot**

```python
while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    
    # Process user input through the LangGraph
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)
```

# Advanced LangGraph

```python
#pip install -U tavily-python langchain_community
from typing import Annotated
from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)


tool = TavilySearchResults(max_results=2)
tools = [tool]
llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")
llm_with_tools = llm.bind_tools(tools)


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=[tool])
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")
graph = graph_builder.compile()
```

- **ToolNode**: This is a node in the graph that represents a **tool** or **action** that can be executed. specifically refers to nodes that are responsible for **invoking** tools or functions.
- **tools_condition**: a mechanism for setting conditions on when a particular tool or action should be executed.

# Adding Memory

**LangGraph's Checkpointing System:**

1. **Checkpointer:** This object is responsible for saving the state of the graph at different points in time.

2. **Thread ID:** Each time you invoke your graph, you provide a thread_id. This ID is used by the checkpointer to keep track of different conversation threads.

- LangGraph **automatically** saves the state after each step of the graph's execution for a given **thread_id**. When you invoke the graph again with the same thread_id, it automatically loads the saved state, enabling the chatbot to continue the conversation where it left off.

```python
# ... (Previous code to define State, graph_builder, nodes, and edges)

from langgraph.checkpoint.memory import MemorySaver

# Create a MemorySaver object to act as the checkpointer
memory = MemorySaver()

# Compile the graph, passing in the 'memory' object as the checkpointer
graph = graph_builder.compile(checkpointer=memory)

# ... (Rest of the code to run the chatbot)
```

# Human in the Loop

- Human-in-the-loop workflows are essential for situations where you want to incorporate human **oversight**, **verification**, or **decision-making** within your AI application.

- The below code illustrates human-in-the-loop implementation using LangGraph's **interrupt_before** or **interrupt_after** functionality. Here's a breakdown:

```python
graph = graph_builder.compile(
    checkpointer=memory,
    # This is new!
    interrupt_before=["tools"],
    # Note: can also interrupt _after_ actions, if desired.
    # interrupt_after=["tools"]
)
```

# Resources
- https://blog.futuresmart.ai/langgraph-tutorial-for-beginners#heading-understanding-langgraph
- https://langchain-ai.github.io/langgraph/tutorials/introduction/