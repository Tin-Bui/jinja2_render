"""Initialize the Jinja2 Render component."""
from .render_template import async_setup

DOMAIN = "jinja2_render"

async def async_setup_entry(hass, config_entry):
    """Set up the Jinja2 Render component from a config entry."""
    await async_setup(hass)
    return True
