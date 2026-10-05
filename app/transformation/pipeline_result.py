from dataclasses import dataclass

@dataclass
class PipelineResult:
    valid: list
    rejected: list
