# [SRS] 요구사항명세서

1. **소개 (Introduction)**
    1. **목적 (Purpose)**
        - 딥러닝 영상 처리 기반의 손쉬운 자가 진단 서비스를 제공하여 뇌졸중 환자의 신속한 발견을 목표로 한다.
2. **전체 설명 (Overall Description)**
    1. **제품 조망 (Product Perspective)**
        - 제품의 구성과 유래
    2. **제품 기능 (Product Features)**
        - 제품이 가지고 있는 주요 기능 또는 제품이 수행하는 중요한 기능 나열
    3. **사용자 계층과 특징 (User Classes and Characteristic)**
        - 일반인, 뇌졸중 의심 환자, 의사 등 전문 지식이 있는 자
    4. **운영 환경 (Operation Environment)**
        - HTML5, CSS3 이상을 지원하는 Web Browser
    5. **설계 및 구현 제약사항 (Desing and Implementation Constraint)**
        - 개발자가 선택할 수 있는 사항을 제약하는 모든 요소와 제약 조건의 이유
            - pycharm, flask, github, python3.8 (3.9부터는 지원하지 않는 모듈이 많음)
            - 사용의 표준이 될 웹 브라우저는 Chrome Browser
            - Mac Air M1으로 개발하였음.
    6. **사용자 문서 (User Documentation)**
        - 사용자 매뉴얼, 온라인 도움말, 교재 등 소프트웨어와 함께 제공할 사용자 문서
3. **외부 인터페이스 요구사항 (External Interface Requirment)**
    1. **사용자 인터페이스 (User Interface)**
        - 각각의 사용자 인터페이스의 논리적 특징 설명
        - 폰트, 아이콘, 버튼 레이블, 이미지, 색상 체계, 필드탭 순서 등
        - 화면 레이아웃 또는 해상도 제약 조건
        - 도움말 버튼과 같이 모든 화면에 나타나는 표준 버튼, 기능 또는 탐색 링크
        - 단축키
        - 메시지 표시 규칙
        - 소프트웨어 번역을 원할하게 하는 레이아웃 표준
        - 시각장애자를 위한 기능
    2. **하드웨어 인터페이스 (Hardware Interface)**
        - 지원되는 장비 유형, 소프트웨어와 하드웨어간의 데이터와 컨트롤 연동, 사용될 통신 프로토콜 등이 포함
    3. **소프트웨어 인터페이스 (Software Interface)**
        - 소프트웨어 컴포넌트 (데이터베이스, 운영체제, 툴, 라이브러릴, 통합 상업용 컴포넌트) 간의 연결을 설명
        - 컴포넌트 간 교환되는 메시지, 데이터와 컨트롤 항목 설명
        - 외부 소프트웨어 컴포넌트가 요구하는 서비스와 컴포넌트 간 통신 성격을 설명하고 소프트웨어 컴포넌트들이 공유할 데이터를 파악
    4. **통신 인터페이스 (Communications Interface)**
        - 이메일, 웹 브라우저, 네트워크 통신 프로토콜, 전자 문서와 같이 제품이 사용할 모든 통신 기능에 대한 요구사항을 설명
        - 관련된 모든 메시지 형태를 정의하고 통신 보안 또는 암호화 문제, 데이터 전송률과 동기화 메커니즘을 명시
4. **기능 이외의 다른 요구사항 (Other Nonfunctional Requirment)**
    1. **성능 요구사항 (Performance Requirment)**
        - 다양한 시스템 운영에 대한 특정 성능 요구 사항을 설명
    2. **안전 요구사항 (Safety Requirement)**
        - 반드시 방지해야 하는 잠재적으로 위험한 행동 뿐만 아니라 반드시 취해야 할 모든 안전장치 또는 행동을 정의
        - 제품이 따라야 하는 보안 인증, 정책 또는 규제를 정의
    3. **보안 요구사항 (Security Requirement)**
        - 제품 사용에 영향을 미치는 보안, 무결성 또는 사생활 문제, 제품이 사용하거나 만드는 데이터를 모두 명시한다.
        - 보안 요구사항은 일반적으로 비지니스 규칙에서 만들어지기 때문에, 제품이 준수해야 하는 모든 보안, 사생활 정책 또는 규제를 모두 명시
        - 이것 대신에, 무결성이라고 부르는 품질 특성을 통해 이 요구사항들을 해결할 수 있다.
5. **다른 요구사항 (Other Requirement)**
    1. SRS의 다른 부분에서는 다루지 않는 모든 요구 사항을 정의