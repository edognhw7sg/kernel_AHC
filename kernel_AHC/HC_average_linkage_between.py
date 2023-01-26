import numpy as np
from scipy import sparse
import matplotlib.pyplot as plt

class Cluster:
    def __init__(self, data_list = np.array([]), cluster_list = np.array([]), dsim = 0):
        self.data_list = data_list
        self.cluster_list = cluster_list
        self.dsim = dsim
        self.x_point = None

    def get_data_list(self):
        return self.data_list

    def get_cluster_list(self):
        return self.cluster_list

    def get_dsim(self):
        return self.dsim

    def get_x_point(self):
        return self.x_point

    def set_x_point(self, point):
        self.x_point = point


class HC_average_linkage_between:
    def __init__(self, input_data):
        self.data_list = input_data.copy()
        self.cluster_list = np.array([])
        self.dsim_list = np.full((self.data_list.shape[0], self.data_list.shape[0]), np.inf, dtype = float)


    def fit(self):
        #初期クラスタリスト作成
        for i in range(self.data_list.shape[0]):
            cluster_obj = Cluster(data_list = np.array([i]))
            self.cluster_list = np.append(self.cluster_list, cluster_obj)

        #初期クラスタ間の非類似度を計算
        self.dsim_list_set()

        #結合処理開始
        while self.cluster_list.shape[0] != 1:
            self.updata()


    def dsim_list_set(self):
        for i in range(self.data_list.shape[0] - 1):
            self.dsim_list[i + 1:, i] = self.data_list[i + 1:, i]


    def cal_dsim(self, cluster_1_index, cluster_2_index):
        new_dsim_list = np.array([])
        for cluster_index in range(self.cluster_list.shape[0]):
            if cluster_index == cluster_1_index or cluster_index == cluster_2_index:
                continue

            if cluster_1_index > cluster_index:
                dsim_1 = self.dsim_list[cluster_1_index, cluster_index]

            else:
                dsim_1 = self.dsim_list[cluster_index, cluster_1_index]

            if cluster_2_index > cluster_index:
                dsim_2 = self.dsim_list[cluster_2_index, cluster_index]

            else:
                dsim_2 = self.dsim_list[cluster_index, cluster_2_index]

            cluster_1_num = self.cluster_list[cluster_1_index].get_data_list().shape[0]
            cluster_2_num = self.cluster_list[cluster_2_index].get_data_list().shape[0]

            new_dsim_list = np.append(new_dsim_list, ((cluster_1_num * dsim_1) + (cluster_2_num * dsim_2)) / (cluster_1_num + cluster_2_num))

        return new_dsim_list


    def updata(self):
        #新規クラスタ作成と，新規非類似度行列の作成
        min_dsim = self.dsim_list.min() #最小の非類似度取得
        min_dsim_list_index = np.where(self.dsim_list == min_dsim) #非類似度が最小となる組み合わせ取得
        cluster_1 = self.cluster_list[min_dsim_list_index[0][0]] #クラスター取り出し
        cluster_2 = self.cluster_list[min_dsim_list_index[1][0]] #クラスター取り出し
        new_dsim_list = self.cal_dsim(cluster_1_index = min_dsim_list_index[0][0], cluster_2_index = min_dsim_list_index[1][0]) #追加する非類似度行列を取得
        new_cluster = Cluster(data_list = np.append(cluster_1.get_data_list(), cluster_2.get_data_list()), cluster_list = np.array([cluster_1, cluster_2]), dsim = min_dsim) #クラスタ作成

        #非類似度行列の不要部分を削除
        self.cluster_list = np.delete(self.cluster_list, min_dsim_list_index[0][0])
        self.cluster_list = np.delete(self.cluster_list, min_dsim_list_index[1][0])
        self.dsim_list = np.delete(self.dsim_list, min_dsim_list_index[0][0], 0)
        self.dsim_list = np.delete(self.dsim_list, min_dsim_list_index[0][0], 1)
        self.dsim_list = np.delete(self.dsim_list, min_dsim_list_index[1][0], 0)
        self.dsim_list = np.delete(self.dsim_list, min_dsim_list_index[1][0], 1)

        #新規クラスタと新規行列の追加
        self.cluster_list = np.append(self.cluster_list, new_cluster)
        self.dsim_list = np.append(self.dsim_list, np.array([new_dsim_list]), 0)
        self.dsim_list = np.append(self.dsim_list, np.full((self.dsim_list.shape[0], 1), np.inf), 1)


    def get_label_list(self, num):
        return_cluster_list = np.array([[self.cluster_list[0]], [self.cluster_list[0].get_dsim()]]) #クラスタオブジェクトとクラスタの非類似度を指定数格納するリスト
        while return_cluster_list.shape[1] != num:
            max_dsim_index = np.where(return_cluster_list[1] == return_cluster_list[1].max())[0][0]
            add_cluster_list = return_cluster_list[0, max_dsim_index].get_cluster_list()
            return_cluster_list = np.append(return_cluster_list, np.array([add_cluster_list, [add_cluster_list[0].get_dsim(), add_cluster_list[1].get_dsim()]]), 1)
            return_cluster_list = np.delete(return_cluster_list, max_dsim_index, 1)

        return_label_list = np.zeros(self.data_list.shape[0])
        cluster_count = 0
        for return_cluster in return_cluster_list[0]:
            for data_index in return_cluster.get_data_list():
                return_label_list[data_index] = cluster_count

            cluster_count += 1

        return return_label_list

    def create_dendrogram(self):
        plt.figure(figsize = (20, 12))
        plt.xlabel("data_ID")
        plt.ylabel("Dissimilarity")
        self.x_label_point = np.array([], dtype = int)
        self.x_label_point_name = np.array([], dtype = int)
        self.x_point_count = 0
        self.set_x_point(self.cluster_list[0])
        plt.xticks(self.x_label_point, self.x_label_point_name)
        plt.savefig("HC_average_linkage_between.png")
        plt.show()

    def set_x_point(self, cluster_obj):
        cluster_obj_have_list = cluster_obj.get_cluster_list()
        if cluster_obj_have_list.shape[0] == 2:
            self.set_x_point(cluster_obj_have_list[0])
            self.set_x_point(cluster_obj_have_list[1])
            cluster_obj.set_x_point((cluster_obj_have_list[0].get_x_point() + cluster_obj_have_list[1].get_x_point()) / 2)
            plt.plot([cluster_obj.get_x_point(), cluster_obj_have_list[0].get_x_point(),cluster_obj_have_list[0].get_x_point()], [cluster_obj.get_dsim(), cluster_obj.get_dsim(), cluster_obj_have_list[0].get_dsim()], color = "r")
            plt.plot([cluster_obj.get_x_point(), cluster_obj_have_list[1].get_x_point(),cluster_obj_have_list[1].get_x_point()], [cluster_obj.get_dsim(), cluster_obj.get_dsim(), cluster_obj_have_list[1].get_dsim()], color = "r")

        else:
            cluster_obj.set_x_point(self.x_point_count)
            self.x_label_point = np.append(self.x_label_point, self.x_point_count)
            self.x_label_point_name = np.append(self.x_label_point_name, cluster_obj.get_data_list()[0])
            self.x_point_count += 1
