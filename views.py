from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Rule
from .rule_engine import create_rule, evaluate_rule
import json

@csrf_exempt
def create_rule_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        rule_string = data['rule_string']
        
        # Save rule string to the database
        rule = Rule(rule_string=rule_string)
        rule.save()
        
        return JsonResponse({'rule_id': rule.id})

@csrf_exempt
def evaluate_rule_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        rule_id = data['rule_id']
        attributes = data['data']
        
        # Fetch the rule from the database
        rule = Rule.objects.get(id=rule_id)
        rule_ast = create_rule(rule.rule_string)
        
        # Evaluate the rule
        result = evaluate_rule(rule_ast, attributes)
        
        return JsonResponse({'result': result})
