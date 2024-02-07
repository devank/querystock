# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import OpenAI

agent = create_csv_agent(
    OpenAI(temperature=0),
    "archive/HDFC.csv",
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

@csrf_exempt
def index(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body.decode("utf-8"))
        query = received_json_data['messages']
        print(query)
        result = agent.run(query)
        print(result)
        response_data = {}
        response_data['message'] = result
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    return HttpResponse("You're at the query home.")