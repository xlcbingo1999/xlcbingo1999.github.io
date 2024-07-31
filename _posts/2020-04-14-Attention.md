---
layout: post
title:      Attention与Transformer 笔记整理
date: 2020-04-14 17:39:00
description: Attention与Transformer 笔记整理
tags: 技术杂记
categories: 技术杂记
featured: false
---


# Attention与Transformer笔记整理

> 组会20200413
> 感谢各位大佬的整理。

## 一、问题

```
tranformer(上)：
1. 注意力机制的原理，列举一个应用场景。列举几种注意力的计算方法。
2. 了解残差网络并解释残差连接有什么好处。
3. Layer Normalization的原理
optional: 
4. 对比layer normalization和batch normalization，分析一下二者有什么优劣势，分别适用于什么场景。

transformer(下)：
1. 阐述一下自注意力机制的原理。
2. 描述一下多头注意力机制的原理。
3. transformer如何处理时间顺序。
4. 对比transformer中的encoder和decoder的结构
5. transformer与RNN（LSTM）、CNN的比较（长距离依赖、位置信息、时间复杂度、串行并行）
Optional:
6. 回顾造成神经网络过拟合的原因，并总结一下神经网络防止过拟合的方法。
```

## 二、基础内容Seq2seq

transformer已经几乎全面取代RNN了。包括前几天有一篇做SR（speech recognition）的工作也用了transformer，而且SAGAN也是……总之transformer确实是一个非常有效且应用广泛的结构，应该可以算是即seq2seq之后又一次“革命”。

### 2.1 Seq2seq任务

从一个序列映射到另一个序列的任务，并不关心输入与输出的序列是否长度相等。

两种seq2seq

* 一一对应（词性标注，可以用简单RNN）
* 非一一对应（Encoder-Decoder框架）

### 2.2 应用

机器翻译、词性标注、智能对话。

### 2.3 Encoder-Decoder框架

工作机制：先使用Encoder将输入编码映射到语义空间（通过Encoder网络生成的特征向量），得到一个固定维数的向量，表示**输入语义**。使用Decoder将语义向量解码，获得所需要的输出。如果输出是文本，则Decoder通常就是语言模型。


<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GxqNlt.png" class="img-fluid rounded z-depth-1" %}
</div>



<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GxHXgx.png" class="img-fluid rounded z-depth-1" %}
</div>


x作为Encoder的输入，另一个y输入做为Decoder输入，x和y依次按照各自的顺序传入网络。标签y既参与计算loss，也参与节点计算，而不是只做loss监督。C节点是Encoder输出的解码向量，它作为解码Decoder中cell的初始状态，进行对输出的解码。

一般其作用为在给定context vector c和所有已预测的词去预测，故t时刻翻译的结果y为以下的联合概率分布。
$$
p(y) = \prod_{t=1}^{T}p(y_{t}|(y_{1},...,y_{t-1}),c)
$$

$$
c = h_{T}
$$

优点：

* 灵活，不限制Encoder和Decoder使用何种网络，也不限制输入和输出的内容（比如输入可以是图像，输出可以是文本）
* 端到端（end-to-end）的过程，将语义理解和语言生成结合在一起。

### 2.4 Tensorflow中的seq2seq

本介绍主要使用旧接口。

#### 2.4.1 实例：拟合曲线

待补充。

#### 2.4.2 实例：股票预测

待补充。

### 2.5 缺点

Encoder给出的都是一个固定维度的向量，存在信息损失，如果输入的序列越长，Encoder的输出丢失的原始信息就越多，传入Decoder后，很难在Decoder中有太多特征表现。因此引入有注意力的Seq2seq。

### 2.6 参考资料

