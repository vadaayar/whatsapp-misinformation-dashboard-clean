# Dataset for the paper 'A Dataset of Fact-Checked Images Shared on WhatsApp during the Brazilian and Indian Elections'

# this folder contains data from India

There are three files/folders, each corresponding to one set of images

1. misinfo: Contains 740 images which were labelled as misinformation either using automated matching to fact checking sites or by professional journalists.

	misinfo/ folder contains the images.
	misinfo.txt contains details of the shares of these images (and their variants obtained by clustering similar images)

	group_id: Anonmyized group id in which the image was shared, consistent across the three folders
	user_id: Anonymized user id who shared the image, consistent accross the three folders (if a user X shared misinfo and notmisinfo, their anonymized id is the same)
	image_id: Anonymized id of the actual image that was shared. Note that even though two users post the exact same image, this image_id might differ. This is why we cluster the images together and only release the centroid image represented by cluster_image_name
	cluster_image_name: Name of the image. This is the image that represents the cluster to which the actual shared image belongs to.
	timestamp: unix timestamp.


2. notmisinfo and random: Similar to the above.


For any questions, please refer to the paper.
