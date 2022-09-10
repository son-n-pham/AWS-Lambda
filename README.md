# AWS Lambda
This is the note for AWS Lambda

## Price

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

