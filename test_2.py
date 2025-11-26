import yaml
from pprint import pprint

with open('astronomy/prompt_base.yaml') as f:
    templates = yaml.safe_load(f)

print(templates['user_input_template']['name'])
