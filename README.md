# NUS CS5242 Project <br> Emotion & Gender Classification

## Project Motivation & Descrition
Face detection, gender detection and emotion recognition has many common applications in the area of surveillance systems, criminology, security, psychology, biometric authentication (Rahman et al., 2015), social robotics and many other human-computer interaction systems (Li & Deng, 2020).

The project seeks to first process a given picture by extracting the faces, standardise the face images, before carrying out classification tasks. We would classify the face images into seven different emotions (angry, disgusted, fearful, happy, neutral, sad and surprised) and gender (male/female).

## Proposed Solution
### Data Collection
Use Google Images to search for faces with specified emotion, e.g. “happy man” and save the file. For example, a raw image obtained using the search keyword “happy man” would have the true label for emotion identified as “happy” and gender identified as “male”. This would form the raw dataset of our project. Selenium is used to automate the scraping from Google Images using the chromedriver.

### Data Pre-processing
Use OpenCV library to detect faces in the raw images gathered during preprocessing to get the bounding box and crop to apply standardisation like image resizing, grayscale filter, etc. If there are multiple faces in a raw image, the true label of the face images would be broadcasted accordingly based on the true label assigned to the raw image.

### Model Development, Improvement & Evaluation
For a start, we can implement MLP as a baseline. Then, we can apply CNNs to improve MLP for emotion and gender classification. This is because CNNs are generally used for image classification tasks. As a bonus, we can attempt to replicate reputable research papers for gender detection and emotion recognition which uses more advanced techniques such as a multi-task learning framework. In addition to evaluating the model on the dataset that we have created, we also intend to evaluate the model on a Kaggle dataset to ensure that the real-life dataset that we have built does not have too much noise.

## References
Li, S., & Deng, W. (2020). Deep facial expression recognition: A survey. IEEE Transactions on Affective Computing, 1–1. https://doi.org/10.1109/taffc.2020.2981446

Rahman, M. M., Rahman, S., Dey, E. K., &amp; Shoyaib, M. (2015). A gender recognition approach with an embedded preprocessing. International Journal of Information Technology and Computer Science, 7(7), 19–27. https://doi.org/10.5815/ijitcs.2015.07.03