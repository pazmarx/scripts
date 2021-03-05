# ------------------------
#   USAGE
# ------------------------
# python download-from-s3.py

# ------------------------
#   IMPORTS
# ------------------------
# import the necessary packages
import boto3
import botocore

# set the bucket name along with:
# (1) the path of the folder in the bucket
# (2) the folder to download to
BUCKET_NAME = 'stude'
FOLDER = 'Paz_images/dog/'
OUTPUT = 'dataset/dog/'

s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)
i = 0
for image in bucket.objects.filter(Prefix=FOLDER):
    try:
        bucket.download_file(image.key, OUTPUT + 'image' + str(i) + '.jpg')
        i += 1
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise
