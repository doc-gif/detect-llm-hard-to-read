from typing import List


def do_algebra(operator: List[str], operand: List[int]) -> int:
    expression = str(operand[0])
    for op, num in zip(operator, operand[1:]):
        expression += op + str(num)
    return eval(expression)
