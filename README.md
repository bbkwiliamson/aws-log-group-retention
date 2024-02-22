# log-group-retention

#creator: Brian Bapela (bbkwiliamson.ovi@gmail.com)
# this is about automating log-group retention period on cloudwatch

**S3Bucket.yml file**

basically this template just create an s3 bucket which its use is just to store the python code zip and .py files.

**lambda-log-group-retention-template.yam**

this template creates various resources that are needed to make the whole project work successfully.
the template has _ parameters_: which is where i define values that might be different to different teams.
1. under resources there is IAM ROLE which the lambda function will need in order to function properly.
2. IAM ROLE has IAM Policy/permission attached to it specifying what the lambda function need access to.
3. I then create the Lambda function on line 58 and configuring all the properties it needs. most importantly linking the bucket created above to the function as that's where the code is located and also specifying its key.
4. creating the lambda function log-group for monitoring purposes
5. i then create events rule that explains how the lambda function will be triggered, this rule is optional meaning it can be either ENABLED/DISABLED and making sure it is linked to the Lambda function.
6. creating another role that will be assumed or used by the scheduler.amazon.aws for schedule events to mainly invoke the lambda function
7. the scheduler role linked to the scheduler defined as cron with specific date and also linked to the lambda function and the schedule role
8. finally i create the lambda permissions for both the schedule and events triggers.


it is also important to note that permission boundary policy is already created in the accounts. if you want to use the templates, your own account might not need it or have it, so you can remove the line or just use comments so that CloudFormation won't demand it.


  **sns-topic.yaml**
   this template simply creates a simple notification topic with subsbrictions using protocol E-mail as the prefered method of communication

  **lambda.py**

  this is the actual lambda python code file.
  first two lines import required libraties

  the send_sns function:
      it gets the accound ID/number and sns client from aws. it checks for required sns topic and forward the message to the destination, otherwise the function 
      will display error message if that topic does not exist or the function failed to send the message.

  the lambda_handler function:
     this is the main function and what gets triggered when specified events occurs.
     the function fetches all log groups from cloudwatch 
     from the list that the function has got, it filters the metadata of the log group to just the name of the log group.
     then the function looks for retention period in each of the log groups to match the specified condition and log groups that breach the condition are added to       an array of list and forward that to the send_sns function to finally send the message.


 the zip file is just the .py file
