# 操作系统 / 系统软件 / 桌面应用界面文案风格

## 目录

1. 什么时候用这份
2. 语气和人格
3. 代表厂商和规范
4. 术语和叫法
5. 按元素写
6. 合规和硬约束
7. 高风险场景
8. 这个行业的 AI 腔和坏写法
9. 改前 → 改后
10. 审查时加查的项
11. 台港市场差异

## 1. 什么时候用这份

信号（命中任意两条就用；只命中一条时，结合用户的话判断）：

- 代码 / 依赖：`electron`、`electron-builder`、`@tauri-apps/api`、`tauri.conf.json`、`Microsoft.UI.Xaml`（WinUI）、`.xaml`/`App.xaml.cs`（WPF）、`QtWidgets`/`QtQuick`/`.ui`（Qt）、`Gtk.Application`/GtkBuilder `.ui` XML、`libadwaita`/`Adw.*`、`org.kde.kirigami`、`.desktop` 文件、Windows 服务（`sc.exe`、`ServiceBase`）、驱动工程（`.inf`、`.sys`、WDK）、`manifest.xml` 里的 `requestedExecutionLevel`（UAC 清单）、`NSStatusItem`/`Tray`/`SystemTrayIcon`
- 目录 / 文件名：`installer/`、`updater/`、`src-tauri/`、`electron-builder.yml`、`Info.plist`、`entitlements.plist`、安装包脚本 `.nsi`（NSIS）、`.wxs`/`Product.wxs`（WiX）、`.iss`（Inno Setup）、`.spec`（rpm）、`control`（deb）、`dmg/`、`AppImage`
- 界面里的词：权限、授权、崩溃、闪退、更新、重启、安装、卸载、存储空间、磁盘空间、证书、未受信任、签名、开机启动、托盘、通知、省电模式、性能模式、快捷键、驱动、蓝屏、安全模式、后台运行、清理缓存、恢复出厂设置
- 用户的话：「桌面应用」「系统弹窗」「安装包」「托盘图标」「开机启动项」「驱动签名」「UAC 弹窗」「更新要重启」

和别的行业重叠时：「系统软件 + 安全软件」（杀毒、防火墙、EDR）先按这份的安全警告规则定调，再叠安全行业自己的分级用词（如果项目另有安全行业文件）；「系统软件 + 企业 IT / MDM」在本文件基础上，语气可以更正式、更少省略，面向 IT 管理员而不是终端用户。

## 2. 语气和人格

- 一句话定调：像系统本身在说话——克制、中性、不炫耀、一次只交代一件事；日常文案平和，涉及不可逆操作或安全风险时语气要收紧，不能和「已保存」这种寻常提示一个调子。
- 人称：中文统一用「你」，不用「您」——苹果、微软、HarmonyOS 的中文系统文案都用「你」；「您」是客服口吻，系统不是客服。英文系统文案里少用 my / your 这类所有格（"Favorites" 就够，不必 "Your Favorites"），完全不用 "we"——Apple HIG 指出 "We're having trouble loading this content" 不如 "Unable to load content" 清楚；警告文案要直接、中性，不能含糊或带指责（<https://developer.apple.com/design/human-interface-guidelines/writing>、<https://developer.apple.com/design/human-interface-guidelines/alerts>）。
- 正式程度：比聊天类产品更正式，比法律文书口语。日常状态提示、报错一律不用感叹号；首次使用引导允许偶尔轻松，但不能盖过信息本身。
- emoji：系统级界面（设置、对话框、通知、安装向导）不用 emoji，这和消费类 App 不同；第三方桌面应用的营销页面不算在内。
- 能不能幽默：操作结果、报错、安全提示绝不幽默；空状态、引导页可以有一点轻松语气，但功能说明要先到位。
- 和 `principles.md` 不同、要覆盖它的地方：
  - 「按状态过一遍」在系统软件里要多加一种状态——**已完成但需要重启才生效**。这是系统软件特有的坑：很多操作点了「保存」/「应用」就弹「已完成」，实际上配置要重启才真正生效，用户以为改好了。
  - 「只说确认了的事」在这里要加码：系统操作大多有可核实的真实进度（安装百分比、剩余时间、第几步），不像网络请求那样常常没有回执，所以能查到的进度要给用户用得上的具体数字（字节数这类内部计量不算），不能退回到含糊的「请稍候」。
  - 危险操作按钮 `principles.md` 已经要求写动作本身；系统软件里的危险操作（格式化、清除数据、卸载驱动）通常还需要比普通确认框更重的二次确认（见第 7 节「高风险场景」），不是点一下「删除」就完事。
  - 系统托盘 / 菜单栏图标本身没有文字，状态只靠工具提示和右键菜单传达，所以这类工具提示要能独立说清楚当前状态，不能假设用户已经注意到图标颜色或角标的变化。

