from dataclasses import dataclass


@dataclass(init=False, unsafe_hash=True, frozen=True)
class ImageUrl:
    resource: str

    def __init__(self, resource: str):
        super().__setattr__('resource', resource)
