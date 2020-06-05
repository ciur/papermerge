

class Diff:
    """
    A list of Models which can be propagated from parent to child node
    an operation associated.

    This structure is necessary because of
    the access permissions/kv/kvcomp
    propagation from parent to child nodes i.e. if some access/kv/kvcomp(es)
    is (are) applied to a node - it will affect (update, insert, delete)
    all its descendents.
    """
    DELETE = -1
    UPDATE = 0
    ADD = 1  # accesses in the list will be added
    REPLACE = 2

    def __init__(self, operation, instances_set=[]):
        self._op = operation

        if len(instances_set) == 0:
            self._set = set()
        else:
            self._set = instances_set

    @property
    def operation(self):
        return self._op

    def add(self, instance):
        self._set.add(instance)

    def __len__(self):
        return len(self._set)

    def __iter__(self):
        return iter(self._set)

    def first(self):
        if len(self) > 0:
            return list(self._set)[0]

        return None

    def pop(self):
        return self._set.pop()

    def is_update(self):
        return self.operation == self.UPDATE

    def is_add(self):
        return self.operation == self.ADD

    def is_delete(self):
        return self.operation == self.DELETE

    def is_replace(self):
        return self.operation == self.REPLACE

    def __str__(self):
        op_name = {
            self.DELETE: "delete",
            self.UPDATE: "update",
            self.ADD: "add",
            self.REPLACE: "replace"
        }
        inst_list = [
            str(inst) for inst in self._set
        ]
        op = op_name[self._op]

        return f"Diff({op}, {inst_list})"

    def __repr__(self):
        return self.__str__()
