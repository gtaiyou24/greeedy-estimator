#!/bin/bash

algorithm_name=$1
algorithm_name=${algorithm_name:-greeedy-estimator}

profile=${AWS_PROFILE:-}
account=$(aws sts get-caller-identity --query Account --output text --profile "${profile}")

# Get the region defined in the current configuration (default to us-west-2 if none defined)
region=$(aws configure get region --profile "${profile}")
region=${region:-ap-northeast-1}

echo "account: ${account}  region: ${region}  profile: ${profile}"

fullname="${account}.dkr.ecr.${region}.amazonaws.com/${algorithm_name}:latest"

# If the repository doesn't exist in ECR, create it.
aws ecr describe-repositories --repository-names "${algorithm_name}" --profile "${profile}" 2>&1

if [ $? -ne 0 ]
then
    aws ecr create-repository --repository-name "${algorithm_name}" --profile "${profile}"
fi

aws ecr get-login-password --region ${region} --profile "${profile}" | docker login --username AWS --password-stdin ${account}.dkr.ecr.${region}.amazonaws.com

# Build the docker image locally with the image name and then push it to ECR
# with the full name.

docker build -t ${algorithm_name} . -f ./Dockerfile.aws.sagemaker
docker tag ${algorithm_name} ${fullname}

docker push ${fullname}
