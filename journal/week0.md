# Week 0 — Billing and Architecture

##Install AWS CLI

I installed AWS CLI as follows

Moved in to worksapce directory  `cd workspace`

```curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" ```

```unzip awscliv2.zip```

```sudo ./aws/install```


I Updated the `.gitpod.yml` to include the following task as shown

![image](https://user-images.githubusercontent.com/50416701/219223311-32974d4e-ddf2-489a-9e1e-4a08116d3cdb.png)


#Create a new User and Generate AWS Credentials

`aws sts get-caller-identity`

![aws_identity](https://user-images.githubusercontent.com/50416701/219276050-62a3581c-38da-4944-af41-c9fe9bebf4f2.png)

