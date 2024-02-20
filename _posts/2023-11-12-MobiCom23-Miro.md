---
layout: post
title: 阅读笔记 - (MobiCom'23) Cost-effective On-device Continual Learning over Memory Hierarchy with Miro
date: 2023-11-12 17:39:00
description: 阅读笔记 - (MobiCom'23) Cost-effective On-device Continual Learning over Memory Hierarchy with Miro
tags: 系统-ML任务级调度论文集合
categories: 论文阅读笔记
featured: false
---

## 作者、优点和问题

- 优点
  - 12 月发现代码开源，很伟大，代码写的算是不错的，结构清晰，代理设置得很好，值得学习：[https://github.com/omnia-unist/Miro](https://github.com/omnia-unist/Miro)
  - 针对持续学习（CL）的新场景提出算法
  - 根据持续学习场景中的资源动态变化情况来动态配置 CL 系统，以获得最优的成本效应
  - HEM 可以让数据更加充分地混合？避免 Non-iid 的场景
  - 这张图画的很好，体现了“权衡”的特点。也能看出来，accuracy 的边际效应递减，energy 的增长是比较偏线性的
- 问题：
  - 为什么是多个 task? => xlc: 感觉这个场景又有点像我之前做的那个隐私预算分配的场景，然后把 cache 加进来...
  - 整篇工作基本都是在讲测量的事情，测量的基本基本上都是那种最边界的结果，因此完全不需要任何的算法就写完了这篇文章....

<div class="row mt-3">
    {% include figure.html path="assets/img/2023-11-12-MobiCom23-Miro/HCfCbR39WowXujxBOx0cEsDxned.png" class="img-fluid rounded z-depth-1" %}
</div>

<div class="row mt-3">
    {% include figure.html path="assets/img/2023-11-12-MobiCom23-Miro/ByDibeE0aoIfcCxdUcIczgRrnzg.png" class="img-fluid rounded z-depth-1" %}
</div>

## Introduction

- CL 范式：随着新数据的到达，模型要从新数据的中逐步学习知识。
- 挑战
  - 灾难性遗忘（catastrophic forgetting）：在学习新的知识之后很快就遗忘了 => 解决方案：情景记忆（Episodic Memory, EM），同时基于深度存储器结构（HEM）将存储分为快速访问的小存储器和慢速访问的大存储器 => xlc: 感觉出现了可以针对内存空间做调度的点了！类似强化学习的 Replay Buffer，只要在讲一下边缘设备具有严格的内存容量限制就可以做调度了......
- 贡献
  - Systematic study of on-device CL：测量
  - System runtime for HEM：从 insight 来优化 HEM 以实现成本增益，主要配置以下表中的参数来获得最优的调度方案
    - Capacity：文章描述中对性能影响不太关键，似乎是通过限制 I/O 来实现的【在 [Jellyfish Testbed](https://we5lw6jk7r.feishu.cn/wiki/N9dmwc1vXiNkf5k0GH5cXKXknKb) 的源码实现中，似乎可以为每个进程提供独立的带宽约束，这让实验成为可能！】
    - (Accuracy-Energy) Trade-off：对性能影响最大，通过修改 EM size 和 SB size 来实现【】
    - Static：似乎就外部设置？不去进行优化

<div class="row mt-3">
    {% include figure.html path="assets/img/2023-11-12-MobiCom23-Miro/X5pKbs4RwoKJKbxOU20cKmFWncg.png" class="img-fluid rounded z-depth-1" %}
</div>

## CONTINUAL LEARNING ON HEM

### Workflow

- 简单描述了非层级式的存储结构不能满足速度的需求和空间的需求
  - **B**uffering：Stream Buffer(SB)的大小需要依赖于任务的学习方法
  - **T**raining：训练
  - **S**wapping：将 in-memory 的样本和 in-storage 的样本进行交换
  - **F**lushing：在 Task N 完成之后，EM 会用 SB 中的样本进行更新，如果 EM 的内存空间不足，HEM 就会使用采样策略。旧的任务应该将一些样本驱逐出去避免对内存空间的占用。SB 中的数据需要被刷到 Storage 中。

<div class="row mt-3">
    {% include figure.html path="assets/img/2023-11-12-MobiCom23-Miro/O7EabUp3JouJCAxG4vocpRRpnJh.png" class="img-fluid rounded z-depth-1" %}
</div>

### Data Diversity

- 在 Storage 中的数据有一天也会被使用，避免出现遗忘问题

## MIRO: SYSTEM RUNTIME

### Design Overview

<div class="row mt-3">
    {% include figure.html path="assets/img/2023-11-12-MobiCom23-Miro/GlswbQStGo8SqJxm9hEcu4LenQe.png" class="img-fluid rounded z-depth-1" %}
</div>

### Data Swapping Strategy

- 三个原则
  - (P1) I/O energy consumption is insignificant.  I/O 能耗微不足道。
  - (P2) Increasing the swap ratio provides benefits across a broad range, with a knee point appearing at a relatively low swap ratio (15–20%) in the ratio-accuracy curve, as demonstrated in Figure 6.  提高 swap ratio 可以带来广泛的好处，在 ratio-accuracy curve 中，拐点出现在相对较低的 swap ratio（15-20%）处
  - (P3) Other programs running on the device can abruptly compete for I/O resources. But, under normal circumstances, HW typically allows training jobs to leverage ample bandwidth for full-fledged data swapping. 设备上运行的其他程序可能会突然竞争 I/O 资源。但是，在正常情况下，硬件通常允许训练作业利用充足的带宽来进行全面的数据交换。
- 实际的 data swapping 算法
  - Data swapping 策略：类似 TCP 的拥塞控制，先从 100%->50%->25%。Miro 通过首先增加交换间隔来降低交换比率。我们发现更新间隔值对于 100% 到 20% 范围内的 swap ratio 是有利的。然而，对于低于 20% 的掉期比率，我们将间隔固定在 5 个 epoch，并适当调整 swap ratio 以达到所需的 target swap ratio。

<div class="row mt-3">
    {% include figure.html path="assets/img/2023-11-12-MobiCom23-Miro/VyGnb0KqPo1YaZxqxaMcUJGqneg.png" class="img-fluid rounded z-depth-1" %}
</div>

### Stream Buffer and EM Sizes

#### Our Method

- 决定 EM 和 SB 的大小的策略：Miro 系统中的 config 选取是一种非常启发式的方案，根据 SB 和 EM 的大小构建一个表，然后每个方法都去试，计算得到$util = \frac{acc\ gain}{energy\ usage}$，然后选择出一个剪切线 cutline，在这个区间里面的可以成为 configs 的候选。【本文是实验验证 20%-50% 的剪切线范围效果比较好】

#### [有借鉴意义]Profiling at Low Overhead

- A1) Avoid exhaustive profiling that covers all size variations. Profile a small subset of confs.
  - 本文的解决方案：通过均匀采样实例来减少 conf 的数量。【因为过去的 conf 可能无法表达出未来 conf 的重要性】
- A2.1) Do not use the entire training data that includes all stream buffer and EM samples. Use a subset of the data.
  - 本文的解决方案：降低 Training Samples 的数量，
- A2.2) Do not go through all epochs. Perform training for a small number of epochs and infer the accuracy that could be obtained if there were many more epochs.
  - 本文的解决方案：降低 Epochs，不需要完整进行 profile【比如只执行 5 个 epoches】，可以考虑像 Optimus 一样进行插值啥的

#### Tying All Together in Miro Workflow
