from pathlib import Path

def encode_retrievals(retrievals, retrieved_key, prediction_key, utility):

    encoded_retrievals = []

    all_retrieveds = set()

    for retrieval in retrievals:
        for retrieved in retrieval[retrieved_key]:
            all_retrieveds.add(retrieved)

    all_retrieveds = list(all_retrieveds)
    all_retrieveds.sort()

    mapping = {retrieved:index for index, retrieved in enumerate(all_retrieveds)}

    for retrieval in retrievals:
        retrieveds = [mapping[name] for name in retrieval[retrieved_key]]
        utilities = [utility(retrieval, prediction) for prediction in retrieval[prediction_key]]
        encoded_retrievals.append({
            "retrieved": retrieveds,
            "utility_contributions": utilities
        })

    return encoded_retrievals, mapping


def encode_groups(mapping, group):
    groups = set()

    for retrieved in mapping.keys():
        assigned_group = group(retrieved)
        groups.add(assigned_group)

    all_groups = list(groups)
    all_groups.sort()

    group_mapping = {name:index for index, name in enumerate(all_groups)}

    grouping = [0 for _ in range(0, len(mapping))]

    for retrieved in mapping.keys():
        assigned_group = group(retrieved)
        retrieved_index = mapping[retrieved]
        group_index = group_mapping[assigned_group]
        grouping[retrieved_index] = group_index

    return grouping, group_mapping


def v_grouped(v, grouping, group_mapping):

    v_per_group = {}

    num_groups = len(group_mapping)

    retrieved_index_per_group = {}

    for retrieved_index, group_index in enumerate(grouping):
        retrieved_index_per_group[group_index] = retrieved_index
        # TODO add break

    for group, group_index in group_mapping.items():
        v_per_group[group] = v[retrieved_index_per_group[group_index]]

    return v_per_group


def most_important(v, mapping, how_many):
    importances = {name:v[index] for name, index in mapping.items()}
    sorted_importances = sorted(importances.items(), key=lambda x:-x[1])
    return sorted_importances[:how_many]


def least_important(v, mapping, how_many):
    importances = {name:v[index] for name, index in mapping.items()}
    sorted_importances = sorted(importances.items(), key=lambda x:x[1])

    return sorted_importances[:how_many]


def most_important_groups(v_per_group, how_many):
    sorted_importances = sorted(v_per_group.items(), key=lambda x:-x[1])
    return sorted_importances[:how_many]


def least_important_groups(v_per_group, how_many):
    sorted_importances = sorted(v_per_group.items(), key=lambda x:x[1])
    return sorted_importances[:how_many]

def get_project_root() -> Path:
    """Returns the project root folder."""
    return Path(__file__).parent.parent.parent
