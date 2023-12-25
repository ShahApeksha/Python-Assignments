

# Import necessary modules
import os
import re

def ExtractReviewInfo(review_line):
    # Regular expression pattern to match the required information in the review line
    pattern = r'(\w{6}) (\w{10}) (\d{4}-\d{2}-\d{2}) (\d) <(.*?)>'
    match = re.search(pattern, review_line)

    if match:
        # Extracting data from the matched groups
        customerID, productID, reviewDate, reviewRating, reviewText = match.groups()
        # Converting reviewRating to an integer
        reviewRating = int(reviewRating)
        return customerID, productID, reviewDate, reviewRating, reviewText
    else:
        return None

def ProcessReviewsInDirectory(directoryPath):
    # Dictionary to store reviews data for each product
    productReviewsData = {}
    # Counter for invalid reviews
    invalidReviewsCount = 0

    # Loop through all files in the directory
    for filename in os.listdir(directoryPath):
        filePath = os.path.join(directoryPath, filename)
        # Check if the file is a regular file
        if os.path.isfile(filePath):
            # Open the file for reading
            with open(filePath, 'r', encoding='utf-8') as file:
                # Loop through each line in the file
                for line in file:
                    # Extract review information from the line
                    reviewInfo = ExtractReviewInfo(line)

                    # If valid review information is obtained
                    if reviewInfo:
                        # Unpack the reviewInfo tuple
                        customerID, productID, reviewDate, reviewRating, reviewText = reviewInfo

                        # Create a dictionary for each product if it doesn't exist in productReviewsData
                        if productID not in productReviewsData:
                            productReviewsData[productID] = {
                                'ratings': [],
                                'reviews': []
                            }

                        # Append the rating and reviewText to the respective lists in the dictionary
                        productReviewsData[productID]['ratings'].append(reviewRating)
                        productReviewsData[productID]['reviews'].append(reviewText)
                    else:
                        # If review information is invalid, increment the counter
                        invalidReviewsCount += 1

    # Return the processed data and the count of invalid reviews
    return productReviewsData, invalidReviewsCount

def CalculateAverageRatings(productReviewsData):
    averageRatings = {}

    # Loop through each product and its data in productReviewsData dictionary
    for productID, data in productReviewsData.items():
        ratings = data['ratings']
        # Calculate average rating for each product
        averageRating = sum(ratings) / len(ratings)
        averageRatings[productID] = averageRating

    return averageRatings

def GetTopNProducts(averageRatings, n=3):
    # Sort the averageRatings dictionary based on values in descending order
    sortedRatings = sorted(averageRatings.items(), key=lambda x: x[1], reverse=True)
    # Return the top N products
    return sortedRatings[:n]

def WriteSummaryFile(totalReviewsCount, validReviewsCount, invalidReviewsCount, topProducts, outputFile):
    with open(outputFile, 'w', encoding='utf-8') as file:
        file.write(f"Total Reviews Processed: {totalReviewsCount}\n")
        file.write(f"Total Valid Reviews: {validReviewsCount}\n")
        file.write(f"Total Invalid Reviews: {invalidReviewsCount}\n\n")
        file.write("Top 3 Products with Highest Average Ratings:\n")
        # Write the productID and averageRating for the top products
        for productID, averageRating in topProducts:
            file.write(f"Product ID: {productID}, Average Rating: {averageRating:.2f}\n")

def Main():
    # Example usage:
    reviewDirectoryPath = 'review'  # Directory containing review files
    summaryOutputFile = 'summary.txt'  # Output file name for the summary

    # Process reviews in the given directory
    productReviewsData, invalidReviewsCount = ProcessReviewsInDirectory(reviewDirectoryPath)

    # Calculate average ratings for each product
    averageRatings = CalculateAverageRatings(productReviewsData)

    # Determine top 3 products with highest average ratings
    topProducts = GetTopNProducts(averageRatings, n=3)

    # Write the summary to the output file
    totalReviewsCount = sum(len(data['ratings']) for data in productReviewsData.values()) + invalidReviewsCount
    validReviewsCount = sum(len(data['ratings']) for data in productReviewsData.values())
    WriteSummaryFile(totalReviewsCount, validReviewsCount, invalidReviewsCount, topProducts, summaryOutputFile)

# Execute main function
if __name__ == "__main__":
    Main()


