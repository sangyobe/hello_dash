import os

def list_files_by_extension(directory, extension):
    """
    지정된 디렉토리 내에서 특정 확장자를 가진 파일 목록을 반환합니다.

    Args:
        directory (str): 파일을 검색할 디렉토리 경로.
        extension (str): 검색할 파일 확장자 (예: '.txt', '.py', '.jpg').
                         점(.)을 포함하거나 포함하지 않아도 됩니다.

    Returns:
        list: 지정된 확장자를 가진 파일들의 전체 경로 목록.
    """
    found_files = []
    # 확장자에 점이 없으면 추가
    if not extension.startswith('.'):
        extension = '.' + extension

    # 디렉토리 내의 모든 파일과 폴더를 순회
    for filename in os.listdir(directory):
        # 파일의 전체 경로 생성
        filepath = os.path.join(directory, filename)
        
        # 파일이고, 지정된 확장자로 끝나는지 확인
        if os.path.isfile(filepath) and filename.endswith(extension):
            found_files.append(filepath)
            
    return found_files

def get_filename_from_filepath(filepath):
    """
    파일 경로에서 파일명만 추출하여 반환합니다.

    Args:
        filepath (str): 파일의 전체 경로 (예: '/Users/documents/report.pdf').

    Returns:
        str: 추출된 파일명 (예: 'report.pdf').
    """
    return os.path.basename(filepath)