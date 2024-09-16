from sklearn.cluster import KMeans
import numpy as np


class Market:
    def __init__(self, G) -> None:
        self.G = G
        self.datasets = {}
        self.initialize_market()
    
    # 市場の各ノードをDataとして初期化
    def initialize_market(self):
        # ノードごとにDataインスタンスを作成
        for node in self.G.nodes():
            variables = [int(var) for var in self.G.nodes[node]['variables'].split(',')]
            self.datasets[node] = Data(node, variables)
        
        # 市場全体のデータ価格を初期化
        self.initialize_data_prices()
        
        # 変数に基づいてタグを作成
        self.assign_tags()
    
    def initialize_data_prices(self):
        for data_id, data in self.datasets.items():
            data.update_price()
    
    def assign_tags(self):
        vars_vec = []
        data_ids = list(self.datasets.keys())
        max_vars_len = max(len(data.variables) for data in self.datasets.values())
        
        for data_id in data_ids:
            variables = self.datasets[data_id].get_vars_vector(max_vars_len)
            vars_vec.append(variables)
        
        # 1段階目のクラスタリング
        kmeans_parent = KMeans(n_clusters=5, random_state=42)
        parent_clusters = kmeans_parent.fit_predict(vars_vec)
        
        # 親タグを割り当てる
        for i, data_id in enumerate(data_ids):
            parent_tag = parent_clusters[i]
            self.datasets[data_id].set_parent_tag(parent_tag)
        
        # 2段階目のクラスタリング
        for parent_tag in set(parent_clusters):
            parent_tag_data_ids = [data_id for data_id in data_ids if self.datasets[data_id].parent_tag == parent_tag]
            parent_tag_vars = [self.datasets[data_id].get_vars_vector(max_vars_len) for data_id in parent_tag_data_ids]
            
            if len(parent_tag_data_ids) < 4:
                for data_id in parent_tag_data_ids:
                    self.datasets[data_id].set_child_tag(0)
            
            else:
                kmeans_child = KMeans(n_clusters=3, random_state=42)
                child_clusters = kmeans_child.fit_predict(parent_tag_vars)
                
                # 子タグを割り当てる
                for i, data_id in enumerate(parent_tag_data_ids):
                    child_tag = child_clusters[i]
                    self.datasets[data_id].set_child_tag(child_tag)
        
    # 市場全体でデータ価格の更新
    def update_data_prices(self, buyers):
        # 変数の需要を計算
        var_demand = self.calc_var_demand(buyers)
        
        # 変数の価格を更新
        for data_id, data in self.datasets.items():
            data.update_var_price(var_demand)
        
        # データの価格を更新
        self.update_data_price()
    
    # 市場全体でデータの購入回数を更新
    def update_data_purchase_count(self, buyers):
        for data_id, data in self.datasets.items():
            data.update_purchase_count(buyers)
    
    # 変数の需要を計算
    def calc_var_demand(self, buyers):
        var_demand = {}
        for data_id, data in self.datasets.items():
            purchase_count = sum(1 for buyer in buyers if buyer.step_purchased_data == data_id)
            for var_id, var in data.variables.items():
                if var_id not in var_demand:
                    var_demand[var_id] = 0
                var_demand[var_id] += purchase_count
        return var_demand
    
    # 市場全体でデータ価格を更新
    def update_data_price(self):
        for data_id, data in self.datasets.items():
            data.update_price()

class Data:
    def __init__(self, data_id, variables) -> None:
        self.data_id = data_id
        self.price = 0
        self.variables = {var_id: Variable(var_id, 10) for var_id in variables}
        self.purchase_count = 0 # このデータが合計で何回購入されたか
        self.parent_tag = None
        self.child_tag = None
    
    # データの購入回数の更新
    def update_purchase_count(self, buyers):
        self.purchase_count = sum(
            1 for buyer in buyers if buyer.step_purchased_data == self.data_id
        )
    
    # 変数の価格を更新
    def update_var_price(self, var_demand):
        for var_id, var in self.variables.items():
            demand = var_demand.get(var_id, 0)
            
            # 閾値の更新
            if demand >= var.threshold:
                var.threshold += 1
            elif demand < var.threshold:
                var.threshold = max(0, var.threshold - 1)
            
            # 更新された閾値に基づいて価格を更新
            if demand >= var.threshold:
                var.increase_price(1)
            elif demand < var.threshold:
                var.decrease_price(1)
    
    # データ価格の更新
    def update_price(self):
        self.price = sum(var.get_price() for var in self.variables.values())
    
    # 変数ベクトルを返す
    def get_vars_vector(self, max_vars_len, fill_value=-1):
        vars_vector = np.full(max_vars_len, fill_value)
        for i, var_id in enumerate(self.variables.keys()):
            vars_vector[i] = var_id
        return vars_vector
    
    # 親タグを設定
    def set_parent_tag(self, parent_tag):
        self.parent_tag = parent_tag
    
    # 子タグを設定
    def set_child_tag(self, child_tag):
        self.child_tag = child_tag

class Variable:
    def __init__(self, var_id, price=10) -> None:
        self.var_id = var_id
        self.price = price
        self.threshold = 1
    
    def set_price(self, price):
        self.price = price
    
    def get_price(self):
        return self.price
    
    def increase_price(self, amount):
        self.price += amount
    
    def decrease_price(self, amount):
        self.price = max(0, self.price - amount)