# jinja2_render

Render a jinja2 template and output it to a specified path.
Useful to reduce repeatition when creating configuration base on states or other entities.

*Note: Need a Home Assistant restart or YAMl reload to take effect after template generation.

It's simple enough to get started.

Install through HACS, or just manually copy the custom_component folder to home assistant; enable the component via configuration.yaml:

jinja2_render:

Execute the service jinja2_render.render_template to generate the output file, either via:

- script

- automation

- or developer tools's service tab

