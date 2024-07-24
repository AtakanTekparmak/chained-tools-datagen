from dotenv import load_dotenv

from src.models import construct_model      
from src.schemas import ChainedFNCResponse, FunctionsMetadata
from src.models.config import ModelConfig
from src.utils import load_fnc_template, load_curriculum

from easy_fnc.function_caller import FunctionCallingEngine, create_functions_metadata

def function_calling_flow():
    # Load the .env file
    load_dotenv()

    # Load the function call template
    fnc_metadata = create_functions_metadata(file_path="static/sample_functions.py")
    fnc_template = load_fnc_template(
        fnc_metadata=FunctionsMetadata.from_list(fnc_metadata)
    )
    
    # Create a ModelConfig instance
    model_config = ModelConfig(
        client="groq",
        system_prompt=fnc_template,
        temperature=0.5,
        fewshot_examples=None
    )
    # Create a GroqModel instance
    model = construct_model(config=model_config)

    # Chat with the model
    user_query = "Can you get me a random city and the weather forecast for it?"
    raw_response = model.chat(user_query)
    #print(raw_response)

    # Create a ModelResponse object from the response
    model_response = ChainedFNCResponse.from_raw_response(raw_response=raw_response)
    print(model_response)

    # Create a FunctionCallingEngine instance
    fnc_engine = FunctionCallingEngine()
    fnc_engine.add_user_functions("static/sample_functions.py")

    # Call the functions from the model response
    outputs = fnc_engine.call_functions(model_response.function_calls)
    print(outputs)

def function_generating_flow():
    from src.components.function_schema_generator import FunctionSchemaGenerator

    # Create a ModelConfig instance
    model_config = ModelConfig(
        client="groq",
        system_prompt="You are a helpful assistant that generates function schemas.",
        temperature=0.7,
        fewshot_examples=None
    )
    generator = FunctionSchemaGenerator(model_config)
    
    # Load the curriculum
    curriculum = load_curriculum()
    
    # Generate schemas for each subcategory in the curriculum
    schemas = []
    for subcategory in curriculum:
        tasks = [row.task for row in curriculum[subcategory]]
        category = curriculum[subcategory][0].category
        print(f"Generating schemas for subcategory: {subcategory}")
        print(f"Tasks: {tasks}")
        task_schemas = generator.generate_schemas(category, subcategory, tasks)
        schemas.extend(task_schemas)
        print("Task schemas:", task_schemas)

if __name__ == "__main__":
    #function_calling_flow()
    function_generating_flow()