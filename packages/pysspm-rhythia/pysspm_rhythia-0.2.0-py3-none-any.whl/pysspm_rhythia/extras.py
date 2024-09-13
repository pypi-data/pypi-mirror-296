from pysspm import SSPMParser

def calcObsiidRating(self: SSPMParser, notes: list = None) -> SSPMParser:
    """
    calculates difficulty by using Obsiids difficulty calculation.
    This method is essentially just the dot product of the notes
    """

    print(self.Notes[1:5])

    if not notes: # if we pass in notes
        pass
    raise NotImplementedError("CalcObsiidRating function is a W.I.P.")

    return self


def calcPPRating(self: SSPMParser) -> float:
    """
    This calculation method is the method used in rhythia-online. | May change in future updates
    """
    return len(self.Notes) / 100 

def calcStarRating(self: SSPMParser) -> float:
    """
    # Pseudo-code outline:

    - get notes [0, 0, 100, 1, 0, 150]
    - apply exponential decay (of some sorts)
    """