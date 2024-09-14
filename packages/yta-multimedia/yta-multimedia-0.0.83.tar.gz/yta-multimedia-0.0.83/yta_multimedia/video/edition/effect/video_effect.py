from abc import ABC, abstractmethod


class VideoEffect(ABC):
    """
    Abstract class to be inherited by all my custom effects so I can 
    control they belong to this family.

    A video effect is an effect that is customly made by using 
    personal modifications, calculations, involving maybe some
    image manipulation, etc.
    """
    @abstractmethod
    def apply(self):
        pass