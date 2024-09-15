from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel

from apropos.src.core.lms.helpers import LLM


class Topic(BaseModel):
    topic_name: str
    topic_template: str
    instructions_fields: Dict[str, str]
    input_fields: List[str]


class SystemMessage(BaseModel):
    premise: List[
        Topic
    ] = []  # Assuming 'premise' and 'objective' are the keys you need
    objective: List[Topic] = []
    constraints: List[Topic] = []  # Add this if 'constraints' is also a key you need


class UserMessage(BaseModel):
    user: List[Topic] = []  # Assuming 'user' is the key for user topics


class Demonstration(BaseModel):
    inputs: Union[Dict, str]
    outputs: Union[Dict, str]
    prompt: str
    gold_outputs: Optional[str]
    annotation: Optional[str]

    def to_string(self):
        return f"Input: {self.inputs}\nOutput: {self.outputs}\nPrompt: {self.prompt}\nGold Output: {self.gold_outputs}\nAnnotation: {self.annotation}"


class PromptTemplate(BaseModel):
    name: str
    system: SystemMessage
    user: UserMessage
    response_type: Literal["pydantic", "str"]
    response_model_scheme: Optional[Dict]
    demonstrations: List[Demonstration]

    def to_dict(self):
        return {
            "name": self.name,
            "system": self.system.dict(),
            "user": self.user.dict(),
            "response_type": self.response_type,
            "response_model_scheme": self.response_model_scheme,
            "demonstrations": [d.dict() for d in self.demonstrations],
        }

    def get_input_fields(self):
        input_fields = []
        for topic in self.system.premise:
            input_fields += topic.input_fields
        for topic in self.system.objective:
            input_fields += topic.input_fields
        for topic in self.system.constraints:
            input_fields += topic.input_fields
        for topic in self.user.user:
            input_fields += topic.input_fields
        return input_fields

    def get_line_by_key(self, key: str):
        def search_segment_for_key(segment: List[Topic]):
            for topic in segment:
                if key in topic.instructions_fields.keys():
                    return topic.instructions_fields[key]
                if key in topic.input_fields:
                    return topic.input_fields[key]
            return None

        for source in [
            self.system.premise,
            self.system.objective,
            self.system.constraints,
            self.user.user,
        ]:
            result = search_segment_for_key(source)
            if result:
                return result
        return None

    def set_line_by_key(self, key: str, value: str):
        def search_segment_for_key(segment: List[Topic], key: str, value: str):
            for topic in segment:
                if key in topic.instructions_fields.keys():
                    topic.instructions_fields[key] = value
                if key in topic.input_fields:
                    topic.input_fields[key] = value
            return segment

        self.system.premise = search_segment_for_key(self.system.premise, key, value)
        self.system.objective = search_segment_for_key(
            self.system.objective, key, value
        )
        self.system.constraints = search_segment_for_key(
            self.system.constraints, key, value
        )
        self.user.user = search_segment_for_key(self.user.user, key, value)

    def to_markdown(self):
        markdown = f"# Template: {self.name}\n\n"
        markdown += "## System\n\n"
        for topic in self.system.premise:
            markdown += f"### {topic.topic_name}\n\n"
            markdown += f"**Template**: {topic.topic_template}\n\n"
            markdown += f"**Instructions Fields**: {topic.instructions_fields}\n\n"
            markdown += f"**Input Fields**: {topic.input_fields}\n\n"
        markdown += "## User\n\n"
        for topic in self.user.user:
            markdown += f"### {topic.topic_name}\n\n"
            markdown += f"**Template**: {topic.topic_template}\n\n"
            markdown += f"**Instructions Fields**: {topic.instructions_fields}\n\n"
            markdown += f"**Input Fields**: {topic.input_fields}\n\n"
        return markdown

    def compile(
        self, inputs: Dict[str, str], custom_instructions_fields: Dict[str, str] = {}
    ):
        system = ""
        for topic in self.system.premise:
            template = topic.topic_template
            for field in topic.input_fields:
                if field not in template:
                    continue
                template = template.replace(
                    f"{field}", inputs[field] if inputs[field] else ""
                )
            for field in topic.instructions_fields:
                if field not in template:
                    continue
                if field in custom_instructions_fields:
                    template = template.replace(
                        f"{field}", custom_instructions_fields[field]
                    )
                else:
                    template = template.replace(
                        f"{field}", topic.instructions_fields[field]
                    )
            system += template + "\n\n"
        for topic in self.system.objective:
            template = topic.topic_template
            for field in topic.input_fields:
                if field not in template:
                    continue
                template = template.replace(
                    f"{field}", inputs[field] if inputs[field] else ""
                )
            for field in topic.instructions_fields:
                if field not in template:
                    continue
                if field in custom_instructions_fields:
                    template = template.replace(
                        f"{field}", custom_instructions_fields[field]
                    )
                else:
                    template = template.replace(
                        f"{field}", topic.instructions_fields[field]
                    )
            system += template + "\n\n"

        for topic in self.system.constraints:
            template = topic.topic_template
            for field in topic.input_fields:
                if field not in template:
                    continue
                template = template.replace(
                    f"{field}", inputs[field] if inputs[field] else ""
                )
            for field in topic.instructions_fields:
                if field not in template:
                    continue
                if field in custom_instructions_fields:
                    template = template.replace(
                        f"{field}", custom_instructions_fields[field]
                    )
                else:
                    template = template.replace(
                        f"{field}", topic.instructions_fields[field]
                    )
            system += template + "\n\n"
        if len(self.demonstrations) > 0:
            system += "\n\nDemonstrations of Successful Responses:\n\n"
            for i, demo in enumerate(self.demonstrations):
                demo_snippet = f"\n<demonstration_{i}>"
                demo_snippet += f"\n<input>"
                for input_field, value in demo.inputs.items():
                    input_field = input_field.replace("<<<", "").replace(">>>", "")
                    input_field = input_field.replace("_", " ").lower()
                    demo_snippet += f"\n<{input_field}>{value}</{input_field}>"
                demo_snippet += f"\n</input>"
               
                if isinstance(demo.outputs, dict):
                    demo_snippet += f"\n<valid_output>"
                    for output_field, value in demo.outputs.items():
                        output_field = output_field.replace("<<<", "").replace(">>>", "")
                        output_field = output_field.replace("_", " ").lower()
                        demo_snippet += f"\n<{output_field}>{value}</{output_field}>"
                    demo_snippet += f"\n</valid_output>"
                else:
                    demo_snippet += f"\n<valid_output>{demo.outputs}</valid_output>"
                if demo.annotation:
                    demo_snippet += f"\n<annotation>"
                    demo_snippet += f"\n{demo.annotation}"
                    demo_snippet += f"\n</annotation>"
                demo_snippet += f"\n</demonstration_{i}>"
                system += demo_snippet
        
        user = ""
        for topic in self.user.user:
            template = topic.topic_template
            for field in topic.input_fields:
                if field not in template:
                    continue
                try:
                    template = template.replace(
                        f"{field}", inputs[field] if inputs[field] else ""
                    )
                except TypeError as e:
                    raise Exception(
                        f"Inputs must be strings, instead got: {type(inputs[field])} for input field: {field}"
                    )

            for field in topic.instructions_fields:
                if field not in template:
                    continue
                if field in custom_instructions_fields:
                    template = template.replace(
                        f"{field}", custom_instructions_fields[field]
                    )
                else:
                    template = template.replace(
                        f"{field}", topic.instructions_fields[field]
                    )
            user += template + "\n\n"
        return system, user

    def run(
        self,
        inputs: Dict[str, str],
        lm: LLM,
        custom_instructions_fields: Dict[str, str] = {},
        response_model: Optional[Any] = None,
        multi_threaded: bool = False,
    ):
        system, user = self.compile(inputs, custom_instructions_fields)
        if response_model:
            response = lm.sync_respond(
                system_prompt=system,
                user_prompt=user,
                response_model=response_model,
                multi_threaded=multi_threaded,
            )
        else:
            response = lm.sync_respond(
                system_prompt=system, user_prompt=user, multi_threaded=multi_threaded
            )
        return response

    async def arun(
        self,
        inputs: Dict[str, str],
        lm: LLM,
        custom_instructions_fields: Dict[str, str] = {},
        response_model: Optional[Any] = None,
    ):
        system, user = self.compile(inputs, custom_instructions_fields)
        if response_model:
            response = await lm.async_respond(
                system_prompt=system, user_prompt=user, response_model=response_model
            )
        else:
            response = await lm.async_respond(system_prompt=system, user_prompt=user)
        assert isinstance(response, str) or isinstance(
            response, BaseModel
        ), f"Response: {response}"
        return response
