# 필요 모듈
    pip install
- flask
- requests
- bs4
- selenium
- image
- opencv-python
- tensorflow
- scikit-learn

# API
1. '/image/analyze', [POST]

    요청 변수
    
    |요청 변수명|타입|필수 여부|기본값|설명|
    |:------:|:---:|:---:|:---:|:---:|
    |files|files|O|없음|파일들 업로드|
    <br />
    
    출력 결과
    
    |필드|타입|설명|
    |:------:|:---:|:---:|
    |status|string|분석 성공 여부|
    |analysis_result|array[result]|이미지들의 색상 분석 결과|
    
    Object: result
    
    |필드|타입|설명|
    |:------:|:---:|:---:|
    |src|string|이미지의 소스 url|
    |colors|array[{hex, ratio}]|색상의 hex값과 비율값의 배열|
    <br />

2. '/url', [POST]
    
    요청 변수
    
    |요청 변수명|타입|필수 여부|기본값|설명|
    |:------:|:---:|:---:|:---:|:---:|
    |url|string|O|없음|스크랩하고 싶은 url 주소를 입력
    |width|string/int|X|100|스크랩할 이미지의 최소 width
    |height|string/int|X|100|스크랩할 이미지의 최소 height
    <br />

    출력 결과
    
    |필드|타입|설명|
    |:------:|:---:|:---:|
    |status|string|스크랩 성공했는지 여부|
    |src_list|array[string]|이미지들의 소스 url|
    <br />
    
3. '/url/analyze', [POST]

    요청 변수
    
    |요청 변수명|타입|필수 여부|기본값|설명|
    |:------:|:---:|:---:|:---:|:---:|
    |src_list|JSON string|O|없음|분석하고 싶은 이미지 소스 배열을 json.stringify한 문자열을 입력|
    <br />
    
    출력 결과
    
    |필드|타입|설명|
    |:------:|:---:|:---:|
    |status|string|분석 성공 여부|
    |analysis_result|array[result]|이미지들의 색상 분석 결과|
    
    Object: result
    
    |필드|타입|설명|
    |:------:|:---:|:---:|
    |src|string|이미지의 소스 url|
    |colors|array[{hex, ratio}]|색상의 hex값과 비율값의 배열|
    <br />
    