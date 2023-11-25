import openai
import time

openai.api_key = "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"

default = "Extract price, service, taste, atmosphere keywords form the following reviews.\n"
# str2 = "점심시간에 오기 좋은 이대인도음식 맛집이에요! 런치세트 메뉴의 가성비가 미쳤기 때문 .. ㅎㅎ"
# str3 = "저는 2인 아건세트로 먹었는데 구성이 알차서 좋았어요 ㅎㅎ 커리는 “치킨티카마살라“ 난은 ”갈릭난“ 음료는 ”망고라씨“로 골랐는데 다 실패없었어요 🧡 "
# str4 = "난은 플레인난으로 리필이 가능하다는 것도 너무 좋았어요 플레인난도 담백해서 정말 맛있더라구요 😌😌"
# str5 = "직원분들도 너무 친절하고 플레이팅이랑 매장 인테리어도 예쁘고!! 너무 좋았습니다 ㅎㅎ"
# str = str1 + str2 + str3 + str4 + str5
index = [7, 9, 7, 12]
retry_time = 10

def getKW(review):
    content = default + review
    while True:
        try:
            response = openai.ChatCompletion.create(
                model="ft:gpt-3.5-turbo-1106:personal::8Mds7N5n",
                temperature=0,
                max_tokens=2048,
                messages=[
                    {"role": "system",
                     "content": "You are an expert in extracting keywords from the given review on restaurants."},
                    {"role": "user", "content": content}
                ],
            )
            break
        except openai.error.RateLimitError as e:
            print(f"Rate limit exceeded. Retrying in {retry_time} seconds...")
            time.sleep(retry_time)

    # print(response['choices'][0]['message']['content'])
    lines = response['choices'][0]['message']['content'].splitlines()

    keywords = [[] for i in range(4)]
    for line in lines:
        category = {"p": 0, "s": 1, "t": 2, "a": 3}.get(line[0], "err")
        if category == "err":
            print(f"Error in response: {line}")
            continue
        keystr = line[index[category]:].split(", ")
        for keyword in keystr:
            if keyword == '':
                continue
            keywords[category].append(keyword)

    return keywords
