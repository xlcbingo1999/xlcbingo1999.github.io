---
layout: post
title: 博弈论
date: 2023-08-10 17:39:00
description: Game Theory
tags: 理论类笔记
categories: 理论类笔记
featured: false
---

## 基础概念
Game theory翻译过来就是博弈论，其实是研究多个玩家在互相交互中取胜的方法。例如在耶鲁大学的博弈论公开课中，有一个游戏是让全班同学从0到100中选一个数，其中如果选择的数最接近所有数的平均值的三分之一则这个玩家获胜。首先大家应该不会选择比33大的数，因为其他人都选择100也不能赢不了，那么如果大家都选择比33小，自己就应该选择比11小的数，考虑到其他人也是这样想的，那么自己应该选择比11小很多的数，如果我知道别人也知道自己选择比11小很多的数的话，那应该选择更小的数。那么这个游戏的理想值是0，也就是纳什均衡点，就是当对方也是深晦游戏规则并且知道你也很懂游戏规则时做出的最优决定，当然第一次游戏大家都不是完美的决策者（或者不知道对方是不是完美的决策者），因此不一定会选择纳什均衡点，但多次游戏后结果就是最终取胜的就是非常接近0的选择。

## 纳什均衡点
所有人已经选择了对自己而言的最优解并且自己单方面做其他选择也无法再提高的点。也就是说，如果玩家都是高手，能达到或者逼近纳什均衡的策略就是最优策略，如果对手不是高手不会选择最优策略，那么纳什均衡点不一定保证每局都赢，但长远来看极大概率会赢这样的新手。

## Combinatorial Game
- 满足以下环境条件可以称为Combinatorial Game
  - Zero-sum
  - Perfect information
  - Deterministic
  - Discrete
  - Sequential
 

## Minmax策略
- 目标是找到逼近纳什均衡的搜索策略
- 从树的叶子结点开始看，如果是本方回合就选择max的，如果是对方回合就是min的，实际上这也是假设对方是聪明的也会使用minmax算法，这样在博弈论里面就达到一个纳什均衡点。


## 蒙特卡洛树搜索
- 论文：A Survey of Monte Carlo Tree Search Methods http://pubs.doc.ic.ac.uk/survey-mcts-methods/survey-mcts-methods.pdf 
- 可以参考的源码：MCTS的完整实现代码在 tobegit3hub/ml_implementation
- 基于树结构，权衡探索和利用，在搜索空间巨大的时候仍有效的搜索算法。目标是找到逼近纳什均衡的搜索策略。 
- 探索和利用策略：
  - 得分不仅是由这个子节点最终赢的概率来，而且与这个子节点玩的次数成负相关，也就是说这个子节点如果平均得分高就约有可能选中（因为认为它比其他节点更值得利用），同时如果子节点选中次数较多则下次不太会选中（因为其他节点选择次数少更值得探索），因此MCTS根据配置探索和利用不同的权重，可以实现比随机或者其他策略更有启发式的方法。
  - UCT（Upper Confidence bounds for Trees）使用的UCB算法：$$argmax_{v' \in Child(v)} \frac{Q(v')}{N(v')} + c \sqrt{\frac{2 \ln{N(v)}}{N(v')}}$$，其中v'表示当前树节点，v表示父节点，Q表示这个树节点的累计quality值，N表示这个树节点的visit次数，C是一个常量参数（可以控制exploitation和exploration权重）。这个公式的意思时，对每一个节点求一个值用于后面的选择，这个值有两部分组成，左边是这个节点的平均收益值（越高表示这个节点期望收益好，越值得选择，用于exploitation），右边的变量是这个父节点的总访问次数除以子节点的访问次数（如果子节点访问次数越少则值越大，越值得选择，用户exploration），因此使用这个公式是可以兼顾探索和利用的。c常量我们可以使用$$1/\sqrt{2}$$，这是Kocsis、Szepesvari提出的经验值
