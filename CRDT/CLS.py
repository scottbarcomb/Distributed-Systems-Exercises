class CLS:
    def __init__(self, node_id):
        # ID for the nodes, such as Alice or Bob
        self.node_id = node_id
        self.counter = 0
        self.add_set = set()
        self.remove_set = set()

    def add(self, element):
        self.counter += 1
        tag = (self.node_id, self.counter)
        self.add_set.add((element, tag))

    def remove(self, element):
        tags_to_remove = {tag for (e, tag) in self.add_set if e == element}
        for tag in tags_to_remove:
            self.remove_set.add((element, tag))

    def contains(self, element): # boolean
        tags_in_add = {tag for (e, tag) in self.add_set if e == element}
        tags_in_remove = {tag for (e, tag) in self.remove_set if e == element}
        return len(tags_in_add - tags_in_remove) > 0

    def mutual_sync(self, other_lists):
        for other in other_lists:
            self.add_set |= other.add_set # merge sets with or-equals
            self.remove_set |= other.remove_set
            other.add_set |= self.add_set # do the same for the other set
            other.remove_set |= self.remove_set

def main():
    alice_list = CLS('Alice')
    bob_list = CLS('Bob')

    alice_list.add('Milk')
    alice_list.add('Potatoes')
    alice_list.add('Eggs')

    bob_list.add('Sausage')
    bob_list.add('Mustard')
    bob_list.add('Coke')
    bob_list.add('Potatoes')

    bob_list.mutual_sync([alice_list])

    alice_list.remove('Sausage')
    alice_list.add('Tofu')
    alice_list.remove('Potatoes')

    alice_list.mutual_sync([bob_list])

    print("Bob's list contains 'Potatoes'?", bob_list.contains('Potatoes'))

if __name__ == "__main__":
    main()