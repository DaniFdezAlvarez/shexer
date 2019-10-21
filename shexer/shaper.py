from shexer.utils.obj_references import check_just_one_not_none, check_one_or_zero_not_none

from shexer.consts import SHEX, NT, TSV_SPO, N3, TURTLE, RDF_XML, FIXED_SHAPE_MAP
from shexer.utils.factories.class_profiler_factory import get_class_profiler
from shexer.utils.factories.instance_tracker_factory import get_instance_tracker
from shexer.utils.factories.class_shexer_factory import get_class_shexer
from shexer.io.profile.formater.abstract_profile_serializer import AbstractProfileSerializer
from shexer.utils.factories.shape_serializer_factory import get_shape_serializer


class Shaper(object):

    def __init__(self, target_classes=None, file_target_classes=None,
                 input_format=NT, instances_file_input=None,
                 graph_file_input=None, graph_list_of_files_input=None,
                 raw_graph=None,
                 url_graph_input=None, list_of_url_input=None,
                 namespaces_dict=None, namespaces_dict_file=None,
                 instantiation_property=None,
                 namespaces_to_ignore=None,
                 infer_numeric_types_for_untyped_literals=False,
                 discard_useless_constraints_with_positive_closure=True,
                 all_instances_are_compliant_mode=True,
                 keep_less_specific=True,
                 all_classes_mode=False,
                 shape_map_file=None,
                 shape_map_raw=None,
                 depth_for_building_subgraph=1,
                 track_classes_for_entities_at_last_depth_level=True,
                 strict_syntax_with_corners=False,
                 url_endpoint=None,
                 shape_map_format=FIXED_SHAPE_MAP):
        """

        :param target_classes:
        :param file_target_classes:
        :param input_format:
        :param instances_file_input:
        :param graph_file_input:
        :param graph_list_of_files_input:
        :param namespaces_dict:
        :param namespaces_dict_file:
        :param instantiation_property:
        :param namespaces_to_ignore:
        :param infer_numeric_types_for_untyped_literals:
        :param discard_useless_constraints_with_positive_closure:
        :param all_instances_are_compliant_mode:
        :param keep_less_specific:
        """

        check_just_one_not_none((graph_file_input, "graph_file_input"),
                                (graph_list_of_files_input, "graph_list_of_files_input"),
                                (raw_graph, "raw_graph"),
                                (url_graph_input, "url_input"),
                                (list_of_url_input, "list_of_url_input"),
                                (url_endpoint, "url_endpoint")
                                )

        check_one_or_zero_not_none((namespaces_dict, "namespaces_dict"),
                                   (namespaces_dict_file, "namespaces_dict_file"))

        self._check_target_classes(target_classes=target_classes,
                                   file_target_classes=file_target_classes,
                                   all_classes_mode=all_classes_mode,
                                   shape_map_raw=shape_map_raw,
                                   shape_map_file=shape_map_file)

        #TODO ---> Param check of shape_map and graph_via_shape_map

        self._check_input_format(input_format)

        self._target_classes = target_classes
        self._file_target_classes = file_target_classes
        self._input_format = input_format
        self._instances_file_input = instances_file_input
        self._graph_file_input = graph_file_input
        self._graph_list_of_files_input = graph_list_of_files_input
        self._url_graph_input = url_graph_input
        self._list_of_url_input = list_of_url_input
        self._namespaces_dict = namespaces_dict
        self._namespaces_dict_file = namespaces_dict_file  # TODO Need to parse this
        self._instantiation_property = instantiation_property
        self._namespaces_to_ignore = namespaces_to_ignore
        self._infer_numeric_types_for_untyped_literals = infer_numeric_types_for_untyped_literals
        self._discard_useles_constraints_with_positive_closure = discard_useless_constraints_with_positive_closure
        self._all_compliant_mode = all_instances_are_compliant_mode
        self._keep_less_specific = keep_less_specific
        self._raw_graph = raw_graph
        self._all_classes_mode = all_classes_mode
        self._shape_map_file = shape_map_file
        self._shape_map_raw = shape_map_raw
        self._depth_for_building_subgraph = depth_for_building_subgraph
        self._track_classes_for_entities_at_last_depth_level = track_classes_for_entities_at_last_depth_level
        self._url_endpoint=url_endpoint
        self._strict_syntax_with_corners = strict_syntax_with_corners
        self._shape_map_format = shape_map_format
        #TODO check correctness of these last five params



        self._instance_tracker = None
        self._target_classes_dict = None
        self._class_profiler = None
        self._profile = None
        self._class_shexer = None
        self._shape_list = None

    def profile_graph(self, string_output=False, output_file=None):
        self._check_correct_output_params(string_output, output_file)
        if self._target_classes_dict is None:
            self._launch_instance_tracker()
        if self._profile is None:
            self._launch_class_profiler()
        if string_output:
            return AbstractProfileSerializer(self._profile).get_string_representation()
        return AbstractProfileSerializer(self._profile).write_profile_to_file(target_file=output_file)

    def shex_graph(self, string_output=False, output_file=None, output_format=SHEX, aceptance_threshold=0.4):
        """
        :param string_output:
        :param output_file:
        :param output_format:
        :param aceptance_threshold:
        :return:
        """
        self._check_correct_output_params(string_output, output_file)
        self._check_output_format(output_format)
        self._check_aceptance_threshold(aceptance_threshold)
        if self._target_classes_dict is None:
            self._launch_instance_tracker()
        if self._profile is None:
            self._launch_class_profiler()
        if self._shape_list is None:
            self._launch_class_shexer()
        serializer = self._build_shapes_serializer(target_file=output_file,
                                                   string_return=string_output,
                                                   output_format=output_format,
                                                   aceptance_threshold=aceptance_threshold)
        return serializer.serialize_shex()  # If string return is active, returns string.
        # Otherwise, it writes to file and returns None

    def _launch_class_profiler(self):
        if self._class_profiler is None:
            self._class_profiler = self._build_class_profiler()
        self._profile = self._class_profiler.profile_classes()

    def _launch_class_shexer(self):
        if self._class_shexer is None:
            self._class_shexer = self._build_class_shexer()
        self._shape_list = self._class_shexer.shex_classes()

    def _launch_instance_tracker(self):
        if self._instance_tracker is None:
            self._instance_tracker = self._build_instance_tracker()
        self._target_classes_dict = self._instance_tracker.track_instances()

    def _build_shapes_serializer(self, target_file, string_return, output_format, aceptance_threshold):
        return get_shape_serializer(shapes_list=self._shape_list,
                                    target_file=target_file,
                                    string_return=string_return,
                                    namespaces_dict=self._namespaces_dict,
                                    output_format=output_format,
                                    aceptance_threshold=aceptance_threshold,
                                    instantiation_property=self._instantiation_property,
                                    all_compliant_mode=self._all_compliant_mode,
                                    keep_less_specific=self._keep_less_specific,
                                    discard_useless_constraints_with_positive_closure=
                                    self._discard_useles_constraints_with_positive_closure)

    def _build_class_profiler(self):
        return get_class_profiler(target_classes_dict=self._target_classes_dict,
                                  source_file=self._graph_file_input,
                                  list_of_source_files=self._graph_list_of_files_input,
                                  input_format=self._input_format,
                                  instantiation_property_str=self._instantiation_property,
                                  namespaces_to_ignore=self._namespaces_to_ignore,
                                  infer_numeric_types_for_untyped_literals=self._infer_numeric_types_for_untyped_literals,
                                  raw_graph=self._raw_graph,
                                  namespaces_dict=self._namespaces_dict,
                                  url_input=self._url_graph_input,
                                  list_of_url_input=self._list_of_url_input,
                                  shape_map_file=self._shape_map_file,
                                  shape_map_raw=self._shape_map_raw,
                                  track_classes_for_entities_at_last_depth_level=self._track_classes_for_entities_at_last_depth_level,
                                  depth_for_building_subgraph=self._depth_for_building_subgraph,
                                  url_endpoint=self._url_endpoint,
                                  strict_syntax_with_corners=self._strict_syntax_with_corners,
                                  target_classes=self._target_classes,
                                  file_target_classes=self._file_target_classes)


    def _build_instance_tracker(self):
        return get_instance_tracker(instances_file_input=self._instances_file_input,
                                    graph_file_input=self._graph_file_input,
                                    graph_list_of_files_input=self._graph_list_of_files_input,
                                    target_classes=self._target_classes,
                                    file_target_classes=self._file_target_classes,
                                    input_format=self._input_format,
                                    instantiation_property=self._instantiation_property,
                                    raw_graph=self._raw_graph,
                                    all_classes_mode=self._all_classes_mode,
                                    namespaces_dict=self._namespaces_dict,
                                    url_input=self._url_graph_input,
                                    list_of_url_input=self._list_of_url_input,
                                    shape_map_file=self._shape_map_file,
                                    shape_map_raw=self._shape_map_raw,
                                    track_classes_for_entities_at_last_depth_level=self._track_classes_for_entities_at_last_depth_level,
                                    depth_for_building_subgraph=self._depth_for_building_subgraph,
                                    url_endpoint=self._url_endpoint,
                                    strict_syntax_with_corners=self._strict_syntax_with_corners,
                                    shape_map_format=self._shape_map_format
                                    )

    def _build_class_shexer(self):
        return get_class_shexer(class_instances_target_dict=self._target_classes_dict,
                                class_profile_dict=self._profile)

    @staticmethod
    def _check_correct_output_params(string_output, target_file):
        if not string_output and target_file is None:
            raise ValueError("You must provide a target path or set string output to True")

    @staticmethod
    def _check_input_format(input_format):
        if input_format not in [NT, TSV_SPO, N3, TURTLE, RDF_XML]:
            raise ValueError("Currently unsupported input format: " + input_format)

    @staticmethod
    def _check_target_classes(target_classes, file_target_classes, all_classes_mode, shape_map_file, shape_map_raw):
        if not all_classes_mode:
            check_just_one_not_none((target_classes, "target_classes"),
                                    (file_target_classes, "file_target_classes"),
                                    (shape_map_file, "shape_map_file"),
                                    (shape_map_raw, "shape_map_raw")
                                    )
        else:
            if target_classes is not None or file_target_classes is not None:
                raise ValueError("You must provide a list of target classes XOR set all_classes_mode to True")
            # But all_classes mode is compatible with shape_map_selectors. Setting all_classes_mode = True and
            # providing some selectros will cause shexer to shex both the shapes specified in the selectors
            # and to create a shape for eahc element with an instance in the target graph

    @staticmethod
    def _check_output_format(output_format):
        if output_format != SHEX:
            raise ValueError("Currently unsupported output format: " + output_format)

    @staticmethod
    def _check_aceptance_threshold(aceptance_threshold):
        if aceptance_threshold < 0 or aceptance_threshold > 1:
            raise ValueError("The acceptance threshold must be a value in [0,1]")