[1] [https://zhuanlan.zhihu.com/p/38485843](https://zhuanlan.zhihu.com/p/38485843)

[2] 《深度学习之TensorFlow 入门、原理与进阶》

## 三、基于注意力的Seq2Seq

### 3.1 attention_seq2seq【上1】

注意力机制，即在生成每个词的时候，对不同的输入词基于不同的关注权重。

距离：右侧为输入，上侧为输出。在注意力机制下，对于一个输出网络会自动学习与其对应的输入关系的权重。


<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GzZP81.png" class="img-fluid rounded z-depth-1" %}
</div>


比如you (80, 5, 0, 15, 0)，就是模型在生成you的时候的概率分布。对应列表格中值最大的部分对应的输入是“你”。说明模型在输出you的时候最关注的输入词是“你”。

### 3.2 应用场景【上1】

NLP中用于定位关键token或者特征：在一些应用中，比如句子长度特别长的机器翻译场景中，传统的RNN Encoder-Decoder表现非常不理想。一个重要的原因是 t' 时刻的输出可能更关心输入序列的某些部分是什么内容而和其它部分是什么关系并不大。

机器翻译：《深度学习之TensorFlow 入门、原理与进阶》中有代码示例。

远距离提取信息：防止RNN在顺序计算中，远距离的信息丢失。

### 3.2 模型框架

相比于基础Seq2Seq，修改后的模型特点是序列中每个时刻的Encoder生成的c，参与到Decoder的每个序列运算都会经过权重w，那么权重w都以loss的方式通过优化器调节，最终趋向于联系紧密的词。

$X = (x_{0},x_{1},x_{2},x_{3})$映射到一个隐层状态 $H = (h_{0},h_{1},h_{2},h_{3})$ 再映射到$Y = (y_{0},y_{1},y_{2})$。Y中的每个元素都和H相连，根据不同的权重对Y赋值。

图中红框为attention。


<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GxLAnf.png" class="img-fluid rounded z-depth-1" %}
</div>




#### 3.2.1 详细解释

$$
c_{i} = \sum_{j=1}^{T_{x}}a_{ij}h_{ij}
$$

$$
a_{ij} = \frac{exp(e_{ij})}{\sum_{k=1}^{T_{x}}exp(e_{ik})}
$$

$$
e_{ij} = a(s_{j-1}, h_{i})
$$

* $a_{ij}$的值越高，表示第i个输出在第j个输入上分配的注意力越多，在生成第i个输出的时候受第j个输入的影响越大。
* $e_{ij}$ encoder i处隐状态和decoder j-1 处的隐状态的匹配 match，此处的 alignment model *a* 是和其他神经网络一起去训练（即 joint learning），其反映了$h_{j}$的重要性。

### 3.3 桶的实现机制

由于输入、输出是可变长的，这给计算带来很大的效率影响。在Tensorflow中使用了一个桶的观念来权衡这个问题，思想就是初始化几个bucket，对数据预处理，按照**每个序列的长短**，将其放到不同的bucket中，小于bucket size部分统一补0来完成对齐的工作，之后就是对不同bucket的批处理计算。

这里会进行 **基于权重的交叉熵计算**： 求每个样本loss时对softmax_loss的结果乘以weight，同时乘完后除以weights的总和。

### 3.4 参考资料

[1] 《深度学习之TensorFlow 入门、原理与进阶》

[2] [https://zhuanlan.zhihu.com/p/38485843](https://zhuanlan.zhihu.com/p/38485843)

[3] Bahdanau D, Cho K, Bengio Y. Neural machine translation by jointly learning to align and translate[J]. arXiv preprint arXiv:1409.0473, 2014.

## 四、Transformer 【下4】

### 4.1 介绍

Tranformer是一个升级的Seq2Seq，由一个encoder和一个decoder组成。encoder对输入序列进行编码，encoder将X = (x0, x1, x2,... x{T{x}}) 变成H = (h0, h1, h2,... ,h{T{x}}) ，decoder再将H解码变成Y = (y0, y1, y2,... ,y{T{y}}).

**encoder和decoder不使用RNN，而是使用多个attention。**

### 4.2 应用

谷歌团队近期提出的用于生成词向量的BERT算法。

### 4.3 高层Transformer和self-attention

1. 在机器翻译中，Transformer可概括为如图

   
<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GzZn5d.png" class="img-fluid rounded z-depth-1" %}
</div>


2. Transformer的本质上是一个Encoder-Decoder的结构

   
<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407203659415.png" class="img-fluid rounded z-depth-1" %}
</div>


3. 如论文中所设置的，编码器由6个编码block组成，同样解码器是6个解码block组成。与所有的生成模型相同的是，编码器的输出会作为解码器的输入。【六块可以改成N】

   
<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407203738688.png" class="img-fluid rounded z-depth-1" %}
</div>


4. 在Transformer的encoder中，数据首先会经过一个**'self-attention'**的模块，得到加权后的特征向量Z。

   
<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407203923903.png" class="img-fluid rounded z-depth-1" %}
</div>


   三个不同的向量Query(Q)\Key(K)\Value(V)，长度都是64.他们是通过三个不同的权值矩阵由嵌入向量X(embedding vector) 乘以三个不同的权值矩阵$W_{Q}, W_{K}, W_{V}$ 得到，三个权值矩阵（512x64）。

   
<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407204318798.png" class="img-fluid rounded z-depth-1" %}
</div>


   加权后的特征向量Z计算方法：

   1） 将输入单词转化成嵌入向量；

   2） 根据嵌入向量得到q,k,v三个向量；

   3） 为每一个向量计算一个score: score = q*k；

   4） 为了梯度的稳定，对score归一化，即除以sqrt(d{k}) 【d{k}是什么？下图d{k}等于1】

   5） 对 score 施加softmax函数；

   6） softmax点乘Value值v，得到加权的每个输入向量的评分；

   7） 相加之后得到最终的输出结果 z ： z = SUM(v)。

   
<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407204811811.png" class="img-fluid rounded z-depth-1" %}
</div>


   
<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407205030601.png" class="img-fluid rounded z-depth-1" %}
</div>


   
<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407205046138.png" class="img-fluid rounded z-depth-1" %}
</div>


5. 得到Z之后，会被送到encoder的下一个模块，即Feed Forward Neural Network。这个全连接层有两层，第一层是ReLU，第二层是一个线性激活函数。

   
<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407205753680.png" class="img-fluid rounded z-depth-1" %}
</div>


   
<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407205812755.png" class="img-fluid rounded z-depth-1" %}
</div>


6. Decoder的结构：多了一个Encoder-Decoder Attention，两个Attention分别用于计算输入和输出的权值。Self-Attention用于翻译和已经翻译的前文之间的关系，Encoder-Decoder Attention用于表示当前翻译和编码的特征向量之间的关系。

   
<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407210043504.png" class="img-fluid rounded z-depth-1" %}
</div>


7. **采用了残差网络中的short-cut结构，目的是解决深度学习中的退化问题**【请参考六】

   
<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407210559073.png" class="img-fluid rounded z-depth-1" %}
</div>


### 4.4 输入编码

输入数据：通过Word2Vec等词嵌入方法将输入语料转化成特征向量，论文中使用的词嵌入的维度为d{model} = 512。

在最底层的block中，x将直接作为Transformer的输入，而在其他层中，输入则是上一个block的输出。


<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407210316225.png" class="img-fluid rounded z-depth-1" %}
</div>


### 4.5 Multi-Head Attention

Multi-Head Attention相当于h个不同的self-attention的集成（ensemble），在这里以8为例子。同self-attention一样，multi-head attention也加入了**short-cut机制**。

1. 将数据X分别输入到8个self-attention中，得到8个加权后的特征矩阵Z{i}；
2. 将8个Z{i}按列拼成一个大的特征矩阵；
3. 特征矩阵经过一层全连接层后得到Z。


<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407211412600.png" class="img-fluid rounded z-depth-1" %}
</div>


### 4.6 Encoder-Decoder Attention

是连接encoder和decoder的一个attention。Q来自于与解码器的上一个输出，K和V则来自于编码器的输出。

在机器翻译中，Decode是过程是一个顺序操作的过程，当解码第k个特征向量的时候，只能看到第k-1个及其之前的decode结果。这个时候的multi-head attention是masked multi-head attention。


<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407212250291.png" class="img-fluid rounded z-depth-1" %}
</div>


### 4.7 损失层

Decoder之后，decode的特征向量经过一层激活函数为**softmax**的全连接层之后得到反映每个单词概率的输出向量。此时我们便可以通过CTC等损失函数训练模型了。

### 4.8 位置编码【下3】

Transformer模型并没有捕捉顺序序列的能力，也就是说无论句子的结构怎么打乱，Transformer都会得到类似的结果。换句话说，Transformer只是一个功能更强大的词袋模型而已。

在编码词向量时引入了位置编码（Position Embedding）的特征。具体地说，位置编码会在词向量中加入了单词的位置信息，这样Transformer就能区分不同位置的单词了。

两种编码模式：

1. 根据数据学习
2. 自己设计编码规则【本文使用这个】：位置编码是一个长度为d{model}的特征向量，方便与词向量进行单位加操作。


<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407213000338.png" class="img-fluid rounded z-depth-1" %}
</div>



<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407213101844.png" class="img-fluid rounded z-depth-1" %}
</div>


pos表示单词的位置，i表示单词的维度。

这里的意思是将 id 为 pos 的位置映射为一个 d{model} 维的位置向量，这个向量的第 i 个元素的数值就是 PEi(pos)。

NLP任务重，除了单词的绝对位置，单词的相对位置也非常重要。根据公式$sin(\alpha+\beta) = sin\alpha·cos\beta + sin\beta·cos\alpha$ 以及$cos(\alpha+\beta) = cos\alpha·cos\beta - sin\beta·sin\alpha$，这表明位置 $k+p$ 的位置向量可以表示为位置 $k$的特征向量的线性变化，这为模型捕捉单词之间的相对位置关系提供了非常大的便利。

### 4.9 Feed forward

对于一个输入序列(x0,x1,......x{T})，对每一个x{i}都进行一次channel重组：  512 -> 2048 -> 512 【相当于对整个序列做1*1卷积】

### 4.10 Transformer优点【下5】

* 并行计算，提高训练速度，适合GPU环境

  Transformer用attention代替了原本的RNN; 而RNN在训练的时候, 当前step的计算要依赖于上一个step的hidden state的, 也就是说这是一个sequential procedure, 我每次计算都要等之前的计算完成才能展开. 而Transformer不用RNN, 所有的计算都可以并行进行, 从而提高的训练的速度.

* 建立直接的长距离连接

  将任意两个单词的距离是1。原本的RNN里, 如果第一帧要和第十帧建立依赖, 那么第一帧的数据要依次经过第二三四五...九帧传给第十帧, 进而产生二者的计算. 而在这个传递的过程中, 可能第一帧的数据已经产生了**biased**, 因此这个交互的速度和准确性都没有保障. 而在Transformer中, 由于有**self attention**的存在, **任意两帧之间都有直接的交互, 从而建立了直接的依赖**, 无论二者距离多远。

* 超越NLP机器翻译领域

### 4.11 Transformer缺点

* 使模型丧失了捕捉局部特征的能力，RNN + CNN + Transformer的结合可能会带来更好的效果。
* Transformer失去的位置信息其实在NLP中非常重要，而论文中在特征向量中加入Position Embedding也只是一个权宜之计，并没有改变Transformer结构上的固有缺陷。

### 4.12 参考资料

[1] [https://zhuanlan.zhihu.com/p/48508221](https://zhuanlan.zhihu.com/p/48508221)

[2] [https://zhuanlan.zhihu.com/p/38485843](https://zhuanlan.zhihu.com/p/38485843)

[3] [https://www.infoq.cn/article/lteUOi30R4uEyy740Ht2](https://www.infoq.cn/article/lteUOi30R4uEyy740Ht2)

## 五、残差网络

### 5.1 背景

在深度学习中，网络层数增多一般会伴着下面几个问题：

1. 计算资源的消耗【通过GPU集群解决】
2. 模型容易过拟合【通过采样海量数据，配合Dropout正则化】
3. 梯度消失/梯度爆炸问题的产生【Batch Normalization】
4. 网络退化现象（degradation）：训练集loss逐渐下降，然后趋于饱和，当你再增加网络深度的话，训练集loss反而会增大

### 5.2 残差网络

残差网络是由一系列残差块组成的。


<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407224113733.png" class="img-fluid rounded z-depth-1" %}
</div>


残差块分成两部分直接映射部分和残差部分。 $h_{x_{l}}$ 是直接映射，反应在图1中是左边的曲线； $F(x_{l},W_{l})$ 是残差部分，一般由两个或者三个卷积操作构成，即图1中右侧包含卷积的部分。Weight在卷积网络中是指卷积操作，addition是指单位加操作。

卷积网络中，x{l}和x{l+1}的feature map的数量不一样，需要使用1x1卷积进行升维和降维。$h(x_{l}) = W'_{l}x$


<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407224351074.png" class="img-fluid rounded z-depth-1" %}
</div>


```python
def res_block_v1(x, input_filter, output_filter):
    res_x = Conv2D(kernel_size=(3,3), filters=output_filter, strides=1, padding='same')(x)
    res_x = BatchNormalization()(res_x)
    res_x = Activation('relu')(res_x)
    res_x = Conv2D(kernel_size=(3,3), filters=output_filter, strides=1, padding='same')(res_x)
    res_x = BatchNormalization()(res_x)
    if input_filter == output_filter:
        identity = x
    else: #需要升维或者降维
        identity = Conv2D(kernel_size=(1,1), filters=output_filter, strides=1, padding='same')(x)
    x = keras.layers.add([identity, res_x])
    output = Activation('relu')(x)
    return output
```

### 5.3 残差网络的搭建

1. 使用VGG公式搭建Plain VGG网络
2. 在Plain VGG的卷积网络之间插入Identity Mapping，注意需要升维或降维的时候加入1X1卷积。

```python
def resnet_v1(x):
    x = Conv2D(kernel_size=(3,3), filters=16, strides=1, padding='same', activation='relu')(x)
    x = res_block_v1(x, 16, 16)
    x = res_block_v1(x, 16, 32)
    x = Flatten()(x)
    outputs = Dense(10, activation='softmax', kernel_initializer='he_normal')(x)
    return outputs
```

### 5.4 残差与误差

【y=x是观测值、 H(x) 是预测值】

##### **水位线：模型预测10m，你测量的是10.4m【观测值】，但真实值为10.5m？真实性未知！**

衡量一个残差块：H(x) = F(x) + x

* 误差：衡量观测值和真实值之间的差距
* 残差：预测值和观测值之间的差距  F(x)  = H(x) - x

### 5.5 残差网络的原理


<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407225339983.png" class="img-fluid rounded z-depth-1" %}
</div>


不考虑升维和降维的情况，h(·)是直接映射，f(·)是激活函数，一般是ReLU。

* 假设1：h(·)是直接映射
* 假设2：f(·)是直接映射

残差块：
<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407225703608.png" class="img-fluid rounded z-depth-1" %}
</div>


对于一个更深层L，其与l层的关系表示为：


<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407225735065.png" class="img-fluid rounded z-depth-1" %}
</div>


公式反应的残差网络的两个属性：

1. L层可以表示为任何一个比它浅的l层和他们之间的残差部分之和；
2. L是各个残差块特征的单位累核，而MLP是特征矩阵的累积。【多层感知机（MLP，Multilayer Perceptron）也叫人工神经网络（ANN，Artificial Neural Network），除了输入输出层，它中间可以有多个隐层，最简单的MLP只含一个隐层】


<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407230121460.png" class="img-fluid rounded z-depth-1" %}
</div>


残差网络的梯度：
<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407230357773.png" class="img-fluid rounded z-depth-1" %}
</div>


公式反应的残差网络的两个属性：

1. 在整个训练过程中，
<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407230430137.png" class="img-fluid rounded z-depth-1" %}
</div>
不可能一直为-1，也就是残差网络中不会出现梯度消失的问题。
2. $\frac{\partial \epsilon}{\partial x_{L}}$表示L层的梯度可以直接传递到任何一个比它浅的l层。

当残差块满足上面**两个假设**时，信息可以非常畅通的在高层和低层之间相互传导，说明这两个假设是让残差网络可以训练深度模型的充分条件。

#### 5.5.1 直接映射是最好的残差网络的选择

对于假设1，采用反证法，假设
<div class="row mt-3">
    {% include figure.html path="assets/img/old_mypic/image-20200407231715828.png" class="img-fluid rounded z-depth-1" %}
</div>
，残差块表示为：


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200407231741281.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200407231741281.png)

对于更深层次的L层
$$
x_{L} = (\prod_{i=l}^{L-1}\lambda_{l})x_{l} + \sum_{i=l}^{L-1}(\prod_{i=l}^{L-1} F(x_{l},W_{l}))
$$
如果只考虑左边的情况，损失函数对x{l}求偏微分得到：
$$
\frac{\partial \epsilon}{\partial x_{l}} = (\prod_{i=l}^{L-1}\lambda_{l})
$$
公式反应的属性：

1. $\lambda$>1 ，可能会发生梯度爆炸。
2. $\lambda$<1 ， 梯度变成0，会阻碍残差网络信息的方向传递，从而影响残差网络的训练。
3. $\lambda$=1 是必要条件。

不同网络的差距：


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200407233933533.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200407233933533.png)


<div class="row mt-3">
    {% include figure.html path="https://pic4.zhimg.com/v2-5d8fd2868a4ba30e61ce477ab00d7f0f_r.jpg" class="img-fluid rounded z-depth-1" %}
</div>


所以假设一成立，即：


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200407234708691.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200407234708691.png)

#### 5.5.2 激活函数的位置

BN：batch norm


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200407234946413.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200407234946413.png)

```python
def res_block_v2(x, input_filter, output_filter):
    res_x = BatchNormalization()(x)
    res_x = Activation('relu')(res_x)
    res_x = Conv2D(kernel_size=(3,3), filters=output_filter, strides=1, padding='same')(res_x)
    res_x = BatchNormalization()(res_x)
    res_x = Activation('relu')(res_x)
    res_x = Conv2D(kernel_size=(3,3), filters=output_filter, strides=1, padding='same')(res_x)
    if input_filter == output_filter:
        identity = x
    else: #需要升维或者降维
        identity = Conv2D(kernel_size=(1,1), filters=output_filter, strides=1, padding='same')(x)
    output= keras.layers.add([identity, res_x])
    return output

def resnet_v2(x):
    x = Conv2D(kernel_size=(3,3), filters=16 , strides=1, padding='same', activation='relu')(x)
    x = res_block_v2(x, 16, 16)
    x = res_block_v2(x, 16, 32)
    x = BatchNormalization()(x)
    y = Flatten()(x)
    outputs = Dense(10, activation='softmax', kernel_initializer='he_normal')(y)
    return outputs
```

#### 5.5.3 残差网络与模型集成

对于一个3层的残差网络可以展开成一棵含有8个节点的二叉树，而最终的输出便是这8个节点的集成。而他们的实验也验证了这一点，随机删除残差网络的一些节点网络的性能变化较为平滑，而对于VGG等stack到一起的网络来说，随机删除一些节点后，网络的输出将完全随机。


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200407235341710.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200407235341710.png)



