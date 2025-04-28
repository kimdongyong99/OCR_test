vimport pytesseract
from PIL import Image
import re
import os

# Tesseract 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 정규 표현식 패턴
PATTERNS = {
    "주민등록번호": r'\d{6}-([1-4]\d{6}|\*{7}|[1-4]\*{6}|[1-4]\d{1}\*{5}|[1-4]\d{2}\*{4}|[1-4]\d{3}\*{3}|[1-4]\d{4}\*{2}|[1-4]\d{5}\*{1})',
    "전화번호": r'\b(?:010|011|016|017|018|019)-\d{3,4}-\d{4}\b',
    "계좌번호": r'\b\d{2,3}-\d{3,6}-\d{4,6}\b',
    "신용카드 번호": r'\b(?:\d{4}[- ]?){3}\d{4}\b',
    "이메일 주소": r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
    "이름": r'[가-힣]{2,4}\s?[가-힣]{1,4}',
    "사업자등록번호": r'\b\d{3}-\d{2}-\d{5}\b',
    "세금 관련 번호": r'\b\d{3}-\d{2}-\d{6,10}\b',
    "웹사이트 주소": r'https?://[a-zA-Z0-9./?=&_-]+',
    "고유 식별자": r'\b(?:USR|EMP)-\d{4,6}\b',
    "IP 주소": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
    "MAC 주소": r'\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b',
    "차량 번호판": r'\b[가-힣]{1,2}\s?\d{1,4}\s?[가-힣]\s?\d{4}\b',
    "커스텀 필터": r'\b(?:내부문서-\d{4}|보안등급:\s?[가-힣]+)\b',
    "금액 정보": r'(₩\s?\d[\d,]*(\.\d+)?|\d{1,3}(?:,\d{3})+\b)'
}

IMAGE_FOLDER = "./image"

def extract_sensitive_data_from_image(image_path):
    img = Image.open(image_path)
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    results = []
    checked_indices = set()

    for i in range(len(data['text'])):
        word = data['text'][i].strip()
        if not word or i in checked_indices:
            continue

        # 현재 단어 + 다음 단어 조합도 검사
        if i + 1 < len(data['text']):
            next_word = data['text'][i + 1].strip()
            combined = f"{word}{next_word}"

            # 주민등록번호 패턴 검사
            pattern = PATTERNS["주민등록번호"]
            if re.fullmatch(pattern, combined):
                x1, y1 = data['left'][i], data['top'][i]
                x2 = data['left'][i + 1] + data['width'][i + 1]
                y2 = max(data['top'][i], data['top'][i + 1]) + max(data['height'][i], data['height'][i + 1])
                width = x2 - x1
                height = y2 - y1

                results.append({
                    "label": "주민등록번호",
                    "text": combined,
                    "x1": x1, "y1": y1,
                    "x2": x2, "y2": y2,
                    "width": width,
                    "height": height
                })

                checked_indices.update([i, i + 1])
                continue  # skip to next word

        # 단일 단어 검사
        for label, pattern in PATTERNS.items():
            if label == "주민등록번호":
                continue  # 주민번호는 이미 위에서 따로 처리

            if re.fullmatch(pattern, word):
                x1, y1 = data['left'][i], data['top'][i]
                width, height = data['width'][i], data['height'][i]
                x2, y2 = x1 + width, y1 + height

                results.append({
                    "label": label,
                    "text": word,
                    "x1": x1, "y1": y1,
                    "x2": x2, "y2": y2,
                    "width": width,
                    "height": height
                })

                checked_indices.add(i)
                break

    return results
def process_images_in_folder(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg'))]

    if not image_files:
        print(f"❗ '{folder_path}' 폴더에 이미지 파일이 없습니다.")
        return

    for image_file in image_files:
        full_path = os.path.join(folder_path, image_file)
        results = extract_sensitive_data_from_image(full_path)

        print(f"\n📂 [파일]: {image_file}")
        if results:
            for r in results:
                coord_info = f"→ 좌표: (x1={r['x1']}, y1={r['y1']}, x2={r['x2']}, y2={r['y2']}, w={r['width']}, h={r['height']})" if r['x1'] is not None else "(🔍 위치 정보 없음)"
                print(f"[{r['label']}] {r['text']} {coord_info}")
        else:
            print("🔍 탐지된 개인정보 없음.")

# 실행
if __name__ == "__main__":
    process_images_in_folder(IMAGE_FOLDER)

