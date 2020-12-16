# Elbow Method For K-means

## Introducton
K-means is a method in Data Science. It divides a data set into subsets of records with a center for every subset. The records must be  more close to its subset center than to other subset centers. Such subsets are called _clusters_. The method needs for a user to input the number of desired clusters, meaning that the user should have an idea for the optimal number. 

There are a few ways to estimate the number. One of them is Elbow method. It is a visualization which requires a user to determine the optimal number by a graph. The eyeballing such number might be not reliable, as I show in my notebook here.

## My experience
When I had been teaching my students had asked me if there is a function which does it, so I replied that we can use cosines and their properties to create such function. It would be more dependable than looking at a visualization. Afterwards I wrote to scikit-learn developers and offered the method. I was told that it is relatively simple and people who need it can implement it themselves.

Since then some of my linguistic students told me that they cannot handle math for it, and some non-linguistic people have said that they would prefer a ready debugged script. I put it here and I was allowed to publish it on scikit-learn. Dozens of people  have cloned it.

## The repo content
The repository contains a notebook with explanation how current visual application of Elbow method fails in some cases called Numeric_Elbow_Method_for_K-Means_Clustering_with_Justification.ipynb. In addition there is a video which demonstrate what happens when a horizontal axis shrinks called CompressingHorizonalAxis.mkv. The function separate version is in the file NumericElbowMethod.py, and it is called `ElbowMethod`.