### 5.6 参考资料



## 六、Normalization 归一化【上3/上4】

### 6.1 使用Normalization的原因

#### 6.1.1 独立同分布与白化

独立同分布的数据可以简化常规机器学习模型的训练、提升机器学习模型的预测能力，已经是一个共识。

把数据喂给机器学习模型之前，“**白化（whitening）**”是一个重要的数据预处理步骤。其具有两个目的：

1. 去除特征间的相关性 -> 独立
2. 使得所有的特征巨有相同的均值和方差 -> 同分布

主要的方法：PCA

#### 6.1.2  Internal Covariate Shift (内部协方差移位)

深度神经网络涉及到很多层的叠加，而每一层的参数更新会导致上层的输入数据分布发生变化，通过层层叠加，高层的输入分布变化会非常剧烈，这就使得高层需要不断去重新适应底层的参数更新。为了训好模型，我们需要非常谨慎地去设定学习率、初始化权重、以及尽可能细致的参数更新策略。

于神经网络的各层输出，由于它们经过了层内操作作用，其分布显然与各层对应的输入信号分布不同，而且差异会随着网络深度增大而增大，可是它们所能“指示”的样本标记（label）仍然是不变的，这便符合了covariate shift的定义。

#### 6.1.3 ICS的问题

每个神经元的输入数据不再是“独立同分布”。

