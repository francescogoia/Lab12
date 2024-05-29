from dataclasses import dataclass

@dataclass
class Retailer:
    Retailer_code: int
    Retailer_name: str
    Type: str
    Country: str


    def __repr__(self):
        return f"{self.Retailer_code}-{self.Retailer_name}-{self.volume}"

    def __hash__(self):
        return hash(self.Retailer_code)

    def __eq__(self, other):
        return self.Retailer_code == other.Retailer_code

    def __str__(self):
        return f"{self.Retailer_name} - {self.volume}"

    def add_volume(self, v):
        self.volume += v

    def initialize_volume(self):
        self.volume = 0