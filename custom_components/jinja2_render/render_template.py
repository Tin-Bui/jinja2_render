import os
import logging
import jinja2
import voluptuous as vol
from homeassistant.helpers.service import async_register_admin_service
from homeassistant.const import CONF_PATH
from homeassistant.exceptions import HomeAssistantError

DOMAIN = "jinja2_render"

# Validate the path is an absolute path or relative to the Home Assistant config path
def resolve_path(value, hass, allow_nonexistent=True):
    config_path = hass.config.path()
    path = os.path.abspath(os.path.join(config_path, value))

    if not allow_nonexistent and not os.path.exists(path):
        raise HomeAssistantError(f"File not found: {path}")

    return path

# Render the template and output it to the specified path
async def render_template_service(hass, call):

    # Get the logger for the current module
    logger = logging.getLogger(__name__)

    logger.info(f"{DOMAIN}:Rendering template and writing to output file.")
    
    template_path = resolve_path(call.data.get("template_path"), hass, allow_nonexistent=False)
    logger.info(f"{DOMAIN}:Received template path: {template_path}")
    
    output_path = resolve_path(call.data.get("output_path"), hass)
    logger.info(f"{DOMAIN}:Output file: {output_path}")
    
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))

    rendered_template = template.render()

    # Create the directory if it doesn't exist
    output_folder = os.path.dirname(output_path)
    os.makedirs(output_folder, exist_ok=True)
    with open(output_path, "w") as output_file:
        output_file.write(rendered_template)

# Register the custom service
async def async_setup(hass, config):
    schema = vol.Schema(
        {
            vol.Required("template_path"): str,
            vol.Required("output_path"): str,
        }
    )

    logger.info(f"{DOMAIN}:Registering component.")  

    async def wrapper(call):
        return await render_template_service(hass, call)

    async_register_admin_service(
        hass,  
        DOMAIN,  
        "render_template",  
        wrapper,  
        schema=schema  
    )

    return True
