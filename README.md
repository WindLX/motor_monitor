## 协议

协议总长度为 16 + 8 + 1 + 151 = 176 bytes 分为四段
1. `UUID` 16 bytes `string` 消息唯一标识
2. `Timestamp` 8 bytes `f64` 毫秒级时间戳
3. `MessageType` 1 byte `uint8` 消息类型
4. `Payload` 151 bytes 数据负载

消息的前8位记录当前消息的类型：

### 命名规则

消息类型缩写：
+ `CC`: `Control Command` 控制命令
+ `QS`: `Query Status` 查询状态

后接短句以目标名字加短句的格式。目标名字缩写列表如下：
+ `P`: `Platform` 指向平台整体
+ `M`: `Motor` 指向电机
+ `SM`: `State Machine` 指向状态机

1-49 的消息归于 `CC` 使用，不会带有额外的数据包
51-99 的消息归于 `CC` 使用，会带有额外的数据包
101-199 的消息归于 `QS` 使用，会带有额外的数据包

### 控制命令

只会由上位机发送给下位机。

#### 1-49 不带有数据包的消息

1. `CC_P_START` 平台启动
2. `CC_P_ZERO` 平台回零
3. `CC_P_CENTER` 平台回中
4. `CC_P_BRAKE` 平台软件刹车
5. `CC_P_AUTO` 进入平台的洗出算法和逆运动学自动控制的位置模式
6. `CC_P_DISABLE` 平台电机失能
7. `CC_SM_CLEAN_ERROR` 清除状态机错误
8. `CC_P_ENTER_CORRECTION` 进入平台的校正模式
9. `CC_P_EXIT_CORRECTION` 退出平台的校正模式

#### 51-99 带有数据包的消息

51. `CC_M_MANUAL` 手动设置电机位置
52. `CC_M_STEP_CORRECTION` 平台校正模式下电机位置步进，该消息只在平台进入校正模式下才有效

##### `CC_M_MANUAL` 的 Payload 数据包结构

数据包长度为 1 + 54 = 55 bytes，分为两段
+ `arr_len` 1 byte `uint8` 后续数据的有效长度, 最大不超过 6
+ `objects` 6 * (1 + 8) = 54 bytes 数据的数组, 最多不超过 6 个元素
  + `motor_id` 1 byte `uint8` 电机的ID
  + `target_position` 8 bytes `uint32` 目标位置 (mm)

##### `CC_M_STEP_CORRECTION` 的 Payload 数据包结构

数据包长度为 1 + 12 = 13 bytes，分为两段
+ `arr_len` 1 byte `uint8` 后续数据的有效长度, 最大不超过 6
+ `objects` 6 * (1 + 1) = 12 bytes 数据的数组, 最多不超过 6 个元素
  + `motor_id` 1 byte `uint8` 电机的ID
  + `direction` 1 byte `uint8` 1 为正向步进，2 为反向步进

### 查询状态

只会由下位机发往上位机。

#### 101-199 查询类的数据消息

101. `QS_SM_STATE` 查询状态机的状态
102. `QS_M_STATE` 查询电机的状态

##### `QS_SM_STATE` 的 Payload 数据包结构

数据包长度为 1 byte `uint8`
0. `SM_UNKNOWN` 未知
1. `SM_INITIALIZING` 初始化中
2. `SM_ZEROING` 归零中
3. `SM_CENTERING` 回中中
4. `SM_BRAKING` 制动中
5. `SM_AUTOMATING` 自动模式中
6. `SM_IDLE` 空闲状态
8. `SM_CORRECTION` 校正模式中
101. `SM_MANUALING` 手动模式中

##### `QS_M_STATE` 的 Payload 数据包结构

数据包长度为 1 + 150 = 151 bytes，分为两段
+ `arr_len` 1 byte `uint8` 后续数据的有效长度, 最大不超过 6
+ `objects` 6 * (1 + 8 + 8 + 8) = 150 bytes 数据的数组, 最多不超过 6 个元素
  + `motor_id` 1 byte `uint8` 电机的ID
  + `position` 8 bytes `uint32` 位置 (mm)
  + `velocity` 8 bytes `uint32` 速度 (rpm)
  + `torque` 8 bytes `uint32` 扭矩 (Nm)

## 确定网络接口卡

首先，在MATLAB中使用slrtexplr对话框建立TCP/IP链接，按照工业控制计算机的配置进行操作。然后，在对话框中使用以下MATLAB代码检查网络接口卡信息：
```matlab
getPCIInfo(slrt, 'installed')
```
