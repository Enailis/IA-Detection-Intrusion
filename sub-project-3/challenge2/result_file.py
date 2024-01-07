def create_result_file(predictions, probabilities, method_name: str, version: str):
    import json
    res = dict()

    predictions = ["Normal" if x == 0 else "Attack" for x in predictions]
    probabilities = [[x, 1- x] for x in probabilities]

    res['preds'] = list(predictions)  # list of predicted labels
    res['probs'] = list(probabilities)  # list of probas/scores (probas of attack (class 1))

    res['names'] = ['HARDY', 'LUCAS']  # list of team member name(s )
    res['method'] = method_name  # methode name
    res['version'] = version  # submission version number
    f = open(f'results/HARDY_LUCAS_{version}.res', "w")  # VERSION = 1, 2 ou 3
    f.write(json.dumps(res))
    f.close()
