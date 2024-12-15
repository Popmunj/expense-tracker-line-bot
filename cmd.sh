docker build --platform linux/arm64 -t docker-image:test .

aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account_id>.dkr.ecr.<region>.amazonaws.com
aws ecr create-repository --repository-name <repo_name> --region <region> --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE

docker tag docker-image:test  <account_id>.dkr.ecr.<region>.amazonaws.com:latest
docker push  <account_id>.dkr.ecr.<region>.amazonaws.com:latest

aws lambda create-function \
  --function-name handler \
  --package-type Image \
  --code ImageUri=<account_id>.dkr.ecr.<region>.amazonaws.com:latest \
  --role <role_arn> \
  --architectures arm64

# build and push again before updating
aws lambda update-function-code \
  --function-name handler \
  --image-uri <account_id>.dkr.ecr.<region>.amazonaws.com:latest \
  --publish