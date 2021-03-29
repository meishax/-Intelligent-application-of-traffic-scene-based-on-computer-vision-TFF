# -Intelligent-application-of-traffic-scene-based-on-computer-vision-TFF
基于计算机视觉的交通场景智能应用（流量预测部分） 
- 通过Hadoop-Spark处理数据，通过Echats组件实现处理后的数据可视化，为后期流量预测提供数据支持。
数据可视化无处不在，并且随着城市、交通、气象等数据容量和复杂性的与日俱增，数据可视化的需求越来越大，成为人类对信息的一种新的阅读和理解方式。在GIS领域，通过大数据可视化手段进行数据分析，可以实现从秘密麻麻、错综复杂的数据挖掘信息，再通过可视化的方式展示出来，使读者对数据的空间分布模式、趋势、相关性和统计信息一目了然，而这些可能会在其他呈现方式下难以被发现。
数据可视化可以做到实时，还可以根据地图比例尺的变化实时更新分析结果。因此实现数据可视化是必由之路。
1、概念明确
数据可视化就是将大型数据集中的数据通过图形图像方式表示，并利用数据分析和开发工具发现其中未知信息。通过对原始数据进行标准化、结构化的处理，把它们整理成数据表。将这些数值转换成视觉结构，通过视觉的方式把它表现出来。将视觉结构进行组合，把它转换成图形传递给用户，用户通过人机交互的方式进行反向转换，去更好地了解数据背后有什么问题和规律。
2、可行性分析
数据可视化技术成熟，完全能够满足本项目的需求。部分开源可以免费使用对学生团队友好。
“盖亚开放数据技术计划”由滴滴出行在2017年10月正式发起，旨在通过开放滴滴出行平台的部分脱敏数据（例如原始轨迹数据、订单OD数据等），供高校和科研机构的专家学者、数据分析爱好者们进行学术研究之用，但相关开放的数据不得用于商业目的。“计划”在当时开放的一期数据，包含了2016年11月成都二环局部区域（约65平方公里）的滴滴快车、专车平台的脱敏轨迹数据。本次实验使用的原始数据就是2016年11月成都市二环局部轨迹数据”，数据大小为100GB。
1、Hadoop-Spark简介
Hadoop
主要是由HDFS和MapReduce组成。HDFS是Google File System（GFS）的开源实现。MapReduce是Google MapReduce的开源实现。 具体而言，Apache Hadoop软件库是一个允许使用简单编程模型跨计算机集群处理大型数据集合的框架，其设计的初衷是将单个服务器扩展成上千个机器组成的一个集群为大数据提供计算服务，其中每个机器都提供本地计算和存储服务。
Hadoop的核心:
HDFS和MapReduce是Hadoop的两大核心。通过HDFS来实现对分布式储存的底层支持到高速并行读写与大容量的储存扩展
通过MapReduce实现对分布式任务进行处理程序支持，保证高速分区处理数据。
MapReduce的计算模型分为Map和Reduce两个过程。在日常经验里，我们统计数据需要分类，分类越细、参与统计的人数越多，计算的时间就越短，这就是Map的形象比喻，在大数据计算中，成百上千台机器同时读取目标文件的各个部分，然后对每个部分的统计量进行计算，Map就是负责这一工作的；而Reduce就是对分类计数之后的合计，是大数据计算的第二阶段。可见，数据的计算过程就是在HDFS基础上进行分类汇总。
HDFS把节点分成两类：NameNode和DataNode。NameNode是唯一的，程序与之通信，然后从DataNode上存取文件。这些操作是透明的，与普通的文件系统API没有区别。MapReduce则是JobTracker节点为主，分配工作以及负责和用户程序通信。
Hadoop一个作业称为一个Job，Job里面分为Map Task和Reduce Task阶段，每个Task都在自己的进程中运行，当Task结束时，进程也会随之结束。
Hadoop实质上更多是一个分布式系统基础架构: 它将巨大的数据集分派到一个由普通计算机组成的集群中的多个节点进行存储，同时还会索引和跟踪这些数据，大幅度提升大数据处理和分析效率。Hadoop 可以独立完成数据的存储和处理工作，因为其除了提供HDFS分布式数据存储功能，还提供MapReduce数据处理功能。
Hadoop是磁盘级计算，计算时需要在磁盘中读取数据。其采用的是MapReduce的逻辑，把数据进行切片计算用这种方式来处理大量的离线数据.Hadoop将每次处理后的数据写入磁盘中，对应对系统错误具有天生优势。Hadoop适合处理静态数据，对于迭代式流式数据的处理能力差。Hadoop中中间结果存放在HDFS中，每次MR都需要刷写-调用。
Spark，是一种通用的大数据计算框架，正如传统大数据技术Hadoop的MapReduce、Hive引擎，以及Storm流式实时计算引擎等。Spark包含了大数据领域常见的各种计算框架：比如Spark Core用于离线计算，Spark SQL用于交互式查询，Spark Streaming用于实时流式计算，Spark MLlib用于机器学习，Spark GraphX用于图计算。Spark主要用于大数据的计算，而Hadoop以后主要用于大数据的存储（比如HDFS、Hive、HBase等），以及资源调度（Yarn）。
Spark用户提交的任务称为application，一个application对应一个SparkContext，app中存在多个job，每触发一次action操作就会产生一个job。这些job可以并行或串行执行，每个job中有多个stage，stage是shuffle过程中DAGScheduler通过RDD之间的依赖关系划分job而来的，每个stage里面有多个task，组成taskset，由TaskScheduler分发到各个executor中执行；executor的生命周期是和app一样的，即使没有job运行也是存在的，所以task可以快速启动读取内存进行计算。
Spark 是一个专门用来对那些分布式存储的大数据进行处理的工具，没有提供文件管理系统，自身不会进行数据的存储。它必须和其他的分布式文件系统进行集成才能运作。可以选择Hadoop的HDFS,也可以选择其他平台。
Spark，它会在内存中以接近“实时”的时间完成所有的数据分析。Spark的批处理速度比MapReduce快近10倍，内存中的数据分析速度则快近100倍。Spark的数据对象存储在弹性分布式数据集(RDD:)中。“这些数据对象既可放在内存，也可以放在磁盘，所以RDD也提供完整的灾难恢复功能。Spark通过在内存中缓存处理的数据，提高了处理流式数据和迭代式数据的性能。Spark中间结果存放优先存放在内存中，内存不够再存放在磁盘中，不放入HDFS，避免了大量的IO和刷写读取操作。
ECharts，一个使用 JavaScript 实现的开源可视化库，可以流畅的运行在 PC 和移动设备上，兼容当前绝大部分浏览器（IE8/9/10/11，Chrome，Firefox，Safari等），底层依赖轻量级的矢量图形库 ZRender，提供直观，交互丰富，可高度个性化定制的数据可视化图表。
ECharts 提供了常规的折线图、柱状图、散点图、饼图、K线图，用于统计的盒形图，用于地理数据可视化的地图、热力图、线图，用于关系数据可视化的关系图、旭日图，多维数据可视化的平行坐标，还有用于 BI 的漏斗图，仪表盘，并且支持图与图之间的混搭。
Ajax的全称是：Asynchronous JavaScript And XML，指的是异步 JavaScript 及 XML（其实主要用的就是javascript技术），它不是一种新的编程语言，而是一种用于创建更好更快以及交互性更强的 Web 应用程序的技术。 Ajax的特点是异步 ，通过在后台与服务器进行少量数据交换，Ajax 可以使网页实现异步更新。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新，比如可以使用Ajax更新局部网页、使用Ajax在不刷新页面的情况下查询数据、验证用户注册的用户名是否唯一等。
使用Ajax的最大优点，就是能在不更新整个页面的前提下维护数据。这使得Web应用程序更为迅捷地回应用户动作，并避免了在网络上发送那些没有改变的信息。此外Ajax不需要任何浏览器插件，但需要用户允许Javascript在浏览器上执行。
Echart获取：在 ECharts 的GitHub获取。或者通过CDN 引入。
前端调用Echarts组件最终实现可视化，使用Jquery实现Ajax异步刷新图表。

- 对交通流量预测，依赖于当前时间t之前的交通流量数据，循环神经网络RNN正是被设计出来处理这一类序列数据的神经网络。但是传统RNN网络由于激活函数和自身结构的缺陷，会出现梯度弥散/梯度爆炸问题，在交通流量预测中，难以使用距离当前时间较久远的流量数据，进而印象了预测结果的准确性。为了解决这一问题，我们使用了LSTM并修改了激活函数。通过堆叠增加LSTM的深度，我们搭建了属于自己的LSTM神经网络回归模型，并将其应用在了本项目的流量预测模块上。
RNN（Recurrent Neural Network）是一类用于处理序列数据的神经网络。序列数据是指在不同时间点上收集到的数据，这类数据反映了某一事物、现象等随时间的变化状态或程度。
神经网络包含输入层、隐层、输出层，通过激活函数控制输出，层与层之间通过权值连接。激活函数是事先确定好的，那么神经网络模型通过训练的结果就蕴含在权值中。
基础的神经网络只在层与层之间建立了权连接，RNN最大的不同之处就是在层之间的神经元之间也建立的权连接。
一个标准的RNN结构图，图中每个箭头代表做一次变换，也就是说箭头连接带有权值。左侧是折叠起来的样子，右侧是展开的样子，左侧中h旁边的箭头代表此结构中的“循环“体现在隐层。
在展开结构中我们可以观察到，在标准的RNN结构中，隐层的神经元之间也是带有权值的。也就是说，随着序列的不断推进，前面的隐层将会影响后面的隐层。图中O代表输出，y代表样本给出的确定值，L代表损失函数，我们可以看到，“损失“也是随着序列的推荐而不断积累的。
除上述特点之外，标准RNN的还有以下特点：
1、权值共享，图中的W全是相同的，U和V也一样。
2、每一个输入值都只与它本身的那条路线建立权连接，不会和别的神经元连接。
普通卷积神经网络的优化使用的是反向传播， RNN使用的通常还是反向传播，不过是带时序的版本，即BPFT（backpropagation through time），它与BP的原理是完全一样的，只不过计算过程与时间有关。
与普通的反向传播算法一样，它重复地使用链式法则，区别在于损失函数不仅依赖于当前时刻的输出层，也依赖于下一时刻。所以参数W在更新梯度时，必须考虑当前时刻的梯度和下一时刻的梯度。 
t时刻的导数会传播到t-1，t-2，... ，1时刻，这样就有了连乘的系数。连乘一直带来了两个问题：梯度爆炸和消失。而且，在前向过程中，开始时刻的输入对后面时刻的影响越来越小，这就是长距离依赖问题。这样一来，就失去了“记忆”的能力。
RNN使用两种激活函数，分别是sigmoid与tanh。
二者何其的相似，都把输出压缩在了一个范围之内。他们的导数图像也非常相近，我们可以从中观察到，sigmoid函数的导数范围是(0,0.25]，tanh函数的导数范围是(0,1]，他们的导数最大都不大于1。
这就会导致一个问题，在累乘的过程中，如果取sigmoid函数作为激活函数的话，那么必然是一堆小数在做乘法，结果就是越乘越小。随着时间序列的不断深入，小数的累乘就会导致梯度越来越小直到接近于0，这就是“梯度消失“现象。其实RNN的时间序列与深层神经网络很像，在较为深层的神经网络中使用sigmoid函数做激活函数也会导致反向传播时梯度消失，梯度消失就意味消失那一层的参数再也不更新，那么那一层隐层就变成了单纯的映射层，毫无意义了，所以在深层神经网络中，有时候多加神经元数量可能会比多加深度好。
sigmoid函数还有一个缺点，sigmoid函数输出不是零中心对称。sigmoid的输出均大于0，这就使得输出不是0均值，称为偏移现象，这将导致后一层的神经元将上一层输出的非0均值的信号作为输入。关于原点对称的输入和中心对称的输出，网络会收敛地更好。
RNN的特点本来就是能“追根溯源“利用历史数据，现在可利用的历史数据竟然是有限的，这就令其效率大大下降，解决“梯度消失“是非常必要的。解决“梯度消失“的方法主要有：
1、选取更好的激活函数
2、改变传播结构
关于第一点，一般选用ReLU函数作为激活函数。ReLU函数的左侧导数为0，右侧导数恒为1，这就避免了“梯度消失“的发生。但恒为1的导数容易导致“梯度爆炸“，但设定合适的阈值可以解决这个问题。
关于第二点，LSTM结构可以解决这个问题。
RNN 的关键点之一就是他们可以用来连接先前的信息到当前的任务上，例如使用过去的视频段来推测对当前段的理解。如果 RNN 可以做到这个，他们就变得非常有用。有时候，我们仅仅需要知道先前的信息来执行当前的任务。例如，我们有一个语言模型用来基于先前的词来预测下一个词。如果我们试着预测 “the clouds are in the sky” 最后的词，我们并不需要任何其他的上下文 —— 因此下一个词很显然就应该是 sky。在这样的场景中，相关的信息和预测的词位置之间的间隔是非常小的，RNN 可以学会使用先前的信息。
但是同样会有一些更加复杂的场景。假设我们试着去预测“I grew up in France… I speak fluent French”最后的词。当前的信息建议下一个词可能是一种语言的名字，但是如果我们需要弄清楚是什么语言，我们是需要先前提到的离当前位置很远的 France 的上下文的。这说明相关信息和当前预测位置之间的间隔就肯定变得相当的大。不幸的是，在这个间隔不断增大时，RNN 会丧失学习到连接如此远的信息的能力。
在理论上，RNN 绝对可以处理这样的 长期依赖 问题。人们可以仔细挑选参数来解决这类问题中的最初级形式，但在实践中，RNN 肯定不能够成功学习到这些知识。Bengio, et al. (1994)等人对该问题进行了深入的研究，他们发现一些使训练 RNN 变得非常困难的相当根本的原因。
然而，幸运的是，LSTM 并没有这个问题
LSTM（long short-term memory）。长短期记忆网络是RNN的一种变体，RNN由于梯度消失的原因只能有短期记忆，LSTM网络通过精妙的门控制将短期记忆与长期记忆结合起来，并且一定程度上解决了梯度消失的问题。
LSTM 由Hochreiter & Schmidhuber (1997)提出，并在近期被Alex Graves进行了改良和推广。在很多问题，LSTM 都取得相当巨大的成功，并得到了广泛的使用。LSTM 通过刻意的设计来避免长期依赖问题。记住长期的信息在实践中是 LSTM 的默认行为，而非需要付出很大代价才能获得的能力！
所有 RNN 都具有一种重复神经网络模块的链式的形式。在标准的 RNN 中，这个重复的模块只有一个非常简单的结构，例如一个 tanh 层。
LSTM 同样是这样的结构，但是重复的模块拥有一个不同的结构。不同于 单一神经网络层，整体上除了h在随时间流动，细胞状态c也在随时间流动，细胞状态c就代表着长期记忆。
LSTM引入了若干门，相比RNN多了一个状态cell state。这个cell state承载着之前所有状态的信息，每到新的时刻，就有相应的操作来决定舍弃什么旧的信息以及添加什么新的信息。这个状态与隐藏层状态h不同，在更新过程中，它的更新是缓慢的，而隐藏层状态h的更新是迅速的。
遗忘门决定了要从上一个状态中舍弃什么信息，它输入上一状态的输出ht-1、当前状态输入信息xt到一个Sigmoid函数中，产生一个介于0到1之间的数值，与上一个时刻的状态ct-1相乘之后来确定舍弃（保留）多少信息。0 表示“完全舍弃”，1 表示“完全保留”，这个阶段完成了对上一个节点cell state进行选择性忘记。
选择记忆阶段，也就是对输入有选择性地进行“记忆”，重要的记录下来，不重要的少记一些，它决定了要往当前状态中保存什么新的信息。它输入上一状态的输出ht-1、当前输入信息xt到一个Sigmoid函数中，产生一个介于0到1之间的数值it来确定需要保留多少的新信息。
“候选新信息”则通过输入上一状态的输出、当前状态输入信息和一个tanh激活函数生成。有了遗忘门和输入门之后，就得到了完整的下一时刻的状态Ct，它将用于产生下一状态的隐藏层ht，也就是当前单元的输出。
输出门决定了要从cell state中输出什么信息。与之前类似，会先有一个Sigmoid函数产生一个介于0到1之间的数值Ot来确定我们需要输出多少cell state中的信息。cell state的信息在与Ot相乘时首先会经过一个tanh层进行“激活”，得到的就是这个LSTM block的输出信息ht。
以上就是LSTM的基本原理，它通过门控状态来对信息进行选择性的记忆，满足了需要长时间记忆信息和遗忘信息的需求。
在现有 LSTM 模型基础上，我们采用堆叠架构，增加 LSTM 的深度。堆叠式 LSTM 架构可以定义为由多个 LSTM 层组成的 LSTM 模型。上面的 LSTM 层提供序列输出而不是单个值输出到下面的 LSTM 层。具体地说，每个输入时间步长一个输出，而不是所有输入时间步长的一个输出时间步长。堆叠 LSTM 隐藏层使模型更深入，鉴于 LSTM 对序列数据进行操作，这意味着层的添加增加了输入观察随时间的抽象级别。并且足够大的单个隐藏层多层感知器可用于近似大多数功能，增加网络的深度可以优化模型性能。多层 LSTM 神经网络回归模型，包括一个输入层，两个 LSTM 网络层，一个全连接层，激活函数采用 sigmod。
