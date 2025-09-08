from airflow.models import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import numpy as np

DATA_DIR = "/opt/airflow/data"

def prepare_data():
    import pandas as pd
    os.makedirs(DATA_DIR, exist_ok=True)
    print("---- Inside prepare_data component ----")
    # Load dataset
    df = pd.read_csv("https://raw.githubusercontent.com/palak-shete/dataset/refs/heads/main/Health_acitivity_classification.csv")
    df = df.dropna()
    df.to_csv(f'{DATA_DIR}/final_df.csv', index=False)
    
def split():
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder
    
    print("---- Inside train_test_split component ----")
    final_data = pd.read_csv(f'{DATA_DIR}/final_df.csv')
    target_column = 'activity'
    
    le = LabelEncoder()
    final_data[target_column] = le.fit_transform(final_data[target_column])
    
    X = final_data.drop(columns=[target_column]).select_dtypes(include=[np.number]).to_numpy(dtype=np.float64)
    y = final_data[target_column].to_numpy(dtype=np.int64).ravel()
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify= y, random_state=47)
    
    np.save(f'{DATA_DIR}/X_train.npy', X_train)
    np.save(f'{DATA_DIR}/X_test.npy', X_test)
    np.save(f'{DATA_DIR}/y_train.npy', y_train)
    np.save(f'{DATA_DIR}/y_test.npy', y_test)
    
    print("\n---- X_train ----")
    print("\n")
    print(X_train)
    
    print("\n---- X_test ----")
    print("\n")
    print(X_test)
    
    print("\n---- y_train ----")
    print("\n")
    print(y_train)
    
    print("\n---- y_test ----")
    print("\n") 
    print(y_test)
    
def training_basic_classifier():
    import pandas as pd
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
    import pickle
    
    print("---- Inside training_basic_classifier component ----")
    
    X_train = np.load(f'{DATA_DIR}/X_train.npy', allow_pickle=False)
    y_train = np.load(f'{DATA_DIR}/y_train.npy', allow_pickle=False)
    
    classifier = LogisticRegression(max_iter=1000)
    classifier.fit(X_train, y_train)
    
    with open(f'{DATA_DIR}/model.pkl', 'wb') as f:
        pickle.dump(classifier, f)
    
    print(f"\n logistic regression classifier is trained on health activity dataset and saved to PV location {DATA_DIR}/model.pkl \n")
    
def predict_on_test_data():
    import pandas as pd
    import numpy as np
    import pickle
    print("---- Inside predict_on_test_data component ----")
    with open(f'{DATA_DIR}/model.pkl', 'rb') as f:
        logistic_reg_model = pickle.load(f)
    X_test = np.load(f'{DATA_DIR}/X_test.npy', allow_pickle=False)
    y_pred = logistic_reg_model.predict(X_test)
    np.save(f'{DATA_DIR}/y_pred.npy', y_pred)
        
    print("\n---- Predicted classes ----")
    print("\n")
    print(y_pred)
        
def predict_prob_on_test_data():
    import pandas as pd
    import numpy as np
    import pickle
    print("---- Inside predict_prob_on_test_data component ----")
    with open(f'{DATA_DIR}/model.pkl', 'rb') as f:
        logistic_reg_model = pickle.load(f)
    X_test = np.load(f'{DATA_DIR}/X_test.npy', allow_pickle=False)
    y_pred_prob = logistic_reg_model.predict_proba(X_test)
    np.save(f'{DATA_DIR}/y_pred_prob.npy', y_pred_prob)
        
    print("\n---- Predicted probabilities ----")
    print("\n")
    print(y_pred_prob)
    
def get_metrics():
    import pandas as pd
    import numpy as np
    from sklearn.metrics import accuracy_score, precision_score, recall_score, log_loss, classification_report
    from sklearn import metrics
    print("---- Inside get_metrics component ----")
    y_test = np.load(f'{DATA_DIR}/y_test.npy', allow_pickle=False).ravel()
    y_pred = np.load(f'{DATA_DIR}/y_pred.npy', allow_pickle=False).ravel()
    y_pred_prob = np.load(f'{DATA_DIR}/y_pred_prob.npy', allow_pickle=False)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='micro')
    recall = recall_score(y_test, y_pred, average='micro')
    entropy = log_loss(y_test, y_pred_prob)
    
    print(metrics.classification_report(y_test, y_pred, zero_division=0))
    
    print("\n Model Metrics:", {'accuracy': round(acc, 2), 'precision': round(prec, 2), 'recall': round(recall, 2), 'log_loss': round(entropy, 2)})
    
with DAG(
    dag_id = 'ml_pipeline_demo',
    schedule = '@daily',
    start_date = datetime(2025, 9, 8),
    catchup = False,
) as dag:
    
    task_prepare_data = PythonOperator(
        task_id='prepare_data',
        python_callable=prepare_data,
    )
    
    task_split = PythonOperator(
        task_id='train_test_split',
        python_callable=split,
    )
    task_training_basic_classifier = PythonOperator(
        task_id='training_basic_classifier',
        python_callable=training_basic_classifier,
    )
    task_predict_on_test_data = PythonOperator(
        task_id='predict_on_test_data',
        python_callable=predict_on_test_data,
    )
    task_predict_prob_on_test_data = PythonOperator(
        task_id='predict_prob_on_test_data',
        python_callable=predict_prob_on_test_data,
    )
    task_get_metrics = PythonOperator(
        task_id='get_metrics',
        python_callable=get_metrics,
    )
    
    task_prepare_data >> task_split >> task_training_basic_classifier >> task_predict_on_test_data >> task_predict_prob_on_test_data >> task_get_metrics
    