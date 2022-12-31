# Greeedy Estimator

Greeedyサービス内における推論領域を扱うシステム

## Usage
### 1. Upload dataset files to S3

```shell
aws s3 cp ./data/<filename>.csv s3://your-bucket/path/to/<filename>.csv
```

| estimator name | command |
|:-------:|:--------|
| Item Color Estimator | `aws s3 cp ./data/items.csv s3://greeedy-estimator/dataset/items.csv` |

 - [greeedy-estimator - S3 bucket](https://s3.console.aws.amazon.com/s3/buckets/greeedy-estimator?region=ap-northeast-1&tab=objects)

### 2. Build and push the docker image to ECR

```shell
./scripts/build_and_push_ecr.sh greeedy-estimator
```

 - [greeedy-estimator - Elastic Container Registry](https://ap-northeast-1.console.aws.amazon.com/ecr/repositories/private/684886458640/greeedy-estimator?region=ap-northeast-1)

### 3. Train a model with SageMaker

```shell
python scripts/train.py \
    --dataset-path s3://greeedy-estimator/dataset \
    --artifact-path s3://greeedy-estimator/artifacts \
    --image-uri xxxxxxxxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/greeedy-estimator \
    --execution-role arn:aws:iam::xxxxxxxxxxxx:role/SageMakerExecutionRole
```

 - [Amazon SageMaker > トレーニングジョブ](https://ap-northeast-1.console.aws.amazon.com/sagemaker/home?region=ap-northeast-1#/jobs)
 - [IAM Management Console](https://us-east-1.console.aws.amazon.com/iamv2/home?region=ap-northeast-1#/roles)

### 4. Deploy the trained model

```shell
python scripts/deploy.py \
    --endpoint-name your-endpoint-name \
    --training-job training-job-name
```

### 5. Invoke the endpoint

```shell
python scripts/predict.py -n your-endpoint-name data/test.json
```

### 6. Delete the endpoint

```shell
aws sagemaker delete-endpoint --endpoint-name your-endpoint-name
```

## Local mode
### 1. Train a model on your local machine

```bash
docker build -t greeedy-estimator:latest .

docker container run --rm \
    -v `pwd`/app:/app \
    -v `pwd`/data:/app/data \
    greeedy-estimator:latest train --local
```

### 2. Serve the endpoint on your local machine

```bash
python -m app serve --local --port 8080

# on your docker container
docker build -t greeedy-estimator:latest .
docker container run --rm \
    -v `pwd`/app:/app \
    -v `pwd`/data:/data \
    greeedy-estimator:latest serve --local --port 8080
```

### 3. Train a model with local mode

```bash
python scripts/train.py \
    --local \
    --dataset-path file://`pwd`/data/dataset \
    --artifact-path file://`pwd`/data/artifact \
    --image-uri xxxxxxxxxxxx.dkr.ecr.ap-northeast-1.amazonaws.com/greeedy-estimator \
    --execution-role dummy/dummy
```