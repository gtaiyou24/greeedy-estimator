FROM python:3.9

# MeCab,OpenCVをインストール
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8 file git make curl xz-utils sudo build-essential gcc libgl1-mesa-dev

# mecab-ipadic-neologdをインストール
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
    && cd mecab-ipadic-neologd \
    && bin/install-mecab-ipadic-neologd -n -a -y

ARG project_dir=/app/
COPY ./app $project_dir
COPY requirements.txt $project_dir
WORKDIR $project_dir

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8080
ENTRYPOINT ["python", "start_sagemaker.py"]
