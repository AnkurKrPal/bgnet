import sys
import json
import math  # If you want to use math.inf for infinity
import heapq

"""                 
                                                                            WARNINGNININ!!!    
                                                        THIS PROGRAM CONSIDERS ONLY SINGLE COMPONENT IN A GRAPH !!
"""

def ipv4_to_int(ipv4_addr):
    ipv4_array = [int(x) for x in ipv4_addr.split('.')]
    for i in range(0, 4):
        ipv4_array[i] = ipv4_array[i] << (24 - 8*i)

    result = 0
    for i in range(0, 4):
        result = result | ipv4_array[i]
    return result    

def calc_subnet(ipv4, subnet):
    mask = int(subnet[1:3])
    result = ((1 << mask) - 1) << (32 - mask)

    return ipv4 & result

def find_router_for_ip(routers, ip):
    ip_num = ipv4_to_int(ip)

    for router_ip, info in routers.items():
        mask = info["netmask"]

        if calc_subnet(ip_num, mask) == calc_subnet(
            ipv4_to_int(router_ip), mask
        ):
            return router_ip

    return None

def dijkstras_shortest_path(routers, src_ip, dest_ip):
    """
    This function takes a dictionary representing the network, a source
    IP, and a destination IP, and returns a list with all the routers
    along the shortest path.

    The source and destination IPs are **not** included in this path.

    Note that the source IP and destination IP will probably not be
    routers! They will be on the same subnet as the router. You'll have
    to search the routers to find the one on the same subnet as the
    source IP. Same for the destination IP. [Hint: make use of your
    find_router_for_ip() function from the last project!]

    The dictionary keys are router IPs, and the values are dictionaries
    with a bunch of information, including the routers that are directly
    connected to the key.

    This partial example shows that router `10.31.98.1` is connected to
    three other routers: `10.34.166.1`, `10.34.194.1`, and `10.34.46.1`:

    {
        "10.34.98.1": {
            "connections": {
                "10.34.166.1": {
                    "netmask": "/24",
                    "interface": "en0",
                    "ad": 70
                },
                "10.34.194.1": {
                    "netmask": "/24",
                    "interface": "en1",
                    "ad": 93
                },
                "10.34.46.1": {
                    "netmask": "/24",
                    "interface": "en2",
                    "ad": 64
                }
            },
            "netmask": "/24",
            "if_count": 3, #interface count
            "if_prefix": "en"
        },
        ...

    The "ad" (Administrative Distance) field is the edge weight for that
    connection.

    **Strong recommendation**: make functions to do subtasks within this
    function. Having it all built as a single wall of code is a recipe
    for madness.
    """
    src_router = find_router_for_ip(routers, src_ip)
    dest_router = find_router_for_ip(routers, dest_ip)

    if src_router is None or dest_router is None:
        return []

    if src_router == dest_router:
        return []

    distances = {node: math.inf for node in routers}
    parents = {node: None for node in routers}
    distances[src_router] = 0

    pq = [(0, src_router)]

    while pq:
        curr_dist, curr_node = heapq.heappop(pq)

        if curr_dist > distances[curr_node]:
            continue

        if curr_node == dest_router:
            break

        for neigh, conn in routers[curr_node]["connections"].items():
            wt = conn["ad"]

            if curr_dist + wt < distances[neigh]:
                distances[neigh] = curr_dist + wt
                parents[neigh] = curr_node
                heapq.heappush(pq, (distances[neigh], neigh))

    if distances[dest_router] == math.inf:
        return []

    result = []
    curr = dest_router

    while curr is not None:
        result.append(curr)
        curr = parents[curr]

    result.reverse()

    # Exclude the source and destination IPs, as required.
    return result
    
    # TODO Write me!

#------------------------------
# DO NOT MODIFY BELOW THIS LINE
#------------------------------
def read_routers(file_name):
    with open(file_name) as fp:
        data = fp.read()

    return json.loads(data)

def find_routes(routers, src_dest_pairs):
    for src_ip, dest_ip in src_dest_pairs:
        path = dijkstras_shortest_path(routers, src_ip, dest_ip)
        print(f"{src_ip:>15s} -> {dest_ip:<15s}  {repr(path)}")

def usage():
    print("usage: dijkstra.py infile.json", file=sys.stderr)

def main(argv):
    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    routes = json_data["src-dest"]

    find_routes(routers, routes)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
