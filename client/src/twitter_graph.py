class TwitterGraph:
  def __init__(self):
    self.users = {}

  def add_user(self, screen_name):
    self.users[screen_name] = TwitterUser(screen_name)

  def remove_user(self, screen_name):
    if screen_name in self.users:
      del self.users[screen_name]

  def get_user(self, screen_name):
    if screen_name in self.users:
      return self.users[screen_name]
    return None

  def user_follows(self, screen_name1, screen_name2):
    user1 = self.get_user(screen_name1)
    user2 = self.get_user(screen_name2)
    user2.add_follower(user1)

  def get_ranking(self):
    ranks = []
    rankings_rev = sorted(self.users.items(), key=lambda u: u[1].importance, reverse=True)
    for screen_name, user in rankings_rev:
      ranks.append((f'{user.importance:.10f}', screen_name))
    return ranks

  def generate_importance_ranks(self, iterations, tax=0.85, limit=0.000001):
    damp_factor = (1 - tax) / len(self.users)
    for user in self.users.values():
      user.importance = 1 / len(self.users)
    i = 0
    diff = limit
    while i < iterations and diff >= limit:
      user_importances = {n: u.importance for n, u in self.users.items()}
      total = 0
      for user in self.users.values():
        total -= user.importance
        user.importance = damp_factor + tax * user.calculate_sum(user_importances)
        total += user.importance
      diff = total if total > 0 else -total
      i += 1

class TwitterUser:
  def __init__(self, screen_name):
    self.screen_name = screen_name
    self.followers = []
    self.following = []
    self.importance = 0

  def add_follower(self, user):
    self.followers.append(user)
    user.following.append(self)

  def calculate_sum(self, user_importances):
    total = 0
    for follower in self.followers:
      link_in = follower.calculate_link_in(self)
      link_out = follower.calculate_link_out(self)
      total += user_importances[follower.screen_name] * link_in * link_out
    return total

  def calculate_link_in(self, dest):
    total = 0
    for following in self.following:
      total += len(following.followers)
    if total == 0:
      total = 0.5
    return len(dest.followers) / total

  def calculate_link_out(self, dest):
    total = 0
    for following in self.following:
      total += len(following.following)
    if total == 0:
      total = 0.5
    return len(dest.following) / total


def rank_importance(users_data):
  twitter = TwitterGraph()
  users = users_data["users"]
  user_followings = users_data["followings"]

  for u in users:
    twitter.add_user(u)

  for k, followings in enumerate(user_followings):
    for f in followings:
      twitter.user_follows(users[k], users[f])

  twitter.generate_importance_ranks(100)

  return twitter.get_ranking()
