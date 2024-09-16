import random

from enum import Enum


class Buyer:
    def __init__(self, strategies, weights, **kwargs):
        self.purchased_data = []
        self.step_purchased_data = None
        self.asset = 200
        self.strategies = strategies
        self.weights = weights
        self.utility = 1
        self.total_vars = set()
        self.state = BuyerState.ACTIVE # 初期状態はアクティブ
        self.utility_threshold = kwargs.get("utility_threshold", 0)
        self.purchase_limit = kwargs.get("purchase_limit", 10)
        self.waiting_steps = 0
    
    def purchase(self, G, market, isPrice):
        # 状態を確認して、更新
        self.check_state()
        
        # 離脱・待機状態の場合は何もしない
        if self.state == BuyerState.EXITED:
            return None
        if self.state == BuyerState.WAITING:
            return None
        
        # アクティブ状態の場合
        # 重みに基づいて戦略を選択
        strategy = random.choices(self.strategies, weights=self.weights, k=1)[0]
        
        # 購入データを選択
        node = strategy.select_data(G, self.purchased_data)
        
        # 価格を考慮する場合、予算内で購入可能か確認
        if isPrice and not self.can_afford(market, node):
            return None
        
        # 購入データがすでに購入済みの場合は何もしない
        if node in self.purchased_data:
            return None
        
        # 購入データが未購入の場合は購入
        self.step_purchased_data = node
        
        # 効用を更新
        self.update_utility(market, node)
        
        # 価格を考慮する場合、購入データの価格を支払い、資産を更新
        if isPrice:
            self.update_asset(market, node)
        
        return node
    
    def can_afford(self, market, data_id):
        data_price = market.datasets[data_id].price
        return data_price <= self.asset
    
    def update_asset(self, market, data_id):
        data_price = market.datasets[data_id].price
        self.asset -= data_price
    
    def update_utility(self, market, data_id):
        current_data_vars = set(market.datasets[data_id].variables.keys())
        # 初回購入の場合
        if not self.purchased_data:
            self.utility = 0
        else:
            dice_coefficient = self.calc_dice_coefficient(self.total_vars, current_data_vars)
            tag_similarity = self.calc_tag_similarity(market, data_id)
            utility = dice_coefficient + tag_similarity
            self.utility += utility
        
        # 購入データの変数を更新
        self.total_vars.update(current_data_vars)
    
    def calc_dice_coefficient(self, vars_set1, vars_set2):
        intersection = vars_set1 & vars_set2
        union = vars_set1 | vars_set2
        if len(union) == 0:
            return 0
        return 2 * len(intersection) / len(union)
    
    def calc_tag_similarity(self, market, data_id):
        # 初回購入
        if not self.purchased_data:
            return 0
        
        total_sim = 0
        total_weight = 0
        num_purchased = len(self.purchased_data)
        
        # 購入履歴を古い順に重みづけ
        for i, purchased_data in enumerate(self.purchased_data):
            current_data = market.datasets[data_id]
            past_data = market.datasets[purchased_data]
            
            weight = (i + 1) / num_purchased
            
            # 親タグと子タグの比較
            if current_data.parent_tag == past_data.parent_tag:
                if current_data.child_tag == past_data.child_tag:
                    total_sim += weight * 1
                else:
                    total_sim += weight * 0.5
            else:
                total_sim += weight * 0
            
            total_weight += weight
            
        return total_sim / total_weight
    
    def check_state(self):
        # 資産が少なくなった場合は離脱
        if self.asset <= 10:
            self.state = BuyerState.EXITED
            return
        
        # 効用が閾値を下回った場合は待機
        if self.utility < self.utility_threshold:
            self.state = BuyerState.WAITING
            self.waiting_steps = 5
            return
        
        # 購入数が上限に達した場合は待機
        if len(self.purchased_data) >= self.purchase_limit:
            self.state = BuyerState.EXITED
            return
        
        # 待機期間の終了判定
        if self.state == BuyerState.WAITING:
            if self.waiting_steps > 0:
                self.waiting_steps -= 1
            else:
                self.state = BuyerState.ACTIVE
    
    def end_step(self):
        # ステップ終了時に購入データを追加し、リセット
        if self.step_purchased_data is not None:
            self.purchased_data.append(self.step_purchased_data)
        self.step_purchased_data = None


class BuyerState(Enum):
    ACTIVE = 1
    WAITING = 2
    EXITED = 3


class RandomStrategy:
    def select_data(self, G, _):
        return random.choice(list(G.nodes()))


class RelatedStrategy:
    def __init__(self, market):
        self.market = market
    
    def select_data(self, G, purchased_data):
        # 初回購入時はランダムに選択
        if not purchased_data:
            return random.choice(list(G.nodes()))
        
        # 2回目以降の購入時
        else:
            last_purchased_data = purchased_data[-1] # 直前に購入したデータ
            neighbors = list(G.neighbors(last_purchased_data))
            # 直前に購入したデータの近傍ノードが存在する場合
            if neighbors:
                probabilities = self.calc_probabilities(G, neighbors)
                return random.choices(neighbors, weights=[probabilities[node] for node in neighbors])[0]
            # 直前に購入したデータの近傍ノードが存在しない場合
            else:
                return random.choice(list(G.nodes()))
    
    def calc_probabilities(self, G, target_nodes):
        # ノードごとの購入確率を計算
        total_purchase_count = sum(self.market.datasets[node].purchase_count for node in target_nodes)
        if total_purchase_count == 0:
            return {node: 1 / len(target_nodes) for node in target_nodes}
        probabilities = {node: (self.market.datasets[node].purchase_count + 1) / (total_purchase_count + len(target_nodes)) for node in target_nodes}
        
        # 確率を正規化
        total_prob = sum(probabilities.values())
        return {node: prob / total_prob for node, prob in probabilities.items()}


class RankingStrategy:
    def __init__(self, market):
        self.market = market
    
    def select_data(self, G, _):
        # ノードごとの購入確率を計算
        probabilities = self.calc_probabilities(G)
        
        # 確率に基づいてノードを選択
        weights = [probabilities[node] for node in list(G.nodes())]
        return random.choices(list(G.nodes()), weights=weights, k=1)[0]
    
    def calc_probabilities(self, G):
        total_purchase_count = sum(self.market.datasets[node].purchase_count for node in G.nodes())
        if total_purchase_count == 0:
            return {node: 1 / len(G.nodes()) for node in G.nodes()}
        probabilities = {node: (self.market.datasets[node].purchase_count + 1) / (total_purchase_count + len(G.nodes())) for node in G.nodes()}
        
        # 確率を正規化
        total_prob = sum(probabilities.values())
        return {node: prob / total_prob for node, prob in probabilities.items()}


def create_buyer(strategy_weights, market):
    # 各戦略を初期化
    random_strategy = RandomStrategy()
    related_strategy = RelatedStrategy(market)
    ranking_strategy = RankingStrategy(market)
    
    strategies = {
        "random": random_strategy,
        "related": related_strategy,
        "ranking": ranking_strategy
    }
    
    strategy_list = []
    weight_list = []
    
    for strategy, weight in strategy_weights.items():
        strategy_list.append(strategies[strategy])
        weight_list.append(weight)
    
    return Buyer(strategy_list, weight_list)