Voice/non-voice segmentation

1. Select/tag training data:
	1.1 Separate audio into two clusters, vocal and instrumental.
		vocal: The wanted audio are store here. Suggesting that only select predominant vowel.
		instrumental: All kinds of unwanted.
	1.2 As already proved, in the cluster of voice, both male and female can be clustered together - the common feature of male and female voice can be extracted.

2. Segment equivalently by time and extract features:
	2.1 extractFeatures.py
		Specify parameters:
			length, 0.1s suggested
			hopsize,0.05s suggested
	2.2 Hopesize is good but not necessary. It is a good way to increase sensitive training instances and increase the precision of segmentation time resolution. The suggested time are tested that works well.
	2.3 sigCheck.py
		There may fail in some frames, and in the part of *.sig to *.arff process, the missing ones will be shifted. sigCheck.py will scan the names, first solve the name problem and then fill up the slot. (Necessary)
	2.4 essentiaToWeka.py
		Since we use the machine learning algorithm implemented by Weka, we convert the *.sig format to *.arff.
	2.5 normalize.py
		This is a process that make the instances make more sense for the features, also fixes the 'nan' and 'inf' problems.

3. Select/filter features
	3.1 In the machine learning point of view, over-fit means you don't have enough instances, but use too many features to train the model
	3.2 What is "not enough instances": in our case, it means our instances cannot cover most of the sing properties. For example, if we have 10000 instances of a single singer singing 'a' to train the model to find all the vocal sections, it is still not enough.
	3.3 Weka: http://www.cs.waikato.ac.nz/ml/weka/
		When we cannot have enough instances, or we are not sure whether it is enough, Weka is not the only thing we need to consider, but also analysis the features with audio computing knowledge. For example, when are are looking for very spectral feature, like 'i' in all vowels, it doesn't make sense to remain feature "barking band" even if it may be proved to work in the training test.
	3.4 selectfeats.py
		After you have the training Weka file, e.g. train.arff, we want to select these features from the target dataset. It reads the *.arff to detect what are the features you selected and work to *.sig files.

4. Classification
	4.1 This is better to read more in machine learning algorithms.
	4.2 To be suggested, test with more different algorithms, like k-NN, SMO(SVM), using different parameters. For a more "complex" experiment, I suggest to use SMO. e.g. From a simple but comprehensive test to the instances in all kinds of environments, good to use SMO than k-NN.
	4.3 Cross folder test cannot be fully trusted, but high precision is necessary. When the precisions are higher than 85%, it is better not to choose the algorithms depends on this number. e.g. 95% is higher than 92%, so I choose the one got 95%. (This is wrong!)
