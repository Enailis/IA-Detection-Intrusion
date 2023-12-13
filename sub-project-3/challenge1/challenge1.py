import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder

from split_datas import get_pickle_file


def split_ip(ip: str) -> list:
    """Split an IP address given as a string into a list of integers."""
    return list(map(int, ip.split('.')))

# Load train datas #####################################################################################################
print("[+] Loading train datas")
datas = get_pickle_file()
datas_http = pd.DataFrame(datas["HTTPWeb"])
datas_ssh = pd.DataFrame(datas["SSH"])
print("[+] Success\n")

# Sort columns by alphabetical order
datas_http = datas_http.reindex(sorted(datas_http.columns), axis=1)
datas_ssh = datas_ssh.reindex(sorted(datas_ssh.columns), axis=1)

# Print first 5 rows
print(datas_http.head())
print(datas_http.columns)
print(datas_ssh.head())
print(datas_ssh.columns)

x_train_http = datas_http.drop(columns=["Tag", "origin_file", "sensorInterfaceId", "sourcePayloadAsBase64", "sourcePayloadAsUTF", "destinationPayloadAsUTF", "destinationPayloadAsBase64"], axis=1)
y_train_http = datas_http["Tag"]

x_train_ssh = datas_ssh.drop(columns=["Tag", "origin_file", "sensorInterfaceId", "sourcePayloadAsBase64", "sourcePayloadAsUTF", "destinationPayloadAsUTF", "destinationPayloadAsBase64"], axis=1)
y_train_ssh = datas_ssh["Tag"]

# Edit source and destination IP
print("\n[+] Editing source and destination IP")
x_train_http[['sourceIP1', 'sourceIP2', 'sourceIP3', 'sourceIP4']] = x_train_http['source'].apply(split_ip).apply(pd.Series)
x_train_http[['destinationIP1', 'destinationIP2', 'destinationIP3', 'destinationIP4']] = x_train_http['destination'].apply(split_ip).apply(pd.Series)

x_train_ssh[['sourceIP1', 'sourceIP2', 'sourceIP3', 'sourceIP4']] = x_train_ssh['source'].apply(split_ip).apply(pd.Series)
x_train_ssh[['destinationIP1', 'destinationIP2', 'destinationIP3', 'destinationIP4']] = x_train_ssh['destination'].apply(split_ip).apply(pd.Series)

# Drop source and destination IP
x_train_http = x_train_http.drop(columns=['source', 'destination'])
x_train_ssh = x_train_ssh.drop(columns=['source', 'destination'])
print("[+] Success\n")

# Encode strings into numerical values
label_encoder = LabelEncoder()

x_train_encoded_http = x_train_http.apply(label_encoder.fit_transform)
y_train_encoded_http = label_encoder.fit_transform(y_train_http)

x_train_encoded_ssh = x_train_ssh.apply(label_encoder.fit_transform)
y_train_encoded_ssh = label_encoder.fit_transform(y_train_ssh)

imputer = SimpleImputer(strategy='mean')
X_train_imputed_http = imputer.fit_transform(x_train_encoded_http)
X_train_imputed_ssh = imputer.fit_transform(x_train_encoded_ssh)
########################################################################################################################

# Init RandomForestClassifier
# random_forest_classifier_http = RandomForestClassifier(n_estimators=100)
# random_forest_classifier_ssh = RandomForestClassifier(n_estimators=100)

# Init KNNClassifier
knn_classifier_http = KNeighborsClassifier(n_neighbors=5)
knn_classifier_ssh = KNeighborsClassifier(n_neighbors=5)

# Train model
print("[+] Training model")
print("[+] --> HTTPWeb")
# random_forest_classifier_http.fit(X_train_imputed_http, y_train_encoded_http)
knn_classifier_http.fit(X_train_imputed_http, y_train_encoded_http)
print("[+] --> SSH")
# random_forest_classifier_ssh.fit(X_train_imputed_ssh, y_train_encoded_ssh)
knn_classifier_ssh.fit(X_train_imputed_ssh, y_train_encoded_ssh)
print("[+] Success\n")

# Load test datas ######################################################################################################
print("[+] Loading test datas")
from load_file import get_dictionnaries
datas_http_test = get_dictionnaries("challenge1_data/benchmark_HTTPWeb_test.xml")
datas_http_test = pd.DataFrame(flow['_source'] for flow in datas_http_test)

datas_ssh_test = get_dictionnaries("challenge1_data/benchmark_SSH_test.xml")
datas_ssh_test = pd.DataFrame(flow['_source'] for flow in datas_ssh_test)

# Sort columns by alphabetical order
datas_http_test = datas_http_test.reindex(sorted(datas_http_test.columns), axis=1)
datas_ssh_test = datas_ssh_test.reindex(sorted(datas_ssh_test.columns), axis=1)

