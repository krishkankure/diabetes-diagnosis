
def dpf_calculate(rel):
    pos_relatives = []
    neg_relatives = []
    for x in rel:
        if x.diagnosis:
            pos_relatives.append(x)
        else:
            neg_relatives.append(x)

    numerator_sum = 0
    for y in pos_relatives:
        temp = y.K * (88 - y.ADM) + 20
        numerator_sum += temp

    denominator_sum = 0
    for z in neg_relatives:
        temp = z.K * (z.ACL - 14) + 50
        denominator_sum += temp

    if denominator_sum == 0:
        denominator_sum = 1
    dpf = numerator_sum / denominator_sum
    return dpf