## 3. 代表厂商和规范

| 厂商 / 规范 | 风格要点（能落到句子上的） | 出处 |
|---|---|---|
| Apple Human Interface Guidelines – Writing（含 Alerts） | 警告标题清楚简短地描述情况；标题是完整句子就用句子大小写加句尾标点，是短语就用标题大小写、不加句尾标点；正文只在有用时才加，越短越好，尽量别让警告框需要滚动；语气直接、中性，不含糊、不指责、不掩盖严重程度；按钮用一两个词、和正文直接相关的动词（"Erase"、"Delete"），只有纯告知类警告才用 "OK"；少用 my/your，不用 "we" | <https://developer.apple.com/design/human-interface-guidelines/alerts>、<https://developer.apple.com/design/human-interface-guidelines/writing> |
| Apple Style Guide | 覆盖苹果产品文案里缩写、大小写、标点、度量单位的统一写法，按年更新 | <https://help.apple.com/pdf/applestyleguide/en_US/apple-style-guide.pdf> |
| Microsoft Windows apps – Writing style | concise 不等于「字少」，而是「efficient」——刚好够用；按钮文字最多两三个短词；报错标题描述问题本身，不描述解决动作；按钮/复选框/单选项文字不加句尾句号，工具提示和报错正文要加句号 | <https://learn.microsoft.com/en-us/windows/apps/design/style/writing-style> |
| Microsoft Windows UX Guide – Error Messages | 报错写法「温暖放松、随时搭把手、干脆清楚」三原则；结构上先说问题，再给用户能执行的现实解决办法；modal 对话框只用在必须让用户立刻处理、无法忽略的场景 | <https://learn.microsoft.com/en-us/windows/win32/uxguide/mess-error> |
| Microsoft Windows UX Guide – User Account Control | UAC 术语口径：首次出现写全称 User Account Control，之后简写 UAC；不要用省略号暗示「这个命令需要提权」，提权要靠盾牌图标表达，不是靠标点 | <https://learn.microsoft.com/en-us/windows/win32/uxguide/winenv-uac> |
| GNOME Human Interface Guidelines – Writing Style | 文本尽量短，但不能短到丢意思或变得含糊；用中性视角，少用「你/我的」，确有归属关系时用「你的」而不是「我的」；标题大小写（4 字母以上首字母大写）和句子大小写分场合使用，复选框/单选项/正文一律句子大小写 | <https://developer.gnome.org/hig/guidelines/writing-style.html> |
| KDE Human Interface Guidelines – Text and Labels | 按钮、菜单项用祈使语气（「Apply」而不是「Yes」）；正向措辞描述「开启后会怎样」，不描述关闭；优先用「folder」而不是「directory」，删除文件的操作统一叫「Delete」；尽量不用缩写词，非用不可时第一次出现要展开解释 | <https://develop.kde.org/hig/text_and_labels/> |
| Mozilla Acorn（Firefox 设计系统）– Content Guidelines | 桌面端、Android 端、网站默认用句子大小写（sentence case），更利于快速扫读、语气更亲和；技术缩写能不用就不用，必须用时给一句话解释，避免难以本地化的俚语和比喻 | <https://acorn.firefox.com/latest/content-guidelines/capitalization.html> |
| Android Developers – Permissions | 系统权限弹窗本身的文案由系统固定，应用能写的是弹窗之前「为什么需要这个权限」的说明；这段说明要贴着触发它的具体操作出现，不要在启动时一次性要齐所有权限 | <https://developer.android.com/training/permissions/requesting>、<https://developer.android.com/training/permissions/explaining-access> |
| HarmonyOS Design（华为开发者联盟设计规范） | 官方设计系统覆盖视觉、交互、动效、字体等规范，但没有找到独立公开的中文文案写作规范；写鸿蒙应用的文案时，点按动作叫「点击」还是「轻点」等用词，以鸿蒙系统自带应用的实际文案为准，不要凭印象从别的平台搬 | <https://developer.huawei.com/consumer/cn/design/> |
| 小米 HyperOS / MIUI 开发者文档 | 《MIUI10通知样式及能力适配说明》：标准通知一般只有「标题、内容、图标、时间戳」四个元素，大文本样式要长按才展开——关键信息要放进标题和第一行内容，不能指望用户展开看；这份是开发适配文档，不是文案风格指南 | <https://dev.mi.com/xiaomihyperos/documentation/detail?pId=1581> |
| 统信 UOS / DTK（Deepin Tool Kit） | DtkWidget 提供深度桌面的基础控件，自带 DDialog、DInputDialog、DFloatingMessage 等对话框和浮动消息组件；写 UOS 应用时复用这些组件的结构，不自造一套确认框 / 报错样式。DTK 本身不规定文案措辞 | <https://github.com/linuxdeepin/dtkwidget> |
| Apple 简体中文支持文档 | 可直接查证的真实简体中文系统文案用例：iPhone / iPad 用「轻点」，Mac 用「点按」（不用「点击」）；统一用「文件夹」 | <https://support.apple.com/zh-cn/guide/iphone/iph1a2a3a2c/ios>、<https://support.apple.com/zh-cn/guide/mac-help/mh35840/mac> |
| Microsoft Windows apps – Dialog controls | 标题是主要指示，可省略，要短，并和按钮选项直接对应；正文不要换个说法重复标题；至少有一个安全、无破坏性的按钮（如 "Cancel"、"Close"），放在最右边，执行类按钮在左边；按钮文字用对正文问题的具体回答（如 "Allow" / "Block"），不用笼统的 OK | <https://learn.microsoft.com/en-us/windows/apps/develop/ui/controls/dialogs-and-flyouts/dialogs> |
| Android Developers – Notifications | 通知标题要能在不看正文的情况下独立传达关键信息；正文给补充信息或下一步，避免把标题和正文写成同一句话的重复 | <https://developer.android.com/develop/ui/views/notifications> |