- 必要假设
  - （博弈论领域假设）Zero-sum：零和博弈，所有玩家的收益之和为0，一定能分出输赢。
  - （博弈论领域假设）Perfect information / Fully information：对称信息（完全信息）。 游戏的所有信息和状态都是所有玩家可以观察到的，因此双方的游戏策略只需要关注共同的状态即可。不能像打牌一样隐藏自己的手牌
  - （博弈论领域假设）Determinism：确定性策略，每一个操作都没有随机因素
  - （博弈论领域假设）Sequential：顺序执行，所有的操作都是顺序执行的
  - （博弈论领域假设）Discrete：离散动作，没有一个动作是连续值
  - （优化领域假设）Black box optimization：黑盒优化，类似多臂老虎机，不能通过求导或者凸优化方法找到最优解，否则使用MCTS也是没有意义。【机器学习就是典型的优化过程，但我们用的机器学习算法如LR、SVM、DNN都不是黑盒，而是根据数学公式推导通过对函数求导等方式进行的优化。如果我们能把问题描述成一个函数或者凸优化问题，那么我们通过数学上的求导就可以找到最优解，这类问题并不需要用到MCTS等搜索算法，但实际上很多问题例如围棋就无法找到一个描述输赢的函数曲线，这样就无法通过纯数学的方法解决。】【这类问题统称为黑盒优化问题，我们不能假设知道这个场景内部的函数或者模型结构，只能通过给定模型输入得到模型输出结果来优化。例如多臂老虎机（Multi-arm Bandit）问题，我们有多台老虎机可以投币，但不知道每一台输赢的概率，只能通过多次投币来测试，根据观察的结果预估每台机器的收益分布，最终选择认为收益最大的，这种方法一般会比随机方法效果好。】【黑盒优化的算法也有很多，例如进化算法、贝叶斯优化、MCTS也算是，而这些算法都需要解决如何权衡探索和利用（Exploration and Exploitation）的问题。】
- 流程：通过不断的模拟得到大部分节点的UCB值，然后下次模拟的时候根据UCB值有策略得选择值得利用和值得探索的节点继续模拟，在搜索空间巨大并且计算能力有限的情况下，这种启发式搜索能更集中地、更大概率找到一些更好的节点。
  - Selection：在树中找到一个最好的值得探索的节点，一般策略是先选择未被探索的子节点，如果都探索过就选择UCB值最大的子节点。
  - Expansion：在前面选中的子节点中走一步创建一个新的子节点，一般策略是随机执行一个操作并且这个操作不能与前面的子节点重复。
  - Simulation：在前面新Expansion出来的节点开始模拟游戏，直到到达游戏结束状态，这样可以收到到这个expansion出来的节点的得分是多少。
  - Backpropagation：把前面expansion出来的节点得分反馈到前面所有父节点中，更新这些节点的quality value和visit times，方便后面计算UCB值。
  - 源代码：其中TREE_POLICY就是实现了Selection和和Expansion两个阶段，DEFAULT_POLICY实现了Simulation阶段，BACKUP实现了Backpropagation阶段。
- AlphaGo算法对MCTS算法的优化
  - 利用policy network的输出替换UCB的父节点访问次数，同样使用子节点访问次数作为分母保证exploration
  - Q值改为快速走子网络得到的所有叶子节点的均值，神经网络改成ResNet
  - 首先，AlphaGo每个节点可选action太多了，selection阶段不能像前面先遍历完所有子节点再expansion，这里是用改进的UCB算法来找到最优的需要expansion子节点，算法基本类似也是有控制exploration/exploitation的常量C并且与该子节点visit times成反比。
  - 其次，进行expansion时不会像前面这样直接random选择任意的action，而是这里也考虑到exploration/exploitation，一般前30步根据visit times成正比来选择，这样可以尽可能得先探索（根节点加入了狄利克雷分布保证所有点都经过），后面主要是根据visit times来走了。
  - 第三，新版AlphaGo Zero去掉了基于handcraft规则的rollout policy，也就是快速走子网络，以前是必须有快速走子直到完成比赛才能得到反馈，现在是直接基于神经网络计算预估的winer value概率值，然后平均得到每个子节点的state-action value也就是Q值。
  - 第四，AlphaGo在MCTS基础上收集最终的比赛结果作为label，MCTS作为policy evalution和policy iteration来实现增强学习。


## Counterfactual Regret
- 适用于非信息对称游戏（Imperfect information / Partial information），目标是找到逼近纳什均衡的搜索策略
- 德州扑克AI的常见算法