# OOP 物件導向程式設計
OOP=Object-oriented Programming
## 為什麼我要講這個?
YTP進來的人大部分都是比較熟悉競賽程式，而沒有其他程式設計經驗。可能連基本OOP的概念都不理解，在運用Python套件時比較有障礙。
## 重點
思想比較重要，要知道在哪些地方可能會需要用OOP  

**資料和行為放在一起**  

競程中，通常都是要用什麼變數就開全域變數，比如[這題](https://ojdl.ck.tp.edu.tw/problem/7139)需要用兩棵線段樹，還得要支援區間修改、加值，如果是用陣列型，宣告變數可能會長這樣:  
```cpp
int seg[4][4*N],seg2[4][4*N],lzadd[4][4*N],lzmod[4][4*N];
bool mod[4][4*N],mod2[4][4*N];
```
而在修改或查詢時，會需要用陣列index來指定要修改哪顆線段樹，程式碼會變得不好讀、維護。  
如果把資料和行為放在一起，可以明確知道資料和行為具體是在做什麼。  
使用物件導向後，可以把節點、樹做成類別(Class)，就不會發生變數太多搞混的問題。  


<details close>

  <summary>範例程式</summary>

  ```python
class Node:
    def __init__(self, v=None, lc=None, rc=None):
        self.v=None
        self.lc=None
        self.rc=None
        if v!=None:
            self.v=v
        elif lc!=None and rc!=None:
            self.lc=lc
            self.rc=rc
class SegmentTree:
    def __init__(self, pullFunction, mergeFunction, noneValue, l=None, r=None, values=None, root=None):
        self.l=None
        self.r=None
        self.root=Node()
        self.pullFunction=pullFunction#for Node
        self.mergeFunction=mergeFunction#for value
        self.noneValue=noneValue

        if l!=None and r!=None and values!=None:
            self.l=l
            self.r=r
            self.curInit(self.root, l, r, values)
        elif root!=None:
            self.root=root
    def curInit(self, node, l, r, values):
        if l>=r:
            return
        if l+1==r:
            node.v=values[l]
            return
        node.lc=Node()
        node.rc=Node()
        m=(l+r)//2
        self.curInit(node.lc, l, m, values)
        self.curInit(node.rc, m, r, values)
        self.pullFunction(node)

    def curQuery(self, cur, l, r, ql, qr):
        if r<=ql or qr<=l:
            return self.noneValue
        if ql<=l and r<=qr:
            return cur.v
        m=(l+r)//2
        return self.mergeFunction(self.curQuery(cur.lc, l, m, ql, qr), self.curQuery(cur.rc, m, r, ql, qr))
    def query(self, ql, qr):
        return self.curQuery(self.root, self.l, self.r, ql, qr)
    
    def curUpdate(self, cur, l, r, pos, value):
        if l+1==r:
            cur.v=value
            return
        m=(l+r)/2
        if pos<m:
            self.curUpdate(cur.lc, l, m, pos, value)
        else:
            self.curUpdate(cur.rc, m, r, pos, value)
        self.pullFunction(cur)
    def update(self, pos, value):
        self.curUpdate(self.root, self.l, self.r, pos, value)
def maxPull(a:Node):
    a.v=max(a.lc.v, a.rc.v)
def maxMerge(a:int, b:int):
    return max(a, b)

def addPull(a:Node):
    a.v=a.lc.v+a.rc.v
def addMerge(a:int, b:int):
    return a+b
n=int(input())
a=list(map(int, input().split()))
tree=SegmentTree(addPull, addMerge, 0, 0, n, a)
q=int(input())
for i in range(q):
    l, r=map(int, input().split())
    l-=1
    r-=1
    if l>r:
        l, r=r, l
    print(tree.query(l, r+1))
```

</details>

程式結構

* Node
    * \_\_init\_\_
    
* SegmentTree
    * \_\_init\_\_
    * curInit : 遞迴初始化
    * curQuery : 遞迴查詢
    * query : 區間查詢
    * curUpdate : 遞迴修改
    * update : 單點修改

值得一提的是，pullFunction、mergeFunction、noneValue，在class中未定義，要當成參數傳進來，不同功能的線段樹就不用分開寫

## 特性
封裝 (Encapsulation)：  
把物件當成黑盒子，不用管裡面是怎麼運作的，有點像函數。  
    
繼承 (Inheritance)：  
一個類別可能有一些子類別，比如Car底下有各種車。  
可以定義抽象類別，只寫出要實作哪些方法，具體的類別需要用繼承的方式定義，如Python的abc(Abstract Base Classes)，可以參考[我寫的程式](https://github.com/kennychenfs/2048-ai/blob/fa992f332f08bc5f5bc95e79559ad448a75bf6df/network.py#L146-L558)

## AI(Tensorflow)的應用
Tensorflow2中定義Keras的Model有很多種方式，比如：
* 直接用Sequential，把一些Layer串起來(Sequential API)
* 用tf.Keras.models.Model指定輸入輸出來建構模型(Functional API)
* 繼承tf.Keras.Model，自己定義\_\_init\_\_、call(Model Subclassing)

把各個不同的功能交給不同類別的物件來做，比如訓練、存取硬碟中的資料、爬蟲、主要流程控制等，每個功能寫成獨立的類別，會更容易懂。

## Python基本實作
類別(Class): 定義事物的抽象特點，包含屬性(Attribute，變數)和方法(Method，函數)
物件(Object): 用類別生出的實例
```python
class Car:
    def __init__(self, name):
        self.name=name
class SpeakingCar(Car):
    def speak(self):
        print(f'Hello, I\'m {self.name}!')
Alice = SpeakingCar('Alice')
Alice.speak()
```
## 延伸閱讀
[給OOP初學者的建議：先搞懂「資料跟行為在一起」就好，其它的慢慢來](https://blog.turn.tw/?p=3093)  
[物件導向(Object Oriented Programming)概念](https://totoroliu.medium.com/%E7%89%A9%E4%BB%B6%E5%B0%8E%E5%90%91-object-oriented-programming-%E6%A6%82%E5%BF%B5-5f205d437fd6)