## 4. 术语和叫法

| 用 | 不用 | 说明 |
|---|---|---|
| 文件夹 | 目录 | 面向普通用户的系统文案统一用「文件夹」；「目录」留给命令行 / 开发者文档语境，GNOME、KDE 的 HIG 也明确倾向日常词「folder」而非「directory」 |
| 设置 | 选项、首选项 | 系统级配置入口统一叫「设置」；「选项」留给某个功能内部的一组开关（如「打印选项」）；「首选项」是 macOS Preferences 的旧译法，新文案不用 |
| 点击 | 单击、点按（通用 / 触屏场景） | 面向触屏或「鼠标 + 触屏」通用场景统一用「点击」；「单击」是需要和「双击」对比区分时才用的精确词，不要在不需要区分的地方多此一举 |
| 轻点 | 点击（纯触屏产品内） | 纯触屏 / 平板场景的中文文案可用「轻点」；桌面鼠标 + 键盘场景不用「轻点」。一个产品选一种，不要和「点击」混用 |
| 应用 | 程序、软件、App | 系统设置、应用商店统一叫「应用」；「程序」是旧版 Windows 叫法，「软件」偏口语，混用会显得文案不是一个人写的 |
| 更新 | 升级（版本号提升场景） | 打补丁、推送新版本统一叫「更新」；「升级」留给付费版本跃迁（如「升级到专业版」），避免和系统更新混为一谈 |
| 重启 | 重新启动、重启动 | 统一用「重启」；「重新启动」偏书面、翻译腔，日常 UI 不用 |
| 卸载 | 删除（移除应用场景） | 移除一个应用统一叫「卸载」；「删除」留给文件、数据、记录 |
| 权限 | 许可 | 系统授权能力统一叫「权限」（相机权限、位置权限）；「许可」是许可证 / License 语境的词，不要混用 |
| 存储空间 | 磁盘空间、硬盘空间 | 面向普通用户统一「存储空间」，尤其在 SSD、云盘、手机存储混用的场景下「磁盘」已经不准确；「磁盘空间」是传统叫法，技术文档可以用 |
| 证书 | 凭据（证书场景） | HTTPS、代码签名场景统一「证书」；「凭据」是账号、密码、令牌语境的词 |
| 未受信任 | 不可信、危险 | 签名 / 证书场景统一「未受信任」；「危险」过于主观，没有扫描结论支撑时不能用 |
| 后台运行 | 常驻、挂起 | 面向用户统一「后台运行」；「挂起」（suspended）是开发者语境的词 |
| 开机启动 | 自启动 | 统一「开机启动」（如「开机启动项」），比「自启动」多两个字但指代更清楚 |
| 快捷键 | 热键 | 统一「快捷键」；「热键」只在需要强调「跨应用全局触发」时才用「全局热键」做区分 |
| 通知 | 消息推送 | 系统弹出的提示统一叫「通知」；「推送」强调的是服务端行为，用户看到的始终是「通知」 |
| 任务栏 | 底部栏 | Windows 专有叫法「任务栏」，不要自造「底部栏」 |
| 程序坞 | 底部栏、Dock 栏 | macOS 专有叫法「程序坞」（Dock），不要套用 Windows 的「任务栏」 |
| 文件资源管理器 | 文件管理器（Windows 语境） | Windows 系统自带的文件管理应用全称「文件资源管理器」；跨平台第三方文件管理器可以用通用词「文件管理器」 |
| 访达 | 文件管理器（macOS 语境） | macOS 系统自带的对应功能叫「访达」（Finder），不要和「文件资源管理器」混用 |
| 回收站 | 垃圾桶（Windows 语境） | Windows 统一「回收站」 |
| 废纸篓 | 回收站（macOS 语境） | macOS 统一「废纸篓」（Trash），不要套用 Windows 的「回收站」 |
| 任务管理器 | 进程管理器（Windows 语境） | Windows 统一「任务管理器」 |
| 活动监视器 | 任务管理器（macOS 语境） | macOS 对应功能叫「活动监视器」（Activity Monitor），不要套用 Windows 叫法 |
| 蓝屏 | 系统崩溃（泛指） | 「蓝屏」专指 Windows 的 BSOD 现象，不要泛化成任何平台的任何崩溃都叫蓝屏；macOS / Linux 对应情况用「系统无响应」「内核崩溃」 |
| 安全模式 | 故障排除模式 | Windows、macOS 统一叫「安全模式」（Safe Mode） |
| GB / MB / KB | G、M、K（口语简写） | 容量单位在正式文案里要带完整字母；别用口语化的单字母出现在界面上 |
| 小时 / 分钟 / 秒 | h / min / s（面向用户的时长） | 面向用户的时长写完整中文单位；英文缩写留给技术日志、开发者面板 |
| 睡眠 | 休眠（二者不是近义词） | 「睡眠」（Sleep，内存保持供电）和「休眠」（Hibernate，状态写入磁盘后断电）是两种不同的电源状态，文案不能互换，写错会让用户以为设备没有真正断电或反之 |
| 剪贴板 | 剪切板 | 统一「剪贴板」，「剪切板」是常见别字，不要在同一产品里两种都出现 |
| 恢复出厂设置 | 出厂重置、重置手机 | 统一「恢复出厂设置」，或跟随平台既有翻译（如 Windows 设置项「重置此电脑」），同一产品内只用一种 |
| 深色模式 | 黑夜模式、夜间模式 | 跟随系统设置项的既有叫法「深色模式」（Dark Mode）；「夜间模式」容易和护眼 / 滤蓝光场景的开关混淆 |
| 勿扰模式 | 免打扰模式 | 跟随系统既有翻译「勿扰模式」（Do Not Disturb），不要自造「免打扰模式」 |
| 虚拟内存 | 交换空间（Windows 语境） | Windows 设置项里统一「虚拟内存」；「交换空间」（swap）是 Linux / Unix 语境的叫法，别混用 |
| 锁屏 | 锁定屏幕 | 统一简称「锁屏」（如「锁屏界面」「锁屏密码」），「锁定屏幕」偏书面，日常 UI 不用 |
| 外接显示器 | 扩展屏幕（二者场景不同） | 「外接显示器」指物理接入的第二块屏；「扩展屏幕」特指显示模式（区别于「复制屏幕」），两个词不能互相替代 |
| 格式化 | 清除、抹掉（磁盘场景） | 对磁盘 / 分区的操作统一用「格式化」；「清除」「抹掉」留给数据 / 内容场景，混用会让用户分不清是清空文件还是清空整个分区 |
| 驱动程序 | 驱动器（二者不是同一个词） | 「驱动程序」（Driver）是控制硬件的软件；「驱动器」（Drive）指磁盘、光驱这类物理或虚拟设备。两个词形近但所指完全不同，写错会直接造成误解 |
| 兼容模式 | 兼容性模式 | 跟随 Windows 既有设置项叫法「兼容模式」，同一产品内不要「兼容模式」「兼容性模式」两种都用 |

