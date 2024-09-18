import asyncio

from apropos.src.core.programs.convenience_functions.dag_constructors import (
    build_path_program,
)
from apropos.src.core.programs.prompt import (
    PromptTemplate,
    SystemMessage,
    Topic,
    UserMessage,
)

def code_problem_plan_execute_example(model_names=["gpt-3.5-turbo", "gpt-3.5-turbo"]):
    plan = PromptTemplate(
        name="Plan Solution",
        system=SystemMessage(
            premise=[
                Topic(
                    topic_name="premise",
                    topic_template="# Premise\n$INTRODUCTION\n$MAIN_INSTRUCTIONS",
                    instructions_fields={
                        "$INTRODUCTION": "You are an AI assisting a colleague in solving a coding problem",
                        "$MAIN_INSTRUCTIONS": "You will be given a coding problem statement. Your task is to create a detailed plan to solve the problem, breaking it down into clear, logical steps. Focus on identifying key requirements, outlining necessary algorithms, and providing a structured approach to implement the solution.",
                    },
                    input_fields=[],
                )
            ],
            objective=[
                Topic(
                    topic_name="objective",
                    topic_template="# Objective\n$OBJECTIVE",
                    instructions_fields={
                        "$OBJECTIVE": "Please provide a detailed, step-by-step plan to solve the given coding problem. Include all necessary algorithms, data structures, and intermediate steps. Ensure that your plan covers all aspects of the problem, including input handling, required computations, and the expected output format."
                    },
                    input_fields=[],
                )
            ],
            constraints=[],
        ),
        user=UserMessage(
            user=[
                Topic(
                    topic_name="user",
                    topic_template="# Coding Problem\n<<<CODING_QUESTION>>>\n\n $ENJOINDER",
                    instructions_fields={
                        "$ENJOINDER": "Your plan should include:\n1. A clear statement of the problem requirements\n2. Identification of relevant algorithms and data structures\n3. Definition of functions and their purposes\n4. A step-by-step approach to implementing the solution\n5. Explanation of the reasoning behind each step\n6. Consideration of edge cases and error handling\n7. Description of how to present the final output\n\nPlease provide your detailed plan below:",
                    },
                    input_fields=["<<<CODING_QUESTION>>>"],
                )
            ]
        ),
        response_type="str",
        response_model_scheme=None,
        demonstrations=[],
    )
    execute = PromptTemplate(
        name="Implement Solution",
        system=SystemMessage(
            premise=[
                Topic(
                    topic_name="premise",
                    topic_template="# Premise\n$INTRODUCTION\n$MAIN_INSTRUCTIONS",
                    instructions_fields={
                        "$INTRODUCTION": "You are an AI coding assistant with expertise in various programming languages and problem-solving techniques.",
                        "$MAIN_INSTRUCTIONS": "You will be given the problem statement together with a high-level plan to solve it. Your task is to implement this plan, providing a working solution to the coding problem.",
                    },
                    input_fields=[],
                )
            ],
            objective=[
                Topic(
                    topic_name="objective",
                    topic_template="# Objective\n$OBJECTIVE",
                    instructions_fields={
                        "$OBJECTIVE": "Implement the solution to the coding problem by carefully following the provided plan. Your code should be appended to the provided function signature and be ready for execution."
                    },
                    input_fields=[],
                )
            ],
            constraints=[
                Topic(
                    topic_name="Constraints",
                    topic_template="# Constraints\n$CONSTRAINTS",
                    instructions_fields={
                        "$CONSTRAINTS": "Provide your solution as code that can be appended to the provided code signature and executed to solve the problem. Return your code in the following format: \n```python```. Do not re-write the function signature - return code that can be appended to the signature as-is. Keep in mind that your code, and potentially its file outputs, will be tested - do not delete any files it produces."
                    },
                    input_fields=[],
                )
            ],
        ),
        user=UserMessage(
            user=[
                Topic(
                    topic_name="user",
                    topic_template="# Plan\n<<<PLAN>>>\n\n $ENJOINDER",
                    instructions_fields={
                        "$ENJOINDER": "Your detailed implementation (including all necessary code, following the plan): "
                    },
                    input_fields=["<<<PLAN>>>"],
                )
            ]
        ),
        response_type="str",
        response_model_scheme=None,
        demonstrations=[],
    )
    code_plan_execute_path_dag = asyncio.run(
        build_path_program(
            [plan, execute],
            model_names=model_names,
            dag_input_names=["<<<CODING_QUESTION>>>"],
            dag_input_aliases={"question": "<<<CODING_QUESTION>>>"},
            dag_output_aliases={"<<<ANSWER>>>": "answer"},
        )
    )
    return code_plan_execute_path_dag