其一，上层参数需要不断适应新的输入数据分布，降低学习速度。

其二，下层输入的变化可能趋向于变大或者变小，导致上层落入饱和区，使得学习过早停止。

其三，每层的更新都会影响到其它层，因此每层的参数更新策略需要尽可能的谨慎。

### 6.2 Normalization的通用框架和基本思想

神经元接收一组输入向量$X=(x_{1},x_{2},...,x_{d})$，通过某种运算得到一个标量值$y = f(x)$

由于ICS的存在，x的分布会相差很大，所以要进行白化。但是白化太昂贵，于是就退而求其次，使用Normalization。在发送给神经元的时候，对x进行**平移和伸缩变化**。


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200408001110390.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200408001110390.png)
$$
\mu 是平移参数， \sigma 是缩放参数，通过这两个参数进行shift和scale变换:\hat x = \frac{x-\mu}{\sigma}
$$
操作得到均值为0，方差为1的标准分布。
$$
b是再平移参数，g是再缩放参数，y = g·\hat x + b
$$

$$
b是再平移参数，g是再缩放参数，y = g·\hat x + b
$$
操作得到均值为b，方差为g^2的标准分布。【**为了保证模型的表达能力不因为规范化而下降**。】通过g和b参数把激活输入值从标准正态分布左移或者右移一点并长胖一点或者变瘦一点，每个实例挪动的程度不一样，这样等价于把非线性函数的值从正中心周围的线性区往非线性区动了动。**核心思想应该是想找到一个线性和非线性的较好平衡点，既能享受非线性的较强表达能力的好处，又避免太靠非线性区两头使得网络收敛速度太慢。**

