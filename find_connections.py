def find_connections(entity_data_list):
    connections = []
    for i in range(len(entity_data_list)):
        for j in range(i+1, len(entity_data_list)):
            person1 = entity_data_list[i]
            person2 = entity_data_list[j]
            common_keys = set(person1.keys()) & set(person2.keys())
            shared = {}
            for key in common_keys:
                if person1[key] == person2[key]:
                    shared[key] = person1[key]
            if shared:
                connections.append({
                    "person1": person1["name"],
                    "person2": person2["name"],
                    "shared": shared
                })
    return connections
