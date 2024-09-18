from exa_py import Exa

exa = Exa("a4e1fa44-f6a3-432b-9725-03677ee13e2e");

result = exa.get_contents(
  ["quizlet.com"],
  text=True,
  livecrawl="never",
  filter_empty_results=False
)

print(result)