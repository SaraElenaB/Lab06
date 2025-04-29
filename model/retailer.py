from dataclasses import dataclass


@dataclass
class Retailer():
    #ma posso dare dei nomi fittizi qua o devono essere per forza uguali al database?
    Retailer_code: int
    Retailer_name: str
    Type: str
    Country: str

    def __eq__(self, other):
        return self.Retailer_code == other.codice

    def __hash__(self):
        return hash(self.Retailer_code)

    def __str__(self):
        return f"{self.Retailer_name} ({self.Retailer_code})"


