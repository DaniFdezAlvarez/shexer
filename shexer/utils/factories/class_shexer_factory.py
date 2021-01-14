from shexer.core.class_shexer import ClassShexer


def get_class_shexer(class_instances_target_dict,
                     class_profile_dict,
                     remove_empty_shapes,
                     original_target_classes,
                     original_shape_map,
                     discard_useless_constraints_with_positive_closure,
                     keep_less_specific,
                     all_compliant_mode,
                     instantiation_property,
                     disable_or_statements,
                     disable_comments,
                     namespaces_dict,
                     allow_opt_cardinality,
                     disable_exact_cardinality,
                     shapes_namespace):
    class_count_dicts = {}

    for a_class_key in class_instances_target_dict:
        class_count_dicts[a_class_key] = len(class_instances_target_dict[a_class_key])

    return ClassShexer(
        class_counts_dict=class_count_dicts,
        class_profile_dict=class_profile_dict,
        class_profile_json_file=None,
        remove_empty_shapes=remove_empty_shapes,
        original_target_classes=original_target_classes,
        original_shape_map=original_shape_map,
        discard_useless_constraints_with_positive_closure=discard_useless_constraints_with_positive_closure,
        keep_less_specific=keep_less_specific,
        all_compliant_mode=all_compliant_mode,
        instantiation_property=instantiation_property,
        disable_or_statements=disable_or_statements,
        disable_comments=disable_comments,
        namespaces_dict=namespaces_dict,
        allow_opt_cardinality=allow_opt_cardinality,
        disable_exact_cardinality=disable_exact_cardinality,
        shapes_namespace=shapes_namespace,
    )