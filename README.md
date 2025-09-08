# MLOps-Airflow-Pipeline
End-to-end MLOps pipeline using Apache Airflow and Docker for health activity classification.

## 🌀 My First MLOps Pipeline with Airflow 🚀

Hey there! 👋
This is my little adventure into the world of MLOps + Airflow + Docker. Basically, I built a pipeline that:

- Grabs a health activity dataset 🏃‍♀️

- Cleans it up ✨

- Splits it into train/test 📊

- Trains a Logistic Regression model 🤖

- Makes predictions 🔮

- And finally tells me how good (or bad 😅) my model is.

## 🔧 What’s Inside?

- Airflow DAG → Orchestrates the whole pipeline like a boss 🕹️

- Docker setup → Because who doesn’t love containers 🐳

- Logs & Outputs → Stored in the data/ folder (CSV, NPY files, and even a trained model .pkl).

## ⚙️ How to Run It?

- Clone this repo

- Run docker-compose up airflow-init then docker-compose up

- Open http://localhost:8080

- Find the DAG named ml_pipeline_demo → switch it ON → hit Trigger

- Sit back, sip your coffee ☕, and watch the magic happen ✨

## 📊 What You’ll See

- Train/test split logs with actual values

- A trained logistic regression model

- Predictions + prediction probabilities

- Metrics like Accuracy, Precision, Recall, and even a fancy Classification Report

## 🌟 What’s Next?

- Try out cooler models (Random Forest, XGBoost maybe?) 🌳

- Add monitoring & versioning (MLflow I’m looking at you 👀)

- Deploy the model so it can serve predictions live 🌐

## 👩‍💻 About Me

I’m Palak ✨ a final year B.Tech student who loves mixing AI/ML with real-world fun stuff 💻💡.
This project was my first step into the MLOps world, and trust me—it was chaotic, but I survived 😅.
