---
layout: post
title: 阅读笔记 - (NSDI'23) Transparent GPU Sharing in Container Clouds for Deep Learning Workloads
date: 2023-09-12 17:39:00
description: 阅读笔记 - (NSDI'23) Transparent GPU Sharing in Container Clouds for Deep Learning Workloads
tags: 系统-ML任务级调度论文集合
categories: 论文阅读笔记
featured: false
---


## 作者概述

- 北大
- Johns Hopkins University

## 优点

- 代码开源：

## Introduction

- DNN Training Jobs 可以划分为两种类型

  - Production job：有一些性能要求或者时间要求
  - Opportunistic job：利用的是空闲的资源
- GPU Sharing 的现有解决工作

  - AntMan：应用层 SOTA
  - Nvidia Multiple Process Sharing（MPS）：OS 层解决方案，所有的任务都共用一个 cuda context，无法 提供 fault isolation。要求进程的总 GPU 内存需求要适配 GPU 内存容量，而且依赖应用程序去处理 GPU 内存和 host 内存之间的交换。
  - NVIDIA Multi-Instance GPU (MIG)：OS 层解决方案，只能适配部分 GPU；只给了固定的 GPU Sharing 方案，只能将 GPU 划分为 7 等分，无法使用超过 4/7 的 GPU；当 GPU 上有任务执行的时候，无法再动态调整 GPU 的资源
- 贡献

  - 满足了 Transparency【用户是不需要修改 DL 框架】、High GPU utilization【】、Performance isolation【主要是针对 Production Jobs 而言，不能因为 GPU Sharing 导致性能的下降】、Fault isolation【一个容器中的应用的 fault 不能 crash 其他容器的应用】
