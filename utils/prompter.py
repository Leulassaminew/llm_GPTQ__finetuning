"""
A dedicated helper to manage templates and prompt building.
"""

import json
import os.path as osp
from typing import Union


def count_tokens(texts, tokenizer):
    return sum(
        len(item)
        for item in tokenizer(texts, padding=True, return_tensors="pt")["input_ids"]
    )


class PromptSelector(object):
    @staticmethod
    def from_template_name(template_name: str = "", verbose: bool = False):
        if "sharegpt" in template_name:
            prompter = ChatPrompter(template_name, verbose)
        elif template_name == "text":
            prompter = None
        else:
            prompter = AlpacaPrompter(template_name, verbose)

        return prompter


class AlpacaPrompter(object):
    __slots__ = ("template", "_verbose")

    def __init__(self, template_name: str = "", verbose: bool = False):
        self._verbose = verbose
        if not template_name:
            # Enforce the default here, so the constructor can be called with '' and will not break.
            template_name = "alpaca"
        file_name = osp.join("templates", f"{template_name}.json")
        if not osp.exists(file_name):
            raise ValueError(f"Can't read {file_name}")
        with open(file_name) as fp:
            self.template = json.load(fp)
        if self._verbose:
            print(
                f"Using prompt template {template_name}: {self.template['description']}"
            )

    def generate_prompt(
        self,
        Question: str,
        Answer: Union[None,str] = None,
        **kwargs,  # ignore these additional keywords
    ) -> str:
        # returns the full prompt from instruction and optional input
        # if a label (=response, =output) is provided, it's also appended.
        res = self.template["prompt_input"].format(input=Question)
        if Answer:
            res = f"{res}{Answer}"
        if self._verbose:
            print(res)
        return res

    def get_response(self, output: str) -> str:
        try:
            result = output.split(self.template["response_split"])[1].strip()
        except (KeyError, IndexError):
            result = output
        return result


class ChatPrompter(object):
    __slots__ = ("template", "_verbose")

    def __init__(self, template_name: str = "", verbose: bool = False):
        self._verbose = verbose
        if not template_name:
            # Enforce the default here, so the constructor can be called with '' and will not break.
            template_name = "alpaca"
        file_name = osp.join("templates", f"{template_name}.json")
        if not osp.exists(file_name):
            raise ValueError(f"Can't read {file_name}")
        with open(file_name) as fp:
            self.template = json.load(fp)
        if self._verbose:
            print(
                f"Using prompt template {template_name}: {self.template['description']}"
            )

    def generate_prompt(self, **kwargs) -> str:
        res = self.template["prompt"] + "\n"
        input_key = self.template["input"]
        user_key = self.template["user"]
        text_key = self.template["text"]

        if input_key in kwargs:
            for item in kwargs[input_key]:
                user = item[user_key].upper()
                text = item[text_key]
                res += self.template["chat"].format(user=user, text=text)

        if self._verbose:
            print(res)
        return res

    def get_response(self, output: str) -> str:
        return output
