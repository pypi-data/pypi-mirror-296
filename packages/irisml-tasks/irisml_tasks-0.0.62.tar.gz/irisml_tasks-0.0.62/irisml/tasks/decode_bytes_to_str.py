import dataclasses
import irisml.core


class Task(irisml.core.TaskBase):
    """Convert bytes to string."""
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        data: bytes

    @dataclasses.dataclass
    class Config:
        encoding: str = 'utf-8'

    @dataclasses.dataclass
    class Outputs:
        string: str

    def execute(self, inputs):
        return self.Outputs(inputs.data.decode(self.config.encoding))

    def dry_run(self, inputs):
        return self.execute(inputs)
