---
layout: post
title: 任务调度场景中的模拟器、源代码与数据集 Trace 汇总
date: 2023-08-10 17:39:00
description: 任务调度场景中的模拟器、源代码与数据集 Trace 汇总
tags: 系统-ML任务级调度论文集合
categories: 开源资源汇总文档
featured: false
---

## 开源代码集合

- 这个知乎账号经常会分享很多源代码：[https://www.zhihu.com/people/jwwthu](https://www.zhihu.com/people/jwwthu)

## 模拟器、源代码

### CloudSim 系列

- CloudSim 系列及其衍生

  - CloudSimPy： [https://github.com/FengcunLi/CloudSimPy](https://github.com/FengcunLi/CloudSimPy)
  - 详细代码解析：[CloudSimPy 模拟器](https://we5lw6jk7r.feishu.cn/wiki/wikcnOiCCOD020L9N2VIc0S4CCc)
  - DynamicCloudSim: Simulating heterogeneity in computational clouds[SigComm'19]
- 基础模块：SimPy

### Tiresias 开源模拟器

- Tiresias 开源的模拟器
  - [https://github.com/SymbioticLab/Tiresias](https://github.com/SymbioticLab/Tiresias)
  - 该模拟器的具体代码解析：[Tiresias 模拟器](https://we5lw6jk7r.feishu.cn/wiki/wikcnxb4Bz4fZ1i6SwYwtnaS5eI)

### Decima 模拟器

- 来源论文：[[12.25]SIGCOMM'19@Learning scheduling algorithms for data processing clusters.pdf](https://we5lw6jk7r.feishu.cn/wiki/wikcnn5Pzyzx1DfPHDigE7NhKMb)
  - github 地址：[https://github.com/hongzimao/decima-sim](https://github.com/hongzimao/decima-sim)
  - 浙大的一个学生进行复现：
- 优点
- 缺点
  - 不能使用 GPU。。。
- 基础模块

### DL 模拟器

- 来源论文：[[12.10]TPDS'21@DL2_A_Deep_Learning-Driven_Scheduler_for_Deep_Learning_Clusters.pdf](https://we5lw6jk7r.feishu.cn/wiki/wikcnisowy8bNvHxPGX1b4ldTYe)

  - Python2.7 + Tensorflow 1.13-gpu
  - 包含 multiprocessing
  - 包含各种已有的调度算法
- 详细代码解析：[DL2 模拟器](https://we5lw6jk7r.feishu.cn/wiki/wikcnLqM0S7GYhpBcVObjRhf3Fb)

### 商汤科技自研模拟器

- 来源论文：[[2.4]A Simulation Platform for Multi-tenant Machine Learning Services on Thousands of GPUs.pdf](https://we5lw6jk7r.feishu.cn/wiki/wikcnrLNTJSiKVYPYCmXxUZ4kPE)

### Qore-DL 源代码

- github 地址：[https://github.com/qore-dl/qore-dl-code](https://github.com/qore-dl/qore-dl-code)

### ekya

- Github 地址：[https://github.com/edge-video-services/ekya](https://github.com/edge-video-services/ekya)
- 概述

  - 边缘段资源分配
  - log 了很多信息，构建准确度和资源之间的函数关系?
  - 存在现成的模拟器可以使用

### DSS Python 实现的离散调度模拟器

- Github 地址：[https://github.com/epfl-labos/DSS](https://github.com/epfl-labos/DSS)

### Synergy 模拟器 [正在阅读]

- Github 地址：[https://github.com/msr-fiddle/synergy](https://github.com/msr-fiddle/synergy)
- 中文的介绍文档：[https://hliangzhao.cn/articles/000001660896665118db6926f214a2cab4f42f1ebdd563f000](https://hliangzhao.cn/articles/000001660896665118db6926f214a2cab4f42f1ebdd563f000)#
- 根据文章的结论，使用文章提供的模拟器得到的结论与真实的 Trace 差距小于 5%，确认了模拟器的保真性。
- 模拟器代码阅读：[Synergy 模拟器](https://we5lw6jk7r.feishu.cn/wiki/V9eAw3AiDiitnFkuKtMcn9WJnhc)

### DL_cluster_simulator

- 地址: [https://github.com/nexuslrf/DL_cluster_simulator](https://github.com/nexuslrf/DL_cluster_simulator)
- 优点
  - 有很漂亮的监控界面
- 缺点

  - 数据文件都不给
  - 暂时搁置，等作者回复后检查是否可以把监控界面拿过来用
- 基础模块

### YAFS

- fog 节点的调度器的
- 优点

  - 有非常多现成的例子，可以直接使用
  - 因为是 Fog 节点，因此包含大量的拓扑结构，使用 NetworkX 可以直接快速构建一个图拓扑结构
  - 官方文档【目前看来非常齐全】：[https://yafs.readthedocs.io/en/latest/index.html](https://yafs.readthedocs.io/en/latest/index.html)
  - 发了论文：
- 基础模块

### Privacy Budget Scheduling

- 阅读地址：[Privacy Budget Scheduling](https://www.usenix.org/conference/osdi21/presentation/luo)
- 模拟器/源码地址：[https://github.com/columbia/PrivateKube](https://github.com/columbia/PrivateKube)
- 中文导读：[https://zhuanlan.zhihu.com/p/479524282](https://zhuanlan.zhihu.com/p/479524282)
- 优点：
- 基础模块：

  - desmod（一个用于离散事件处理的模拟器组成模块，docs：[https://desmod.readthedocs.io/en/latest/index.html](https://desmod.readthedocs.io/en/latest/index.html)）
- 流程全整理【确认模拟器的流程】

  - 如何获取数据？
  - 数据集从哪里来？
  - 如何执行数据层面的 DP 调度？
  - 如何执行 GPU 层面的调度？
  - 可否整合到 Gavel 中？

### Gavel [很好]

- 模拟器/源码地址：[https://github.com/stanford-futuredata/gavel](https://github.com/stanford-futuredata/gavel)
- 优点：

  - 提供了一个调度上的通用最优化问题；
  - 使用时间片轮转调度机制，决策变量是 X，然后根据最优化目标的不同，确定一个最优化问题；
  - 提供了 Space Sharing 和 Placement Sensitivity 的模拟；
  - 提供了性能指标相关数据，为后续研究给予了更多的自信。
- 缺点：

  - 目前看来主要还是针对轮转作业进行优化；
  - 代码中存在一些小 Bug，而且 GPU 种类写死，不太方便进行定制。
- 流程全整理

  - Total step 确定？【默认是随机生成的，然后会和 Throughput 的已有数据进行乘操作】
  - 算法得到 Allocation 后，还会根据当前实际的任务在 worker 上的处理时间，动态调整得到的结果，最后变成一个_priority 用于队列计算。可能有时候还会遇到_priority 相同的情况，则还会根据_depolit【即衡量目标分配和实际分配的差距，多减少增】去进行划分
  - 算法在任务到来和任务结束的时候才会更新 allocation，减少对算法求解器的使用
  - 带上 Pref 表示使用数据集中提供的 throughout 【OK】
  - Pack 算法的异同点
    - Pack：任务提交【OK】
    - Pack：选中 packing 任务的调度处理方式【OK，没看到什么复杂的，正常处理】
    - Pack：任务单步完成如何结算，任务整体完成如何结算【OK，没看到什么复杂的，正常处理】
    - Pack 算法的计算方式：
  - 接入 philly_job_distribution 后的异同点
    - 其实就是改变了 scale_factor，使得任务可以获得很大的 scale_factor（即使用多 multi_gpu），在代码中好像就是直接在任务生成的时候就模拟好 philly_job_distribution 的情况，而不是直接从 philly 数据集中获取
    - multi_gpu：任务提交【OK，会在 load throughputs 的时候根据任务的 scale_factor 去获取不同的 throughputs 以用来计算 step】
    - multi_gpu：任务单步完成/整体完成如何结算：多个相同的 GPU 会平均分配单轮的 step 结果，直接考虑使用即可
  - 如何获取 GPU 上的性能数据
    - 学习并了解 measure_throughput.py 可以获得具体的方法
  - Water_filling 算法的异同点
    - 目前没看出来...
  - SLO 算法的异同点
    - 其实就是增加了几种云服务厂商给的资源价格，但是没有完整数据，需要自己去收集
    - [https://github.com/search?q=p3.2xlarge&type=Code](https://github.com/search?q=p3.2xlarge&type=Code) 进行一波搜索可以找到很多 AWS 的定价数据，这块内容还是比较全面的。直接接入使用即可。最后接入的数据集是：[https://github.com/LucianaMarques/amazon-spot-dataset](https://github.com/LucianaMarques/amazon-spot-dataset)
    - 应该使用 scripts/drivers/simulate_scheduler_with_generated_jobs.py 去测试
  - Allox 算法与实现
    - 使用匈牙利算法进行计算：[https://www.hungarianalgorithm.com/examplehungarianalgorithm.php](https://www.hungarianalgorithm.com/examplehungarianalgorithm.php)
    - 无法注入多 GPU 任务
  - FIFO 系列算法的实现方法
    - 这个算法其实很简单，就是一个队列按顺序调度即可
    - Base: 非抢占式 FIFO；Perf 和 Packed: 抢占式 FIFO, 每个时刻都重新计算 FIFO 的方式
  - FinishedTimeFairness 系列算法的实现方法（Themis）
- 如何画图

  - `scheduler/notebooks/figures/evaluation/continuous_jobs.ipynb` contains code to parse the resulting logs and produce graphs (can be run using `jupyter notebook`). The notebook should use the appropriate `log_directory` used in the above command line.
- From_trace：

  - 这个参数一般是可以从 checkpoint 中读取数据，该实验的过程总是非常长，我觉得非常合理。同时，也可以跟随着之前的环境进行进一步的测试。
  - 可以从 checkpoint 做恢复进行 debug
- 如何接入价格和 Elastic

  - 可以接入 aws 的价格数据，aws 的 plot prices 是开源的，可以直接拿来用。
  - 每个时刻都会根据价格曲线，从多个数据中心中找最便宜的价格使用即可
- 如何更换一个新算法

  - 如果想要接入那些不需要考虑公平性和时间轮转的算法，只需要控制队列即可

### POP

- 模拟器：[https://github.com/stanford-futuredata/POP](https://github.com/stanford-futuredata/POP)
  - 本质上就是在 Gavel 的基础上，加了一个对大矩阵的分切算法，并提供了算法保证。
  - 集成更多内容：[https://github.com/stanford-futuredata/pop-ncflow](https://github.com/stanford-futuredata/pop-ncflow)

### Willump

- 模拟器：[https://github.com/stanford-futuredata/Willump-Simple](https://github.com/stanford-futuredata/Willump-Simple)
- 目前看来好像是推断任务的调度加速

### ParallelSched [停止阅读]

- 浙大的学生实现的一个调度器模拟器

  - 代码：[https://github.com/hliangzhao/ParallelSched](https://github.com/hliangzhao/ParallelSched)
  - 集成内容：阿里数据集、DL2、Optimus、Tetris、SRTF、DRF、exp_DRF
- 考虑集成 Optimus、Tetris、DL2 进入 Gavel 中

### Resalloc [停止阅读]

- POP/ Gavel 作者搞出来的利用优化问题解决调度问题的模拟器：[https://github.com/cvxgrp/resalloc](https://github.com/cvxgrp/resalloc)
- 论文：[https://web.stanford.edu/~boyd/papers/resource_alloc.html](https://web.stanford.edu/~boyd/papers/resource_alloc.html)
- 和我们想要的场景不太一致...

### TitanSched  & ChronusArtifact

- TitanSched[正在开发中]：[https://github.com/gaow0007/TitanSched](https://github.com/gaow0007/TitanSched)
- ChronusArtifact[代码没法跑..]：[https://github.com/S-Lab-System-Group/ChronusArtifact](https://github.com/S-Lab-System-Group/ChronusArtifact)

  - 系统架构图：

<div class="row mt-3">
    {% include figure.html path="assets/img/2022-06-06-Simulator-Code-Trace/JTW4bDgWJo7WTkxTM0ocoX2ZnVh.png" class="img-fluid rounded z-depth-1" %}
</div>

- Astraea[目前看起来比较适合我来做]：[https://github.com/yzs981130/Astraea_Artifacts](https://github.com/yzs981130/Astraea_Artifacts)
  - 这篇工作的代码是可以跑出来的，而且看起来没有什么大的 bug
  - 具体的方法和后续作者的源码修改：TitanSched

### Ones 模拟器

- 模拟器代码：[https://github.com/kurisusnowdeng/ones_sc21](https://github.com/kurisusnowdeng/ones_sc21)
- 注意：该模拟器是包含任务 epoch 和 acc 的对应关系。

### 强化学习模拟器 [停止阅读]

- 一个专门用于模拟强化学习调度算法的模拟器：[https://github.com/mail-ecnu/VMAgent](https://github.com/mail-ecnu/VMAgent)
- 问题

  - 这个模拟器比较老，很多文档写的比较一般
  - 连实例代码都很难跑起来，感觉这份代码还是有比较大的问题的！
- 状态：暂时搁置

### DeepBoot 模拟器 [正在阅读]

- 来自文章 [TPDS'23] DeepBoot: Dynamic Scheduling System for Training and Inference Deep Learning Tasks in GPU Cluster
- [https://github.com/czq693497091/DeepBoot](https://github.com/czq693497091/DeepBoot)
- 优点

  - 这个代码很简单就能跑起来
  - 似乎没看到什么大的问题，有点想从里面找一些点来做！
  - 适合用来学习以下代码的实现
    - Pollux (OSDI'21)
    - AFS (NSDI'21)
    - Tiresias (NSDI'19)
    - Optimus (EuroSys'18)
    - Ayrl (Lyra, EuroSys'23)
- 问题

### hydra 模拟器 [未读]

- 来自文章：[阅读笔记 - (TC'23) Hydra: Deadline-Aware and Efficiency-Oriented Scheduling for Deep Learning Jobs on Heterogeneous GPUs](https://we5lw6jk7r.feishu.cn/wiki/OsfrwWf58il1Guk77ODcQu7Xn2b)
- github：[https://github.com/dos-lab/Hydra](https://github.com/dos-lab/Hydra)
- 优点

  - 这份代码写的很不错！纯 GO 语言，适合当 Go 语言的学习
  - 似乎没看到什么大的问题，有点想从里面找一些点来做！
  - 适合用来学习以下代码的实现
    - Allox
    - Gavel
    - Chronus
- 问题

### Beware of Fragmentation 模拟器 [正在阅读]

- 来自论文：[阅读笔记 - (ATC'23)Beware of Fragmentation: Scheduling GPU-Sharing Workloads with Fragmentation Gradient Descent](https://we5lw6jk7r.feishu.cn/wiki/G8GtwdbAui85kDkVfLTckrBhnFj)
- github：[https://github.com/hkust-adsl/kubernetes-scheduler-simulator](https://github.com/hkust-adsl/kubernetes-scheduler-simulator)
- K8S 调度器、Client-go 和 controller 的源码解读：[https://github.com/jindezgm/k8s-src-analysis/tree/master](https://github.com/jindezgm/k8s-src-analysis/tree/master)
- 自定义 K8S 调度插件：[https://www.qikqiak.com/post/custom-kube-scheduler/](https://www.qikqiak.com/post/custom-kube-scheduler/)
- K8S 调度器性能测试代码：[https://github.com/nexuslrf/cl2-scheduler-throughput/tree/master](https://github.com/nexuslrf/cl2-scheduler-throughput/tree/master)
- 经典的 K8S 调度流程：[Beware of Fragmentation 模拟器](https://we5lw6jk7r.feishu.cn/wiki/JXJfwb362ivNz7kMeF5cKneenad)
- 源码简单阅读：[Beware of Fragmentation 模拟器](https://we5lw6jk7r.feishu.cn/wiki/JXJfwb362ivNz7kMeF5cKneenad)

  - 整个流程完整地调用了 K8S 中的很多调度接口，对了解和学习 K8S 中的调度接口设计是非常有帮助的！
  - 代码里给出的较大规模测试是可以执行的！【但是缩小规模后容易出错，需要仔细看一下】
  - Data => 比较简单的数据，直接阅读即可理解
  - generate_config_and_run.py
    - 执行逻辑：全部都是使用二进制文件 ./bin/simon 来执行的
    - -gpusel： 这个参数让人疑惑，如果选择了一般的 GPU，执行时间如何获得呢？
    - Gpu sharing 的场景如何进行模拟？
  - 不同的调度算法的区别体现在 yaml 中的，通过更改 `-f` 和 `--default-scheduler-config` 的配置文件达成
  - 核心的调度代码如下 [没有看懂这段代码在.CoreV1().Pods().Get() 执行了何种操作，瞬间就完成了调度逻辑，需要在调试的时候切入一下]

    ```go
    func (sim *Simulator) createPod(p *corev1.Pod) error {
        if _, err := sim.client.CoreV1().Pods(p.Namespace).Create(sim.ctx, p, metav1.CreateOptions{}); err != nil {
        return fmt.Errorf("%s(%s): %s", simontype.CreatePodError, utils.GeneratePodKey(p), err.Error())
        }


        // synchronization
        sim.syncPodCreate(p.Namespace, p.Name, 2*time.Millisecond)
        pod, _ := sim.client.CoreV1().Pods(p.Namespace).Get(sim.ctx, p.Name, metav1.GetOptions{})
        if pod != nil {
                if pod.Spec.NodeName != "" {
                        sim.syncNodeUpdateOnPodCreate(pod.Spec.NodeName, pod, 2*time.Millisecond)
                        log.Infof("pod(%s) is scheduled to node(%s)\n", utils.GeneratePodKey(pod), pod.Spec.NodeName)
                }
        } else {
                log.Errorf("[createPod] pod(%s) not created, should not happen", utils.GeneratePodKey(p))
        }
        return nil
    }
    ```



### Rotary模拟器+testbed [未读]

- github：[https://github.com/csruiliu/rotary-dlt/tree/main](https://github.com/csruiliu/rotary-dlt/tree/main)

- 论文导读：[阅读笔记 - (ICDE'23) Rotary: A Resource Arbitration Framework for Progressive Iterative Analytics](https://we5lw6jk7r.feishu.cn/wiki/XxE4w7hEFi2mQ2kOVVscR4xrn4b)



### InfAdapter testbed [未读]

- github：[https://github.com/reconfigurable-ml-pipeline/InfAdapter](https://github.com/reconfigurable-ml-pipeline/InfAdapter)

- 论文导读：

- 使用K8S集群+TF Serving

### Jellyfish testbed [正在阅读]

- Github： [https://github.com/vuhpdc/jellyfish](https://github.com/vuhpdc/jellyfish)
- 论文导读：
- 代码详细分析：



### Vessim [未读] 碳排放模拟器

- Github：[https://github.com/dos-group/vessim](https://github.com/dos-group/vessim)

- 

## Trace 整合

### MS Philly Cluster数据集

- Microsoft提出的一个模拟器
	- 需要git lfs下载：[https://zhuanlan.zhihu.com/p/146683392](https://zhuanlan.zhihu.com/p/146683392) 
	- 地址：[https://github.com/msr-fiddle/philly-traces](https://github.com/msr-fiddle/philly-traces) 

- 数据集中为什么会出现那种一分钟结束的任务？
	- 在Tiresias文章的附录中，讲到因为用户的配置导致的bug，使得这个任务被快速地结束了。

- 可能有点作用的分析结果
	- 来自Tiresias文章的附录



### Google数据集

-  Google Cluster Traces 
	- [https://github.com/google/cluster-data](https://github.com/google/cluster-data)



### 阿里数据集

- [https://github.com/alibaba/clusterdata](https://github.com/alibaba/clusterdata)
- <em>cluster-trace-v2017</em>
- <em>cluster-trace-v2018</em>
- <em>cluster-trace-gpu-v2020</em>
- <em>cluster-trace-microservices-v2021</em>
- <em>cluster-trace-microarchitecture-v2022</em> 
- <em>cluster-trace-gpu-v2023</em>
	- 来自论文：[阅读笔记 - (ATC'23)Beware of Fragmentation: Scheduling GPU-Sharing Workloads with Fragmentation Gradient Descent](https://we5lw6jk7r.feishu.cn/wiki/G8GtwdbAui85kDkVfLTckrBhnFj) 



### 商汤数据集

- HeliosData
	- [https://github.com/S-Lab-System-Group/HeliosData](https://github.com/S-Lab-System-Group/HeliosData)



### planetlab-workload-traces数据集

- planetlab-workload-traces
	- [https://github.com/beloglazov/planetlab-workload-traces](https://github.com/beloglazov/planetlab-workload-traces)



### pollux论文的一些实验数据

- Pollux: Co-adaptive Cluster Scheduling for Goodput-Optimized Deep Learning 提供的部分开源数据集
	- 只有在他们的testbed实验系统上跑的，用于绘图的数据集
	- 特点：
		- 数据集很小
		- 都是从实际系统上采样得到结果，主要是通过nvidia-smi获得的硬件在每个时刻的使用情况
		- 其结果用于绘制下面的几张图
	- 地址：[https://github.com/petuum/pollux-results](https://github.com/petuum/pollux-results)

### Azure Trace数据集

- [https://github.com/Azure/AzurePublicDataset](https://github.com/Azure/AzurePublicDataset)

- 特点：
	- 不针对深度学习任务
	- 主要是追踪Azure的VM情况

- 被引用
	- [[12.20]SOSP'21@Generating Complex, Realistic Cloud Workloads using Recurrent Neural Networks.pdf](https://we5lw6jk7r.feishu.cn/file/boxcnZjVUcgmtWybMjmJKowyntc) 

## 任务Workload性能建模

- 一篇性能建模的blog（未更新完全）：[https://zhuanlan.zhihu.com/p/548465440](https://zhuanlan.zhihu.com/p/548465440)





### MLPref

- 介绍文献：[https://juejin.cn/post/7115232074323197960](https://juejin.cn/post/7115232074323197960)



### torch.profiler

- Pytorch原生提供的一个profiler工具：[https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html](https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html)

- 一篇介绍的blog：[https://zhuanlan.zhihu.com/p/403957917](https://zhuanlan.zhihu.com/p/403957917)



### Rotary

- 源码提供了一个profiler工具的新写法：[https://github.com/csruiliu/rotary-dlt/tree/main](https://github.com/csruiliu/rotary-dlt/tree/main)


