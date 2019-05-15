
from dbshx.model.hierarchy_tree import HTree, HNode, HMacro
from dbshx.model.Macro import Macro
from dbshx.model.const_elem_types import DOT_ELEM_TYPE, IRI_ELEM_TYPE, LITERAL_ELEM_TYPE


def get_basic_h_tree():
    result = HTree()
    dot_node = HNode(hcontent=HMacro(value=Macro(macro_const=DOT_ELEM_TYPE)),
                     htree=result)
    result.root = dot_node
    literal_node = HNode(hcontent=HMacro(value=Macro(macro_const=LITERAL_ELEM_TYPE)),
                         htree=result)
    iri_node = HNode(hcontent=HMacro(value=Macro(macro_const=IRI_ELEM_TYPE)),
                     htree=result)

    dot_node.add_child(literal_node)
    dot_node.add_child(iri_node)
    return result



