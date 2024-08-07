from os.path import join
import json

from jinja2 import Environment, FileSystemLoader

from src.schemas import FunctionsMetadata, FunctionSchema
from src.settings import STATIC_DIR, FN_CALL_TEMPLATE_PATH, FN_GENERATE_TEMPLATE_PATH, QUERY_GENERATE_TEMPLATE_PATH, DUMMY_FN_TEMPLATE_PATH

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader(join(STATIC_DIR, "templates")))

def load_jinja_template(template_name: str, context: dict[str, any]) -> str:
    """Load a Jinja2 template and render it with the given context"""
    template = env.get_template(template_name)
    return template.render(context)
    
def load_fn_call_template(
        template_name: str = FN_CALL_TEMPLATE_PATH,
        fnc_metadata: FunctionsMetadata = None
    ) -> str:
    """Load the function template from the Jinja2 template file"""
    context = {"functions_metadata": fnc_metadata} if fnc_metadata else {"functions_metadata": []}
    return load_jinja_template(template_name, context)

def load_fn_generate_template(
        template_name: str = FN_GENERATE_TEMPLATE_PATH,
        category: str = None,
        subcategory: str = None,
        tasks: list[str] = []
    ) -> str:
    """Load the function generation template from the Jinja2 template file"""
    context = {"category": category, "subcategory": subcategory, "tasks": tasks}
    return load_jinja_template(template_name, context)

def load_query_generate_template(
        template_name: str = QUERY_GENERATE_TEMPLATE_PATH,
        schemas: list[FunctionSchema] = [],
        num_examples: int = 10
    ) -> str:
    """Load the query generation template from the Jinja2 template file"""
    context = {"schemas": schemas, "num_examples": num_examples}
    return load_jinja_template(template_name, context)

def load_dummy_fn_template(
        template_name: str = DUMMY_FN_TEMPLATE_PATH,
        schemas: list[FunctionSchema] = []
    ) -> str:
    """Load the dummy function generation template from the Jinja2 template file"""
    context = {"schemas": schemas}
    rendered_template = load_jinja_template(template_name, context)

    # Check if the template is rendered correctly
    if "{{ schemas | indent(2) }}" in rendered_template:
        # Replace the "{{ schemas | indent(2) }}" with the actual schemas
        json_schemas = [schema.model_dump() for schema in schemas]
        return rendered_template.replace("{{ schemas | indent(2) }}", json.dumps(json_schemas, indent=2))