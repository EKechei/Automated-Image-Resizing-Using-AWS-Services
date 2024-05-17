# Automated-Image-Resizing-Using-AWS-Services

![image](https://github.com/EKechei/Automated-Image-Resizing-Using-AWS-Services/assets/128794751/e3125421-c579-4a2b-9524-2e0a26c351ab)



# Project Description:
This project focuses on building an automated system for image processing and management within the AWS ecosystem. The goal is to streamline the handling of images by automatically resizing them and transferring them to a designated storage location while keeping stakeholders informed through notifications.

# AWS services:
1. AWS Lambda
2. Amazon S3
3. Amazon SNS

# Key Features:
1. Image processing automation: Automatically resize and optimize images upon upload.
2. Secure storage: Store processed images in a secure and reliable S3 bucket.
3. Real-time notifications: Receive immediate updates about image processing via SNS.
4. Scalable architecture: Design for scalability to handle image processing demands.
5. Cost-efficient solution: Leverage AWS serverless technologies to minimize operational costs.

# Step 1: Create both Source and Destination S3 Buckets
In the S3 Console, click Create Bucket and create your buckets.

![image](https://github.com/EKechei/Automated-Image-Resizing-Using-AWS-Services/assets/128794751/df610d3b-f085-4a7d-bbaf-f0413fd5c143)

# Step 2: Create SNS Notification
In the SNS Console, create an SNS Topic and then create a subscription.

![image](https://github.com/EKechei/Automated-Image-Resizing-Using-AWS-Services/assets/128794751/a776e5c6-6242-466c-8407-4b77f8c9a841)

# Step 3: Create Lambda

![image](https://github.com/EKechei/Automated-Image-Resizing-Using-AWS-Services/assets/128794751/aa2d17fa-644a-4ccb-bace-1402b2c63d9c)
![image](https://github.com/EKechei/Automated-Image-Resizing-Using-AWS-Services/assets/128794751/88a47991-e4ec-42b3-8a54-7df995f6829d)

Replace the default code with the Lambda_Function.py and deploy the changes, Don't test the code now we have some more actions to do before testing.
Add Trigger to your function so that whenever a new object is added to our source bucket, it will trigger the lambda function automatically.

![image](https://github.com/EKechei/Automated-Image-Resizing-Using-AWS-Services/assets/128794751/a9a90d84-d61d-41c5-ad8f-aa434731f819)
![image](https://github.com/EKechei/Automated-Image-Resizing-Using-AWS-Services/assets/128794751/d89d0e01-0245-460b-ad26-ae83d87bc32c)

The next step is to add Layer, This is because to resize the image uploaded in our source S3 bucket, We need a Python library called pillow in our code to resize the image. So first, we need to create a lambda layer with Pillow library.
To achieve this we need to do the following tasks:

- Create an EC2 instance with the AMI “Amazon Linux 2023 AMI”.
- Attach an IAM role to the EC2 instance with Lambda permissions to enable the instance to interact with Lambda.
- Connect to the EC2 instance and run the following commands. These commands installs pip3, creates a zip file with “Pillow” library, and creates a lambda layer with the name “pillow-layer”.
  

```
sudo dnf install python3-pip
mkdir -p lambda-layer/python
cd lambda-layer/python
pip3 install --platform manylinux2014_x86_64 --target . --python-version 3.9 --only-binary=:all: Pillow
cd ..
zip -r layer.zip python
aws lambda publish-layer-version --layer-name pillow-layer --zip-file fileb://layer.zip --compatible-runtimes python3.9 --region us-east-1
```

You can terminate the EC2 instance. Since the lambda layer has been created, we can go ahead and add it.

![image](https://github.com/EKechei/Automated-Image-Resizing-Using-AWS-Services/assets/128794751/20c61b72-f4f5-4af7-b80b-c859c5a70d6c)

# Step 4: Test

Upload some images to the Source Bucket.

![image](https://github.com/EKechei/Automated-Image-Resizing-Using-AWS-Services/assets/128794751/c6177cae-2b28-4017-9cfb-b90f73f7821a)

Our images were resized and uploaded to the destination bucket as you can see below.

![image](https://github.com/EKechei/Automated-Image-Resizing-Using-AWS-Services/assets/128794751/d7bdb10d-fe90-495d-87c3-ef9752536f6e)

![image](https://github.com/EKechei/Automated-Image-Resizing-Using-AWS-Services/assets/128794751/47e335f2-88b8-4ee7-a5da-b7740e5e7a6c)









