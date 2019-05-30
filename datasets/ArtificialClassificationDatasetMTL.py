# -*- coding: utf-8 -*-
# @Author: Andre Goncalves
# @Date:   2018-11-13 08:37:27
# @Last Modified by:   Andre Goncalves
# @Last Modified time: 2019-05-29 16:33:20
import numpy as np
import pandas as pd
from design import DatasetMTL
from sklearn.datasets import make_classification


class ArtificialClassificationDatasetMTL(DatasetMTL):
    """
        Implement an MTL Artificial Classification dataset generator.
        The generated data is mainly to test MTL methods' recovery capabilities.
    """

    def __init__(self, nb_tasks, nb_samples, dimension, nb_useless_vars=1):
        """
        Args:
            nb_tasks (int): number of tasks
            nb_samples (int): number of sample per task
            dimension (int): problem dimension (all tasks have the same dim)
            nb_useless_vars (int): number of unrelated variables to be added to design matrix
        """
        assert nb_samples > 0
        assert dimension > 0
        assert nb_tasks > 0
        assert nb_useless_vars < dimension

        self.nb_tasks = nb_tasks
        self.nb_samples = nb_samples
        self.dimension = dimension
        self.data = None
        self.train_split = 0.7
        self.unique_values_categ = None

        self.y_eps = 0.5
        self.wg1_eps = 0.5
        self.wg2_eps = 0.7
        self.alpha_group_1 = 0.8
        self.alpha_group_2 = 1.0
        self.nb_useless_vars = nb_useless_vars

    def prepare_data(self):
        """
        Generate synthetic dataset.
        """
        self.data = {'train': {'x': list(),
                               'y': list(),
                               'sample_id': list(),
                               'censor_flag': list(),
                               'svv_time': list()},
                     'test': {'x': list(),
                              'y': list(),
                              'sample_id': list(),
                              'censor_flag': list(),
                              'svv_time': list()},
                     'db_names': list(),
                     'true_w': dict()}

        self.column_names = ['X_{}'.format(d + 1) for d in range(self.dimension)]
        self.column_dtypes = [np.dtype(np.float32) for d in range(self.dimension)]

        for t in range(self.nb_tasks):

            xt, yt = make_classification(n_samples=self.nb_samples,
                                         n_features=self.dimension,
                                         n_informative=2, n_redundant=2)

            # number of training samples
            ntr = int(self.nb_samples * self.train_split)

            # encapsulate into a DataFrame object
            xtr = pd.DataFrame(xt[0:ntr, :], columns=self.column_names)
            ytr = pd.DataFrame(yt[0:ntr], columns=('Y',))

            # encapsulate into a DataFrame object
            xts = pd.DataFrame(xt[ntr:, :], columns=self.column_names)
            yts = pd.DataFrame(yt[ntr:], columns=('Y',))

            # organize it into a dictionary
            self.data['train']['x'].append(xtr)
            self.data['train']['y'].append(ytr)
            self.data['train']['sample_id'].append(None)
            self.data['train']['censor_flag'].append(None)
            self.data['train']['svv_time'].append(None)

            self.data['test']['x'].append(xts)
            self.data['test']['y'].append(yts)
            self.data['test']['sample_id'].append(None)
            self.data['test']['censor_flag'].append(None)
            self.data['test']['svv_time'].append(None)

            self.data['db_names'].append('Task %d' % (t))

    def shuffle_data(self):
        '''Shuffle and re-split the data into training and test '''

        ntasks = len(self.data['train']['x'])

        for t in range(ntasks):
            # pool the data from old train/test splits
            x = np.vstack((self.data['train']['x'][t],
                           self.data['test']['x'][t]))

            y = np.vstack((self.data['train']['y'][t],
                           self.data['test']['y'][t]))

            # number of training samples
            ntr = int(self.train_split * x.shape[0])
            ids = np.random.permutation(x.shape[0])  # shuffle data

            # split between train and test
            self.data['train']['x'][t] = x[ids[:ntr], :]
            self.data['test']['x'][t] = x[ids[ntr:], :]

            self.data['train']['y'][t] = y[ids[:ntr]]
            self.data['test']['y'][t] = y[ids[ntr:]]

    def get_data(self):
        '''Return dataset structure. '''
        if self.data is None:
            raise ValueError('Must call \'prepare\' data first.')
        else:
            return self.data

    def get_nb_tasks(self):
        """ Return the number of tasks in the dataset. """
        return len(self.data['db_names'])
