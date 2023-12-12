import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

from split_datas import get_pickle_file

# Load train datas #####################################################################################################
print("[+] Loading train datas")
datas = get_pickle_file()
datas_http = pd.DataFrame(datas["HTTPWeb"])
datas_ssh = pd.DataFrame(datas["SSH"])
print("[+] Success\n")

x_train = datas_http.drop(columns=["Tag", "origin_file", "startTime"], axis=1)
y_train = datas_http["Tag"]

# Encode strings into numerical values
label_encoder = LabelEncoder()
X_train_encoded = x_train.apply(label_encoder.fit_transform)
y_train_encoded = label_encoder.fit_transform(y_train)

imputer = SimpleImputer(strategy='mean')
X_train_imputed = imputer.fit_transform(X_train_encoded)
########################################################################################################################

# Init KNN
random_forest_classifier = RandomForestClassifier(n_estimators=100)

# Train model
print("[+] Training model")
random_forest_classifier.fit(X_train_imputed, y_train_encoded)
print("[+] Success\n")

# Load test datas ######################################################################################################
print("[+] Loading test datas")
from load_http import get_dictionnaries
datas_http_test = get_dictionnaries()
datas_http_test = pd.DataFrame(flow['_source'] for flow in datas_http_test)

x_test = datas_http_test.drop(columns=["Tag"], axis=1)
y_test = datas_http_test["Tag"]

# Encode strings into numerical values
label_encoder = LabelEncoder()
X_test_encoded = x_test.apply(label_encoder.fit_transform)
y_test_encoded = label_encoder.fit_transform(y_test)

imputer = SimpleImputer(strategy='mean')
X_test_imputed = imputer.fit_transform(X_test_encoded)
print("[+] Success\n")

# Predict using test datas #############################################################################################
print("[+] Predicting using test datas")
y_pred = random_forest_classifier.predict(X_test_imputed)
print("[+] Success\n")
print(y_pred)

# Get probability of each prediction
y_pred_proba = random_forest_classifier.predict_proba(X_test_imputed)
print(y_pred_proba)