# Print first 5 rows
print(datas_http_test.head())
print(datas_http_test.columns)
print(datas_ssh_test.head())
print(datas_ssh_test.columns)

x_test_http = datas_http_test.drop(columns=["Tag"], axis=1)
x_test_ssh = datas_ssh_test.drop(columns=["Tag"], axis=1)

# Edit source and destination IP
x_test_http[['sourceIP1', 'sourceIP2', 'sourceIP3', 'sourceIP4']] = x_test_http['source'].apply(split_ip).apply(pd.Series)
x_test_http[['destinationIP1', 'destinationIP2', 'destinationIP3', 'destinationIP4']] = x_test_http['destination'].apply(split_ip).apply(pd.Series)

x_test_ssh[['sourceIP1', 'sourceIP2', 'sourceIP3', 'sourceIP4']] = x_test_ssh['source'].apply(split_ip).apply(pd.Series)
x_test_ssh[['destinationIP1', 'destinationIP2', 'destinationIP3', 'destinationIP4']] = x_test_ssh['destination'].apply(split_ip).apply(pd.Series)

# Drop source and destination IP
x_test_http = x_test_http.drop(columns=['source', 'destination', "sourcePayloadAsBase64", "sourcePayloadAsUTF", "destinationPayloadAsUTF", "destinationPayloadAsBase64"])
x_test_ssh = x_test_ssh.drop(columns=['source', 'destination', "sourcePayloadAsBase64", "sourcePayloadAsUTF", "destinationPayloadAsUTF", "destinationPayloadAsBase64"])

# Encode strings into numerical values
X_test_encoded_http = x_test_http.apply(label_encoder.fit_transform)
X_test_encoded_ssh = x_test_ssh.apply(label_encoder.fit_transform)

X_test_imputed_http = imputer.fit_transform(X_test_encoded_http)
X_test_imputed_ssh = imputer.fit_transform(X_test_encoded_ssh)
print("[+] Success\n")

# Predict using test datas #############################################################################################
print("[+] Predicting using test datas")
print("[+] --> HTTPWeb")
# y_pred_http = random_forest_classifier_http.predict(X_test_imputed_http)
y_pred_http = knn_classifier_http.predict(X_test_imputed_http)
print("[+] --> SSH")
# y_pred_ssh = random_forest_classifier_ssh.predict(X_test_imputed_ssh)
y_pred_ssh = knn_classifier_ssh.predict(X_test_imputed_ssh)

print("[+] Success\n")
print(f'HTTP Prediction :', y_pred_http)
print(f'Number of 1 {len([i for i in y_pred_http if i == 1])}, number of 0 {len([i for i in y_pred_http if i == 0])}')
print(f'SSH Prediction :', y_pred_ssh)
print(f'Number of 1 {len([i for i in y_pred_ssh if i == 1])}, number of 0 {len([i for i in y_pred_ssh if i == 0])}')

# Get probability of each prediction
# y_pred_proba_http = random_forest_classifier_http.predict_proba(X_test_imputed_http)
# y_pred_proba_ssh = random_forest_classifier_ssh.predict_proba(X_test_imputed_ssh)
y_pred_proba_http = knn_classifier_http.predict_proba(X_test_imputed_http)
y_pred_proba_ssh = knn_classifier_ssh.predict_proba(X_test_imputed_ssh)
print(f'http :', y_pred_proba_http)
print(f'ssh :', y_pred_proba_ssh)

# Pourcentage de 1 et de 0
http_attack = len([i for i in y_pred_http if i == 1]) / len(y_pred_http)
http_normal = len([i for i in y_pred_http if i == 0]) / len(y_pred_http)

ssh_attack = len([i for i in y_pred_ssh if i == 1]) / len(y_pred_ssh)
ssh_normal = len([i for i in y_pred_ssh if i == 0]) / len(y_pred_ssh)

# Plot pie chart
import matplotlib.pyplot as plt

labels = 'Attack', 'Normal'
sizes_http = [http_attack, http_normal]
sizes_ssh = [ssh_attack, ssh_normal]
explode = (0, 0.1)

fig1, ax1 = plt.subplots()
ax1.pie(sizes_http, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')
ax1.set_title('HTTPWeb')
plt.show()

fig2, ax2 = plt.subplots()
ax2.pie(sizes_ssh, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax2.axis('equal')
ax2.set_title('SSH')
plt.show()

# Create result file ###################################################################################################
print("[+] Creating result file")
from result_file import create_result_file

create_result_file(y_pred_http, y_pred_proba_http, "RandomForest", "HTTPWeb", "1")
create_result_file(y_pred_ssh, y_pred_proba_ssh, "RandomForest", "SSH", "1")

print("[+] Success\n")