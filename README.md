# Report about Volumes in all AWS Regions


![Cost](/assets/aws-costs.jpg)

 We want reduce costs in our AWS account. Normally in DEVs accounts we have a lot of Volumes that users forget to delete and it doesn't remove automatically when you destroy an EC2 Instance (It depends).

This small script help you to identify them to take some action.

Your boss Finance will appreciate it ;-)

# Technologies we’ll use:

*  AWS API (EC2)
*  Python3.9


```bash
https://linuxhostsupport.com/blog/how-to-install-python-3-9-on-ubuntu-20-04/ (Google)
```

# Pre-requisites:
```bash
pip3 install boto3
pip3 install xlsxwriter
```

# Deploy:

```bash
AWS_PROFILE=XXX python3 infoEC2VolumesReportUsage.py
```

![Deploy](/assets/deploy1.PNG)
![Deploy](/assets/deploy2.PNG)



# Testing

If everything is working well, we will see a new Excel in your same location:

![Result](/assets/result.PNG)

# Licence

Apache

![Result](/assets/meme.gif)

# Information

More info --> 

https://aws.amazon.com/blogs/mt/controlling-your-aws-costs-by-deleting-unused-amazon-ebs-volumes/

https://github.com/akhan4u/unused_volumes/blob/master/unused_volumes.py


https://xlsxwriter.readthedocs.io/

https://www.nops.io/unused-aws-ebs-volumes/

David Álvarez Quiroga