## 5. 按元素写

只写和通用写法不同的部分，结构、按钮、空状态等通用规则见 `principles.md`。

**权限请求（相机、位置、文件）**
系统弹窗本身的文案由操作系统固定，应用能写的是弹窗前的「预告」说明：讲清楚用在哪个具体操作上，不说「为了提供更好的体验」这类空话；用户拒绝后不要反复弹、不要阻断核心流程，在设置里留一条路让用户后悔。
- zh：需要访问相机才能扫描二维码。
- en：Allow access to your camera to scan QR codes.
- 反例（不要这样写）：为了给您提供更好的体验，请开启全部权限。

**更新 / 重启提示**
先说清楚是什么更新（安全更新 / 功能更新）以及为什么必须重启才能完成，再给选项；能推迟的要给出推迟期限或下一次提醒时间；强制的安全更新要给出最终期限。
- zh：需要重启电脑以完成安装。你可以现在重启，也可以选择今晚 2:00 自动重启。
- en：Restart to finish installing updates. Restart now, or schedule it for tonight at 2:00 AM.

**安装 / 卸载**
安装前说清楚大小和安装位置（如果可改）；卸载前说清楚是否连带删除用户数据或配置，按钮写动作本身而不是「确定」。
- zh：卸载后，「记事本增强版」及其设置会被移除，已保存的文档不受影响。
- en：Uninstalling will remove TextEditor Pro and its settings. Your saved documents won't be affected.
（Windows 11 的卸载确认框采用类似结构：「此应用及其相关信息将被卸载」+「卸载」按钮）

