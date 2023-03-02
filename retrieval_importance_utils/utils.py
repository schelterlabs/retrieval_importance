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


def most_important(v, mapping, how_many):
    importances = {name:v[index] for name, index in mapping.items()}
    sorted_importances = sorted(importances.items(), key=lambda x:-x[1])
    return sorted_importances[:how_many]


def least_important(v, mapping, how_many):
    importances = {name:v[index] for name, index in mapping.items()}
    sorted_importances = sorted(importances.items(), key=lambda x:x[1])

    return sorted_importances[:how_many]