import boto3
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import BytesIO
from PIL import Image

bucket_name = ''
image_key = ''
access_key=''
secret_key=''


def detect_labels(photo, bucket):

    # Initialize Rekognition client
    client=boto3.client(service_name='rekognition', region_name='us-east-1',
                         aws_access_key_id=access_key,
                         aws_secret_access_key=secret_key)

    response = client.detect_labels(
        Image={'S3Object':{'Bucket':bucket_name,'Name':image_key}},
        MaxLabels=10,
        MinConfidence=70
    )

    print('Detected labels for ' + photo) 
    print()

    # Fetch image from S3 for plotting
    s3_client = boto3.client(service_name='s3', region_name='us-east-1',
                         aws_access_key_id=access_key,
                         aws_secret_access_key=secret_key)
    s3_response = s3_client.get_object(Bucket=bucket_name, Key=image_key)
    image_data = s3_response['Body'].read()
    image_pil = Image.open(BytesIO(image_data))

    # Convert the image to an RGB format that can be displayed by Matplotlib
    image_rgb = image_pil.convert('RGB')

    # Plot the image using matplotlib
    fig, ax = plt.subplots(1, figsize=(12, 8))
    ax.imshow(image_rgb)


    for label in response['Labels']:
       for instance in label['Instances']:
            # Get the bounding box coordinates (normalized)
            bbox = instance['BoundingBox']
            left = bbox['Left'] * image_rgb.width
            top = bbox['Top'] * image_rgb.height
            width = bbox['Width'] * image_rgb.width
            height = bbox['Height'] * image_rgb.height

            # Create a Rectangle patch for the bounding box
            rect = patches.Rectangle(
                (left, top), width, height, linewidth=2, edgecolor='red', facecolor='none'
            )

            # Add the rectangle to the plot
            ax.add_patch(rect)

            # Add label text next to the bounding box
            ax.text(
                left, top, label['Name'], color='red', fontsize=12,
                verticalalignment='bottom', horizontalalignment='left'
            )

    # Hide axes and show the image
    ax.axis('off')
    plt.show()

    # Return the number of labels detected
    return len(response['Labels'])


def main():
    photo=''
    bucket=''
    label_count=detect_labels(photo, bucket)
    print("Labels detected: " + str(label_count))


if __name__ == "__main__":
    main()
