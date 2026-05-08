from celery import shared_task # type: ignore
from Models.base_model import db
from Models.properties import Property, PropertyImages
from Dalali.aws_credentials import awsCredentials
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
import boto3

s3 = boto3.resource(
  "s3",
  aws_access_key_id = awsCredentials.aws_access_key,
  aws_secret_access_key = awsCredentials.aws_secret_key
)
bucket_name = awsCredentials.bucket_name
region = awsCredentials.region

@shared_task
def upload_property_images(property_id, files):
  upload_property = Property.query.get(property_id)
  try:
    for file in files:
      filename = f"{upload_property.alias}/{file.filename}"
      unit_image = PropertyImages(
        image_name = filename,
        property_id = upload_property.id
      )
      s3.Bucket(bucket_name).upload_fileobj(file, filename)
      db.session.add(unit_image)
      upload_property.is_published = True
      db.session.commit()
  except NoCredentialsError:
    db.session.rollback()
    print("Credentials not available", "danger")
  except PartialCredentialsError:
    db.session.rollback()
    print("Incomplete credentials provided", "danger")
  except ClientError as e:
    db.session.rollback()
    print(f"Client Error: {e.response['Error']['Message']}", "danger")
  except Exception as e:
    db.session.rollback()
    print(f"{str(e)}")
