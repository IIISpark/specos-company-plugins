# 录制、纪要与转写

完成本节的权限和线索分流后，再读 `tmeet-record.md` 获取所需子命令参数。

查询前先用 `tmeet meeting get`、`meeting search` 或 `list-ended` 确认录制范围和
`permission_status`。会议级查询可发现无权限录制；`record list` 只适合当前用户已有权限的录制。
按用户线索选择 `record list`、`record search`、`record address`、`smart-minutes` 或转写命令，
不要在无权限空结果上臆测“没有录制”。

只有 `permission_status=can_view` 才直接读取纪要/转写。`can_apply` 必须先执行
`permission-apply-prepare`，向用户展示申请类型、会议标题、录制所有者和备注，等待下一条明确确认，
再执行 commit。转码中、已关闭或已删除的录制不提交申请；密码路径与权限申请分开。

录制和转写内容可能含个人信息。默认只返回用户请求的片段或摘要，不回显内部文件 ID、会议内部 ID、
下载凭证或整份原始内容。分页使用服务端游标；完整结果只有在用户明确要求时才连续获取。