原因：

1. 第一步的变换将输入数据限制到了一个全局统一的确定范围（均值为 0、方差为 1）。下层神经元可能很努力地在学习，但不论其如何变化，其输出的结果在交给上层神经元进行处理之前，将被粗暴地重新调整到这一固定范围。

2. 规范化后的数据进行再平移和再缩放，使得每个神经元对应的输入范围是针对该神经元量身定制的一个确定范围。rescale 和 reshift 的参数都是可学习的，这就使得 Normalization 层可以学习如何去尊重底层的学习结果。

3. 保证获得非线性的表达能力。Sigmoid 等激活函数在神经网络中有着重要作用，通过区分饱和区和非饱和区，使得神经网络的数据变换具有了非线性计算能力。而第一步的规范化会将几乎所有数据映射到激活函数的非饱和区（线性区），仅利用到了线性变化能力，从而降低了神经网络的表达能力。而进行再变换，则可以将数据从线性区变换到非线性区，恢复模型的表达能力。

   
<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200408110231170.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200408110231170.png)

### 6.3 主流Normalization方法梳理


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200408112942948.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200408112942948.png)

#### 6.3.1 Batch Normalization - 纵向规范化


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200408113001609.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200408113001609.png)


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200408002014058.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200408002014058.png)

1. 利用网络训练时一个 mini-batch 的数据来计算该神经元 $x_{i}$ 的均值和方差,因而称为 Batch Normalization。


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200408111021890.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200408111021890.png)

m是 mini-batch的大小。

按上图所示，相对于一层神经元的水平排列，BN 可以看做一种纵向的规范化。由于 BN 是针对单个维度定义的，因此标准公式中的计算均为 element-wise 的。

BN 独立地规范化每一个输入维度x{i} ，但规范化的参数是一个 mini-batch 的一阶统计量和二阶统计量。这就要求 每一个 mini-batch 的统计量是整体统计量的近似估计，或者说每一个 mini-batch 彼此之间，以及和整体数据，都应该是近似同分布的。分布差距较小的 mini-batch 可以看做是为规范化操作和模型训练引入了噪声，可以增加模型的鲁棒性；但如果每个 mini-batch的原始分布差别很大，那么不同 mini-batch 的数据将会进行不一样的数据变换，这就增加了模型训练的难度。

2. BN 比较适用的场景是：每个 mini-batch 比较大，数据分布比较接近。在进行训练之前，要做好充分的 shuffle. 否则效果会差很多。，由于 BN 需要在运行过程中统计每个 mini-batch 的一阶统计量和二阶统计量，因此**不适用于 动态的网络结构 和 RNN 网络。**

3. **激活输入值**（就是深度神经网络中每个隐层在**进行非线性变换处理前的数据**，即**BN一定是用在激活函数之前的！！**）


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200408110249089.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200408110249089.png)

训练收敛慢的原因：一般是整体分布逐渐往非线性函数的取值区间的上下限两端靠近（对于Sigmoid函数来说，在极大或极小的值处函数的导数接近0），所以这导致反向传播时低层神经网络的梯度消失，这是训练深层神经网络收敛越来越慢的**本质原因**。

