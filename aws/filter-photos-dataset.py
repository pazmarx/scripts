# ------------------------
#   USAGE
# ------------------------
# python filter-photos-dataset.py

# ------------------------
#   IMPORTS
# ------------------------
# import the necessary packages
import boto3

# set the bucket name along with:
# (1) the path of the folder in the bucket
# (2) the label to filter
# (3) the confidence level for the rekognition
BUCKET_NAME = 'stude'
FOLDER_PATH = 'Paz_images/dog/'
LABEL_TO_FILTER = 'Dog'
CONF_LEVEL = 75

s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)
client = boto3.client('rekognition')


def is_label(photo, bucket):
    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}})

    for label in response['Labels']:
        if label['Name'] == LABEL_TO_FILTER and label['Confidence'] >= CONF_LEVEL:
            return True
    return False


i = 0
for image in bucket.objects.filter(Prefix=FOLDER_PATH):
    try:
        if not is_label(image.key, BUCKET_NAME):
            s3.Object(BUCKET_NAME, image.key).delete()
            print('deleted')
        else:
            print('not deleted')
            i += 1
    except:
        s3.Object(BUCKET_NAME, image.key).delete()
        print('not valid')
print(str(i) + 'have not deleted')
