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

### Lambda Throttling aka RateExceeded
- Throttling is when Lambda rejects a request
- Occurs when in flight invocations exceeds available concurrency
