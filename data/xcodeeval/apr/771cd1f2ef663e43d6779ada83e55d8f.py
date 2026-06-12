debug = False

def gcd(a, b):
    """Return greatest common divisor using Euclid's Algorithm."""
    while b:      
        a, b = b, a % b
    return a

def lcm(a, b):
    """Return lowest common multiple."""
    return a * b // gcd(a, b)

def lcmm(list_of_integers):
    """Return lcm of args."""   
    if len(list_of_integers) > 2:
        return lcm(list_of_integers.pop(), lcmm(list_of_integers))
    else:
        return lcm(*list_of_integers)

def is_bijection(list_of_integers):
    buckets = [ 0 for _ in range(len(list_of_integers)) ]
    for number in list_of_integers:
        buckets[number] += 1
    return 0 not in buckets
    
def get_cycle_with_person(person, cycles):
    for cycle in cycles:
        if cycle[-1] == person:
            if debug:
                print('found person ' + str(person) + ' in cycle ' + str(cycle))
            return cycle
    return None


def get_cycle_with_crush(crush, cycles):
    for cycle in cycles:
        if cycle[0] == crush:
            if debug:
                print('found crush ' + str(crush) + ' in cycle ' + str(cycle))
            return cycle
    return None

def append_cycle_to_other_cycle(cycles, cycle, other_cycle):
    if debug:
        print('appending' + str(cycle) + ' to ' + str(other_cycle))
    for element in cycle:
        other_cycle.append(element)
    cycles.remove(cycle)


def make_new_cycle(first, second, cycles):
    cycles.append([first, second] if first != second else [first])

def get_cycle_length(cycle):
    return len(cycle)//2 if len(cycle)%2 == 0 else len(cycle)

def main():
    numer_of_people = int(input())
    crushes = list(map(lambda x: int(x) - 1, input().split(' ')))
    if debug:
        print(crushes)
    if not is_bijection(crushes):
        print('-1')
        return 0
    list_of_cycles = []
    for person, crush in enumerate(crushes):
        cycle_with_person = get_cycle_with_person(person, list_of_cycles)
        cycle_with_crush = get_cycle_with_crush(crush, list_of_cycles)
        if cycle_with_person is not None:
            if cycle_with_crush is not None:
                if cycle_with_person != cycle_with_crush:
                    append_cycle_to_other_cycle(list_of_cycles, cycle_with_crush, cycle_with_person)
            else:
                cycle_with_person.append(crush)
        else:
            if cycle_with_crush is not None:
                cycle_with_crush.insert(0,person)
            else:
                make_new_cycle(person, crush, list_of_cycles)
    print(lcmm([ get_cycle_length(cycle) for cycle in list_of_cycles]))
    return 0

if __name__ == "__main__":
    main()
