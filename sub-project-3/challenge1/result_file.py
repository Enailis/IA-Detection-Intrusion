def create_result_file(predictions, probabilities, METHOD_NAME, APP_NAME, VERSION):
    import json
    res = dict()

    res['preds'] = list(predictions)  # list of predicted labels
    res['probs'] = list(probabilities)  # list of probas/scores (probas of attack (class 1))

    res['names'] = ['NAME1', 'NAME2']  # list of team member name(s )
    res['method'] = METHOD_NAME  # methode name
    res['appName'] = APP_NAME  # "SSH" ou "HTTPWeb"
    res['version'] = VERSION  # submission version number
    f = open("<NAME1>_<NAMES2>_<APP_NAME>_<VERSION>" + ".res", "w")  # VERSION = 1, 2 ou 3
    f.write(json.dumps(res))
    f.close()
