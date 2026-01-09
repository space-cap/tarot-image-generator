
import os
import time
import json
import base64
import requests
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# ---------------------------------------------------------
# 설정 (Configuration)
# ---------------------------------------------------------
# Google AI Studio(aistudio.google.com)에서 무료 티어 키를 받아서 사용 가능합니다.
# .env 파일에 GEMINI_API_KEY="your_key" 형태로 저장하세요.
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY or API_KEY == "YOUR_GEMINI_API_KEY":
    print("[ERROR] API_KEY가 설정되지 않았습니다. .env 파일에 GEMINI_API_KEY를 설정해주세요.")
    print("참고: .env.example 파일을 .env로 복사하여 사용할 수 있습니다.")
    exit(1)

# 이미지가 저장될 디렉토리
OUTPUT_DIR = "assets/cards"

# 사용할 모델 (Nano Banana = gemini-2.5-flash-image-preview)
MODEL_NAME = "gemini-2.5-flash-image-preview"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"

# 공통 프롬프트 스타일 (전체적인 톤앤매너)
COMMON_STYLE = (
    "Tarot card design, mystical and spiritual atmosphere, "
    "highly detailed, 8k resolution, cinematic lighting, "
    "art nouveau style mixed with modern fantasy, "
    "vibrant colors, golden ratio composition, "
    "full card illustration without text borders."
)

# ---------------------------------------------------------
# 함수 정의
# ---------------------------------------------------------

def generate_image_with_retry(prompt, filename, max_retries=5):
    """
    Gemini API를 호출하여 이미지를 생성하고 저장합니다.
    무료 티어의 Rate Limit(429 에러) 발생 시 자동으로 대기 후 재시도합니다.
    """
    
    full_prompt = f"{COMMON_STYLE}, {prompt}"
    
    payload = {
        "contents": [{
            "parts": [{"text": full_prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "temperature": 0.9 
        }
    }

    retry_count = 0
    while retry_count < max_retries:
        try:
            print(f"Generating: {filename} (Attempt {retry_count + 1})...")
            response = requests.post(API_URL, json=payload)
            
            # 429 Too Many Requests (무료 티어 한도 초과 시) 처리
            if response.status_code == 429:
                wait_time = 30 * (retry_count + 1) # 점진적으로 대기 시간 증가 (30초, 60초...)
                print(f"⚠️ Quota limit reached. Waiting for {wait_time} seconds...")
                time.sleep(wait_time)
                retry_count += 1
                continue
                
            response.raise_for_status()
            
            result = response.json()
            
            candidates = result.get('candidates', [])
            if not candidates:
                print(f"Error: No candidates returned for {filename}")
                return

            parts = candidates[0].get('content', {}).get('parts', [])
            image_data = None
            
            for part in parts:
                if 'inlineData' in part:
                    image_data = part['inlineData']['data']
                    break
            
            if image_data:
                img_bytes = base64.b64decode(image_data)
                filepath = os.path.join(OUTPUT_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(img_bytes)
                print(f"✅ Saved: {filepath}")
                return # 성공 시 함수 종료
            else:
                print(f"⚠️ Failed to find image data for {filename}")
                return

        except Exception as e:
            print(f"❌ Error generating {filename}: {str(e)}")
            return # 기타 에러 시 중단

    print(f"❌ Failed to generate {filename} after {max_retries} retries.")

def main():
    # 저장 폴더 생성
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 프롬프트 데이터 로드
    try:
        with open('tarot_prompts.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: 'tarot_prompts.json' file not found.")
        return

    # 1. 메이저 아르카나 생성 (22장)
    print("--- Generating Major Arcana (22 cards) ---")
    for card_id, prompt_desc in data['major_arcana'].items():
        filename = f"major_{card_id}.png"
        generate_image_with_retry(prompt_desc, filename)
        time.sleep(2) # 기본 쿨다운

    # 2. 마이너 아르카나 생성 (56장)
    print("\n--- Generating Minor Arcana (56 cards) ---")
    suits = data['minor_arcana']['suits']
    ranks = data['minor_arcana']['ranks']

    for suit, suit_desc in suits.items():
        for rank, rank_desc in ranks.items():
            prompt = f"{suit} suit card, {rank}, {suit_desc}, {rank_desc}"
            filename = f"minor_{suit}_{rank}.png"
            generate_image_with_retry(prompt, filename)
            time.sleep(4) # 마이너 카드는 장수가 많으므로 쿨다운을 조금 더 둠 (무료 티어 보호)

    print("\n🎉 All processes finished!")

if __name__ == "__main__":
    main()