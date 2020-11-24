def check_missing_keys(keys, dict_to_check):
  filtered_list = list(
      filter(
          lambda key: dict_to_check.get(key) is None or len(
              dict_to_check.get(key)) == 0, keys
      )
  )
  return filtered_list
