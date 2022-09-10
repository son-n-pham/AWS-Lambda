# AWS Lambda
This is the note for AWS Lambda. The content was from Udemy course AWS Lambda - A Practical Guide from Daniel who has a Youtube channel Be A Better Dev

Presentation from Daniel can be found below:
https://docs.google.com/presentation/d/1UBgzd0WdBlKygAuTEEhFTMrRiwTKD5ebZvcaYzL68BE/edit#slide=id.g35f391192_04

## Pricing

![image](https://user-images.githubusercontent.com/79841341/189026256-2eb2cf83-235f-477d-98ae-6f3d866b26fd.png)

### Tips to save cost:
- Start with low memory settings
- Once collecting enough invocation history, use the Compute Optimizer Tool to optimze memory provision and running time of function
- 1 Million free requests per month and 400,000 GB Seconds
- Use lambda cost calculator

### Decomposing a Function Execution:
- Steps:
  - Code download:
    - Depending on programming language and whether we run that lambda or not
  - Start execution environment
  - Execute init code: It is everything outside Lambda's handler function
    - Try to specific when import environment
  - Execute handler code

![image](https://user-images.githubusercontent.com/79841341/189029220-d98a7351-2104-4923-99d7-bf9543045913.png)

- Strategies to minimize cold start
  - Minimize number of library dependencies
  - Only import what you need
  - Raise memory configuration: It is not only increasing memory but also computer nodes behind the scene: It can be an expensive option
  - Utilize provisioned concurrency: Keep Lambda always in the warm state by having some lambda containers behind the scene. It is an expensive option

## Concurrency and Throttling
### Lambda Concurrency:
- Number of requests being served at a given moment
- New containers are spawned for each concurrent request
- Concurrency is a major scaling consideration, and can cause applications to fail due to **Throttling**
- Default 1000 units of concurrency per AWS account per region.
- Unreserved, Reserved, and Provisioned

![image](https://user-images.githubusercontent.com/79841341/189031910-d4b2ca06-0ef6-4558-90bc-cb9cf43391f5.png)

![image](https://user-images.githubusercontent.com/79841341/189033208-3a769f51-2aac-485b-b6e6-19f70548ec38.png)

### Lambda Throttling aka RateExceeded
- Throttling is when Lambda rejects a request
- Occurs when in flight invocations exceeds available concurrency

### Tips:
- Alarm on throttles for early indicators of issues by Cloudwatch
- Evaluate your concurrency needs and plan accordingly
- Have your clients use Exponential Backoff to avoid retry storms
- Raising Memory Limit can help, but be careful
- Use provision concurrency to avoid cold starts, but be careful

## Configuration

### Version:

- Version is optional.
- New upload default to $LATEST version. When create a version, $LASTEST is assigned automatically to the new version if the new version does not have any specific name.

![image](https://user-images.githubusercontent.com/79841341/189034258-e4247502-f91d-4b02-88f4-8786536fcd0b.png)

### Aliases

![image](https://user-images.githubusercontent.com/79841341/189034688-9fc9e60d-ffc0-4315-85b0-70c983a0b3e8.png)

Example of Aliases:
- In the begining, we creat Python version 1, and assign Alias prod to that version:

![image](https://user-images.githubusercontent.com/79841341/189459673-90a0623b-7177-49f8-9d5b-66fc31013430.png)

- Now we have version 2, $LATEST version is automatically moved from version 1 to version 2. Alias is still kept at version 1.

![image](https://user-images.githubusercontent.com/79841341/189460061-595577f5-ce0f-4f7e-b12d-2195881b59c7.png)

-Then we create version 3, again $LATEST version is automatically moved from version 2 to version 3. Version 3's performance is good, thus we decide to use it. So we move prod Alias to version 1 to version 3 to direct all flow to that version.

![image](https://user-images.githubusercontent.com/79841341/189460175-d1f7d212-1468-4498-9fa0-96deca661c23.png)

- Interestingly, we can assign weight to different version/alias

### Environment

![image](https://user-images.githubusercontent.com/79841341/189469297-05a17d8a-f7d7-46dc-b4a8-d30dd9b378fe.png)

- AWS environment is stored. We can access it with os.environ
- We can also add new key, value into the environment

![image](https://user-images.githubusercontent.com/79841341/189469210-c35bac71-b71e-437a-a017-ce7845598489.png)

- The below code in Lambda would list all AWS environment's keys and values to dictionary.
```python
import os

def lambda_handler(event, context):
    allAWSEnv = os.environ
    print(f"This is all environment variables: {allAWSEnv}")
    
    # I added a environment variable son_pham
    # Now I access and print that variable out
    sonPham = os.environ["son_pham"]
    print(f"This is the value of environment variable son_pham: {sonPham}")
```

![image](https://user-images.githubusercontent.com/79841341/189471555-1febc6cc-6ef2-4d3f-b446-1addba331f26.png)


### Virtual Private Cloud (VPC)
- Is isolated and private network within AWS
- Public abd Private Subnets
- Critical for security and apps with compliance guidelines

#### VPC and Lambda
- Only necessary when the function needs to access resources not accessible over public internet such as RDS or ElasticSearch in private subnet
- Behind the scenes, Lambda creates Elastic Network Interfaces (ENI)s for each subnet the function is deployed into. This used to be the issue with cold start latency, but not anymore.
- VPC Endpoints can be used to communicate with some AWS services privately
- Below is an example that Lambda cannot access directly to internet, but have to go through NAT Gateway in Public Subnet, and NAT Gateway to got Internet Gateway to go out. To connect S3, instead of going out to internet to connect (which cause latency and security issue), we can config VPC for Lambda to connect with S3.

![image](https://user-images.githubusercontent.com/79841341/189471873-74ba0b65-ca84-4485-85be-cf27730e74fd.png)

## Monitoring:
### Logging
- All logs are automatically  saved in CloudWatch

![image](https://user-images.githubusercontent.com/79841341/189477065-24dab305-ed70-4b65-a8c0-406b42a76670.png)

![image](https://user-images.githubusercontent.com/79841341/189477092-adb8cc78-e3fc-4c7b-b1fd-6ee9b2051608.png)

### Metric Filters
- Allow to write patterns (similar to REGEX) to extract metrics from log times
- Much cheaper than PutMetric
- More suitable for high traffic application

### Cloudwatch Logs Insight
- Search for patterns across multiple functions at one
- Pay per use
- Query similar to SQL

![image](https://user-images.githubusercontent.com/79841341/189477178-d80ac9ee-97b5-479a-8dc5-4b5b362be1e7.png)

### Tips
- Don't be overly verbose with Logging
- Embed log lines with important ids to make tracing easier
- Use Cloudwatch Logs Insights for fuzzy searching
- Set up a log retention policy or archive regularly

### Hands-on

Create the below function to the result when having error

```python
def lambda_handler(event, context):
    print("UploadError 1")
```

Then we go to CloudWatch to setup the metric filters in Log groups after selecting the targetted function.

![image](https://user-images.githubusercontent.com/79841341/189478045-e87828e1-cd7e-4129-9ebf-913dea6f9f7a.png)

We then define the pattern to capture, and test if the pattern is working

![image](https://user-images.githubusercontent.com/79841341/189478143-106acb35-c081-4f3e-802a-c93602cfe587.png)

Move to the next page to complete the setup for metric filter.

![image](https://user-images.githubusercontent.com/79841341/189478274-f30eaa2c-ec48-4d1b-aa0f-ca41e10001cc.png)

## Performance Tuning and Observability

We can use an open-source step function AWS Lambda Power Tuning to optimize memory and cost

https://serverlessrepo.aws.amazon.com/applications/arn:aws:serverlessrepo:us-east-1:451282441545:applications~aws-lambda-power-tuning

We use the above tool to optimize the below function

