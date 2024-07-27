---
layout: post
title: RADICAL-Cybertools调度框架介绍
date: 2024-05-22 00:00:00
description: RADICAL-Cybertools调度框架介绍
tags: 系统-高性能计算
categories: 开源项目源码
---

> 更好的排版请阅读: https://we5lw6jk7r.feishu.cn/wiki/KQGIw9x6Li549gkUOfWcRRlYnmh?from=from_copylink

# RADICAL Cybertools

- RADICAL-Cybertools 是一套基于抽象的明确定义的功能，专为可扩展、可互操作和可持续的方法而设计，以支持一系列高性能和分布式计算系统上的科学。
- 它目前由三个组件组成：

  - RADICAL-SAGA：一个基于标准的接口，提供跨一系列计算中间件的基本互操作性 【RADICAL Cybertools 堆栈的基础设施访问层。它为大多数生产 HPC 排队系统、网格和云服务提供同质编程接口。 RADICAL-SAGA 支持 XSDE 和 OSG 资源以及学术和商业云计算平台。】
  - RADICAL-Pilot：一个可扩展且灵活的 Pilot-Job 系统，提供灵活的应用程序级资源管理功能
  - Ensemble Toolkit (RADICAL-EnTK)： 简化实现基于集成的应用程序的能力【提供了一种简单的方法来开发由多个任务组成并遵循预定义模式的应用程序。该工具预定义了常见的执行模式，因此用户可以快速调整该工具包以满足他们的需求；可以定义更复杂的执行模式。通过基于 RADICAL-Pilot 构建，Ensemble Toolkit 可以利用灵活且可扩展的资源管理技术。】
- 特点

  - 实际任务黑盒化: 没有任何的任务图内部节点的优化逻辑
  - bash 描述所有逻辑
  - 任务数据依赖需要文件系统的接入
  - 异构的支持在于实际任务放置节点的支持程度

# RADICAL-EnTK

## 常见模式: Ensemble of Pipelines


<div class="row mt-3">
    {% include figure.html path="assets/img/feishu_docs_static/UP37b4iAWoJmlpxdgmMctjPrnYf.png" class="img-fluid rounded z-depth-1" %}
</div>


- Pipeline 并行执行
- Pipeline 中的 Stage 是串行的，由 Barrier 管理其同步
- Stage 中的 Task 是并行的，执行的程序理应是类似的逻辑

## 常见模式: Sequence of Workflows

- 另一种常见的执行模式由同会话顺序工作流程组成，其中多个并发管道具有多个阶段，其中每个阶段由多个任务组成。我们称之为工作流程序列。
- 在以下示例中，我们创建 2 个 Sequence of Workflows，每个工作流有 2 个 Pipeline，每个管道有 3 个 Stage。出于演示目的，每个任务除了“睡眠”3 秒之外什么都不做。该示例建议使用 autoterminate=False 启动 AppManager，并在所有管道完成后使用 appman.terminate()。这允许您对第二个工作流程使用相同的应用程序管理器。

```cpp
#!/usr/bin/env python

from radical.entk import Pipeline, Stage, Task, AppManager


def generate_pipeline():

    p = Pipeline()
    s1 = Stage()

    t1 = Task()
    t1.executable = '/bin/sleep'
    t1.arguments = ['3']

    s1.add_tasks(t1)

    p.add_stages(s1)
    s2 = Stage()
    t2 = Task()
    t2.executable = '/bin/sleep'
    t2.arguments = ['3']

    s2.add_tasks(t2)
    p.add_stages(s2)
    s3 = Stage()

    t3 = Task()
    t3.executable = '/bin/sleep'
    t3.arguments = ['3']

    s3.add_tasks(t3)
    p.add_stages(s3)

    return p


if __name__ == '__main__':

    appman   = AppManager()
    res_dict = {
        'resource': 'local.localhost',
        'walltime': 10,
        'cpus'    :  8
    }
    appman.resource_desc = res_dict


    pipelines = list()
    for cnt in range(2):
        pipelines.append(generate_pipeline())

    appman.workflow = set(pipelines)
    appman.run()

    print('1 ===================================================')


    pipelines = list()
    for cnt in range(2):
        pipelines.append(generate_pipeline())

    appman.workflow = set(pipelines)
    appman.run()

    print('2 ===================================================')

    appman.terminate()

    print('t ===================================================')
```

## 类图


<div class="row mt-3">
    {% include figure.html path="assets/img/feishu_docs_static/Y5JMbZP4soPUnzxvD61coexdn6e.png" class="img-fluid rounded z-depth-1" %}
</div>


## 顺序流图


<div class="row mt-3">
    {% include figure.html path="assets/img/feishu_docs_static/DlIzbjK4GoBzcZxXajQcs0bnn4f.png" class="img-fluid rounded z-depth-1" %}
</div>


## 状态转换图


<div class="row mt-3">
    {% include figure.html path="assets/img/feishu_docs_static/AOZBbDypWoon8txbMj2cezRWnwb.png" class="img-fluid rounded z-depth-1" %}
</div>

