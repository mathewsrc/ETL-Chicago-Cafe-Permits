## Huggingface Hub 

This project implements some features of Hugging Face Hub such as: models and datasets 

## Setup

Create virtual environment

```bash
make setup
```
Activate virtual environment

On Windows

```bash
source .env/Script/activate
```
On Linux

```bash
source .env/bin/activate
```

Installing dependencies

```bash
make install
```

### Create a Huggingface account
1. First use the command below to login to Hugging Face 
```py
huggingface-cli login on terminal
```
2. Copy a new token 

#paste image here

3. Paste token in terminal

## Running

Using CLI with a local example


Summarization

Files

```py
python app/main.py summarize --file examples/polars.txt
```

Text
```py
python app/main.py summarize --text "You can use the huggingface_hub library to create, delete, update and retrieve information from repos. You can also download files from repos or integrate them into your library! For example, you can quickly load a Scikit-learn model with a few lines."
```

Sentiment Analysis

Files

```py
python app/main.py sentiment --file examples/polars.txt
```

Text
```py
python app/main.py sentiment --text "You can use the huggingface_hub library to create, delete, update and retrieve information from repos. You can also download files from repos or integrate them into your library! For example, you can quickly load a Scikit-learn model with a few lines."
```

Pushing model to Hugging Face

4. Create a new model repo: 
    ```huggingface-cli repo create demo-onx --type model```
5. Create a directory and clone Huggingface repo
6. Push your model by running:
    ```git add model```
    ```git push```