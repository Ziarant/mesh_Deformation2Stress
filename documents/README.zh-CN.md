# mesh_Deformation2Stress
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)

![Icon](../src/icon.png)
>  基于逆有限元(iFEM)的思想和理论，根据变形前后的网格计算应力分布，即通过位移场推算应力场。

---

## 版本
- v0.1.0
> 项目目前正在进行中。将在接下来的几个月里完成代码的编写。

## 语言
- [English]

## 许可协议
- MIT

## 说明
该程序基于变形前后的源网格和目标网格提取位移场，计算应力分布。为了易于阅读和快速开发，程序使用<b>python</b>编写代码，因此没有发挥出完全的计算效率。计划后续版本（V2）使用C++语言对核心代码进行优化。

输入的变形前后网格应保证节点和单元编号能够对应（允许不完全对应），如下图所示。

![源网格和目标网格](../src/mesh.png)

程序模块如下图所示：

![流程图](../src/process.png)

- <b>格式转化处理器：</b>提供输入接口，用于处理输入信息，将其转化为程序所接受的格式。[当前版本](#版本)程序输入为源网格和目标网格的`.inp`文件，其中源网格需要包含网格的类型和节点坐标信息、材料信息。
- <b>预处理器:</b>解析网格数据，提取并重构节点、单元、材料等对象；
- <b>位移场求解器:</b>对比源网格和目标网格的节点坐标，求解位移场；
- <b>应变场求解器:</b>结合单元类型，对位移场进行计算，求解应变场；
- <b>应力场求解器:</b>结合材料属性，对应变场进行计算，求解应力场；
- <b>输出:</b>以`np.ndarray(N, 2)`格式输出节点上应力张量, 其中N为节点数量，第1列为节点编号，第2列为元组形式表示的无量纲张量值(节点平均)。

## 快速使用

在python环境中运行`main.py`：

```
python main.py source.inp target.inp \
    --averageMethod='Advanced' \
    --averageVariation=75 \
    --useCornerData=True \
    --outputFile=True \
    --tolerance=False \
    --unit='N-mm' \
    --boundary='False' \
```
其中可选参数：<font color=red>(当前版本`v0.1.0`未开放参数设置)</font>
- averageMethod:结果平均方法(默认为`Advanced`)；
- averageVariation:差异值(百分比，默认为`75`)
- useCornerData:纳入角节点(默认为`True`)
- outputFile: 指定输出`.txt`文件(默认为`True`，将保存在`source.inp`所在目录，名称为`result.txt`)；
- tolerance: 位移容差，位移超出容差的节点不进行应力计算(默认为`False`，目的是避免配准错误造成的计算结果异常，计划在V2后续版本进行开发)；
- unit:单位制(默认为`'N-mm'`)
- boundary:边界点监测(默认为`False`，开启后将视0位移边界点为固定约束，并基于力学平衡进行补偿计算，当前版本此参数无影响，计划在V2后续版本进行开发)
- registration: 配准方法，用于平滑或补偿(默认为`None`，当前版本此参数无影响，计划在V2后续版本进行开发)；

## [已完成工作](FinishedWork.md)
## [未来工作](FutureWork.md)


## 参考资料

[English]: ../README.md