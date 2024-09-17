from duckduckgo_search import DDGS

def web_search(query, max_results):
    results = DDGS().text(query, max_results=max_results)
    results = "\n"+"\n\n".join([f"""<observation>\n<title>{res["title"]}</title>\n<content>{res["body"]}</content>\n</observation>""" for res in results])
    return results