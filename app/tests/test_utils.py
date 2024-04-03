from ..utils import validate_payload, get_hashtag_accounts, get_similar_screen_names

def test_validate_payload():
    input_data = [{"field1": "a", "field2": "b"},
                  {"field1": "a", "field2": "b", 'field3': "c"}]
    required_fields = ['field1', 'field2', 'field3']
    expected_output = {"field1": "a", "field2": "b"}
    actual_output = validate_payload(data=input_data, required_fields=required_fields)
    assert actual_output == expected_output

def test_get_hashtag_accts_repost():
    post_data_example = [{"author_id": "a", "is_repost": False, "hashtags": ["#CatLover", "#catlife"]},
                         {"author_id": "b", "is_repost": False, "hashtags": None},
                         {"author_id": "c", "is_repost": True, "hashtags": ["#CatLover"]}]
    actual_output = get_hashtag_accounts(posts=post_data_example, hashtag='#catlover')
    expected_output = ['a']
    assert actual_output == expected_output

def test_get_similar_screen_names():
    account_data_example = [{"id": "a", "screen_name": "catlover"},
                            {"id": "c", "screen_name": "catluvr"},
                            {"id": "d", "screen_name": "dogperson"}]
    actual_output = get_similar_screen_names(accounts=account_data_example, min_similarity=.5)
    expected_output = [("catlover","catluvr")]
    assert actual_output == expected_output
