# ML
## 簡介
<a href="https://youtu.be/dQw4w9WgXcQ"><img src="https://ithelp.ithome.com.tw/upload/images/20181015/20112540OrwLllgNdy.png" title="會有人點圖片嗎？"/></a>  
* AI: 讓電腦表現得像是人類般有智慧並進而幫助人類
* ML: 用數學模型進行迴歸(Regression)、分類(Classification)、分群(Clustering)
<a href="https://youtu.be/dQw4w9WgXcQ"><img src="https://i.imgur.com/FaJAnOp.png" title="會有人點圖片嗎？"/></a>  
* DL: 用更大型的數學模型做ML做的事
如NN、CNN、RNN等

## ML 模型
* 迴歸(Regression)，比如迴歸直線，把一堆(x,y)數據用一次函數近似，也可以輸入多變數、或模型更複雜(高次、非線性)
* 決策樹(Decision Tree)，從根節點開始，根據條件判斷往哪個子節點走，最終到葉節點就得到答案
<a href="https://youtu.be/dQw4w9WgXcQ"><img src="https://miro.medium.com/max/700/1*L9AcBn8WmWN44s-NQiDbOQ.png" title="會有人點圖片嗎？"/></a>  
訓練時條件是大小比較，演算法會找到最適合的模型，可以調整最大深度的參數來防止過擬和或增加模型複雜程度
* K-Means，把一堆點分群(Clustering)，算是非監督式學習。具體作法:指定k個中心，每次依據距離公式把點分到最近中心的群，並以群的中心點作為下一次的中心。

## 術語介紹
* 監督式學習(Supervised Learning):給定輸入輸出，叫AI去學它的規律
* 非監督式學習(Unsupervised Learning):只給資料，叫AI分類、分群
* 強化式學習(Reinforcement Learning):給定一個環境(Environment)，AI根據狀態(State)選擇動作(Action)，環境回饋獎勵(Reward)讓AI學習與環境互動(最大化Reward)

---

* 過擬和(Overfitting):擬和指AI模型逼近資料的過程，過擬和指AI模型過於複雜，做出過當的逼近
<a href="https://youtu.be/dQw4w9WgXcQ"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Overfitting.svg/1200px-Overfitting.svg.png" title="會有人點圖片嗎？"/></a>  
黑線可以較適當的描述紅點與藍點的邊界，而綠線太過誇大，實際使用會有極端數值出現(INF)
