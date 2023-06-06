FROM jupyter/scipy-notebook:2022-06-02

RUN mkdir my-model predict-code output script
ENV MODEL_DIR=/home/jovyan/my-model
ENV LOCAL_PATH=/home/jovyan/data
ENV MODEL_FILE_LDA=clf_lda.joblib
ENV MODEL_FILE_NN=clf_nn.joblib

RUN pip install --no-cache-dir joblib==1.1.0

COPY test.csv /home/jovyan/predict-code/test.csv
COPY clf_nn.joblib /home/jovyan/my-model/clf_nn.joblib
COPY inference.py /home/jovyan/predict-code/inference.py
COPY a.txt /home/jovyan/output/a.txt

HEALTHCHECK CMD curl -fs http://localhost/ || exit 1

#從本地資料夾內copy run.sh檔案
COPY run.sh /home/jovyan/script/run.sh
ENTRYPOINT ["/bin/bash", "/home/jovyan/script/run.sh"]
