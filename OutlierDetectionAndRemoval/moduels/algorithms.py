import pandas as pd
import numpy as np
import scipy
from sklearn.neighbors import KDTree
import matplotlib.pyplot as plt
import seaborn as sns

class CleaningAlgorithm:
    def __init__(self, dataset_path, delimiter=None, metric=None, k=None, n=None):
        """
        :param dataset_path: the path to the dataset
        :param delimiter: the delimeter of the dataset
        :param metric: the metric for computing the distances
        :param k: number of neighbors to consider
        :param n: number of outliers to detect
        """
        self.dataset_path = dataset_path
        self.delimiter = delimiter if delimiter else ','
        self.metric = metric if metric else "euclidean"
        self.k = k if k else 3
        self.n = n if n else 10
        self.outliers_indices = None

    def visualize_outliers(self, outliers, cols_pairs):
        dtf = pd.read_csv(self.dataset_path, header=None, low_memory=False)
        for (x, y) in cols_pairs:
            x_axis = dtf[x]
            y_axis = dtf[y]
            x_outliers = dtf.loc[outliers][x]
            y_outliers = dtf.loc[outliers][y]
            plt.scatter(x_axis, y_axis, color='b')
            plt.scatter(x_outliers, y_outliers, color='r')
            try:
                plt.savefig(f'{x}, {y}')
            except:
                print("Could not save the image. There might not be permission.")
        
    def copy_without_outliers(self, to_path):
        """
        :param to_path: the path of the new file to copy the dataset without the outliers to
        """
        dtf = pd.read_csv(self.dataset_path, header=None, low_memory=False)
        dtf_without_outliers = dtf.drop(self.outliers_indices)
        try:
            dtf_without_outliers.to_csv(to_path, index=False, header=False)
        except:
            print("Could not save the file. There might not be permission.")
        
        
class TreeCleaningAlgorithm(CleaningAlgorithm):
    def get_outliers_indices(self):
        # Parsing the dataset
        dtf = np.genfromtxt(self.dataset_path, delimiter=self.delimiter)
        # Creating a KDTree to store the dataset - letting us find neighbors quickly
        tree = KDTree(dtf, metric=self.metric)
        # Querying the tree, finding k-th neighbor to each vector (NOTE: k is k+1)
        distances, indices = tree.query(dtf, self.k + 1)
        # Retrieving only the desired column
        distances_k = distances[:, self.k]
        # Retrieving the top n outlier indices
        self.outliers_indices = np.argpartition(distances_k, len(distances_k) - self.n)[-self.n:]
        # Minus one to all indices
        # self.outliers_indices = np.subtract(self.outliers_indices, 1)
        return self.outliers_indices

class MatrixCleaningAlgorithm(CleaningAlgorithm):
    def get_outliers_indices(self):
        # Pasring the dataset
        dtf = pd.read_csv(self.dataset_path, header=None, low_memory=False)
        # Computing a distance matrix from all vectors to all vectors in the dataset
        distances = scipy.spatial.distance.cdist(dtf.values, dtf.values,self.metric)
        # Creating a dataframe from the distances matrix
        distances_dtf = pd.DataFrame(distances, index=dtf.index, columns=dtf.index)
        # Sorting the distance matrix by value for each row
        sorted_distances_dtf = distances_dtf.apply(lambda x: np.sort(x), axis=1, raw=True)
        # Sorting the sorted distance matrix by the k-th column
        k_sorted_distances_dtf = sorted_distances_dtf.sort_values([self.k], ascending=False)
        # Getting the top n outliers indices in the distance matrix based on the distance to their k-th nearest neighbor
        self.outliers_indices = list(k_sorted_distances_dtf.index)[:self.n]
        return self.outliers_indices
    
def k_mean_data_cleaning(dataset_name, ds):
    k = 5
    n = round(len(ds) * 0.1)
    #print("Dataset size is: {0}, number of outlier isL {1}", len(ds), n)
    tree = KDTree(ds, metric='euclidean')
    distances, indices = tree.query(ds, k + 1)
    distances_k = distances[:, k]
    outliers_indices = np.argpartition(distances_k, len(distances_k) - n)[-n:]
    #print(outliers_indices)
    ds = ds.drop(ds.index[outliers_indices])
    #clean_ds = np.delete(ds, outliers_indices, axis=0)
    return ds