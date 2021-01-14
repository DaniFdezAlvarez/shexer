from shexer.model.graph.endpoint_sgraph import EndpointSGraph

def get_remote_graph_if_needed(endpoint_url, store_locally):
    if endpoint_url is None:
        return None
    return EndpointSGraph(endpoint_url=endpoint_url,
                          store_locally=store_locally)