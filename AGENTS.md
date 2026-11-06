# ddddocr 服务说明

## 项目用途

这是一个独立的 Python HTTP 服务，使用 `ddddocr` 识别验证码图片，供 `jyj-auto` Go 容器调用。

## 文件结构

```text
app.py             HTTP 服务和验证码识别逻辑
requirements.txt   Python 依赖
Dockerfile         容器构建文件
.dockerignore      Docker 构建上下文排除规则
```

## 启动

本地启动：

```powershell
cd D:\DancingCodes\Codes\ym\ddddocr
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

服务监听 `9103`。

## Docker 部署

```bash
docker build -t ddddocr:latest .
docker compose up -d --force-recreate
```

`ddddocr` 和 `jyj-auto` 必须加入同一个 Docker 网络，例如 `jyj-net`。Go 服务通过 `http://ddddocr:9103` 调用本服务，其中 `ddddocr` 是容器名称。容器之间访问不依赖 `ports`；`ports` 仅用于宿主机或外部访问。

## 接口

- `GET /health`：成功返回 HTTP `200` 和 `ok`。
- `POST /recognize`：请求体为 `{"image":"Base64 图片"}`，成功返回 HTTP `200` 和 `{"text":"识别结果"}`。
- 请求路径错误、请求内容错误或识别失败：返回 HTTP `500`，响应体为中文纯文本错误信息。

服务只应在受信任的 Docker 网络或内网中运行，不要将 `9103` 直接暴露到公网。

## 开发约定

- 不在日志或响应中输出验证码原图、账号、密码或会话 token。
- 修改 Python 代码后运行：

```powershell
.\.venv\Scripts\python.exe -m py_compile app.py
```