**磁盘空间 / 存储警告**
给具体的可用空间数字和明确动作，不要只说「空间不足」；安装或更新前空间不够时，说清楚还差多少。
- zh：存储空间只剩 1.2 GB，完成这次更新还需要 3 GB。清理缓存或卸载不用的应用后再试。
- en：You have 1.2 GB free. This update needs 3 GB. Free up space, then try again.

**崩溃对话框**
先说应用退出了，不渲染技术异常；「重新打开」和「查看详情 / 发送报告」分成两个按钮，不要混在一句话里；「抱歉」最多出现一次。
- zh：「设计器」意外退出。［重新打开］［查看报告］
- en：Designer unexpectedly quit. [Reopen] [Report…]
（macOS 的系统崩溃对话框正是 Reopen / Report 两按钮结构）

**安全警告（未签名应用、恶意软件、不受信任证书）**
说清楚具体的不受信任原因（未验证发布者 / 证书过期 / 域名不匹配），不要只说「有风险」；提供「仍要继续」和「返回安全」两个选择，默认焦点放在更安全的选项上；没有真实扫描结论时不要说「病毒」「恶意软件」。
- zh（对应 SmartScreen）：Windows 已保护你的电脑。Microsoft Defender SmartScreen 阻止了一个未被识别的应用启动，运行它可能会给电脑带来风险。
- en：Windows protected your PC. Microsoft Defender SmartScreen prevented an unrecognized app from starting. Running this app might put your PC at risk.（引自 SmartScreen 实际弹窗文案，经多个来源交叉确认）
- zh（证书）：此网站的证书不受信任，继续访问可能会泄露你的信息。
- en（对应 Chrome）：Your connection is not private. Attackers might be trying to steal your information from example.com (for example, passwords, messages, or credit cards).（Chrome 证书错误页实际文案，见 Chromium 源码字符串 `IDS_SSL_V2_HEADING` / `IDS_SSL_V2_PRIMARY_PARAGRAPH`：<https://github.com/chromium/chromium/blob/main/components/security_interstitials_strings.grdp>）