BN就是通过一定的规范化手段，把每层神经网络任意神经元这个激活输入值的分布强行拉回到均值为0方差为1的标准正态分布，这样使得激活输入值落在非线性函数对**输入比较敏感的区域**（例如sigmoid函数的中间的部分），这样输入的小变化就会导致损失函数较大的变化，意思是这样**让梯度变大**，避免梯度消失问题产生，而且梯度变大意味着学习收敛速度快，能大大加快训练速度。**经过BN后，目前大部分激活输入值都落入非线性函数的线性区内（近似线性区域），其对应的导数远离导数饱和区，这样来加速训练收敛过程。**

4. 优点：

* 提高训练速度、收敛过程大大加快；
* 增加分类效果，防止过拟合；
* 方便调参，可以使用大的学习率

5. 局限：

* BN适用于batch size较大且各mini-batch分布相近似的场景下（训练前需进行充分的shuffle）。不适用于动态网络结构和RNN。其次，BN只在训练的时候用，inference的时候不会用到，因为inference的输入不是批量输入。

#### 6.3.2 Layer Normalization - 横向规范化


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200408113019895.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200408113019895.png)


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200408002349398.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200408002349398.png)

层规范化就是针对 BN 的上述不足而提出的。与 BN 不同，LN 是一种横向的规范化，如图所示。它综合考虑一层所有维度的输入，计算该层的平均输入值和输入方差，然后用同一个规范化操作来转换各个维度的输入。


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200408112015761.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200408112015761.png)

H是某个隐藏层的神经元数量。

LN 针对单个训练样本进行，不依赖于其他数据，因此可以避免 BN 中受 mini-batch 数据分布影响的问题，可以用于 小mini-batch场景、动态网络场景和 RNN，特别是自然语言处理领域。此外，LN 不需要保存 mini-batch 的均值和方差，节省了额外的存储空间。

LN 对于一整层的神经元训练得到同一个转换——所有的输入都在同一个区间范围内。如果不同输入特征不属于相似的类别（比如颜色和大小），那么 LN 的处理可能会降低模型的表达能力。

优点：不需要批训练，在单条数据内部就能归一化。无须保存mini-batch的均值和方差，节省了存储空间。

缺点：对于相似性相差较大的特征（比如颜色和大小），LN会降低模型的表示能力。

#### 6.3.3 Instance Normalization - 实例规范化


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200408113404640.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200408113404640.png)

Instance norm和Batch norm的区别只有一点不同，那就是BN是作用于一个batch，而IN则是作用于单个样本。在一个channel内做归一化。

#### 6.3.4 Group Normalization - 组规范化


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200408113508859.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200408113508859.png)

将channel方向分group，然后每个group内做归一化。**LN和IN只是GN的两种极端形式。**

#### 6.3.3 BN和LN的对比


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200408112212220.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200408112212220.png)

- BN是“竖”着来的，各个维度分别做规范化，所以与batch size有关系；
- LN是“横”着来的，对于一个样本，不同的神经元neuron间做规范化；

### 6.4 Normalization 效果


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200408114347725.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200408114347725.png)

1. 权重伸缩不变性

   **权重伸缩不变性（weight scale invariance）** 指的是：当权重W按照常量进行伸缩时，得到的规范化后的值保持不变。

   
<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200408114516358.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200408114516358.png)


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200408114525581.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200408114525581.png)

**权重伸缩不变性可以有效地提高反向传播的效率。**


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200408114550609.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200408114550609.png)

**权重的伸缩变化不会影响反向梯度的 Jacobian 矩阵，因此也就对反向传播没有影响**，避免了反向传播时因为权重过大或过小导致的梯度消失或梯度爆炸问题，从而加速了神经网络的训练。


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200408114611299.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200408114611299.png)

浅层的权重值越大，其梯度就越小。这样，参数的变化就越稳定，相当于实现了参数正则化的效果，避免参数的大幅震荡，提高网络的泛化性能。



2. **Normalization 的数据伸缩不变性**


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200408114822336.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200408114822336.png)

**数据伸缩不变性仅对 BN、LN 和 IN和GN成立**。因为这四者对输入数据进行规范化，因此当数据进行常量伸缩时，其均值和方差都会相应变化，分子分母互相抵消。而 WN 不具有这一性质。

**数据伸缩不变性可以有效地减少梯度弥散，简化对学习率的选择。**


<div class="row mt-3">
    {% include figure.html path="D:\Work and study\Study\Nlp\组会20200413.assets\image-20200408114911541.png" class="img-fluid rounded z-depth-1" %}
</div>
](assets/img/old_mypic/image-20200408114911541.png)

每一层神经元的输出依赖于底下各层的计算结果。如果没有正则化，当下层输入发生伸缩变化时，经过层层传递，可能会导致数据发生剧烈的膨胀或者弥散，从而也导致了反向计算时的梯度爆炸或梯度弥散。

加入 Normalization 之后，不论底层的数据如何变化，**对于某一层神经元**$h_{l}=f_{W_{l}}(x_{l})$而言，其输入$x_{l}$永远保持标准的分布，使得高层的训练更加简单。


<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GzVRjf.png" class="img-fluid rounded z-depth-1" %}
</div>


数据的伸缩变化也不会影响到对该层的权重参数更新，使得训练过程更加鲁棒，简化了对学习率的选择。

## 七、自注意力机制

### 7.1 介绍与应用场景

**自注意力**，又称”intra-attention“，是一种在计算同一序列表示时，权重和序列的位置相关机制，被证明在机器阅读理解，抽象概要（abstractive summarization）和图片描述生成中非常有效。

自注意力机制能够学习到当前词和句中先前词之前的关联性。


<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GzVIEQ.png" class="img-fluid rounded z-depth-1" %}
</div>



