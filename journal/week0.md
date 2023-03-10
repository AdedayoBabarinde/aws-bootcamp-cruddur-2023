# Week 0 — Billing and Architecture

## Install AWS CLI

I installed AWS CLI for linux using the following sets of command

```curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" ```

```unzip awscliv2.zip```

```sudo ./aws/install```

I followed the instruction on [AWS CLI documentation page](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)



I Updated the `.gitpod.yml` to include the following task as shown

![image](https://user-images.githubusercontent.com/50416701/219223311-32974d4e-ddf2-489a-9e1e-4a08116d3cdb.png)


# Create a new User and Generate AWS Credentials

Using IAM Users Console, i created a new user "andy_bootcamp" and granted the user `AdministratorAccess` with security credential(via `Access Key`)

![image](https://user-images.githubusercontent.com/50416701/219513312-6889a1de-0f6b-4af5-a859-e0e810b151f9.png)

![iam_user](https://user-images.githubusercontent.com/50416701/219514933-c0a6beda-d6f6-4871-9c18-c768fea77602.jpg)



# Set Environment Variables for the AWS Account Credentials

`export AWS_ACCESS_KEY_ID="AK********"`

`export AWS_SECRET_ACCESS_KEY="VS**************"`

`export AWS_DEFAULT_REGION="eu-west-2"`

 I configured Gitpod to remember these credentials after relaunching our workspaces as follows
 
 `gp env AWS_ACCESS_KEY_ID="AK******"`

`gp env AWS_SECRET_ACCESS_KEY="VSG***********"`

`gp env AWS_DEFAULT_REGION=eu-west-2`



# I checked if AWS CLI is working as follows

`aws sts get-caller-identity`



# Enable Billing

To create billing alarm, i created an SNS topic

`aws sns create-topic --name billing-alarm`

I created a subscription supply for the TopicARN and Email

aws sns subscribe \
    `--topic-arn="arn:aws:sns:eu-west-2:9*****23045:billing-alarm" \`
    
    `--protocol=email \`
    
  `--notification-endpoint=dba******@gmail.com`


![Create SNS Topic](assets/sns.png)



# Create an AWS Budget

To obtain my AWS Account ID ,i run the following queries

`export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)`

`gp env AWS_ACCOUNT_ID="908********"`

I created the budget by supplying the Accound ID and updating `budget.json` file as follows

`aws budgets create-budget \`

    `--account-id $ACCOUNT_ID \`
    
    `--budget file://aws/json/budget.json \`
    
    `--notifications-with-subscribers file://aws/json/budget-notifications-with-subscribers.json`

![Create a Budget](assets/create%20budget.png)

![Created Budget](assets/budget.png)


## Recreate Logical Achitectural Diagram 

I recreated the Logical Achitectural diagram using Lucid as shown in the url

[Lucid Charts Share Link ](https://lucid.app/lucidchart/34b06133-4f39-4ad1-b568-ca7c6e988e29/edit?viewport_loc=-138%2C-240%2C3330%2C1461%2C0_0&invitationId=inv_1d2954d3-bd8e-4015-8e3b-a32607b6e956)

![Cruddur Logical Design](assets/logical_architectural_diagram.jpg)


## Homework Challenges

[`json` file used to create sample budget](https://github.com/AdedayoBabarinde/aws-bootcamp-cruddur-2023/blob/main/aws/json/budget.json)

[`json` file for alarm configuration](https://github.com/AdedayoBabarinde/aws-bootcamp-cruddur-2023/blob/main/aws/json/alarm_config.json)
