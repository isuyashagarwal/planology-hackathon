import google.generativeai as genai
gemini_api_key = '<YOUR API KEY>'
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-pro')

def clarify_idea(idea):
    chat = model.start_chat(history=[])
    prompt = f"Clearly define my idea in one line. {idea}"
    base_idea = chat.send_message(prompt)
    base_idea = base_idea.text
    detailed_idea = chat.send_message("In 2 lines, describe this idea in detail without using markdown.")
    detailed_idea = detailed_idea.text
    return base_idea,detailed_idea

def genai_problem_statement(one_line_idea):
    response = model.generate_content(f"Based on the idea {one_line_idea}, clearly define the problem this idea is solving. Do not use markdown.")
    return response.text

def genai_target_audience(one_line_idea):
    response = model.generate_content(f"Based on the idea {one_line_idea}, in bullet points, describe the target audience. Do not use markdown.")
    print(response.text)
    return response.text

def genai_market_analysis(one_line_idea):
    response = model.generate_content(f"Based on the idea {one_line_idea}, in bullet points, describe the market size. Do not use markdown.")
    print(response.text)
    return response.text

def genai_competitors(detailed_idea):
    response = model.generate_content(f"Based on the idea {detailed_idea}, in bullet points, list down the competitors. Do not use markdown.")
    return response.text

def genai_pricing_strategy(detailed_idea,market_size):
    response = model.generate_content(f"Based on the idea {detailed_idea} and market size {market_size}, create a pricing strategy. Do not use markdown.")
    print(response.text)
    return response.text

def genai_value_proposition(detailed_idea):
    response = model.generate_content(f"Based on the idea {detailed_idea}, create a value proposition. Do not use markdown.")
    print(response.text)
    return response.text

def genai_gtm(detailed_idea,pricing_strategy,target_audience):
    response = model.generate_content(f"Based on the idea {detailed_idea}, pricing strategy {pricing_strategy} and target audience {target_audience}, create a go to market strategy. Do not use markdown.")
    print(response.text)
    return response.text

def genai_tech_stack(detailed_idea):
    response = model.generate_content(f"Based on the idea\nIdea:{detailed_idea}\nSuggest the tech stack that should be used for this project. Do not use markdown.")
    print(response.text)
    return response.text

def genai_roadmap(detailed_idea,value_proposition):
    response = model.generate_content(f"Based on the idea and value proposition\nIdea:{detailed_idea}\nValue Proposition:{value_proposition}\nCreate a product roadmap in week by week bifurcated format. Do not use markdown.")
    print(response.text)
    return response.text