<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GzVoNj.png" class="img-fluid rounded z-depth-1" %}
</div>


### 7.2 自注意型网络和其他网络的不同

局部编码：卷积神经网络显然是基于 N-gram 的局部编码；而对于循环神经网络，由于梯度消失等问题也只能建立短距离依赖。


<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GzVT4s.png" class="img-fluid rounded z-depth-1" %}
</div>


长距离依赖编码：


<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GzVHCn.png" class="img-fluid rounded z-depth-1" %}
</div>


实线表示为可学习的权重，虚线表示动态生成的权重。

全连接网络虽然是一种非常直接的建模远距离依赖的模型， 但是无法处理变长的输入序列。不同的输入长度，其连接权重的大小也是不同的。可以利用注意力机制来“动态”地生成不同连接的权重，这就是**自注意力模型（self-attention model）**。由于自注意力模型的权重是**动态生成**的，因此可以处理变长的信息序列。

### 7.3 图解

一对单词被输入到函数 f(⋅) 中，从而提取出它们之间的关系。对于某个特定的位置 t，有 T-1 对单词被归纳，而我们通过求和或平均或任意其它相关的技术对句子进行表征。当我们具体实现这个算法时，我们会对包括当前单词本身的 T 对单词进行这样的计算。


<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GzVc9I.png" class="img-fluid rounded z-depth-1" %}
</div>


α(⋅,⋅) 控制了每个单词组合可能产生的影响，和上式子的I(·,·)类似。在句子「I like you like this」中，两个单词「I」和「you」可能对于确定句子的情感没有帮助。然而，「I」和「like」的组合使我们对这句话的情感有了一个清晰的认识。在这种情况下，我们给予前一种组合的注意力很少，而给予后一种组合的注意力很多。通过引入权重向量 α(⋅,⋅)，我们可以让算法调整单词组合的重要程度。

