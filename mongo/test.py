import similarity_check


keyword_list = [['가성비 좋아요'], ['룸을 갖추고 있어요', '직원분들이 친절해요', '고기가 고급스러워요', '프라이빗 룸이 있어요', '직접 구워줘요', '야채 가니쉬가 넉넉해요'], ['런치구성이 다양해요', '다양해요', '고기가 빛깔이 좋아요', '한우육회가 맛있어요', '고기빛깔이 미쳤어요', '맛있었어요', '감탄이 나와요', '퀄리티가 좋아요', '감사해요', '감동이에요', '최상급이예요', '육향이 진해요', '최고예요', '손에 꼽히는 한우 다이닝 중에 제일 맛있어요', '특제 소스가 맛있어요'], ['고급스러운 분위기예요', '단체회식이나 모임장소로 최고예요', '프라이빗하게 식사하기 좋아요']]

# 대표 키워드 추출
for i in range(4):
    print(f"Keywords: {keyword_list[i]}")
    while True:
        integrated = False
        for j, keyword1 in enumerate(keyword_list[i]):
            for k, keyword2 in enumerate(keyword_list[i][j+1:]):
                print(k)
                similarity = similarity_check.calculate_similarity(keyword1, keyword2)
                print(f"Similarity between '{keyword1}' and '{keyword2}': {similarity}")
                if similarity >= 0.7:
                    print(f"delete keyword '{i}', '{j}', '{j + k + 1}' : '{keyword_list[i][j + k + 1]}'")
                    del keyword_list[i][j + k + 1]
                    print(f"After deletion Keywords: {keyword_list[i]}")
                    integrated = True
                    break

            if integrated:
                break

        if not integrated:
            break

print(f"After integration Keywords: {keyword_list}")