#!/root/venv/bin/python

from jinja2 import Template

import extract_json_info

# import template
from jinja2 import Template, FileSystemLoader, Environment

# jinja2 template loader path
j2_loader = FileSystemLoader('./')

# define env， template loader
env = Environment(loader=j2_loader)

# get the template file
j2_tmpl = env.get_template('./client_impl_template.j2')

data = extract_json_info.extract_json_info("my_service.json")

# set parameters to template and render it
result = j2_tmpl.render(data)

print(result)

# save the result to file "{data['package']['package_name']}_impl.h"
output_file = f"{data['package']['package_name']}_client.h"
with open(output_file, 'w') as f:
    f.write(result)


