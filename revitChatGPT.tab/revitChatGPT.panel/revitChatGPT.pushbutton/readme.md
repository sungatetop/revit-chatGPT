# chat At Revit

# Introduction Generate from chatGPT
这是一个 IronPython 脚本，用于使用 OpenAI API 实现 Revit 命令行聊天机器人。下面是代码解释：

* 导入所需的 Python 模块和 Revit API 模块。
* 定义了一个 ViewModel 类，包含用户输入、API token 和对话列表。
* 定义了一个 UI 类，继承了 forms.WPFWindow 和 forms.Reactive，其中包含了处理用户输入、显示对话、发送 API 请求等功能。
* 在 UI 类中定义了许多方法来处理用户交互事件，比如单击提交按钮，输入 API token 和用户输入等。
* 通过调用 ViewModel 类中的属性来获取用户输入和 API token，并使用这些数据调用 OpenAI API。
处理 API 的响应，将其显示在聊天机器人的窗口中，并在需要时执行 Revit 命令。
* AddMessage 方法用于在聊天机器人窗口中添加新的消息，并为消息添加不同的颜色和角色。

# Usage

首先你需要有api_token

然后就两步操作：

* Step1.安装pyrevit
* Step2.将revitChatGPT.tab文件夹放到pyrevit的extensions目录下
* ok！

<image src="./location.png"/>

<image src="./revit-chatGPTDemo.png" />

可以参考visual-chatGPT,要求chatGPT对指定任务按操作集合进行返回，例如:
``` js
    请你担当软件工程师，熟悉Autodesk Revit 二次开发，请你根据我后续提出需求，生成一个实现需求的操作列表，列表项格式为：{order:"",action_name:"",input_value:""}，其中order为执行顺序，action_name为revit中的操作命令，input_value为对应的操作命令的输入参数。如果你能理解我的意思，请回复copied！

```
<image src="./revit-chatGPT-instruction.png" />

要求chatGPT对于指定目标按给定的格式返回数据，这里指定一个操作集合。** 注意：需要约束操作集的来源，比如revit内置的操作，或pyrevit内置的操作，以及自己编写的操作 **，而自动化处理就是让chatGPT从抽象的语言描述中找到实现需要的“途径”(操作集)，agent代理负责执行这些操作集。

<image src="./revit-chatGPT-instruction2.png" />
<image src="./revit-chatGPT-instruction3.png" />
<image src="./revit-chatGPT-instruction4.png" />
<image src="./revit-chatGPT-instruction4.png" />


