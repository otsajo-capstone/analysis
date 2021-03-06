# 이 저장소는...
2020학년도 2학기 중앙대학교 소프트웨어학부 캡스톤디자인 OTSAJO 팀 프로젝트의 이미지 분석 파트의 코드와 API 문서를 포함하고 있습니다.<br />
1. 분석하고 싶은 옷이 포함된 링크나, 옷 사진을 직접 업로드하면 이미지에서 옷을 분리해냅니다. (Thanks to anish9/Fashion-AI-segmentation)
2. 옷 이미지의 색공간을 BGRA에서 CIE-La\*b\*공간으로 변경하고 KMeans Clustering 알고리즘을 수행해 대표색 세 가지를 추출합니다.
3. 준비된 퍼스널 컬러 팔레트를 이용해 대표색에 어올리는 타입을 추천합니다.

# 필요 모듈 설치
    pip install -r requirements.txt

or

    pip install
- flask
- requests
- bs4
- selenium
- image
- scikit-build
- scikit-learn
- opencv-python
- opencv-contrib-python
- tensorflow==2.2.0
- tensorflow-gpu==2.2.0
- flask_cors
- colormath

# API
1. '/image', [GET]
    - 서버에 저장된 이미지 파일 소스
    
    - 요청 변수 (Query String 형식)
    
        |요청 변수명|타입|필수 여부|기본값|설명|
        |:------:|:---:|:---:|:---:|:---:|
        |filename|string|O|없음|파일이름|
    
    - 출력 결과
    
        이미지<br /><br />

2. '/image/analyze', [POST]
    - 이미지(하나 혹은 다수) 파일들을 업로드하면 각각의 색상 분석 결과와 퍼스널 컬러 타입 추천 결과 리턴

    - 요청 변수 (Body 형식)
    
        |요청 변수명|타입|필수 여부|기본값|설명|
        |:------:|:---:|:---:|:---:|:---:|
        |files|files|O|없음|파일들 업로드|
    
    - 출력 결과
    
        |필드|타입|설명|
        |:------:|:---:|:---:|
        |status|string|분석 성공 여부|
        |analysis_result|array(result)|이미지들의 색상, 타입 분석 결과|
    
    - Object: result
    
        |필드|타입|설명|
        |:------:|:---:|:---:|
        |name|string|이미지 파일이름|
        |src|string|이미지의 소스 url|
        |colors|array({hex, ratio, type, subtype})|색의 hex값과 비율, 타입의 배열|
        |result|array({ratio, type})|퍼스널 컬러 타입과 비율의 배열|
        <br />

3. '/url', [POST]
    - 스크랩할 링크를 받으면 이미지 링크들을 리턴
    
    - 요청 변수 (Body 형식)
    
        |요청 변수명|타입|필수 여부|기본값|설명|
        |:------:|:---:|:---:|:---:|:---:|
        |url|string|O|없음|스크랩하고 싶은 url 주소를 입력
        |width|string/int|X|100|스크랩할 이미지의 최소 width
        |height|string/int|X|100|스크랩할 이미지의 최소 height

    - 출력 결과
    
        |필드|타입|설명|
        |:------:|:---:|:---:|
        |status|string|스크랩 성공했는지 여부|
        |src_list|array(string)|이미지들의 소스 url|
        <br />
    
4. '/url/analyze', [POST]
    - 분석할 이미지 링크들을 받으면 각각의 색상 분석 결과와 퍼스널 컬러 타입 추천 결과 리턴

    - 요청 변수 (Body 형식, header='application/json')
    
        |요청 변수명|타입|필수 여부|기본값|설명|
        |:------:|:---:|:---:|:---:|:---:|
        |src_list|array(string)|O|없음|분석하고 싶은 이미지 소스 배열을 입력|
    
    - 출력 결과
    
        |필드|타입|설명|
        |:------:|:---:|:---:|
        |status|string|분석 성공 여부|
        |analysis_result|array(result)|이미지들의 색상, 타입 분석 결과|
    
    - Object: result
    
        |필드|타입|설명|
        |:------:|:---:|:---:|
        |name|string|이미지 파일이름|
        |src|string|이미지의 소스 url|
        |colors|array({hex, ratio, type, subtype})|색의 hex값과 비율, 타입의 배열|
        |result|array({ratio, type})|퍼스널 컬러 타입과 비율의 배열|
        <br />
    