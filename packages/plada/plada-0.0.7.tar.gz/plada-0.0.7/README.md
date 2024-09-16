# plada
**PlaDa** (**Pla**tform for **Da**ta market)

## Install
pipでインストール可能
```
$ pip install plada
$ python
>> import plada
```
notebookで使用する場合は!pipを利用
```
!pip install plada
import plada
```

## How to use
step1：市場モデルの設定
- ただし、modelはGraphオブジェクトで、"variables"を持つ必要あり
```
model = nx.read_graphml("test.graphml")
```
step2：configによる設定
```
config = {
    "Simulation":{
        "num_iterations": 1,
        "num_steps": 10,
        "isPrice": False,
    },
    "Market":{
        "model": model,
    },
    "Agent": {
        "num_buyers": 20,
        "strategy_weights": {
            "random": 0.4,
            "related": 0.3,
            "ranking": 0.3,
        },
    }
}
```
step3：シミュレーションを実行
```
saver = Saver()
runner = Runner(settings=config, logger=saver)

runner.main()
```