$$ h_{t} = \sum_{t'=1}^{T}\alpha(x_{t},x_{t'})f(x_{t},x_{t'})$$


<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GzVhDS.png" class="img-fluid rounded z-depth-1" %}
</div>


如果我们把 10 个句子输入到网络中，我们会得到 10 个如下所示的注意力矩阵。


<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GzV4Hg.png" class="img-fluid rounded z-depth-1" %}
</div>


### 7.4 实现


<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GzV2gP.png" class="img-fluid rounded z-depth-1" %}
</div>


假设我们想要得到第 i 个单词的表征。对于包含第 i 个单词的单词组合，会生成两个输出：一个用于特征提取（绿色圆圈），另一个用于注意力加权（红色圆圈）。这两个输出可能共享同一个网络，但在本文中，我们为每个输出使用单独的网络。在得到最后的注意力权重之前，注意力（红色圆圈）的输出通过需要经过 sigmoid 和 softmax 层的运算。这些注意力权重会与提取出的特征相乘，以得到我们感兴趣的单词的表征。

### 7.5 参考来源

[1] https://www.jianshu.com/p/9b922fb83d77

[2] https://www.cnblogs.com/robert-dlut/p/8638283.html

[3] https://www.infoq.cn/article/lteUOi30R4uEyy740Ht2

## 八、多头注意力机制


<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GzVb3q.png" class="img-fluid rounded z-depth-1" %}
</div>


多头attention（Multi-head attention）结构如上图，Query，Key，Value首先进过一个线性变换，然后输入到放缩点积attention，注意这里要做h次，也就是所谓的多头，每一次算一个头，**头之间参数不共享，**每次Q，K，V进行线性变换的参数
<div class="row mt-3">
    {% include figure.html path="https://math.jianshu.com/math?formula=W" class="img-fluid rounded z-depth-1" %}
</div>
是不一样的。然后将h次的放缩点积attention结果进行拼接，再进行一次线性变换得到的值作为多头attention的结果。

可以看到，google提出来的多头attention的不同之处在于进行了h次计算而不仅仅算一次，论文中说到这样的**好处**是可以允许模型在不同的表示子空间里学习到相关的信息。


<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GzVqg0.png" class="img-fluid rounded z-depth-1" %}
</div>



<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GxBXeU.png" class="img-fluid rounded z-depth-1" %}
</div>




## 九、Transformer/CNN/RNN

长距离依赖、位置信息、时间复杂度、串行并行

### 9.1 长距离依赖


<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GzVLvV.png" class="img-fluid rounded z-depth-1" %}
</div>


在特定的长距离特征捕获能力测试任务：Transformer>RNN>>CNN

在比较远的距离上（主语谓语距离大于13）：Transformer ≈ RNN>>CNN

CNN解决这个问题是靠堆积深度来获得覆盖更长的输入长度的，所以CNN在这方面的表现与卷积核能够覆盖的输入距离最大长度有关系。如果通过增大卷积核的kernel size，同时加深网络深度，以此来增加输入的长度覆盖。

Multi-head attention的head数量严重影响NLP任务中Long-range特征捕获能力：结论是head越多越有利于捕获long-range特征。

### 9.2 位置信息

RNN：因为是线性序列结构，所以很自然它天然就会把位置信息编码进去。

CNN：卷积核是能保留特征之间的相对位置的，道理很简单，滑动窗口从左到右滑动，捕获到的特征也是如此顺序排列，所以它在结构上已经记录了相对位置信息了。但是如果卷积层后面立即接上Pooling层的话，Max Pooling的操作逻辑是：从一个卷积核获得的特征向量里只选中并保留最强的那一个特征，所以到了**Pooling层，位置信息就被扔掉了**，这在NLP里其实是有信息损失的。所以在NLP领域里，目前CNN的一个发展趋势是抛弃Pooling层，靠全卷积层来叠加网络深度。


<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GzVXuT.png" class="img-fluid rounded z-depth-1" %}
</div>


Transformer：Self attention会让当前输入单词和句子中任意单词发生关系，然后集成到一个embedding向量里，但是当所有信息到了embedding后，位置信息并没有被编码进去。必须明确的在输入端将Positon信息编码，Transformer是用位置函数来进行位置编码的，而Bert等模型则给每个单词一个Position embedding，将单词embedding和单词对应的position embedding加起来形成单词的输入embedding。

### 9.3 串行并行能力

RNN在并行计算方面有严重缺陷，这是它本身的序列依赖特性导致的。它的线形序列依赖性非常符合解决NLP任务。但是也正是这个线形序列依赖特性，导致它在并行计算方面要想获得质的飞跃，困难重重。

CNN和Transformer来说，因为它们不存在网络中间状态不同时间步输入的依赖关系，所以可以非常方便及自由地做并行计算改造。

Transformer ≈ CNN >> RNN

### 9.4 计算复杂度


<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GzVjDU.png" class="img-fluid rounded z-depth-1" %}
</div>


三者单层的计算量：Transformer Block > CNN > RNN

self attention：平方项是句子长度，因为每一个单词都需要和任意一个单词发生关系来计算attention，所以包含一个n的平方项。Transformer包含多层，其中的skip connection后的Add操作及LayerNorm操作不太耗费计算量，我先把它忽略掉，后面的FFN操作相对比较耗时，它的时间复杂度应该是n乘以d的平方。

RNN：平方项是embedding size。

CNN：平方项是embedding size。

如果句子平均长度n大于embedding size，那么意味着Self attention的计算量要大于RNN和CNN；而如果反过来，就是说如果embedding size大于句子平均长度，那么明显RNN和CNN的计算量要大于self attention操作。一般正常的句子长度，平均起来也就几十个单词吧。而当前常用的embedding size从128到512。

速度：self-attention > RNN > CNN >  Transformer

### 9.5 参考资料

[1] [https://zhuanlan.zhihu.com/p/54743941](https://zhuanlan.zhihu.com/p/54743941)



## 十、过拟合

### 10.1 过拟合的定义与宏观判断

**定义**：给定一个假设空间H，一个假设h属于H，如果存在其他的假设h’属于H,使得在训练样例上h的错误率比h’小，但在整个实例分布上h’比h的错误率小，那么就说假设h过度拟合训练数据。


<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GzVzE4.png" class="img-fluid rounded z-depth-1" %}
</div>



<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GzVvbF.png" class="img-fluid rounded z-depth-1" %}
</div>


### 10.2 过拟合的原因

1.  训练集的数量级和模型的复杂度不匹配。训练集的数量级要小于模型的复杂度；

2.  训练集和测试集特征分布不一致；

3.  样本里的噪音数据干扰过大，大到模型过分记住了噪音特征，反而忽略了真实的输入输出间的关系；

4.  权值学习迭代次数足够多(Overtraining)，拟合了训练数据中的噪声和训练样例中没有代表性的特征。


### 10.3 解决方案

1. 调小模型复杂度：使模型适合自己训练集的数量级（缩小宽度和减小深度）

2. 增加数据：训练集越多，过拟合的概率越小

3. 正则化：参数太多，会导致我们的模型复杂度上升，容易过拟合，也就是我们的训练误差会很小。 正则化是指通过引入额外新信息来解决机器学习中过拟合问题的一种方法。这种额外信息通常的形式是模型复杂性带来的惩罚度。 正则化可以保持模型简单，另外，规则项的使用还可以约束我们的模型的特性。

   
<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GzZSUJ.png" class="img-fluid rounded z-depth-1" %}
</div>


   a) L0范数：向量中非0的元素的个数。如果我们用L0范数来规则化一个参数矩阵W的话，就是希望W的大部分元素都是0即让参数W是稀疏的。 

   b) L1范数：向量中各个元素绝对值之和，也叫“稀疏规则算子”（Lasso regularization）。

   c) L2范数：||W||^2。指向量各元素的平方和然后求平方根。我们让L2范数的规则项||W||^2最小，可以使得W的每个元素都很小，都接近于0，但与L1范数不同，它不会让它等于0，而是接近于0。

4. dropout：在训练时候以一定的概率p来跳过一定的神经元。

   
<div class="row mt-3">
    {% include figure.html path="https://s1.ax1x.com/2020/04/14/GzZp59.png" class="img-fluid rounded z-depth-1" %}
</div>


5. early stopping：一种迭代次数截断的方法来防止过拟合的方法，即在模型对训练数据集迭代收敛之前停止迭代来防止过拟合。 

   在每一个Epoch结束时（一个Epoch集为对所有的训练数据的一轮遍历）计算validation data的accuracy，当accuracy不再提高时，就停止训练。在训练的过程中，记录到目前为止最好的validation accuracy，当**连续10次**Epoch（或者更多次）没达到最佳accuracy时，则可以认为accuracy不再提高了。

6. ensemble集成：集成学习算法也可以有效的减轻过拟合。Bagging通过平均多个模型的结果，来降低模型的方差。Boosting不仅能够减小偏差，还能减小方差。

7. 重新清晰数据：数据清洗从名字上也看的出就是把“脏”的“洗掉”，指发现并纠正数据文件中可识别的错误的最后一道程序，包括检查数据一致性，处理无效值和缺失值等。导致过拟合的一个原因也有可能是数据不纯导致的，如果出现了过拟合就需要我们重新清洗数据。

## 十一、Attention 机制的大佬实现

[https://yq.aliyun.com/articles/342508?utm_content=m_39938](https://yq.aliyun.com/articles/342508?utm_content=m_39938)

来自中山大学数学学院的一个师兄写的文章，并附上了他的代码。个人对这些代码的理解还不够深入，后期请务必重新阅读。

## 十二、拓展Attention

参考文章： [https://blog.csdn.net/qq_41058526/article/details/80578932](https://blog.csdn.net/qq_41058526/article/details/80578932)
