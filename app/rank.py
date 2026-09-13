from rapidfuzz import fuzz
print(fuzz.token_sort_ratio("Anthropic researcher resigns with warning about the dangers of AI development - AP News", "Apple’s new CEO is reviving a Steve Jobs strategy from 25 years ago - TechCrunch"))

def dedup_articles(articles):
    print(len(articles))
    total_groups = [] # contains a list of group dict
    match_found = False
    for article in articles: #checks if an article is similiar to an article in the dict
        for group in total_groups:
            for existing_article in group:
                if fuzz.token_sort_ratio(article.title, existing_article.title) > 50:
                    group.append(article) # if match is found for similarity, the article is added to that group
                    match_found = True
                    print("match found!")
                    break
            if match_found:
                break
        if(match_found != True): # if no similar match is found, new group is created 
            new_group = []
            new_group.append(article)
            total_groups.append(new_group)
            print("new group created!")
        match_found = False

    print("length of total groups", len(total_groups))
    return total_groups


def rank_and_limit(total_groups, limit=7):
    sorted_groups = sorted(total_groups, key=score_group, reverse=True)
    top_groups = sorted_groups[:limit]
    top_articles = [group[0] for group in top_groups]
    return top_articles


def score_group(group):
    return len(group)