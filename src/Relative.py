class Relative:
    def __init__(self, relative_type, ADM, ACL, diagnosis):
        self.relative_type = relative_type
        self.ADM = ADM  # age of relative, when diabetes is diagnosed >> only for true diagnosis
        self.ACL = ACL  # age of relative, at last physical >> only for true false
        self.diagnosis = diagnosis
        self.K = self.set_K()

    def set_K(self):
        if self.relative_type == "p" or self.relative_type == "s":
            K = 0.5
        elif self.relative_type == "half_sibling" or self.relative_type == "grandparent" or self.relative_type == "uncle_or_aunt":
            K = 0.250
        elif self.relative_type == "half_uncle_or_aunt" or self.relative_type == "first_cousin":
            K = 0.125
        else:
            K = 0.250
        return K