from dataclasses import dataclass

from s2wsjson.s2_validation_error import S2ValidationError
from s2wsjson.generated.gen_s2 import NumberRange as GenNumberRange


@dataclass
class NumberRange:
    start_of_range: float
    end_of_range: float

    def validate(self) -> bool:
        if self.start_of_range > self.end_of_range:
            raise S2ValidationError(self, 'start_of_range should not be higher than end_of_range')

        return True

    def to_json(self) -> str:
        self.validate()
        return GenNumberRange(start_of_range=self.start_of_range, end_of_range=self.end_of_range).json()

    def to_dict(self) -> dict:
        self.validate()
        return GenNumberRange(start_of_range=self.start_of_range, end_of_range=self.end_of_range).dict()

    @staticmethod
    def from_json(json_str: str) -> 'NumberRange':
        gen_model = GenNumberRange.parse_raw(json_str)

        model = NumberRange(gen_model.start_of_range,
                            gen_model.end_of_range)
        model.validate()
        return model
