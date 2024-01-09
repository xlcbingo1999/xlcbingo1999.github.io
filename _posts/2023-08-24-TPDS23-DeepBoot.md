---
layout: post
title: 阅读笔记 - (TPDS'23)DeepBoot Dynamic Scheduling System for Training and Inference Deep Learning Tasks in GPU Cluster
date: 2023-08-10 17:39:00
description: 阅读笔记 - (TPDS'23)DeepBoot Dynamic Scheduling System for Training and Inference Deep Learning Tasks in GPU Cluster
tags: 系统-ML任务级调度论文集合
categories: 论文阅读笔记
featured: false
---

浙江大学团队 Zhenqian Chen , Xinkui Zhao , Chen Zhi , and Jianwei Yin

## 亮点

### 画图的优秀之处

<div class="row mt-3">
    {% include figure.html path="assets/img/2023-08-24-TPDS23-DeepBoot/Bdzdby5Ifol8dvxfmNVcJcpQnof.png" class="img-fluid rounded z-depth-1" %}
</div>

- 在上图中，颜色的深浅、散点的大小，折线的上下远近都很好地表达出资源数量对于分配的影响，是一个很好的图！

<div class="row mt-3">
    {% include figure.html path="assets/img/2023-08-24-TPDS23-DeepBoot/UKEQbC3AToS8HsxJyWQciey6nNb.png" class="img-fluid rounded z-depth-1" %}
</div>

- 上图也不错，不用每次都画一模一样的图！

<div class="row mt-3">
    {% include figure.html path="assets/img/2023-08-24-TPDS23-DeepBoot/Zldmbt3A3opPC8xZ2MSchn3pnDc.png" class="img-fluid rounded z-depth-1" %}
</div>

- 这张图的例子很不错，很简单就表示出了具体的细节，而不是摆很多数值例子！

### 模型的优秀之处

- 跟上了最新的 Pollux 的步伐，采用尺度自适应的调度器（scale-adaptive）的设计模式，可以深入到模型中去调整模型训练的模式，不仅仅是在 GPU 数量上进行【当然，这也带来了比较麻烦的问题，即所有的实验基本上都要有 testbed，simulation 的实验似乎意义不太大，但是他们基本上都写了 simulation 的章节...】

## Intro

- 训练任务：云服务平台的主流工作负载

  - 需要很长的执行时间，需要很大的显存
  - 优化目标：公平性
- 推理任务：主要在应用中

  - 优化目标：低延迟、高吞吐量、SLO
- 问题

  - diurnal traffic pattern 昼夜模式：训练任务和推理任务都有明显的昼夜模式，导致资源利用率偏低【因为需要预留资源给峰值负载】
- 核心思想：

  - 为推理任务服务的空闲 GPU 可以为训练任务服务，降低等待时间，加速训练流程
  - 为训练任务服务的 GPU 可以动态伸缩给推理任务使用，以应对峰值负载
- 核心思想带来的挑战

  - 第一，传统的推理服务系统中，为推理任务服务的 GPU 只会预留给推理服务系统以应对峰值负载，但是在训练-推理集成系统中，GPU 进行频繁的上下文切换是不符合需求的【因为 GPu 上下文切换导致推理服务的 SLO 受到影响】 => 前人解决方案：PipeSwitch，预先初始化 CUDA 上下文，允许并行清除旧任务的内存并初始化新任务，减少 SLO 敏感任务的延迟，使得毫秒级任务切换成为可能。
  - 第二，传统的训练服务系统中，可以支持一段时间间隔内动态增减 GPU 的数量。但是，在 GPU 集群中分配训练任务是一个 NP-hard 问题，Pollux 使用遗传算法 NSGA II 去在小空间内近似搜索最优解【如果在训练-推理集成系统中，这会增加大量的搜索空间，且遗传算法无法在小的搜索空间中获得最优解，且算法的高复杂性使得调度开销很大】。此外，在推理集群中如何 loan 和 reclaim GPU 资源需要被考虑，用于 reclaim 的 GPU 选择不当会导致训练任务的效率大幅度下降，且激进的上下文切换会导致巨大的重启开销。此外，分布式训练的资源分配使用默认的"Stop-Resume"策略，这导致了 checkpoint、dataset、container lifecycle 的大量开销，虽然可以用 Elastic training 方案解决，但只会记录数据集处理流程和保存参数？
- 解决方案

  - adaptive task scaling (ATS)：近似获得 the best solution space for training DLTs allocation【训练任务的分配】 and inference task reclaiming【推理任务的回收】，以解决训练-推理集成系统中的调度问题 => 似乎只是一个为 DLT 寻找 loaning-reclaiming 的最优分配方案！
  - auto-fast elastic (AFE)：基于 Pollux 实现的 elastic training，让弹性训练和 checkpoint 管理更加稳定，避免高重启问题
  - Microsoft philly-traces workload 进行测试 【很经典的一个数据集】

## Background

### 问题分析

- DLT 任务的 Stop-Resume 阶段的高重启开销：容器删除、容器创建、模型初始化、checkpoint 加载【20-100s】

  - 针对轻量的 DLT【ResNet [1] in Cifar10 [33], NeuMF [4] in MovieLens [34]】容器删除和创建是耗费最多时间的！
  - 针对重量级 DLT【Bert (finetune) [2] on SQuAD [35] and ResNet in ImageNet [36]】数据加载成为重启的最大消耗，可能会超过 100s
  - 但是引入推理任务后，频繁的 allocation update 是不可避免的，因为需要快速反馈结果
- 构建了一个基于 Pollux 的模拟器，使用一个 8 小时的负载，推理任务的优先级高于训练任务，可以快速抢占 GPU

  - 指标：K8S 中的 GPU 利用率【直接从 K8S 中读取结果】、真实 GPU 利用率【真实的计算中的 GPU 占比】
  - 观察 1：因为有大量的重启开销，所以尽管 K8S 中的 GPU 利用率为 100%，真实 GPU 利用率波动很厉害远没有达到 100%
  - 观察 2：在传统的 DLT 集群中引入推理任务后，训练任务的重启时间剧烈增加。
  - 观察 3：重启开销大的问题没法在调度层面得到很好的剞劂，需要从根本上去减少重启开销。

### Management of DL Cluster

- 推理任务负载具有昼夜往复性，通常是 one(GPU)-to-one(service)或者 one-to-many 的范式，然后在低负载时大量 GPU 会空闲。但是，训练 DLT 的主要瓶颈是 GPU 数量不足。这两个互补的性质让训练 DLT 引入 elasticity 成为可能。
- 但是，何时 reclaim 空闲的 GPU 会严重影响训练 DLT 的性能【在推理任务高负载的时候将 GPU 弹性分配给 DLT 会导致高重启时延】 => 本文的解决方案：当推理任务的工作负载很忙的时候，会将 GPU 保留给推理集群，保留的时间和推理事件的数量相关。
- 推理服务占用一个 GPU，所以不是一个 NP-hard 问题。但是考虑到 DLT 需要租借推理集群的 GPU，所以需要考虑分布式 DLT 的性能，所以在为推理任务分配一个 GPU 的时候，也需要让剩余的空闲 GPU 针对分布式训练的性能最大化。

### 现有的调度算法

- Pollux：针对 DLT 调度的 SOTA 算法，遗传算法，复杂度较高 => 本文的解决方案：使用启发式算法近似获得最优解

  - Pollux 部分的参考文献来自：[https://diandiangu.github.io/2021/05/14/Pollux/](https://diandiangu.github.io/2021/05/14/Pollux/) ； [https://hliangzhao.cn/articles/000001632804098b0d15f52e2794eba809f483763f603b1000](https://hliangzhao.cn/articles/000001632804098b0d15f52e2794eba809f483763f603b1000)
  - 目前学术界和工业界主流的调度器可以分成两大类：尺度自适应的调度器（scale-adaptive）和非自适应的调度器（non-scale-adaptive）。非自适应的调度器要求用户在提交作业时指定所需要的资源数量，且不会随着任务的状态调整资源的分配。例如，Tiresias [OSDI '19] 和 Gandiva [OSDI'18] 等。自适应的调度器会主动调整资源分配。例如，Optimus [EruoSys '18] 训练了一个系统吞吐量关于各作业资源分配状态的预测模型，并根据这个模型调整资源的配比，从而最小化 JCT。此外还有 Gavel [OSDI'20]、AntMan [OSDI '20]、Themis [NSDI'20]，不一而足。和这些工作相比，Pollux 不仅给出了资源的动态分配方案，还 “将触手伸到了每个作业内部” 去调整这些模型训练本身的超参数：batch size 和 learning rate。 这就是 Pollux 可以取得更好的性能的直接原因。接下来将深入分析 Pollux 是如何对上述两个指标进行建模、如何调整资源的分配和作业的超参数的。
  - 一个正确配置的 DLT 任务需要在两个指标下进行权衡：
    1. <strong>系统</strong><strong>吞吐量</strong><strong>（system </strong><strong>throughput</strong><strong>）</strong>。在训练任务中，该指标可以用 “每个时钟周期处理的样本个数” 进行测算；
    2. <strong>工作效率（statistical efficiency）</strong>。该指标可以用 “每处理单个训练样本在模型参数上所取得的进展” 来衡量。

<div class="row mt-3">
    {% include figure.html path="assets/img/2023-08-24-TPDS23-DeepBoot/YjIwbWku1olNCFxGhlVcNYBsnnb.png" class="img-fluid rounded z-depth-1" %}
</div>


  - <strong>系统</strong><strong>吞吐量</strong><strong>（system </strong><strong>throughput</strong><strong>）主要由 </strong><strong>GPU</strong><strong>数量、</strong><strong>分布式</strong><strong>数据模式和数据同步方法、batch size 决定</strong>
    - 每一轮迭代的运行时间主要由两部分组成：其一是计算梯度的时间，记为$T_{grad}$；其二是平均化操作的时间 (3)，记为$T_{sync}$。 当分配的 GPU 增多时，如果不同时增大 batch size，$T_{grad}$会因为每个 GPU 分得的数据量变小了而减小， 但是$T_{sync}$与 batch size 是独立的，并不会随之降低。相反地，$T_{sync}$会随着 GPU 的增多而变大。 这就会导致$T_{sync}$成为瓶颈。<strong> 当分配的 GPU 增多时，增大 batch size 对于提升系统</strong><strong>吞吐量</strong><strong>而言是一个妥善的决策 </strong>。
  - <strong>工作效率（statistical efficiency）可以用梯度噪声比例（Gradient Noise Scale, GNS）来评估。</strong>
    - GNS 描述了随机梯度中 “噪声和有效信号” 之间的比例。 如果噪声较大，那么适当增大 batch size 和 learning rate 可以 “相对” 减缓工作效率下降的趋势； 如果噪声较小，增大 batch size 可能会显著降低工作效率，但在不同的训练阶段，batch size 对 statistical efficiency 的影响程度也不同，例如在训练初期的影响较大，而在后期影响较小。一般地，learning rate 越大，statistical efficiency 越高。工作效率的下降是不可避免的，其本质原因是边际效应的递减。<strong>Pollux 要做的，就是尽量减缓工作效率下降的速度 </strong>。此外，现有的研究成果表明，在增加 batch size 的时候，也应该同步增大 learning rate，否则模型的质量会打上折扣。 但是，以何种速度增大 learning rate 要视具体的模型和采取的优化算法而定。 常见的规则有 linear scaling rule（$$\eta \propto M$$） 和 squart-root rule（$$\eta \propto \sqrt{M}$$）等。
  - 结合两者的指标：GOODPUT：一个深度学习模型的训练任务在第 t 轮迭代的 goodput 是此时<strong>系统</strong><strong>吞吐量</strong>和该任务在本轮迭代的<strong>工作效率</strong>的乘积：$$Goodput_{t}(*) = Throughput(*) \times Efficiency_{t}(M(*))$$
    - $$* = (\boldsymbol{a} \in \mathbb{R}^{N}, m \in \mathbb{Z}, s \in \mathbb{Z})$$表示（GPU 分配向量，每轮迭代中每个 GPU 的分到 batch size【GPU 的总数是$$\sum_{\vert\boldsymbol{a}\vert} a_{i}$$，似乎这一轮迭代中对这个 DLT 任务的总的 batch size 为$$(\sum_{\vert\boldsymbol{a}\vert} a_{i}) \times m$$】，梯度聚合的操作次数）
    - $$M(*) = M(\boldsymbol{a}, m, s) = (\sum_{\vert\boldsymbol{a}\vert} a_{i}) \times m \times (s + 1)$$  => 为何要乘上梯度聚合的操作次数？？？？
    - 一个模型提交的时候需要指定初始化的 batch size $$M_{0}$$和 learning rate $$\eta_{0}$$，同时$$s = 0$$
  - $$Efficiency_{t}(M(*))$$ 计算方式和实验验证
  - $$Throughput(*)$$ 计算方式和实验验证
  - 系统架构：每一个作业都有一个对应的 PolluxAgent，  负责收集当前 Job 的 efficiency 和 throughput，且将 Goodput 汇报给 PolluxSched。PolluxSched 负责<strong>定期</strong>为每个 Job 动态地分配 GPU 资源。

<div class="row mt-3">
    {% include figure.html path="assets/img/2023-08-24-TPDS23-DeepBoot/H1xzb4Xdloc5n4xO25CcZpudnWe.png" class="img-fluid rounded z-depth-1" %}
</div>

  - PolluxAgent：作业层级的优化【这里是设计了一个神经网络，去用真实 Profile 出来的 GOODPUT 相关指标来优化单个作业 Goodput 的预测，文章介绍了如何进行模型参数的初始化和作业参数的更新】
  - PolluxSched：集群层级的优化【PolluxSched 周期性地为每个作业分配（重新分配）资源】
    - 最优化目标，即分配方案 A 相对于公平分配方案$$a_{f}$$【即每个作业都分得整个集群的$$\frac{1}{J}$$比例的资源，$J$是系统中处于 running 和 pending 状态的 DLT 总数量】带来的加速
    $$\max_{\boldsymbol{A}} \text{FITNESS}_{p}(\boldsymbol{A}) = (\frac{1}{J} \sum_{j=1}^{J} \text{SPEEDUP}_{j}(A_{j})^{p})^{\frac{1}{p}} = (\frac{1}{J} \sum_{j=1}^{J} (\frac{\max_{m, s} \text{GOODPUT}_{j}(A_{j}, m, s)}{\max_{m, s} \text{GOODPUT}_{j}(a_{f}, m, s)})^{p})^{\frac{1}{p}}$$
    - p 是公平系数，当 p=1 的时候，$$\text{FITNESS}(\boldsymbol{A}) = \sum_{j=1}^{J} \text{SPEEDUP}_{j}(A_{j})$$表示的是针对所有任务而言的加速比之和；当 p 趋近于负无穷，重点关注的是集群中取得 speedup 最小的作业。p 可以被认为是一个“公平旋钮”，负值越大越公平。集群运营商可以根据组织优先级选择合适的值。作者发现 p = −1 实现了最大的有效产出改进和合理的公平性。
    - 使用遗传算法去最大化这个优化目标！
  - <strong>重新分配的惩罚 </strong>。如果一个作业被决定调度到别的节点上继续执行，那意味着该作业需要保存当前进度到 checkpoint 中， Pollux 会杀死封装了该作业的 Pod，然后在新的节点上重新启动该作业。这必然会带来一定程度的延迟。 作者发现，基于 checkpoint-restart method，大约会产生 15～120 秒左右的延迟。因此，如果一个作业被多次重新分配，那么它的 SPEEDUP 需要乘上一个衰减系数！
    - $$\text{SPEEDUP}_{j}(\boldsymbol{A}_{j}) \leftarrow \text{SPEEDUP}_{j}(\boldsymbol{A}_{j}) \times \text{REALLOC-FACTOR}_{j}(delay)$$
    - $$\text{REALLOC-FACTOR}_{j}(delay) = \frac{j.age - j.restart\_time \times delay }{j.age + delay }$$， j.age 表示任务 j 已经存在的时间，j.restart_time 表示任务 j 重新分配资源的次数，delay 表示重新分配延迟的估计值
- Optimus：贪心算法，没有考虑到多 worker 的带宽问题
- Aryl【解决的是训练集群和推理集群的借用问题】：背包问题【GPU 数量是物品的重量，对应 GPU 下的加权执行时间是物品的价值】，问题是天然的对短执行时间的 DLT 任务不友好，而且这些任务才是瓶颈。
- 本文的设计：使用背包问题抽象调度问题【避免 Pollux 搜索算法的高复杂性】，但是使用 SPEEDUP 这样更好的优化目标【避免短执行时间任务的不公平】

### Benefits of Fast Elastic Training

- 因为推理任务的优先级更高，所以当一个推理任务到达的时候训练任务借用的 GPU 需要快速归还，这就导致了 DLT 任务上下文切换的高复杂度。
- Elan 和 EDL 要求用户指定保存 checkpoint 的迭代次数

  - 优点：当 DLT 的弹性训练 worker 数量发生变化的时候，参与分布式训练的所有副本只需要同步访问 checkpoint 的进度并恢复即可，理论上可以实现毫秒级别的恢复
  - 缺点：需要确定适当的迭代间隔来保存 checkpoint，较大的模型 checkpoint 时间成本很高，低频率保存也有可能导致恢复时只能获得较旧的模型权重，导致迭代浪费和效率降低【这个思想好像在南昌的会议中被提到，是否可以作为一个 balance 去处理！】
- CheckFreq 讨论了如何进行 checkpoint 的问题，但和 Pollux 不兼容
- 本文的方案[auto-fast elastic (AFE)]：只在 DLT 的分布式 worker 数量变化的时候才进行 checkpoint

  - 显然的问题：在保存模型的时候如果发生了 worker 数量的变化，又要进行一次保存？

## Design

- 蓝色：训练任务的分配方案；红色：推理任务的分配方案

<div class="row mt-3">
    {% include figure.html path="assets/img/2023-08-24-TPDS23-DeepBoot/BLbRbZh97ow9sWxPqDwcHF3QnOb.png" class="img-fluid rounded z-depth-1" %}
</div>

## ADAPTIVE TASK SCALING

- 包含两个部分 ATS-Training 和 ATS-Inferene
- ATS-T

  - 先验知识：计算出每种分配方案的 speedup
  - 构建求解背包问题需要的 W 和 V，W 的每一项 W[j][k]代表任务 j 在消耗 k 个 GPU 的时候的消耗值？似乎 W[j][k] = k。V 的每一项 V[j][k]代表任务 j 在消耗 k 个 GPU 的时候获得的 Speedup，注意这里参考 Pollux 引入了惩罚项机制，但是如果一个任务新的分配和旧的分配一致，则不需要乘上惩罚项，因为不存在重新部署的消耗。
  - 使用 dp 算法求解背包问题的解和路径
  - 根据新的解重新进行系统的分配：
    - 首先从需求 Replica 数量少的任务开始做分配
    - 遍历所有的任务，如果新决策方案没有任务 j 或者任务 j 是不需要更改的 allocation，则跳过；否则先为任务 j 补充 free GPU 最多的 worker，再补充 free GPU 最少的 worker

<div class="row mt-3">
    {% include figure.html path="assets/img/2023-08-24-TPDS23-DeepBoot/JC8hb5J4Po6BodxJhWYcUsrWnab.png" class="img-fluid rounded z-depth-1" %}
</div>

- ATS-I
  - Tensorflow Serving【可以支持一个 GPU 为多个任务并行提供服务】：[https://bookdown.org/leovan/TensorFlow-Learning-Notes/4-5-deploy-tensorflow-serving.html](https://bookdown.org/leovan/TensorFlow-Learning-Notes/4-5-deploy-tensorflow-serving.html)
  - 推理 GPU 的生命周期
    - 最关键的一步就是 Protect 状态，设置这个状态的目的就是为了避免高峰负载的到来导致推理 GPU 集群的性能下降，留有一些空闲的余地。
    - Free 状态：没有为任何的任务进行服务，但也不会被锁定只能为推理集群服务。
    - 当一个 GPU 为推理集群做服务的时候，需要设置保护时间（上图中的 Timeout），由 g.cnt 来决定保护时间的倍数，同时为了避免过短或过长的保护时间，还人为设置了上下界超参数： $$min(t_{p, max}, t_{p})$$， $$t_{p} = t_{p, min} + g.cnt \times interval$$
  - 算法的核心：
    - 先从当前就是 protect 状态的 GPU 中选择 g.cnt（表示 GPU g 被设置为 Protect 状态的次数）最高的 GPU，目的就是让之前一直都是推理专用计算设备的 GPU 继续为推理集群发光发热。
    - 如果当前没有一个 protect 状态的 GPU，就再从 Free 状态中随机选取一个 GPU 来使用【为何这里就要进行探索？】
    - 如果没有任何的 Protect 和 Free 状态，就需要从租借给训练集群的 GPU 中抢占，选择算法是 $$g \leftarrow argmax{\Delta \text{SPEEDUP}(\mathcal{P}_{I})}$$ 【这是 reclaiming 阶段，大多数时候会导致$$\Delta \text{SPEEDUP} < 0$$，作者在这里还举例说明了一种$$\Delta \text{SPEEDUP} > 0$$的情况】
  - 上图给出了一个 6 个推理任务调度的例子
  - 作者标榜的优势：与 Aryl 基于 Worker 的回收策略相比，GPU 粒度回收最大限度地减少了对训练 DLT 的影响。

## AUTO-FAST ELASTIC （AFE）

- Stop-Resume：多 worker 的并行训练，可以通过 stop-resume 来解决，也就是当 worker 需要加入/离开时，其他 worker 停止当前的训练任务，等待需要变动的 worker 完成相应操作，再重构通信拓扑及训练任务，但在这个过程中 worker 通常需要停止 30 秒以上，这种 overhead 限制了并行调整的效率，从而限制了弹性的应用场景。
- EDL / Elan

  - <strong>自动的训练任务管理模块</strong>：对于每一个深度学习训练任务 job 都有一个 leader 来管理所有的 workers，leader 负责监控不同的 worker 训练任务，控制 worker 训练的进度，构建 worker 之间的通信拓扑，以及保存不同 worker 的模型训练元数据（模型参数、数据集索引，worker 训练进度保存等）。但是，承载 leader 角色的 worker 可能会因为 scale-in 或 scale-out 而退出。每个 worker 中都会运行一个 leader 发现/选举进程，当 leader 对所有 worker 不可见时，该进程会启动选举产生一个新的 leader。具体地说，当一个 job 启动时，每个 worker 首先执行 leader 选举过程，并且将 leader 的地址作为连接信息，通过请求该信息与 leader 连接。如果连接信息无效或过期，则 worker 进程会将自己的地址写入该信息（zookeeper/etcd），并成为 leader。leader 需要定期刷新其地址信息。如果 leader 没有定期刷新更新自己信息，则该地址信息将自动过期。此时 worker 再次进行 leader 选举。在选择了一个 leader 之后，它将建立一个接受连接的 RPC 服务器，而其他 worker 将连接到该 leader 并发送注册消息以加入 job。在作业执行期间，leader 从每个 mini-batch 训练之后的梯度同步请求中推断出 worker 进程的活跃度。当调用 scale-in 或 scale-out 时，leader 与新加入的 worker 或已有的 worker 连接，通知 worker 加入或离开当前的 job。
  - <strong>高效的任务并行度调整模块</strong>：为了减少并行调整的开销，EDL 使用 stop-free scaling 来隐藏 scale_out[添加一个新的 worker]时由于任务准备带来的高 overhead，并应用 graceful exit 来减小 scale_in[减少一个已有的 worker]过程的 overhead。
    - scale_out：向正在运行的作业添加新的 worker 进程需要三个步骤：执行上下文准备【准备加载动态库 cuDNN 或 cuBLAS，准备训练数据，在 GPU 或 CPU 内存上分配空间】、通信拓扑结构构建和模型准备。stop-free scaling 策略。当新的 worker 加入时，不需要停止已有 worker 的进程。每个新的 worker 线程启动两个独立的线程，一个主线程和一个后台线程。主线程执行上下文准备，同时后台线程执行 leader 发现并向 leader 发送注册请求。leader 在接收到新 worker 的注册请求后，构建一个新的通信拓扑，并将其广播给所有员工。此时原有的通信拓扑还没有被破坏，因此现有的 worker 可以继续训练而不受影响。当新的 worker 进程完成执行上下文准备并接收到新的通信拓扑时，它会向 leader 发送一个 ready 消息。此时 leader 监控旧的通信拓扑中的 worker 完成 t 轮 mini-batch 的训练之后，由 leader 随机选择一个 worker 将其参数同步给新的 worker，并通知 job 中所有 worker 按照新的通信拓扑组织，并执行训练任务。
    - scale_in：在接收到 scale in 请求时，leader 将构造一个新的通信拓扑并将其广播给其余的 worker。同时 leader 监控旧的通信拓扑中的 worker 完成 t 轮 mini-batch 的训练之后，再允许 worker 退出以及剩余 worker 按照新的通信拓扑开始训练。如果 leader 离开，它将删除其与 worker 连接的地址，以便 worker 可以选举新 leader。旧的 leader 将在退出前将 job 元数据（如 batch size、数据加载进度等）发送给新 leader，其余所有 worker 将在预定时间连接到新 leader。在正常退出的情况下，其余 worker 不需要停下来等待 worker 退出，因此 scale in 的 overhead 可以忽略不计。
- AFE：在 Pollux 系统中，需要通过 ckpt 去同步一些状态【主要在重新分配的惩罚那里！】，所以相比 EDL 还需要 save state 和 load state 的时间

  - Controller： All-reduce 操作【[https://zhuanlan.zhihu.com/p/79030485](https://zhuanlan.zhihu.com/p/79030485)】
