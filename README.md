# Dummy MCP Server

이 프로젝트는 `FastMCP` 프레임워크를 사용하여 구축된 간단한 MCP (Meta-agent Communication Protocol) 서버입니다. 서버는 SSE (Server-Sent Events)를 통해 통신하며, `echo` 도구와 `dummy` 도구를 제공합니다.

## 주요 기술 스택

*   **FastAPI**: 웹 프레임워크 (FastMCP의 기반)
*   **Uvicorn**: ASGI 서버 (FastAPI 애플리케이션 실행)
*   **FastMCP**: MCP 서버 구축을 위한 프레임워크 (버전 1.0.0)
*   **Docker & Docker Compose**: 컨테이너화 및 서비스 관리
*   **Python**: 주 개발 언어

## 프로젝트 구조

```
.dummy_mcp_server/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI 애플리케이션 및 MCP 서버 설정, 도구 등록
│   └── tools/
│       ├── __init__.py
│       ├── dummy.py    # 'dummy' 도구 구현
│       └── echo.py     # 'echo' 도구 구현
├── docker-compose.yml  # Docker Compose 설정 파일
├── README.md           # 이 파일
└── requirements.txt    # Python 의존성 목록`
```

## 설정 및 실행

### 요구 사항

*   Docker
*   Docker Compose

### 로컬 실행 (Docker Compose 사용)

1.  **저장소 클론** (이미 로컬에 있는 경우 생략)

2.  **Docker 이미지 빌드 및 컨테이너 실행**:
    프로젝트 루트 디렉토리에서 다음 명령을 실행합니다. 이 명령은 필요시 이미지를 빌드하고 백그라운드에서 컨테이너를 시작합니다.
    ```bash
    docker-compose up --build -d
    ```
    서버는 Docker 컨테이너 내부의 `0.0.0.0:8002`에서 실행되며, `docker-compose.yml` 설정에 따라 호스트 머신의 `http://localhost:8002` (또는 Docker 호스트 IP의 8002 포트)로 노출됩니다.

3.  **로그 확인**:\
    ```bash
    docker-compose logs -f dummy_mcp_server
    ```

4.  **서버 중지**:\
    ```bash
    docker-compose down
    ```

### n8n 연동 가이드

`dummy-mcp-server`를 n8n 워크플로우와 연동하려면 다음 단계를 따르십시오.

1.  **Docker 네트워크**:
    *   `dummy-mcp-server` 컨테이너와 n8n 컨테이너가 동일한 Docker 네트워크 환경에서 실행되고 있어야 서로 통신할 수 있습니다.
    *   현재 `docker-compose.yml`은 `dummy-mcp-server` 서비스를 생성하며, 별도의 네트워크를 명시하지 않으면 Docker Compose가 생성하는 기본 네트워크에 연결됩니다. n8n 컨테이너도 이 네트워크에 연결되어 있거나, 또는 두 컨테이너가 공유하는 외부 네트워크(예: `nginx-n8n-net`)에 함께 연결되어 있어야 합니다.
    *   만약 n8n과 `dummy-mcp-server`가 동일한 `docker-compose.yml` 파일 내에서 서비스로 정의되어 있다면, Docker Compose가 자동으로 같은 네트워크에 배치하므로 서비스 이름(컨테이너 이름)으로 서로를 찾을 수 있습니다.

2.  **n8n MCP Client 노드 설정**:
    *   n8n 워크플로우에서 "MCP Client" 노드를 추가합니다.
    *   **SSE Endpoint**: 다음 URL을 입력합니다.
        ```
        http://dummy-mcp-server:8002/sse
        ```
        *   `dummy-mcp-server`: `docker-compose.yml`에 정의된 서비스 이름입니다. Docker 내부 DNS가 이 이름을 `dummy-mcp-server` 컨테이너의 IP로 해석합니다. (만약 n8n이 Docker 외부에서 실행되고 `dummy-mcp-server`만 Docker로 실행 중이라면, `localhost` 또는 Docker 호스트의 IP를 사용해야 합니다: `http://localhost:8002/sse`)
        *   `8002`: `dummy-mcp-server`가 리스닝하는 포트입니다.
        *   `/sse`: `FastMCP` 라이브러리가 SSE 스트림을 위해 사용하는 기본 경로입니다.
    *   **Authentication**: 현재 `dummy-mcp-server`는 인증을 사용하지 않으므로 "None"으로 설정합니다.
    *   **Tools to Include**: "All"로 설정하거나 필요에 따라 특정 도구만 선택할 수 있습니다.

### Python 의존성 (`requirements.txt`)

다음은 주요 의존성 목록입니다 (전체 목록은 `requirements.txt` 파일 참조):
```
fastmcp==1.0.0
httpx>=0.27.0
uvicorn
numpy
fastapi==0.109.2
# python-dotenv (주석 처리됨)
# ... 기타 mcp 및 fastapi 의존성
```

## 제공되는 도구

서버는 `app/main.py`에 다음과 같은 두 가지 도구를 등록하여 제공합니다.

1.  **`dummy` 도구**
    *   **소스 파일**: `app/tools/dummy.py`
    *   **설명**: 입력받은 문자열 메시지를 콘솔에 출력하고, 성공 상태와 함께 수신한 메시지를 반환하는 간단한 동기 도구입니다.
    *   **입력 파라미터**:
        *   `message` (str): 더미 도구가 받을 문자열입니다.
    *   **반환**: `{\"status\": \"success\", \"tool_message\": \"Dummy tool received: [입력된 메시지]\"}`

2.  **`echo` 도구**
    *   **소스 파일**: `app/tools/echo.py`
    *   **설명**: SSE 스트리밍 기능을 시연하는 예제 도구입니다. 입력된 메시지를 3회 반복하고, 각 메시지 사이에 1초의 지연을 두어 SSE 스트림으로 반환합니다.
    *   **입력 파라미터**:
        *   `message` (str): 에코할 문자열입니다.
    *   **반환**: 스트리밍 응답 후 `{\"status\": \"Echo stream completed\"}`를 반환합니다.


## MCP 서버 정보

*   **이름**: Dummy MCP Server
*   **설명**: FastMCP 1.0.0 with SSE, echo tool, and dummy tool.
*   **호스트**: `0.0.0.0` (Docker 컨테이너 내부)
*   **포트**: `8002` (Docker 외부 및 내부 동일 포트 매핑)
*   **통신 방식**: SSE (Server-Sent Events) - 기본 엔드포인트 `/sse` 사용. 