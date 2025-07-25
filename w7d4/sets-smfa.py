def analyze_friendships():
    """
    Analyze friendship patterns across different social media platforms
    """
    facebook_friends = {"alice", "bob", "charlie", "diana", "eve", "frank"}
    instagram_friends = {"bob", "charlie", "grace", "henry", "alice", "ivan"}
    twitter_friends = {"alice", "diana", "grace", "jack", "bob", "karen"}
    linkedin_friends = {"charlie", "diana", "frank", "grace", "luke", "mary"}

    all_platforms = facebook_friends & instagram_friends & twitter_friends & linkedin_friends

    facebook_only = facebook_friends - (instagram_friends | twitter_friends | linkedin_friends)

    instagram_xor_twitter = instagram_friends ^ twitter_friends

    total_unique = facebook_friends | instagram_friends | twitter_friends | linkedin_friends

    from collections import Counter
    all_friends = list(facebook_friends) + list(instagram_friends) + list(twitter_friends) + list(linkedin_friends)
    counts = Counter(all_friends)
    exactly_two_platforms = {friend for friend, count in counts.items() if count == 2}

    return {
        "all_platforms": all_platforms,
        "facebook_only": facebook_only,
        "instagram_xor_twitter": instagram_xor_twitter,
        "total_unique": total_unique,
        "exactly_two_platforms": exactly_two_platforms
    }

result = analyze_friendships()
print("All platforms:", result.get('all_platforms'))
print("Facebook only:", result.get('facebook_only'))
print("Instagram XOR Twitter:", result.get('instagram_xor_twitter'))
print("Total unique friends:", result.get('total_unique'))
print("Exactly 2 platforms:", result.get('exactly_two_platforms'))
