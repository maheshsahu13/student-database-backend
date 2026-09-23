from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.ai.nodes import (
    classify_question,
    retrieve_students,
    generate_answer
)


class ChatState(TypedDict, total=False):
    question: str
    retrieval_type: str
    students: list
    semantic_students: list
    answer: str


workflow = StateGraph(ChatState)

workflow.add_node(
    "classify_question",
    classify_question
)

workflow.add_node(
    "retrieve_students",
    retrieve_students
)

workflow.add_node(
    "generate_answer",
    generate_answer
)

workflow.add_edge(
    START,
    "classify_question"
)

workflow.add_edge(
    "classify_question",
    "retrieve_students"
)

workflow.add_edge(
    "retrieve_students",
    "generate_answer"
)

workflow.add_edge(
    "generate_answer",
    END
)

chat_graph = workflow.compile()