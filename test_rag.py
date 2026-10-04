from app.rag import search_knowledge_base

result = search_knowledge_base("What is your return policy?")
print("RETRIEVED CONTEXT:\n", result)

result2 = search_knowledge_base("Do you ship internationally?")
print("\nRETRIEVED CONTEXT:\n", result2)