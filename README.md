# WorkloadSecurity-AWS-SNS-S3 Integration
CloudFormation template for Trend Micro Cloud One Workload Security Events - Amazon SNS Integration with Amazon CloudWatch Logs


## Setup Instructions

Step 1: Create a Cloud One Workload Security API Key. Refer to the Workload Security documentation for steps to create this API key - https://cloudone.trendmicro.com/docs/workload-security/api-send-request/#create-an-api-key

Step 2: Run the CloudFormation template `workloadsecurity-events-aws-sns-cloudformation.json`


## How it works

The CloudFormation template creates the following resources -

- Amazon SNS Topic
    - Workload Security sends security events from various Workload Security modules, like System, Anti-Malware, Web Reputation, Application Control, Integrity Monitoring, Log Inspection, Firewall and Intrusion Prevention (IPS) events.
    - SNS Messages are encrypted with the Default AWS Managed key (AWS-CMK) for SNS (`arn:aws:kms:<AWS::Region>:<AWS::AccountId>:alias/aws/sns`).

- AWS Lambda Function (C1WSLambdaSnsS3Writer)
    - Compute to read Amazon SNS messages and write the security events to Amazon S3 bucket.
    - Can be used to action auto-remediation tasks within the environment. Some use-cases may be included in this code repository.

- Amazon S3 Bucket
    - Storage location for security events. 
    - Can be queried with Amazon Athena.
    - Objects are encrypted by default with the Default SSE-S3 encryption.
    - Objects can only be accessed via HTTPS.

- IAM User
    - Creates an IAM User for Workload Security to post to SNS Topic.

- IAM User Access Key
    - Required. Access and secret keys for the IAM User to authenticate AWS API calls.
    - Access and secret keys are never shared in the CloudFormation Outputs section and sent directly to Workload Security using APIs.

- AWS IAM Policy for SNS
    - Permissions for the IAM User to publish to the SNS Topic.

- AWS Lambda Function (C1WSConfigureSIEMLambdaFunction)
    - Configuration logic to call Workload Security APIs and configure Workload Security for SNS Event Forwarding.
    - You can see the configuration on the Workload Security Console: **Administration > System Settings > Event Forwarding**

- Custom CloudFormation Resource (CloudOneWorkloadSecurityConfigResource)
    - Runs the configuration logic during **Create** and **Update** Stack to populate the following fields on the Workload Security console.
        - SNS Topic Arn
        - Access key and
        - Secret key

- AWS IAM Role for Lambda functions
    - Use the AWS Managed Policy "AWSLambdaBasicExecutionRole" for AWS Lambda.

- AWS IAM Policy for Lambda Service
    - Permissions for the Lambda functions to write to the created S3 bucket.

### Related Projects

| GitHub Repository Name  | Description |
| ------------- | ------------- |
| [cloudOneWorkloadSecurityDemo](https://github.com/GeorgeDavis-TM/cloudOneWorkloadSecurityDemo) | Run an attack simulation on your workload to test policy events and alerts |
| [WorkloadSecurityConnector-AWS](https://github.com/GeorgeDavis-TM/WorkloadSecurityConnector-AWS) | Automation scripts to setup the AWS Connector on Trend Micro Cloud One Workload Security / Deep Security (On-Prem on AWS) |

## Contributing

If you encounter a bug or think of a useful feature, or find something confusing in the docs, please
**[Create a New Issue](https://github.com/GeorgeDavis-TM/WorkloadSecurity-AWS-SNS-S3/issues/new)**

 **PS.: Make sure to use the [Issue Template](https://github.com/GeorgeDavis-TM/WorkloadSecurity-AWS-SNS-S3/tree/master/.github/ISSUE_TEMPLATE)**

We :heart: pull requests. If you'd like to fix a bug or contribute to a feature or simply correct a typo, please feel free to do so.

If you're thinking of adding a new feature, consider opening an issue first to
discuss it to ensure it aligns to the direction of the project (and potentially
save yourself some time!).

