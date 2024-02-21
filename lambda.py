  
  
import json
import boto3


client = boto3.client('logs')
sts = boto3.client('sts')



def send_sns(message, subject):
    
    AccountID = sts.get_caller_identity()
    client = boto3.client('sns')
    
    try:
        
        subject = f"Checking for Cloudwatch Log-Groups with no/HIGH retention period in this account :{AccountID['Account']}"
        topic_arn = f"arn:aws:sns:af-south-1:{AccountID['Account']}:SNS_Notification_for_Log_group_retention"
        result = client.publish(TopicArn=topic_arn, Message=message, Subject=subject)
        if result['ResponseMetadata']['HTTPStatusCode']==200:
                
            print(result)
            print("Notification Send Successfully..!!!")
            return True
         
            
            
    except Exception as e:
        
        print("Error occured while publish while publish notification and error is :", e)
        return True




def lambda_handler(event, context):
    
    
    print("Received event: " + json.dumps(event, indent=2))
    group_list=[]
    extra_args={}

    try:
        while True:

            #checking if there are log groups, and getting all log groups
            log_group_list = client.describe_log_groups(**extra_args)
            group_list= group_list+ log_group_list['logGroups']
            
            if not 'nextToken' in log_group_list:
                break
            extra_args['nextToken'] = log_group_list['nextToken']
                
            
            log_items=[]
            retention_period = 30
            for item in group_list: 
                
                if "retentionInDays" not in item or item['retentionInDays'] > retention_period:
                        
                    log_items.append(item['logGroupName'])
                    
                           
                        
            array_size = len(log_items)                
            subject = "Checking for Cloudwatch Log-Groups with no retention period/with high retention periods"
            message = f"Good Day Team! \nBelow is a list of log groups with retention periods > {retention_period} days\n please review and amend those that belong to your team to atmost {retention_period} days retention period for cost optimization:\n \n"
            message += "\n".join(log_items)
        
        if array_size > 0:
            
            SNSResult = send_sns(message, subject)
            if SNSResult :
                print("Notification Sent")
                return SNSResult
                  
            

    except NameError:
        raise Exception("Invalid Parameter Exception",client.exceptions.InvalidParameterException)
    except:
        raise Exception("The Service is unavailable ",client.exceptions.ServiceUnavailableException)
     