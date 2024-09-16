def get_purchase_distr(saver):
    total_num_purchased = []
    
    for iteration, result in saver.results.items():
        each_num_purchased = {}
        for step, data in result.items():
            for item in data["data_info"]:
                data_id = item["data_id"]
                num_purchased = item["num_purchased"]
                
                if data_id not in each_num_purchased:
                    each_num_purchased[data_id] = 0
                
                each_num_purchased[data_id] += num_purchased
        total_num_purchased.append(each_num_purchased)
    
    purchase_distr = {}
    
    for result in total_num_purchased:
        for value in result.values():
            if value not in purchase_distr:
                purchase_distr[value] = 0
            purchase_distr[value] += 1

    sorted_distr = dict(sorted(purchase_distr.items()))

    return sorted_distr