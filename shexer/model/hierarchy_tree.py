from shexer.model.const_elem_types import IRI_ELEM_TYPE, LITERAL_ELEM_TYPE, BNODE_ELEM_TYPE

class HTree(object):
    def __init__(self):
        self._root = None  # HNode
        self._node_index = {}

    def _subscribe_element(self, hcontent):
        str_value = hcontent.str_value
        if str_value not in self._node_index:
            self._node_index[str_value] = hcontent

    def create_node_literal(self, literal_obj):
        return HNode(hcontent=HLiteral(value=literal_obj),
                     htree=self)

    def create_node_IRI(self, iri_obj):
        return HNode(hcontent=HIri(value=iri_obj),
                     htree=self)

    def create_node_macro(self, macro_obj):
        return HNode(hcontent=HMacro(value=macro_obj),
                     htree=self)

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        self._root = value

    @property
    def iri_node(self):
        return None if not self.contains_element(IRI_ELEM_TYPE) else self.get_node_of_element(IRI_ELEM_TYPE)

    @property
    def literal_node(self):
        return None if not self.contains_element(LITERAL_ELEM_TYPE) else self.get_node_of_element(LITERAL_ELEM_TYPE)

    @property
    def bnode_node(self):
        return None if not self.contains_element(BNODE_ELEM_TYPE) else self.get_node_of_element(BNODE_ELEM_TYPE)

    def contains_element(self, str_type):
        return str_type in self._node_index

    def get_node_of_element(self, str_type):
        return self._node_index[str_type]  # We could get a key violation error here. I decide to risk that
        # assuming that whoever calls this has checked contains_element()



class HNode(object):
    def __init__(self, hcontent, htree, parents=None, children=None):
        self._hcontent = hcontent
        self._parents = parents if parents is not None else {}
        self._children = children if children is not None else {}
        htree._subscribe_element(self)  # Eeeasy python conventions! everything is under control

    def add_child(self, child):
        str_child = child.str_value
        if str_child not in self._children:
            self._children[str_child] = child
            child._parents[self.str_value] = self  # Lets assume consistence


    def add_parent(self, parent):
        str_parent = parent.str_value
        if str_parent not in self._parents:
            self._parents[str_parent] = parent
            parent._children[self.str_value] = self  # Lets assume consistence

    def has_parents(self):
        if self._parents:
            return True
        return False


    @property
    def value(self):
        return self._hcontent.value

    @property
    def str_value(self):
        return self._hcontent.str_value

    def __eq__(self, other):
        if not isinstance(other, HNode):
            return False
        return self._hcontent == other._hcontent

    def __ne__(self, other):
        return not self.__eq__(other)


class HContent(object):  # Abstract, dont instantiate
    def __init__(self, value):
        self._value = value

    @property
    def str_value(self):
        return str(self._value)

    @property
    def value(self):
        return self._value

    def __eq__(self, other):
        if not isinstance(other, HContent):
            return False
        if type(self._value) != type(other._value):
            return False
        return self.str_value == other.str_value

    def __ne__(self, other):
        return not self.__eq__(other)


class HLiteral(HContent):
    def __init__(self, value):  # Value should be a Literal
        super(HLiteral, self).__init__(value)

    def __str__(self):
        return str(self.value)


class HMacro(HContent):
    def __init__(self, value):
        super(HMacro, self).__init__(value)

    def __str__(self):
        return str(self.value)


class HIri(HContent):
    def __init__(self, value):
        super(HIri, self).__init__(value)

    def __str__(self):
        return str(self.value)
