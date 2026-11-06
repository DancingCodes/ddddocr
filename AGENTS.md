# ddddocr 服务说明

## 项目用途

这是一个独立的 Python HTTP 服务，使用 `ddddocr` 识别验证码图片，供 `jyj-auto` Go 服务在本机调用。

## 文件结构

```text
app.py             HTTP 服务和验证码识别逻辑
requirements.txt   Python 依赖
Dockerfile         容器构建文件
```

## 启动

本地启动：

```powershell
cd D:\DancingCodes\Codes\ym\ddddocr
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

服务监听 `9103`。

## 接口

- `GET /health`：成功返回 HTTP `200` 和 `ok`。
- `POST /recognize`：请求体为 `{"image":"Base64 图片"}`，成功返回 HTTP `200` 和 `{"text":"识别结果"}`。
- 请求路径错误、请求内容错误或识别失败：返回 HTTP `500`，响应体为中文纯文本错误信息。

服务只应在本机或受信任的内网中运行，不要将 `9103` 直接暴露到公网。

## 开发约定

- 不在日志或响应中输出验证码原图、账号、密码或会话 token。
- 修改 Python 代码后运行：

```powershell
.\.venv\Scripts\python.exe -m py_compile app.py
```
