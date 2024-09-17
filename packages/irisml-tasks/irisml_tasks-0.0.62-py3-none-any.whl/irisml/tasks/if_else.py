import dataclasses
import logging
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Returns one of the inputs based on a condition.

    If the condition is true, the task returns then_* inputs, otherwise it returns else_* inputs.
    """

    VERSION = '0.2.0'

    @dataclasses.dataclass
    class Inputs:
        condition: bool
        then_float: float | None = None
        then_float_list: list[float] | None = None
        then_int: int | None = None
        then_int_list: list[int] | None = None
        then_str: str | None = None
        then_str_list: list[str] | None = None
        else_float: float | None = None
        else_float_list: list[float] | None = None
        else_int: int | None = None
        else_int_list: list[int] | None = None
        else_str: str | None = None
        else_str_list: list[str] | None = None

    @dataclasses.dataclass
    class Outputs:
        result_float: float | None = None
        result_float_list: list[float] | None = None
        result_int: int | None = None
        result_int_list: list[int] | None = None
        result_str: str | None = None
        result_str_list: list[str] | None = None

    def execute(self, inputs):
        type_names = ['float', 'float_list', 'int', 'int_list', 'str', 'str_list']
        then_inputs = [inputs.then_float, inputs.then_float_list, inputs.then_int, inputs.then_int_list, inputs.then_str, inputs.then_str_list]
        else_inputs = [inputs.else_float, inputs.else_float_list, inputs.else_int, inputs.else_int_list, inputs.else_str, inputs.else_str_list]

        if sum(1 for x in then_inputs if x is not None) != 1:
            raise ValueError(f"Expected exactly one non-None element in then_inputs, got {then_inputs}")
        if sum(1 for x in else_inputs if x is not None) != 1:
            raise ValueError(f"Expected exactly one non-None element in else_inputs, got {else_inputs}")

        index = next(i for i, x in enumerate(then_inputs) if x is not None)
        if else_inputs[index] is None:
            raise ValueError(f"Expected else_{type_names[index]} to be non-None, got {else_inputs[index]}")

        logger.debug(f"then_{type_names[index]}, else_{type_names[index]}: {then_inputs[index]}, {else_inputs[index]}. Condition: {inputs.condition}")
        if inputs.condition:
            result = then_inputs[index]
        else:
            result = else_inputs[index]

        return self.Outputs(**{f'result_{type_names[index]}': result})

    def dry_run(self, inputs):
        return self.execute(inputs)