**数据丢失确认**
说清楚丢的是什么、影响范围、能不能撤回；按钮写动作而不是「确定」；关闭未保存文档要点出文档名。
- zh：「季度报告.docx」还有未保存的修改，是否保存？［保存］［不保存］［取消］
- en：Do you want to save the changes you made to "Quarterly Report.docx"? [Save] [Don't Save] [Cancel]（示意写法，不是逐字引用某个系统的原文）

**设置开关标签和说明**
标签是名词短语，不加句号；说明写「开启后会怎样」，用正向表述；一个开关只管一件事。
- zh：自动更新 / 有新版本时自动下载并安装，无需手动检查。
- en：Automatic Updates / Download and install new versions as soon as they're available.

**系统通知**
标题是事实，正文给下一步或说明不需要做什么；不堆感叹号；后台低优先级事件不要用和前台中断式通知一样的强度词。
- zh：电池电量过低 / 还剩 10%，接入电源以继续使用。
- en：Low Battery / 10% remaining. Connect to power to keep using your device.

**电池 / 性能**
给可感知的数字或时长，不给无法验证的「更省电」「更流畅」；性能模式切换要说明代价。
- zh：性能模式：风扇转速更高、噪音更大，换取更快的处理速度。
- en：Performance mode trades a louder fan for faster processing.

**快捷键记法**
Windows / Linux 用加号连接的大写缩写：Ctrl+Shift+S；macOS 用符号组合，顺序固定为 Control、Option、Shift、Command：⌃⌥⇧⌘。中文界面里快捷键本身不翻译，说明文字可以是中文（「按 Ctrl+Z 撤销」）。不要把 macOS 的符号用进 Windows 文案，或反过来。

**管理员密码 / 提权输入框**
要说明是谁在请求提权、要做什么操作，不能只显示一个应用图标和名字就弹密码框；标准用户没有管理员密码时，要给出能执行的下一步（联系管理员），不能卡在那里不说明原因。
- zh：「系统设置」想要进行更改。输入管理员密码以继续。
- en：System Preferences wants to make changes. Enter an administrator password to allow this.

**首次使用引导（开箱设置向导）**
按步骤给进度（第几步 / 共几步），用祈使句描述当前要做的事，不写产品介绍式的开场白；开机首次设置时语言包可能还没下载完，用词要尽量简单、少成语、少依赖上下文。
- zh：第 2 步，共 5 步：选择 Wi-Fi 网络
- en：Step 2 of 5: Choose a Wi-Fi network
- 反例：恭喜你即将开启不可思议的智能生活新篇章！（营销式开场白，和设置向导的功能性语境不符）

**表单校验（安装路径、磁盘选择）**
路径或盘符不可用时，说清楚具体原因（空间不够 / 没有写入权限 / 路径包含系统保留字符），不要只说「路径无效」；默认安装路径要提前显示出来，不要留空等用户填。
- zh：无法安装到此驱动器：剩余空间只有 1.1 GB，至少需要 4 GB。
- en：Can't install here: only 1.1 GB free, but 4 GB is required.

**状态标签（服务 / 驱动运行状态）**
服务和驱动的状态词要固定成一套，不能时而「运行中」时而「正在运行」；「出错」要和「已停止」分开——前者是非预期失败，后者是主动停止，给用户的下一步完全不同。
- zh：打印服务：运行中 / 已停止 / 已禁用 / 出错（点击查看详情）
- en：Print Spooler: Running / Stopped / Disabled / Error (click for details)

**帮助文档 / 系统说明**
比日常提示更偏参考资料的语气，允许更完整的句子和更高的信息密度，但仍要先给结论，不堆砌「首先…然后…最后…」这类说明书腔；指路径时写用户在界面上能实际看到的名字（菜单项、设置项），不要用「相关选项」这种指代不清的说法。
- zh：打开「设置」>「系统」>「存储」，查看各类文件占用的空间。
- en：Go to Settings > System > Storage to see how much space each type of file is using.

## 6. 合规和硬约束

没有统一的法规条款像金融、医疗那样逐条规定措辞，但有平台审核规则和行业惯例构成的硬约束：

- **必须出现的话**
  - 不可逆的系统级操作（格式化、重置系统、清除所有数据）前必须有二次确认，并明确说明能否撤销；格式化、擦除类操作的行业惯例是要求手动输入确认词（如「ERASE」/「清除」），而不是点一下按钮就完成。
  - 权限请求必须对应到具体会用到该权限的功能——这是平台审核的硬要求：App Store 审核指南 5.1.1(ii) 要求 purpose string「clearly and completely describe your use of the data」，5.1.1(iv) 要求尊重用户的权限设置、不得诱导或强迫用户同意不必要的数据访问（<https://developer.apple.com/app-store/review/guidelines/>）；Google Play 对敏感权限也有对应的使用说明政策。
  - UAC / 提权操作必须说明「谁」在请求、要做什么操作，不能只显示一个应用名了事。
- **不许出现的话**
  - 不能用「永久删除」描述实际进了回收站 / 废纸篓的操作；只有真正跳过回收站、不可恢复时才能说「永久删除，无法恢复」。
  - 崩溃报告、报错界面不能把用户个人信息（含用户名的文件路径、IP、设备序列号）直接显示在界面上，这些信息只能进日志或开发者可见的详情页。
  - 安全警告不能把「未签名」「未验证发布者」直接等同于「病毒」「恶意软件」——这是两个不同结论，没有实际恶意软件扫描结果支撑时不能用后者。
- **必须的格式**
  - 容量单位：面向用户显示的到底是十进制 GB（10⁹ 字节）还是二进制 GiB（2³⁰ 字节），要在产品内部保持一致。Windows 长期被诟病的「buy 500 GB 硬盘显示只有 465 GB」问题，根源正是驱动器按十进制 GB 标注、系统按二进制 GiB 计算却仍标「GB」（参见 <https://en.wikipedia.org/wiki/Gigabyte>）；新写文案时要明确团队用的是哪种换算，别在同一产品里切换。
  - 版本号格式跟随平台惯例：Windows 常见「主版本.次版本.修订号.内部版本号」，macOS 常见「主.次.修订」，不要自造格式。
  - 日期、时间格式跟随系统区域设置（locale），不要在文案里写死美式 `MM/DD/YYYY`。
  - **托盘图标提示文字长度**：Windows 通知区域图标的标准工具提示（`NOTIFYICONDATA.szTip`）最多 128 个字符（含结尾空字符），Windows 2000 之前为 64 个（<https://learn.microsoft.com/en-us/windows/win32/api/shellapi/ns-shellapi-notifyicondataw>）；超出部分写不进去，所以不要堆成一整句说明。
  - **本地化长度余量**：系统软件的按钮、标签、菜单项大多是短字符串，短字符串翻译后的膨胀比例比整段说明文字夸张得多——W3C 引用 IBM 的数据：英文 10 个字符以内的短串译成欧洲语言后，平均长度是原文的 200%–300%，70 个字符以上约为 130%；英文和中文都很紧凑，从这两种语言译出去通常会变长（<https://www.w3.org/International/articles/article-text-size>）。控件宽度要按「可能出现的最长语言」留余量，不要按中文或英文一种语言写死像素宽度，更不能在文案里用换行符手动对齐——翻译成别的语言后对齐方式会整个错位。

## 7. 高风险场景

**格式化 / 重置系统 / 清除所有数据**
必写：影响范围（哪块盘、哪台设备）、能否恢复、需要的确认动作。
- zh：将清除此设备上的所有数据和应用，且无法恢复。输入「清除」以确认。
- en：This will erase all data and apps on this device. This can't be undone. Type ERASE to confirm.

**权限过度索取**
必写：只申请当前功能需要的权限，精确对应触发场景，不要开屏就要齐所有权限——这既是写作问题也是平台审核会拒的问题。

**未签名 / 未受信任安装包运行**
必写：风险来源（未验证发布者，不是「有毒」）、查看详情的入口、默认选中更安全的选项。

**系统更新中断电**
必写：更新过程中不能关闭电源或拔掉电源线、预计时长。
- zh：正在安装更新，请勿关闭电源。预计还需 8 分钟。
- en：Installing updates. Don't turn off your PC. About 8 minutes left.

**驱动 / 内核态组件安装需要重启**
必写：何时生效（重启后）、重启前该功能不可用。

**磁盘分区操作（格式化分区、调整大小）**
必写：当前盘内容是否受影响，操作前是否已有备份提示；这是比普通文件删除更高一级的风险，确认框的分量要相应更重。

**远程擦除设备（查找设备 / 防丢工具）**
必写：触发条件（通常是设备下次联网时才执行）、擦除范围、能否取消、擦除后设备是否还能被定位。
- zh：擦除后，此设备上的所有内容和设置都将被删除，且无法恢复；操作会在设备下次联网时执行。
- en：Erasing this device will delete all content and settings. This can't be undone, and it will happen the next time the device is online.

**崩溃后自动保存 / 恢复文件**
必写：系统帮用户保留了什么、在哪能找回、保存的时间点；不要说「数据可能丢失」这种无法证实的模糊话——真做了自动保存就明确说恢复到了哪个时间点，没做到就别暗示有。
- zh：「设计稿.psd」已恢复到最后一次自动保存的状态（14:32）。
- en："Design.psd" has been recovered to its last autosaved state (2:32 PM).

## 8. 这个行业的 AI 腔和坏写法

| 坏写法 | 例子 | 改法 |
|---|---|---|
| 用「体验」代替具体功能 | 全新体验，让你的电脑更智能 | 说清楚具体改了什么 |
| 把技术原理当文案 | 我们采用了先进的沙箱隔离技术保护你的安全 | 只说用户关心的结果：此应用在隔离环境中运行，无法访问你的个人文件 |
| 滥用「检测到」却不说具体问题 | 检测到您的电脑可能存在风险 | 说清楚检测到的具体问题，不是泛泛的「可能」 |
| 把「未受信任」升级成恐吓 | 警告！警告！您的电脑可能已经感染病毒！！！ | 中性陈述事实和下一步，不堆标点和感叹号 |
| 营销词混进系统文案 | 尊享加速引擎，释放全部性能 | 删掉形容词，写实际效果和代价 |
| 把系统过度拟人化 | 小助手正在为您保驾护航 | 写系统实际在做什么：未发现安全问题 |
| 「可能」当免责声明滥用 | 此操作可能会、也可能不会影响您的数据 | 要么确定会要么确定不会，拿不准就先去确认清楚再写 |
| 编造虚假进度 | 正在为您优化，马上就好（其实不知道还要多久） | 没有真实进度就别编百分比和「马上」，只写「正在处理」 |
| 同义词轮换造成术语漂移 | 同一产品里「软件 / 程序 / 应用」换着用 | 固定一个词，参照第 4 节术语表 |
| 中英夹杂凑时髦 | enable 一下这个 feature 即可 | 用中文写完整 |
| 把英文系统提示直译但不说清楚问题 | 把 "Something went wrong" 直译成「出问题了」，不说哪里出了问题 | 按第 5 节的报错结构写具体问题 + 下一步 |
| 数字模糊化 | 占用了较多存储空间 | 给实际数字，例如「占用 3.2 GB」 |
| 把本地化截断当成没看见 | 按钮里的中文被「…」截断也不处理 | 给控件留翻译余量，或换成不会被截断的短词，参照第 6 节「本地化长度余量」 |
| 用昵称、语气词称呼用户 | 亲，您的存储空间不够啦～ | 系统软件不用昵称和语气词，按第 2 节语气规则来 |
| 把高风险操作说得轻飘飘 | 一键找回爱机，清空数据就像拍照一样简单 | 远程擦除这类不可逆操作不能用轻松口吻淡化后果，按第 7 节「高风险场景」写全必写要素 |

## 9. 改前 → 改后

| 改前 | 改后 | 问题 |
|---|---|---|
| 为了给您提供更好的服务，请允许我们获取您的全部权限 | 需要访问相机才能扫码，其他权限不会用到 | 要求过度权限 + 空话 |
| We need access to provide a better experience | Allow camera access to scan codes | 同上，英文版 |
| 警告：存储空间严重不足！！！ | 存储空间只剩 500 MB，建议清理后再继续 | 堆标点、没有具体数字和下一步 |
| Oops! Something went wrong. | Couldn't save the file. Check your storage space and try again. | 空洞、没有下一步 |
| 是否确定要卸载该软件？ | 卸载「XX 工具」后，它的设置和缓存会一并删除，已保存的文件不受影响 | 没说清范围和后果，按钮还是「确定 / 取消」套话 |
| Are you sure? | Uninstall XX Tool? Its settings and cache will be removed. Your saved files won't be affected. | 同上，英文版 |
| 检测到风险，是否继续？ | 此应用的发布者身份未经验证，运行可能存在风险 | 「检测到风险」模糊，没说风险来源 |
| This might be dangerous | This app is from an unidentified developer. | 同上，英文版 |
| 正在智能优化，请稍候… | 正在清理临时文件，预计还需 20 秒 | 「智能」是空话，没有具体动作和时长 |
| Optimizing your experience… | Clearing temporary files — about 20 seconds left | 同上，英文版 |
| 更新失败，请稍后重试（实际原因是存储空间不足） | 存储空间不足，无法完成更新。清理至少 2 GB 后重试 | 把能确诊的原因写成了含糊的「稍后重试」 |
| Update failed. Try again later. | Not enough storage to update. Free up at least 2 GB, then try again. | 同上，英文版 |
| 小助手已经为您保驾护航，系统很安全 | 未发现安全问题 | 拟人化 + 夸张 |
| Your little guardian has your back — all secure! | No issues found. | 同上，英文版 |
| 您的设备存储空间已满，建议您清理一下哦～ | 存储空间已满，清理文件后才能继续安装 | 昵称语气词 + 没给出「必须清理才能继续」这个硬前提 |
| Your device storage is full, maybe consider cleaning up~ | Storage is full. Free up space to continue installing. | 同上，英文版 |
| 路径无效，请重新选择 | 无法安装到此驱动器：剩余空间只有 1.1 GB，至少需要 4 GB | 没说清楚「无效」具体指什么原因 |
| Invalid path, please choose another | Can't install here: only 1.1 GB free, but 4 GB is required. | 同上，英文版 |

## 10. 审查时加查的项

- [ ] 危险 / 不可逆操作（格式化、清除数据、卸载驱动）是否都有二次确认，并写清了影响范围和能否撤销？
- [ ] 权限请求的说明是否对应到具体会用到该权限的功能，而不是笼统地要「全部权限」？
- [ ] 安全 / 证书警告是否说清楚了具体不受信任的原因，没有把「未签名」直接等同于「病毒」？
- [ ] 容量、时长类数字是否和实际进制（GB=10⁹ 还是 GiB=2³⁰）一致，同一产品里有没有混用？
- [ ] 需要重启才生效的操作，是否明确写了「需要重启」，而不是只说「已保存」？
- [ ] 崩溃 / 报错文案里有没有混进文件路径、用户名、堆栈、错误码这些只对开发者有意义的信息？
- [ ] 平台专属叫法有没有用混（回收站 / 废纸篓、任务管理器 / 活动监视器、任务栏 / 程序坞）？
- [ ] 快捷键记法是否跟对了平台（Windows / Linux 用 Ctrl+字母，macOS 用 ⌘ 等符号），没有两套记法混用？
- [ ] 短文案（按钮、标签、菜单项）有没有按最长语言留出宽度，翻译后会不会被截断或排版错位？
- [ ] 首次使用引导和系统帮助文档的语气，分别对应「按步骤完成任务」和「查参考资料」，而不是都写成营销介绍？

## 11. 台港市场差异

- 无特别规定，按 `locale-zh-hant.md` 换词。系统级文案以 Microsoft zh-TW / zh-HK 术语为准，Windows 的界面用词就是用户最熟的那套。
- 第 6 节提到的 App Store 和 Google Play 权限说明要求，在台港同样适用，平台规则不分地区。
- 个资：崩溃报告、诊断资料上传时，台湾适用《個人資料保護法》（蒐集时依第 8 条告知），香港适用《個人資料（私隱）條例》（Cap. 486），不是大陆《个人信息保护法》。

用词差异（`locale-zh-hant.md` 已有的 内存、硬盘、卸载、运行 等不再列）：

| 简体 | 台湾 | 香港 |
|---|---|---|
| 分辨率 | 解析度 | 解像度 |
| U 盘 | 隨身碟 | USB 手指（口语；界面写「USB 儲存裝置」） |
| 回收站 | 資源回收筒 | 資源回收筒 |
| 任务管理器 | 工作管理員 | 工作管理員 |
| 补丁 | 修補程式 | 修補程式 |
| 端口 | 連接埠 | 連接埠 |

（港栏以 Microsoft zh-HK 术语为准，未逐词核实）
