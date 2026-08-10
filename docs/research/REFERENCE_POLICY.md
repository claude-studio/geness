# External Reference and Reuse Policy

> 상태: Accepted documentation policy

## 1. 목적

외부 프로젝트를 참고한 사실, Geness가 채택한 결정과 실제 저작물 재사용을 구분한다.
출처 링크 하나만 남기거나, 반대로 아이디어 연구를 코드 복사처럼 표현하는 오류를
피한다.

## 2. 세 가지 수준

### Observation

원본의 동작과 구조를 읽고 사실을 기록한다. 저장소, 고정 commit, 파일 permalink,
조사일과 라이선스를 남긴다.

### Design influence

관찰한 원칙을 Geness 계약에 맞게 독립적으로 재설계한다. Research에서
adopted/modified/not-adopted를 나누고, consequential decision은 ADR로 승격한다.

### Expression reuse

코드, 프롬프트, template 또는 문서 문구를 복사·번안한다. 원본 라이선스가 요구하는
고지를 보존하고 재사용 원장에 로컬 파일, 원본 permalink, 수정 여부와 배포 조치를
기록한다.

## 3. 필수 기록

- 움직이는 branch 대신 고정 commit을 기본 링크로 사용한다.
- 원본 저자와 저장소, 라이선스를 표시한다.
- Geness가 채택한 것과 채택하지 않은 것을 함께 적는다.
- 원본과 호환 구현인지, 독립 설계인지 명확히 밝힌다.
- 실제 표현물 재사용이 시작되는 변경에는 라이선스 파일과 배포 검증을 함께 둔다.
- 외부 프로젝트가 Geness를 제휴·보증한다고 암시하지 않는다.

## 4. 검토 Gate

다음 중 하나면 변경을 merge하기 전에 출처·라이선스 검토가 필요하다.

- 외부 파일의 코드나 문구를 붙여 넣거나 번안했다.
- 외부 schema, fixture 또는 template을 실질적으로 재현했다.
- 외부 project name, logo 또는 trademark를 제품 표면에 사용한다.
- 배포 artifact에 제3자 코드가 포함된다.
- 기존 Research의 `현재 재사용 상태`가 더 이상 사실이 아니다.
