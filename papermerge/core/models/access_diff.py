

class AccessDiff:
    """
    A list of access permissions wich an operation
    associated.

    This structure is necessary because of the access permissions
    propagation from parent to child nodes i.e. if some access(es)
    is (are) applied to a node - it will affect (update, insert, delete)
    all its descendents.
    """
    DELETE = -1
    UPDATE = 0
    ADD = 1  # accesses in the list will be added
    REPLACE = 2

    def __init__(self, operation, access_set=[]):
        self._op = operation

        if len(access_set) == 0:
            self._set = set()
        else:
            self._set = access_set

    @property
    def operation(self):
        return self._op

    def add(self, access):
        self._set.add(access)

    def __len__(self):
        return len(self._set)

    def __iter__(self):
        return iter(self._set)

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
        acc_list = [
            str(acc) for acc in self._set
        ]
        op = op_name[self._op]

        return f"AccessDiff({op}, {acc_list})"

    def __repr__(self):
        return self.__str__()
