from graph import graph

question = input("Enter your research question: ")

result = graph.invoke({
    "question": question,
    "intent": "",
    "plan": "",
    "search_query": "",
    "papers": [],
    "filtered_papers": [],
    "report": ""
})

print(result["report"])