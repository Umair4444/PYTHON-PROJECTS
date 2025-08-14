AsyncOpenAI
OpenAIChatCompletionsModel
RunCnfig

Agent
 - tools
      * ModelSetting from agents.agents
    - model_setting = ModelSetting(tool_choice = 'auto' | 'none' | 'required', parallel_tool_calls = True | False)  
    - tool_use_behaviour = 'run_llm_again' | 'stop_on_first_tool'
    # or 
    - tool_use_behaviour = StopAtTools(stop_at_tool_names = ['your tool name'])
    - reset_tool_choice = True | False

 - handoffs
    - Agent Name
    - instruction
    - handoffs
    - handoffs_description
    # or
    - handoffs=[handoff( agent="Agent Name", tool_name_override="", tool_description_override="", is_enable=boolean
        on_handoff="takes context", input_type="", input_filters=handoffs_filter.remove_all_tools )],



 - Runner
    - max_turns
    - sync
    - run_sync
    - run_stream
    - context

@func_tool -- there are more options try it
    - is_enabled = True | False

@input_guardrails
@output_guardrails

GuardrailFunctionOutput

input_guardrails
output_guardrails

InputGuardrailTripwireTriggered
OutputGuardrailTripwireTriggered

# Context
- use Class, DataClass, pydantic class, TypeClass to create anything that is pass/used in context 

# Dynamic Instruction
- Context it is a variable to store context must be first
    - RunContextWrapper from agents it is a Class for type hinting
- Agent it is a variable to store agent must be second
    - Agent from agents it is a Class for type hinting
- must return a string
