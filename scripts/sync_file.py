import os
import sys


def sync(files: list[str]):
    """변경 사항을 감지하고 동기화 수행"""

    # 1. 모든 파일의 내용과 수정 시간 읽기
    file_info = []
    try:
        for f in files:
            mtime = os.path.getmtime(f)
            with open(f, "rb") as fp:
                content = fp.read()
            file_info.append({"name": f, "mtime": mtime, "content": content})
    except OSError as e:
        print(f"[Error] 파일 접근 실패: {e}")
        sys.exit(1)

    # 2. 수정 시간 오름차순 정렬 (가장 오래된 파일이 0번 인덱스)
    # 논리: 가장 오래된 파일은 '수정되지 않은 원본' 상태로 간주
    file_info.sort(key=lambda x: x["mtime"])

    base_content = file_info[0]["content"]
    changed_list = []

    # 3. 기준(가장 오래된 파일)과 내용이 다른 파일 찾기
    for info in file_info:
        if info["content"] != base_content:
            changed_list.append(info)

    # 4. 조건 처리
    # 변경 사항이 없을 경우
    if len(changed_list) == 0:
        print(f"[*] 변경 사항이 없습니다.")
        return

    # 변경된 파일이 2개 이상일 경우 -> 에러 발생
    if len(changed_list) > 1:
        names = [x["name"] for x in changed_list]
        msg = f"[Critical Error] 2개 이상의 파일이 동시에 수정되었습니다 (기준 파일 불일치): {names}"
        raise Exception(msg)

    # 변경된 파일이 딱 1개일 경우 -> 동기화 로직 수행
    src_info = changed_list[0]
    src_file = src_info["name"]
    changed_content = src_info["content"]

    try:
        # 다른 파일들에 쓰기
        for target in files:
            if target == src_file:
                continue
            with open(target, "wb") as f_dst:
                f_dst.write(changed_content)
            print(f"    -> {target} 업데이트 완료")
    except Exception as e:
        print(f"[Error] 동기화 중 오류 발생: {e}")

    # --- 수정된 로직 끝 ---


if __name__ == "__main__":
    TARGET_FILES = ["GEMINI.md", "CLAUDE.md", "AGENTS.md"]
    sync(TARGET_FILES)
