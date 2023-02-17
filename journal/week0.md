# Week 0 — Billing and Architecture

## Install AWS CLI

I installed AWS CLI as follows

Moved in to worksapce directory  `cd workspace`

```curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" ```

```unzip awscliv2.zip```

```sudo ./aws/install```


I Updated the `.gitpod.yml` to include the following task as shown

![image](https://user-images.githubusercontent.com/50416701/219223311-32974d4e-ddf2-489a-9e1e-4a08116d3cdb.png)


# Create a new User and Generate AWS Credentials

Using IAM Users Console, i created a new user "andy_bootcamp" and granted the user `AdministratorAccess` with security credential(via `Access Key`)

![image](https://user-images.githubusercontent.com/50416701/219513312-6889a1de-0f6b-4af5-a859-e0e810b151f9.png)

![iam_user](https://user-images.githubusercontent.com/50416701/219514933-c0a6beda-d6f6-4871-9c18-c768fea77602.jpg)



# Set Environment Variables for the AWS Account Credentials

`export AWS_ACCESS_KEY_ID="AK********"`

`export AWS_SECRET_ACCESS_KEY="VSGPhY**************"`

`export AWS_DEFAULT_REGION="eu-west-2"`

 I configured Gitpod to remember these credentials after relaunching our workspaces as follows
 
 `gp env AWS_ACCESS_KEY_ID="AK******"`

`gp env AWS_SECRET_ACCESS_KEY="VSGPhY***********"`

`gp env AWS_DEFAULT_REGION=eu-west-2`



# I checked if AWS CLI is working as follows

`aws sts get-caller-identity`

![aws_identity](https://user-images.githubusercontent.com/50416701/219276050-62a3581c-38da-4944-af41-c9fe9bebf4f2.png)


# Enable Billing

To create billing alarm, i created an SNS topic

`aws sns create-topic --name billing-alarm`

I created a subscription supply for the TopicARN and Email

aws sns subscribe \
    `--topic-arn="arn:aws:sns:eu-west-2:9*****23045:billing-alarm" \`
    
    `--protocol=email \`
    
  `--notification-endpoint=dba******@gmail.com`



![image](https://user-images.githubusercontent.com/50416701/219518870-b091ca9f-12b9-4a3f-9852-d6b92c309c39.png)





![image](https://user-images.githubusercontent.com/50416701/219518933-2e76713d-49c8-4ada-aed2-f98a0937637b.png)


# Create an AWS Budget

To obtain my AWS Account ID ,i run the following queries

`export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)`

`gp env AWS_ACCOUNT_ID="908743123045"`

I created the budget by supplying the Accound ID and updating `budget.json` file as follows

`aws budgets create-budget \`

    `--account-id $ACCOUNT_ID \`
    
    `--budget file://aws/json/budget.json \`
    
    `--notifications-with-subscribers file://aws/json/budget-notifications-with-subscribers.json`

![image](https://user-images.githubusercontent.com/50416701/219520003-5ebcf1d7-de8a-4021-99fb-7e6a5e109f61.png)


## Achitectural diagram was drawn in Lucid as shown in the url

https://lucid.app/lucidchart/34b06133-4f39-4ad1-b568-ca7c6e988e29/edit?viewport_loc=-138%2C-240%2C3330%2C1461%2C0_0&invitationId=inv_1d2954d3-bd8e-4015-8e3b-a32607b6e956
